from setuptools import setup, find_packages

setup(
    name="ghcs",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["requests", "dotenv"],
    entry_points={"console_scripts": ["ghcs=ghcs.cli:main"]},
    author="Md. Sazzad Hissain Khan",
    author_email='hissain.khan@gmail.com',
    description="GitHub Code Search CLI with file downloading capability.",
    url='https://github.com/hissain/ghcs',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
