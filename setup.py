from setuptools import setup, find_packages

setup(
    name="ghs",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["requests", "dotenv"],
    entry_points={"console_scripts": ["ghs=ghs.cli:main"]},
    author="Md. Sazzad Hissain Khan",
    author_email='hissain.khan@gmail.com',
    description="GitHub Code Search CLI with file downloading.",
    url='https://github.com/hissain/ghs',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
