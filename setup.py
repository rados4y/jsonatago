from setuptools import setup, find_packages, Extension
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel  # type: ignore

# import os


class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False  # Mark the wheel as a non-pure (platform-specific)


setup(
    name="jsonatago",
    version="0.2.6",
    # platforms=platforms,
    description="Your package description here",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rados4y/jsonatago",
    packages=find_packages(),
    python_requires=">=3.8",
    setup_requires=["setuptools-golang>=2.8.0"],
    install_requires=[
        # dependencies here
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",  # Alpha status
    ],
    ext_modules=[
        Extension(
            "jsonatago.jsonatago_capi",
            ["jsonatago/jsonatago_capi/jsonatago_capi.go"],
            py_limited_api=True,
            define_macros=[("Py_LIMITED_API", None)],
        ),
    ],
    cmdclass={
        "bdist_wheel": bdist_wheel,
    },
    build_golang={"root": "jsonatago_capi"},
)
