from setuptools import setup, find_packages

setup(
    name='esanalyzer',
    version='1.0.3',
    author='Ajay Singh Rajput',
    description='Emotion and Sentiment Analysis',
    url='https://github.com/ajaysingh111444/python/tree/esanalyzer/esanalyzer',
    long_description="""# esanalyzer

    The Python Emotion and Sentiment Analysis library you've been looking for.

    ## Services
    - Emotion Analysis
    - Sentiment Analysis

    ## Usage
    - Install using `pip install esanalyzer`

    ```python
    from esanalyzer.emotion_analyzer import EmotionAnalyzer

    # Create an instance of EmotionAnalyzer
    analyzer = EmotionAnalyzer()

    # Call the analyze method with the text
    text = "Wow, I am so happy"
    result = analyzer.analyze(text)

    # Use the result as needed
    print(result)
    
    
    {'library': 'default', 'result': {'surprise': 80}, 'max_prediction': {'label': 'surprise', 'percentage': 80}, 'sentiment': 'Positive', 'sentiment_score': 0.999592125415802, 'threshold_value': 0.8}
    
    """,
    long_description_content_type='text/markdown',
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
