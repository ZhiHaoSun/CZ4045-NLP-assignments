 #!/usr/bin/env python2 -W ignore::UserWarning

import sys
import nltk
from nltk.tokenize import word_tokenize
import warnings
warnings.filterwarnings("ignore")

reload(sys)  
sys.setdefaultencoding('utf8')

with open('stackoverflow_content', 'r') as f:
	contents = f.read()
	tokens = word_tokenize(contents)
	for i in range(3,7):
		content_model = nltk.NgramModel(i, tokens)

		content = content_model.generate(20, ["I", "like"])
		print("\nSentence generated for " + str(i) + "-Gram Model:")
		print(' '.join(content))