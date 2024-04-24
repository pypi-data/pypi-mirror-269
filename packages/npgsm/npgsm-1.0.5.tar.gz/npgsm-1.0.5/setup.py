import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

# Read long description from the readme.md file
with open("README.md", encoding="utf-8") as f:
    readme = f.read()

with open("LICENSE", encoding="utf-8") as f:
    license_data = f.read()

setup(
    name="npgsm",
    version="1.0.5",
    description="A package that could help you manage your secrets in Google Secret Manager",
    long_description_content_type="text/markdown",
    long_description=readme,
    author="Nopporn Phantawee",
    author_email="n.phantawee@gmail.com",
    url="https://github.com/noppGithub/npgsm",
    license="MIT",
    packages=find_packages(exclude=("tests", "docs")),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=[
        "google-cloud-secret-manager>=2.12.6",
        "google-cloud-logging>=3.2.5",
    ],
    extras_require={
        "dev": ["check-manifest"],
        "test": ["coverage"],
    },
    python_requires=">=3.6, <4",
)
