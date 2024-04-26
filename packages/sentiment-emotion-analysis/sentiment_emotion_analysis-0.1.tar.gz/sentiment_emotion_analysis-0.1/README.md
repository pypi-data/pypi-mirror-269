# esa
The Python Emotion and Sentiment library you've been looking for.


## Services
- Emotion Analysis
- Sentiment Analysis


## Usage
- Install using `pip install esa`


```python 


	from sentiment_emotion_analysis.emotion_analyzer import EmotionAnalyzer

	# Create an instance of EmotionAnalyzer
	analyzer = EmotionAnalyzer()

	# Call the analyze method with the text
	text = "This is a test text."
	result = analyzer.analyze(text)

	# Use the result as needed
	print(result)
	

```