from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='EcoStock',
    version='0.1',
    author="Antonio Paparo, Giovanni Paparo, Ludovica De Giacomo and Francesco Caldo",
    author_email="antoniopaparo@outlook.com",
    description='A Python package for investigating the correlation between economic and financial data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tonij10/fastapi-project",
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'pydantic',
        'kaleido',
        'argparse',
        'uvicorn',
        'pandas',
        'numpy',
        'matplotlib',
        'yfinance',
        'plotly',
        'openai',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


# Assicurati di sostituire Your Name, your.email@example.com e https://github.com/yourusername/package_name con le tue informazioni.