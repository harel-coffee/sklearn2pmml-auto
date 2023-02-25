from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn2pmml.util import eval_rows, Predicate

class RuleSetClassifier(BaseEstimator, ClassifierMixin):

	def __init__(self, rules, default_score = None):
		for rule in rules:
			if type(rule) is not tuple:
				raise TypeError("Rule is not a tuple")
			if len(rule) != 2:
				raise TypeError("Rule is not a two-element (predicate, score) tuple")
			predicate, score = rule
			if not isinstance(predicate, (str, Predicate)):
				raise TypeError()
		self.rules = rules
		self.default_score = default_score

	def _eval_row(self, X):
		for predicate, score in self.rules:
			if eval(predicate):
				return score
		return self.default_score

	def fit(self, X, y = None):
		return self

	def predict(self, X):
		func = lambda x: self._eval_row(x)
		return eval_rows(X, func)
