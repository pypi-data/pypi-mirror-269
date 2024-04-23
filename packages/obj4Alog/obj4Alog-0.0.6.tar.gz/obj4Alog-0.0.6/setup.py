from setuptools import setup, find_packages

setup(
    name="obj4Alog",
    version="0.0.6",
    packages=find_packages(),
    install_requires=[
    'matplotlib==3.6.3',
    'numpy>=1.21.1',
    'pandas>=2.0.3',
    'pm4py>=2.7.1',
    'scikit_learn==1.3.2',
    'seaborn==0.13.2',
    'setuptools==68.0.0',
    'tabulate==0.9.0',
    ],
    python_requires=">=3.8.0",
    author="Faizan Khan",
    description="obj4Alog is an event log base library used to build the petri net models of any event log. It also come with the functionality to build abstract model of event log.",
)