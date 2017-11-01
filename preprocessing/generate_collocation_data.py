import os
import json
import nltk
import pandas as pd
from itertools import izip
from nltk.collocations import *
from config import CURRENT_DIR, COLOR_LIST


def get_topic_tokens(data):
    stopwords = set(nltk.corpus.stopwords.words())
    tokens = nltk.word_tokenize(data)
    tokens = [t.lower() for t in tokens]
    stop_list = []
    for i in range(len(tokens)):
        if tokens[i] == '.':
            stop_list.append(i)
    sents_list = []
    for s in izip([0] + stop_list[:-1], stop_list):
        sents_list.append(tokens[s[0]:s[1]])
    tag_token_sents = nltk.pos_tag_sents(sents_list)
    nn_list = []
    for s in tag_token_sents:
        nns = [t[0] for t in s if t[0].isalpha() and t[1] == 'NN']
        nn_list.extend([t for t in nns if t not in stopwords and len(t) > 3])
    print nn_list[:30]
    return nn_list


def collect_collocation(bigrams):
    topic_set = set()
    topic_quota = 20
    matrix = []
    tpl_count = 0
    to_index = {}
    for tpl in bigrams:
        if tpl[0][0] != tpl[0][1]:
            topic_set.add(tpl[0][0])
            topic_set.add(tpl[0][1])
            tpl_count += 1
            if len(topic_set) >= topic_quota:
                break
    topic_list = list(topic_set)
    for i in range(len(topic_list)):
        to_index[topic_list[i]] = i
    for i in range(len(topic_set)):
        matrix.append([0] * len(topic_set))
    i = 0
    while tpl_count > 0:
        if tpl[0][0] != tpl[0][1]:
            bigram = bigrams[i][0]
            matrix[to_index[bigram[0]]][to_index[bigram[1]]] += bigrams[i][1]
            tpl_count -= 1
    return topic_list, matrix


def write_to_file(topics, matrix, out_path):
    with open(os.path.join(out_path, "stack-matrix.json"), "w") as fout:
        fout.write(json.dumps(matrix))
    data = []
    for i in range(len(topics)):
        data.append([topics[i], 0, 0, 0, COLOR_LIST[i]])
    topics_df = pd.DataFrame(data=data, columns=['name', 'x', 'y', 'p', 'colors'])
    topics_df.to_csv(os.path.join(out_path, "stack-topics.csv"), index=False)


def main():
    with open(os.path.join(CURRENT_DIR, 'stackoverflow_content'), 'r') as f:
        data = "".join(line.rstrip() for line in f)
    # bigram_measures = nltk.collocations.BigramAssocMeasures()
    # trigram_measures = nltk.collocations.TrigramAssocMeasures()
    topic_tokens = get_topic_tokens(data.decode('utf-8'))
    finder = BigramCollocationFinder.from_words(topic_tokens)
    sorted_bigrams = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))
    topics, matrix = collect_collocation(sorted_bigrams)
    out_dir = os.path.join(CURRENT_DIR, 'collocation')
    write_to_file(topics, matrix, out_dir)


if __name__ == "__main__":
    main()