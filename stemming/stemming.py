import os
import nltk
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.split(dir_path)[0]
filename = os.path.join(parent_dir, 'stackoverflow_content')
print(filename)
english_stopwords = nltk.corpus.stopwords.words('english')
english_stopwords.extend(["'m", "'re", "'s", "'ve", "n't"])
stemmer = nltk.PorterStemmer()

words = {}
stemmed_words = {}
stem_to_word = {}

with open(filename, encoding='utf-8') as dataset:
    for line in dataset:
        words_in_line = nltk.word_tokenize(line)
        for word in words_in_line:
            word = word.lower()
            # remove words consisting only symbols or stop words
            if re.match(r'^[^a-zA-Z]+$', word) or word in english_stopwords:
                continue
            if word in words:
                words[word] += 1
            else:
                words[word] = 1
            stemmed_word = stemmer.stem(word)
            if stemmed_word in stemmed_words:
                stemmed_words[stemmed_word] += 1
                stem_to_word[stemmed_word].add(word)
            else:
                stemmed_words[stemmed_word] = 1
                stem_to_word[stemmed_word] = set()

word_list = [(count, word) for word, count in words.items()]
word_list = sorted(word_list, reverse=True)
print('Words before stemming: ')
for count, word in word_list[:20]:
    print(word, count)

stemmed_word_list = [(count, word) for word, count in stemmed_words.items()]
stemmed_word_list = sorted(stemmed_word_list, reverse=True)
print('Words after stemming: ')
for count, word in stemmed_word_list[:20]:
    print(word, count, end=' ')
    for origin_word in stem_to_word[word]:
        print(origin_word, end=' ')
    print()
