from setuptools import setup, find_packages
import platform

ext = "so"
if platform.system() == "Windows":
    ext = "dll"
elif platform.system() == "Darwin":
    ext = "dylib"

setup(
    name="jsonatago",
    version="0.2.2",
    description="Your package description here",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rados4y/jsonatago",  # Homepage link
    packages=find_packages(),
    package_data={
        "jsonatago": [
            f"dist/jsonatago-{platform.system().lower()}.{ext}",
        ],
    },
    install_requires=[
        # dependencies here
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",  # Alpha status
    ],
    cmdclass={},
)
