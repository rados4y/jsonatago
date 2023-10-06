from setuptools import setup, find_packages, Command
from plumbum import local


class LibBuildCmd(Command):
    description = "Build Go shared library"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        go = local["go"]
        python = local["python"]
        local.cwd.chdir("jsonatago/golang")
        with local.env(GOOS="windows", GOARCH="amd64"):
            go["build", "-o", "jsonatago.dll", "-buildmode=c-shared", "main.go"]()
        with local.env(GOOS="linux", GOARCH="amd64"):
            go["build", "-o", "jsonatago.so", "-buildmode=c-shared", "main.go"]()


setup(
    name="jsonatago",
    version="0.2.1",
    packages=find_packages(),
    package_data={
        "jsonatago": [
            "golang/jsonatago.dll",
            "golang/jsonatago.so",
        ],  # or jsonatago.so for Linux
    },
    install_requires=[
        # Your dependencies here
    ],
    cmdclass={
        "libbuild": LibBuildCmd,
    },
)
