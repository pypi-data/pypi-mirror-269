import os
import re
import subprocess
import traceback

if __name__ == '__main__':
    token_file = open("token", "r")
    token = token_file.read()
    token_file.close()

    pyproj_file = open("pyproject.toml", "r+")
    pyproj = pyproj_file.read()
    pyproj_file.close()

    pattern = re.compile("version\\s+=\\s+\"(.*)\"")
    version = pattern.findall(pyproj)[0]

    print(f"Current Version: {version}")
    new_version = input("Upload Version: ")
    while True:
        if input(f"Are you sure you want to proceed with new version {new_version}? [y/n] ") == "y":
            break
        new_version = input("Upload Version: ")


    pyproj_file = open("pyproject.toml", "w")
    pyproj_file.write(pattern.sub(f"version = \"{new_version}\"", pyproj))
    pyproj_file.close()

    try:
        import glob

        for f in glob.glob("dist/*"):
            os.remove(f)

        import build.__main__
        build.__main__.main([])

        import twine.cli
        arguments = ["upload", "--repository", "pypi", "-p", token, "dist/*"]
        result = twine.cli.dispatch(arguments)
    except Exception as e:
        print("Error occurred while building")
        traceback.print_exc()
        pyproj_file = open("pyproject.toml", "w")
        pyproj_file.write(pyproj)
        pyproj_file.close()



