from setuptools import setup, find_packages

classifiers = [
    "Intended Audience :: Developers",
    "Topic :: System :: Logging",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
]

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="cli-log",
    packages=find_packages(),
    version="0.2",
    license="MIT",
    description="Command line interface logging.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="DeltaBotics",
    url="https://github.com/DeltaBotics/cli-log",
    keywords=["logging"],
    install_requires=["colorama"],
    classifiers=classifiers,
    project_urls={"Source": "https://github.com/DeltaBotics/cli-log"},
)
