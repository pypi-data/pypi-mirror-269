from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="cloudacious",
    version="0.0.2",
    description="Cloudacious's object-oriented code tooling. Call our classes all day long!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/money-marathon/cloudacious/cloudacious.git",
    author="A. SurfingDoggo",
    author_email="git@surfingdoggo.com",  # Optional
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="setuptools, development",
    package_dir={"": "src"},
    packages=find_packages(),
    python_requires=">=3.11, <4",
    install_requires=[
        "requests",
        "python-gitlab",
        "boto3",
        "python-dotenv",
        "pulumi",
        "pulumi_aws",
        "pulumi_docker",
    ],
)
