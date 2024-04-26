from setuptools import setup, find_packages

setup(
    name='esanalyzer',
    version='1.0.0',
    author='Ajay Singh Rajput',
    description='Emotion and Sentiment Analysis',
    python_requires='>=3.6',
    py_modules=["esanalyzer"],
    packages=find_packages(),
    install_requires=[
        'nrclex',
        'datasets',
        'scikit-learn',
        'pandas',
        'numpy',
        'googletrans==4.0.0-rc1',
        'transformers',
        'nltk'
    ],
    package_dir={'':'esanalyzer/src'}
    # Include other metadata like description, author, etc.
)
