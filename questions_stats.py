import sys
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize

reload(sys)  
sys.setdefaultencoding('utf8')

with open('stackoverflow_content', 'r') as f:
	contents = f.read()
	threads = contents.split('\n\n\n\n\n\n')
	total = float(len(threads))

	print("Number of threads: " + str(total))
	posts_count = []
	words_count = []

	for thread in threads:
		posts = thread.split('\n\n\n')
		posts_count.append(len(posts) - 1)

		for post in posts:
			words = len(word_tokenize(post))
			words_count.append(words)

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