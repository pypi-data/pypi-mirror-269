from setuptools import setup

setup(
    name="paebot",
    description="mne paebot, tebe paebot, vsem paebot",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ebanull/paebot",
    license="MIT",
    author="ebanull",
    version="0.1.3",
    packages=["paebot"],
    install_requires=["requests"],
)
