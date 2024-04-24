from setuptools import setup

PKG_NAME = "simular-eth-stubs"
VERSION = "0.0.4"
setup(
    name=PKG_NAME,
    version=VERSION,
    packages=['simular-stubs'],
    description="Type stubs for simular-evm",
    url=f"https://github.com/james4ever0/{PKG_NAME}",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # install_requires=REQUIREMENTS,
    install_requires = open('requirements.txt').read().splitlines(),
)
