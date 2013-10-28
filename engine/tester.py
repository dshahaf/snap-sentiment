from corpus import Corpus
from sentiment_analysis import SentimentAnalysis
import os

class Tester:
	def __init__(self):
		self.corpus = Corpus()
		self.analysis = SentimentAnalysis()
		return

	"""
	method: 'simple'
	dataName: 'movie'
	Returns,
	{
		'total': {
			'positive': int,
			'negative': int,
		},
		'correct': {
			'positive': int,
			'negative': int,
		},
		'accuracy': {
			'positive': float,
			'negative': float,
		}
	}
	"""
	def test(self, method, dataName, count = 100):
		posData = []
		negData = []

		ret = {
			'total': {
				'positive': 0,
				'negative': 0,
			},
			'correct': {
				'positive': 0,
				'negative': 0,
			},
			'accuracy': {
				'positive': 0.0,
				'negative': 0.0,
			}
		}

		posCorrectCount = 0
		negCorrectCount = 0
		if dataName == 'movie':
			posData = self.corpus.movieReviews('positive', count)
			negData = self.corpus.movieReviews('negative', count)
		if method == 'simple':
			for posText in posData:
				self.analysis.setText(posText)
				sentimentInt = self.analysis.simpleAnalysisInt()
				if sentimentInt is 1:
					posCorrectCount += 1
			for negText in negData:
				self.analysis.setText(negText)
				sentimentInt = self.analysis.simpleAnalysisInt()
				if sentimentInt is -1:
					negCorrectCount += 1
		ret['total']['positive'] = count
		ret['total']['negative'] = count
		ret['correct']['positive'] = posCorrectCount
		ret['correct']['negative'] = negCorrectCount
		ret['accuracy']['positive'] = 1.0 * posCorrectCount / count
		ret['accuracy']['negative'] = 1.0 * negCorrectCount / count

		return ret