from setuptools import setup, find_packages

setup(
    name="ara-tools",
    version="0.1.4.21",   # .0 for local install test purpose
    packages=find_packages(),
    include_package_data=True,  # Add this line
    entry_points={
        "console_scripts": [
            "ara = ara_tools.__main__:cli",
        ],
    },
    install_requires=[
        'langchain',
        'langchain-community',
        'langchain_openai',
        'openai',
        # Add your package dependencies here
    ],
)
