from setuptools import setup, find_packages

setup(
    name='sentiment_emotion_analysis',
    version='0.1',
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
    author='Ajay Singh Rajput',
    description='Emotion and Sentiment Analysis',
    # Include other metadata like description, author, etc.
)
