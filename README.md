# About

This project is an affiliated coursework for CZ4045 Natural Language Processing in Nanyang Technological University (Singapore).
The group has gone through the full data processing life cycle using data collected from online forum Stack Overflow, an online forum dedicated to programming related questions and answers.
The main components of this project are: data collection by self-designed crawler, data analysis and annotation by using stemming followed by POS tagging, tokenizer training and development, further analysis and its applications for sentiment statistics, Shannon generation, grammar parsing & checking, and collocation analysis.

# Used features

The CRF implementation uses only local features (i.e. annotating `John` at the top of a document with `PER` has no influence on another `John` at the bottom of the same document).

The used features are:
* Whether to word starts with an uppercase letter
* Chracter length of a word
* Whether the word contains any digit (0-9)
* Whether the word contains any punctuation, i.e. `. , : ; ( ) [ ] ? !`
* Whether the word contains *only* digits
* Whether the word contains *only* punctuation
* The word pattern of the word, e.g. `John` becomes `Aa+`, `DARPA` becomes `A+`
* The unigram rank of the word among the 1000 most common words, where the most common word would get the rank `1` (words outside the rank of 1000 just get a `-1`).
* The 3-character-prefix of the word, i.e. `John` becomes `Joh`.
* The 3-chracter-suffix of the word, i.e. `John` becomes `ohn`.
* The Part of Speech tag (POS) of the word as generated by nltk.

# Requirements
Run `pip2 install -r requirements.txt` to handle all dependency issues.

## Libraries/code
* python 2.7 (only tested on that version)
* [python-crfsuite](http://python-crfsuite.readthedocs.org/en/latest/)
* [scikit-learn](http://scikit-learn.org/stable/) (used in test to generate classification reports)
* shelve (should be part of python)
* [nltk](http://www.nltk.org/) (used for its wrapper of the stanford pos tagger)

## Corpus
A large annotated corpus is required that *(a)* contains one article/document per line, *(b)* is tokenized (e.g. by the stanford parser) and *(c)* contains annotated named entities with length > 1 of the form `word/LABEL`.
Example:

> They are independent languages with unrelated lineages. Brendan/MISC Eich/MISC created Javascript originally at Netscape. It was initially called Mocha. The choice of Javascript as a name was a nod, if you will, to the then ascendant Java programming language, developed at Sun by Patrick/MISC Naughton/MISC, James/MISC Gosling/MISC , et. al ...

Notice the `/MISC` labels.

*Note*: You can create a large corpus with annotated names of people from the Wikipedia as names (in Wikipedia articles) are often linked with articles about people, which are identifiable. There are some papers about that.

# Usage
(Data are prepared already, so you can jump to step 4 directly.)
1. Run first crawler `python2 stackoverflow_crawler.py` to generate file
 `stackoverflow_questions`. This file contains a list of links to hot StackOverflow questions.
2. Run second crawler `python2 stackoverflow_content_parser.py` to fetch post details of questions in "stackover_questions" file. Result will be stored in `stackoverflow_content` file. 
3. Prepare annotated data. Data is stored in `source.txt`.
4. Install all requirements in requirements.txt
5. (Optional) Change all constants (specifically the filepaths) in `config.py` to match your settings. You will have to change `ARTICLES_FILEPATH` (path to your corpus file), `COUNT_WINDOWS_TRAIN` (number of examples to train on, might be too many for your corpus), `COUNT_WINDOWS_TEST` (number of examples to test on, might be too many for your corpus), `LABELS`.
6. Run `python2 -m preprocessing/collect_unigrams` to create lists of unigrams for your corpus. This will take 2 hours or so, especially if your corpus is large.
7. Run `python2 train.py --identifier="my_experiment"` to train a CRF model with name `my_experiment`.
8. Run `python2 predict.py --identifier="my_experiment"` to test your trained CRF model on an excerpt of your corpus (by default on windows 0 to 4,000, while training happens on windows 4,000 to 24,000). 
9. Application 1: statistics on fetched data and do sentiment statistics.
Run `python2 questions_stats.py`.
10. Application 2: Shannon Generation based on NGram model. Run `python2 generate.py`. Sentences of length 20 with starting words "I like" will be generated. This may need to wait several minutes.

12. Application 4: Collocation analysis basing on nltk.collocation kit. Run 'python2 preprocessing/generate_collocation_data.py' to generate collocation matrix.
    Then run 'python -m SimpleHTTPServer 8080', and the visualisation shall be available on 'http://localhost:8080/collocation/stackoverflow.html'

# Score

Results on our annotated corpus:

                    | precision |   recall | f1-score |  support
              **O** |      0.97 |     1.00 |     0.98 |    23487
            **PER** |      0.84 |     0.73 |     0.78 |      525
    **avg / total** |      0.95 |     0.96 |     0.95 |    25002

*Note:* ~1000 tokens are missing, because they belonged to LOC, ORG or MISC. The CRF model was not really trained on these labels and therefore performed poorly. It was only properly trained on PER.


Results on an automatically annotated Wikipedia corpus (therefore some PER labels might have been wrong/missing):

                    | precision |   recall | f1-score |  support
              **O** |  0.97     | 0.98     | 0.98     | 182952
            **PER** |  0.88     | 0.85     | 0.87     | 8854
    **avg / total** |  0.95     | 0.95     | 0.95     | 199239

*Note:* Same as above, LOC, ORG and MISC were removed from the table.