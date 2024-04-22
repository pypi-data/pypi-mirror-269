import inspect
import re
from typing import Union, Callable, Any
from .arg import ArgMatcher, Arg
from .bundle import BundleManager
from .decorators import __complex_decorator__
from .meta import CommandLike, AbstractFunctionCommandWrapper


class Command:
    """
    Represents a registered command which contains various information about the command including its base function.
    """
    def __init__(self, name: str, command_like: CommandLike,
                 /, aliases: list[str] = None, lowercase: bool = True, case_sensitive: bool = False,
                 args: list["Arg"] = None):

        self.command_like = command_like
        """
        The underlying method (or class) which serves as the target for command invocation
        """

        if isinstance(command_like, AbstractFunctionCommandWrapper):
            self.is_class = False
            self.__wrapped_command__ = True
        else:
            self.is_class = inspect.isclass(command_like)
            self.__wrapped_command__ = False

        self.name: str = name
        """
        The name of the command
        """
        self.description: str = getattr(command_like, "__description__", None)
        """
        An (optional) description of the command
        """
        self.args = args
        """
        A list of arguments for the command, this may be lazily-generated
        """

        self.aliases = aliases
        self._aliases = list(aliases)
        self._aliases.insert(0, self.name)

        self.lowercase = lowercase
        self.case_sensitive = case_sensitive

        self.__subcommands__: set[Command] = set()
        self._parent = None

        self._command_like_instance = None

        self._last_input: str = None
        self._arg_matcher = ArgMatcher(self)

    def execute(self, raw_input: str):
        """
        Executes the command (and therefore the execution function) with the provided raw input
        :param raw_input: The input string containing arguments for execution
        """
        self._last_input = raw_input
        space = re.search(r"\s+", raw_input)
        if space:
            subcommand_name = raw_input[:space.start()]
            sub_raw_input = raw_input[space.end():]
        else:
            subcommand_name = raw_input
            sub_raw_input = ""

        for subcommand in self.__subcommands__:
            if subcommand.matches(subcommand_name):
                return subcommand.execute(sub_raw_input)

        args = self._arg_matcher.match_arguments(raw_input)
        if self.is_class:
            return self.command_like.__execute__(*args)
        else:
            return self.command_like(*args)

    def add_subcommand(self, subcommand: "Command"):
        """
        Adds a subcommand to this command
        :param subcommand: The command to add
        """
        self.__subcommands__.add(subcommand)
        subcommand._parent = self

    def find_subcommand(self, parent: Union[str, CommandLike]) -> "Command":
        """
        Finds a subcommand given a command name or command-like
        :param parent:
        :return:
        """
        for subcommand in self.__subcommands__:
            if isinstance(parent, str) and subcommand.matches(parent):
                return subcommand
            elif subcommand.command_like is parent:
                return subcommand
            return subcommand.find_subcommand(parent)
        return None

    def get_command_like(self):
        """
        Returns the single instance of the wrapped command-like object or creates it if it doesn't exist.
        :return: The singleton command-like object instance,
        """
        if self._command_like_instance is None:
            self._command_like_instance = self.command_like()
        return self._command_like_instance

    def get_parent(self) -> "Command":
        """
        Returns the :class:`Command` parent of this command or `None` if one doesn't exist..
        :return: The :class:`Command` parent instance.
        """
        return self._parent

    def matches(self, cmd_name: str) -> bool:
        """
        Checks if this command matches the given name.
        :param cmd_name: The name to check for matches
        :return: `True` if this command matches the given name otherwise `False`.
        """
        for alias in self._aliases:
            if self.lowercase:
                alias = alias.lower()
            if self.case_sensitive and cmd_name == alias:
                return True
            if cmd_name.lower() == alias:
                return True
        return False

    def last(self, include_roots = False) -> str:
        """
        Returns the last input string this command executed
        :param include_roots whether to use the input executed by the root command
        :return: the last input string if this command was executed, otherwise `None`
        """
        value = self._last_input
        if not include_roots or self._parent is None:
            return value
        return self._parent.last(include_roots)



class CLI:
    def __init__(self, console_input: Callable[[], str] = input, bundle_manager: BundleManager = None):
        """
        :param console_input: A function which probes for user input (default: input())
        """
        self._commands: set[Command] = set()
        self._command_table: dict[CommandLike, Command] = dict()
        self.console_input = console_input
        self._processed = False
        self._last_input = None
        self.result = None
        self.bundles = bundle_manager if bundle_manager else BundleManager(self)

    @__complex_decorator__(no_wrap=False)
    def command(self, command_like,
                aliases: list[str] = None, name: str = None, lowercase: bool = True, case_sensitive: bool = True,
                args: list["Arg"] = None):
        """
        A decorator that registers a command-like object as a command, allowing it to be executed when matched in
        an input string.

        If no aliases are specified the name of the command will match the name of the annotated class or method.

        If this decorator is used on a class, the class must contain a method named **__execute__**, this method CAN
        be static and will be executed if a command is successfully matched. Additionally, the containing class will
        operate as a singleton whenever received as a "self" parameter to __execute__, meaning updates to the class
        will persist between calls.

        Usage::

            cli = CLI()

            @cli.command
            def ping():
                print("pong")

            @cli.command(aliases=["howdy"])
            class Hello:
                @staticmethod  # this does not need to be static
                def __execute__():
                    print("Hi!")

            cli.process_input("pong")   # ping will be called
            cli.process_input("Hello")  # Hello.__execute__() will be called
            cli.process_input("howdy")  # Hello.__execute__() will be called again

        **Advanced Usage:**
        Parameters declared in the target execution method must follow special rules to correspond with a given input.
        The most simple rule is if a parameter is named "self" it will contain the singleton instance of its parent
        class.

        Additionally, each argument of a command must have a matching parameter defined in the target execution method
        which also constructs an instance of :class:`Arg` as its default value.

        The final caveat is that any matching argument supplied to the method will automatically have its type matched
        to its parameter's annotated type. When no type annotation is specified the value will either be a string or
        will match the type of the default value provided by the Arg() constructor.

        Lastly, if any parameter has the annotated type :class:`Command` then its corresponding :class:`Command`
        instance will be passed into the function upon execution.

        Advanced Usage Examples::

            cli = CLI()

            # registers a command that receives the first argument of the 'greeting' command
            @cli.command
            def greet(name: str = Arg(0)):
                print(f"Hello {name}!")

            # registers a command that takes two optional arguments (--value and --hide)
            @cli.command
            def echo(value: str = Arg("--value", default="nothing..."), hide: bool = Arg("--hide"))
                if not hide: print("Echoed " + value)

            cli.process_input("greet Alice")                # prints "Hello Alice!"
            cli.process_input("echo")                       # prints "Echoed nothing..."
            cli.process_input("echo --value text")          # prints "Echoed text"
            cli.process_input("echo --value text --hide)    # prints nothing!

        :param command_like: The command-like object to register
        :param aliases: The aliases the command can also be invoked under
        :param name: The primary name of the command.
        :param lowercase: If the command name should be lowercase (defaults to True)
        :param case_sensitive: If the command name is case-sensitive (defaults to True)
        :param args: A list of :class:`Arg` to be used as an alternative to signature-based declarations
        :return: The wrapped function
        """
        return self._register_command(command_like, None, aliases, name, lowercase, case_sensitive, args)

    @__complex_decorator__(no_wrap=True)
    def subcommand(self, command_like, parent: type = None,
                   aliases: list[str] = None, name: str = None, lowercase: bool = True, case_sensitive: bool = True,
                   args: list[Arg] = None):
        """
        A decorator that registers a command-like object as a command, allowing it to be executed when matched in
        an input string.

        This decorator is nearly identical to the :func:`command` decorator except it takes an additional argument,
        `parent` which is the class of the desired parent command.

        Usage::

            cli = CLI()

            @cli.command
            class Math:
                def __execute__():
                    print("use either math add or math subtract!")

            @cli.subcommand(Math)
            def add(o1: int = Arg(0), o2: int = Arg(1)):
                print(f"{o1} + {o2} = {o1 + o2}")

            @cli.command(Math)
            def sub(o1: int = Arg(0), o2: int = Arg(1)):
                print(f"{o1} - {o2} = {o1 - o2}")

            cli.process_input("math")           # prints "use either math add or math subtract!"
            cli.process_input("math add 5 4)    # prints "5 + 4 = 9"
            cli.process_input("math sub 8 3)    # prints "8 - 3 = 5"


        :param command_like: The command-like object to register.
        :param parent: The class of the parent command.
        :param aliases: The aliases the command can also be invoked under.
        :param name: The primary name of the command.
        :param lowercase: If the command name should be lowercase (defaults to True).
        :param case_sensitive: If the command name is case-sensitive (defaults to True).
        :param args: A list of :class:`Arg` to be used as an alternative to signature-based declarations.
        :return: The wrapped function
        """
        if parent is None:
            raise ValueError("parent cannot be None")
        return self._register_command(command_like, parent, aliases, name, lowercase, case_sensitive, args)

    def identity(self, func):
        """
        A decorator that **modifies a method** to return an instance to its correspond :class:`Command` class.
        :param func: The function to modify
        :return: A modified function that returns a :class:`Command` instance.
        """
        parent_class = func.__qualname__.split(".")[-2]

        def wrapper(*_):
            return self.find_command(parent_class)

        return wrapper

    def find_command(self, identifier: Union[str, CommandLike]) -> Command:
        """
        Finds a command based on a given name or the command-like object used to register the command.
        :param identifier: The name/alias of a command or a command-like object.
        :return: The first matching command or `None` if no suitable command is found.
        """
        for command in self._commands:
            if isinstance(identifier, str) and command.matches(identifier):
                return command
            elif command.command_like is identifier:
                return command

            subcommand = command.find_subcommand(identifier)
            if subcommand:
                return subcommand

    def was_processed(self) -> bool:
        return self._processed

    def process(self) -> str:
        """
        A function that immediately prompts for user input then processes the input,
        invoking any matching registered commands.

        This function returns the input received from self.console_input(). If instead the result of the
        matched command is desired use either :func:`process_input` or read value of `cli.result`.

        :return: The user input
        """
        raw_input = self.console_input()
        self.process_input(raw_input)
        return raw_input

    def process_input(self, raw_input: str) -> Any:
        """
        A function that processes an input string, invoking any matching registered commands.

        :param raw_input: The string to process.
        :return: The result of the first command matched
        """
        self._processed = False
        self._last_input = raw_input

        space = re.search(r"\s+", raw_input)
        if not space:
            command_name = raw_input
            raw_input = ""
        else:
            command_name = raw_input[:space.start()]
            raw_input = raw_input[space.end():]

        commands = list(self._commands)
        for cmd in commands:
            if cmd.matches(command_name):
                self.result = cmd.execute(raw_input)
                self._processed = True
                return self.result

    def unregister(self, command_like: CommandLike):
        """
        Unregisters a command or subcommand via its registered command-like object.

        :param command_like: The command-like object to unregister.
        """
        matched = [cmd for cmd in self._commands if cmd.command_like == command_like]
        for match in matched:
            self._commands.remove(match)
        table_entry = self._command_table.get(command_like)
        if table_entry:
            parent = table_entry.get_parent()
            if parent:
                parent.__subcommands__.remove(table_entry)

    def last(self):
        """
        Returns the last input executed
        :return: the last input executed, otherwise None
        """
        return self._last_input

    def __iter__(self):
        return self._commands.__iter__()

    def _register_command(self, command_like, parent: type = None,
                          aliases: list[str] = None, name: str = None, lowercase: bool = False, case_sensitive: bool = True,
                          args: list["Arg"] = None):

        cmd_name: str = name if name else command_like.__name__

        aliases = [] if aliases is None else list(aliases)

        cmd = Command(cmd_name, command_like, aliases=aliases, lowercase=lowercase,
                      case_sensitive=case_sensitive, args=args)

        self._command_table[command_like] = cmd
        command_like.__boundcommand__ = cmd

        if parent is not None:
            command_parent = self.find_command(parent)
            if command_parent:
                command_parent.add_subcommand(cmd)
                return command_like
            else:
                raise ValueError(f"Parent not found {parent}")

        self._commands.add(cmd)
        return command_like
