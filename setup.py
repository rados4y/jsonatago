from setuptools import setup, find_packages
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel  # type: ignore
import platform

ext = "so"
if platform.system() == "Windows":
    ext = "dll"
elif platform.system() == "Darwin":
    ext = "dylib"


class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False  # Mark the wheel as a non-pure (platform-specific)


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
    cmdclass={
        "bdist_wheel": bdist_wheel,
    },
)
