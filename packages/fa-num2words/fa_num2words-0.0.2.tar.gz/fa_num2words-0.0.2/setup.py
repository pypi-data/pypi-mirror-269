from setuptools import setup, find_packages

setup(
    name='fa-num2words',
    version='0.0.2',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "fa-num2words = fa_num2words: digit",
        ],
    },
)
