import hashlib
import os

import ATD
from nltk import word_tokenize, sent_tokenize
from nltk.draw.tree import TreeView
from nltk.parse.corenlp import CoreNLPParser

h = hashlib.md5()
h.update('zpiao1'.encode())
key = h.hexdigest()

ATD.setDefaultKey(key)

parser = CoreNLPParser()

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.split(dir_path)[0]
filename = os.path.join(parent_dir, 'stackoverflow_content')


def get_valid_filename(s):
    s = s.lower()
    tokens = word_tokenize(s)
    tokens = [token for token in tokens if token.isalnum()]
    return '_'.join(tokens)


def correct(line, errors):
    correct_line = line
    for error in errors:
        correct_line = correct_line.replace(error.string, error.suggestions[0])
    return correct_line


with open(filename, encoding='utf-8') as f:
    file_content = f.read().replace('\n', '')
    file_content = ' '.join(file_content.split())
    lines = sent_tokenize(file_content)
    lines = [line for line in lines if line != ''
             and len(word_tokenize(line)) <= 10
             and line[-1] in '.?!'
             and line[0].isupper()]
    print(len(lines))
    wrong_lines_count = 0
    pic_count = 0
    for i, line in enumerate(lines):
        if wrong_lines_count == 5:
            break
        print('Original line: ' + line)
        tree = next(parser.raw_parse(line))
        if pic_count < 5 and word_tokenize(line) == 10:
            filename = get_valid_filename(line)
            TreeView(tree)._cframe.print_to_file(filename + '.ps')
            pic_count += 1
        errors = ATD.checkDocument(line)
        if len(list(errors)) == 0:
            print('**No errors** ({}/{})'.format(i + 1, len(lines)))
            continue
        else:
            print()
        correct_line = correct(line, errors)
        tree.pretty_print()
        print('Correct line: ' + correct_line)
        correct_tree = next(parser.raw_parse(correct_line))
        correct_tree.pretty_print()
        wrong_lines_count += 1
    print('Number of wrong sentences: {}'.format(wrong_lines_count))
