import unittest

from simplycli import CLI, AbstractCommandClass, Command


def create_commands(cli: CLI):
    @cli.command()
    class Outer(AbstractCommandClass):
        def __execute__(self):
            return "I have been executed"

    @cli.subcommand(Outer)
    def inner(cmd: Command):
        if not isinstance(cmd.get_parent().get_command_like(), Outer):
            raise Exception("Not an inner command")
        return cmd.last(True)

class MyTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cli = CLI()
        create_commands(self.cli)

    def test_something(self):
        self.assertEqual("I have been executed", self.cli.process_input("outer"))
        self.assertEqual("outer inner", self.cli.process_input("outer inner"))


if __name__ == '__main__':
    unittest.main()
