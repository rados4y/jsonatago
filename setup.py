from setuptools import setup, find_packages
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel  # type: ignore
import os

goos = os.environ.get("GOOS")
goarch = os.environ.get("GOARCH")
ext = os.environ.get("EXT")

platforms: list[str] = []

if goos == "linux":
    platforms.append(f"manylinux2014_{goarch}")
elif goos == "windows":
    platforms.append(f"win_{goarch}")
elif goos == "darwin":
    platforms.append(f"macosx_10_9_{goarch}")


class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False  # Mark the wheel as a non-pure (platform-specific)


setup(
    name="jsonatago",
    version="0.2.2",
    platforms=platforms,
    description="Your package description here",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rados4y/jsonatago",  # Homepage link
    packages=find_packages(),
    package_data={
        "jsonatago": [
            f"dist/jsonatago-{goos}-{goarch}.{ext}",
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
