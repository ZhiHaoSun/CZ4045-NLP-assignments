 #!/usr/bin/env python2 -W ignore::UserWarning

import sys
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from afinn import Afinn

reload(sys)  
sys.setdefaultencoding('utf8')

with open('stackoverflow_content', 'r') as f:
	afinn = Afinn()
	threads = contents.split('\n\n\n\n\n\n')
	total = float(len(threads))

	print("Number of threads: " + str(total))
	posts_count = []
	words_count = []

	posts_senti = []
	pos_set = {}
	neg_set = {}

	for thread in threads:
		posts = thread.split('\n\n\n')
		posts_count.append(len(posts) - 1)

		for post in posts:
			words = word_tokenize(post)
			words_count.append(len(words))
			posts_senti.append(afinn.score(post))

			for word in words:
				word = word.lower()
				if not word[-1:].isalpha():
					word = word[-1:]
				score = afinn.score(word)
				if score > 2:
					pos_set[word] = pos_set.get(word, 0) + 1
				elif score < -2:
					neg_set[word] = neg_set.get(word, 0) + 1

	posts_count.sort()
	hmean = np.mean(posts_count)
	hstd = np.std(posts_count)
	print("Questions mean: " + str(hmean))
	print("Questions deviation: " + str(hstd))
	plt.hist(posts_count, bins=70, normed=False)

	oneAnswer = sum(answers == 1 for answers in posts_count)
	twoAnswer = sum(answers == 2 for answers in posts_count)
	threeAnswer = sum(answers == 3 for answers in posts_count)

	print("Question with one answer: " + str(oneAnswer*100 /total) + '%')
	print("Question with two answer: " + str(twoAnswer*100 /total) + '%')
	print("Question with three answer: " + str(threeAnswer*100 / total) + '%')
	plt.show()

	plt.hist(words_count, bins=50, normed=False)
	plt.show()

	plt.hist(posts_senti, bins=50, normed=False)
	plt.show()

	pos_set = sorted(pos_set, key=pos_set.get, reverse=True)
	neg_set = sorted(neg_set, key=neg_set.get, reverse=True)

	print("Most frequent positive words:")
	for i in range(20):
		print(pos_set[i])

	print("Most frequent negative words:")
	for i in range(20):
		print(neg_set[i])