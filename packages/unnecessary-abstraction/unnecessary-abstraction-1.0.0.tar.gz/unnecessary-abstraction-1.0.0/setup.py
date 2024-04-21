from setuptools import find_packages, setup






setup(
    name="unnecessary-abstraction",
    version="1.0.0",
    author="Michael Howard",
    author_email="",
    description="For smooth brains who don't sql good.",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent"
        ], 
    install_requires=["psycopg2-binary"],
    python_requires=">=3.9"
)
