from setuptools import setup, find_packages

setup(
    name="centric_tools",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["fastapi", "pytest", "requests", "google-cloud-storage"],
    author="Centric",
    author_email="david@davu.ai",
    description="A collection of internal tools shared among all Centric Microservices",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/davu-ai/centric_tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
