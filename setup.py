import setuptools

try:
    from pypandoc import convert

    read_md = lambda f: convert(f, "rst")
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, "r").read()

setuptools.setup(
    name="airthings",
    version="3.2.0",
    author="Marius Kotlarz",
    author_email="marius@kotlarz.no",
    description="Fetch sensor measurements from Airthings devices",
    long_description=read_md("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/kotlarz/airthings",
    packages=setuptools.find_packages(),
    install_requires=["bluepy==1.3.0"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Home Automation",
        "Topic :: Utilities",
    ],
)
