from setuptools import setup, find_packages

setup(
    name="simple_ascii_cards",
    version="0.1",
    packages=find_packages(),
    description="A simple ASCII card display package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Cameron Redovian",
    author_email="naivoder@gmail.com",
    url="https://github.com/naivoder/ascii_cards",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="cards games ascii",
    project_urls={
        "Source": "https://github.com/naivoder/ascii_cards",
    },
)
