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
	Returns {
		'positive' : float (success ratio on positive data)
		'negative' : float (success ratio on negative data)
	}
	"""
	def test(self, method, dataName, count = 100):
		posData = []
		negData = []
		ret = {}
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
		ret['positive'] = 1.0 * posCorrectCount / count
		ret['negative'] = 1.0 * negCorrectCount / count
		return ret