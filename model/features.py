# -*- coding: utf-8 -*-
"""
Contains:
    1. Various classes (feature generators) to convert windows (of words/tokens) to feature values.
       Each feature value is a string, e.g. "starts_with_uppercase=1".
    2. A method to create all feature generators.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import re

from model.pos import PosTagger
from model.unigrams import Unigrams

# All capitalized constants come from this file
import config as cfg

def create_features(verbose=True):
    """This method creates all feature generators.
    The feature generators will be used to convert windows of tokens to their string features.

    This function may run for a few minutes.

    Args:
        verbose: Whether to output messages.
    Returns:
        List of feature generators
    """

    def print_if_verbose(msg):
        """This method prints a message only if verbose was set to True, otherwise does nothing.
        Args:
            msg: The message to print.
        """
        if verbose:
            print(msg)

    # Load the most common unigrams. These will be used as features.
    print_if_verbose("Loading top N unigrams...")
    ug_all_top = Unigrams(cfg.UNIGRAMS_FILEPATH, skip_first_n=cfg.UNIGRAMS_SKIP_FIRST_N,
                          max_count_words=cfg.UNIGRAMS_MAX_COUNT_WORDS)

    # Load all unigrams. These will be used to create the Gazetteer.
    print_if_verbose("Loading all unigrams...")
    ug_all = Unigrams(cfg.UNIGRAMS_FILEPATH)

    # Load all unigrams of person names (PER). These will be used to create the Gazetteer.
    print_if_verbose("Loading person name unigrams...")
    ug_names = Unigrams(cfg.UNIGRAMS_PERSON_FILEPATH)

    # Unset ug_all and ug_names because we don't need them any more and they need quite a bit of
    # RAM.
    ug_all = None
    ug_names = None

    # Load the wrapper for the stanford POS tagger
    print_if_verbose("Loading POS-Tagger...")
    pos = PosTagger(cache_filepath=cfg.POS_TAGGER_CACHE_FILEPATH)

    # create feature generators
    result = [
        StartsWithUppercaseFeature(),
        TokenLengthFeature(),
        ContainsDigitsFeature(),
        ContainsPunctuationFeature(),
        OnlyDigitsFeature(),
        OnlyPunctuationFeature(),
        WordPatternFeature(),
        UnigramRankFeature(ug_all_top),
        PrefixFeature(),
        SuffixFeature(),
        POSTagFeature(pos),
    ]
    return result

class StartsWithUppercaseFeature(object):
    """Generates a feature that describes, whether a given token starts with an uppercase letter."""
    def __init__(self):
        """Instantiates a new object of this feature generator."""
        pass

    def convert_window(self, window):
        """Converts a Window object into a list of lists of features, where features are strings.
        Args:
            window: The Window object (defined in datasets.py) to use.
        Returns:
            List of lists of features.
            One list of features for each token.
            Each list can contain any number of features (including 0).
            Each feature is a string.
        """
        result = []
        for token in window.tokens:
            result.append(["swu=%d" % (int(token.word[:1].istitle()))])
        return result

class TokenLengthFeature(object):
    """Generates a feature that describes the character length of a token."""
    def __init__(self, max_length=30):
        """Instantiates a new object of this feature generator.
        Args:
            max_length: The max length to return in the generated features, e.g. if set to 30 you
                will never get a "l=31" result, only "l=30" for a token with length >= 30.
        """
        self.max_length = max_length

    def convert_window(self, window):
        """Converts a Window object into a list of lists of features, where features are strings.
        Args:
            window: The Window object (defined in datasets.py) to use.
        Returns:
            List of lists of features.
            One list of features for each token.
            Each list can contain any number of features (including 0).
            Each feature is a string.
        """
        result = []
        for token in window.tokens:
            result.append(["l=%d" % (min(len(token.word), self.max_length))])
        return result

class ContainsDigitsFeature(object):
    """Generates a feature that describes, whether a token contains any digit."""
    def __init__(self):
        """Instantiates a new object of this feature generator."""
        self.regexp_contains_digits = re.compile(r'[0-9]+')

    def convert_window(self, window):
        """Converts a Window object into a list of lists of features, where features are strings.
        Args:
            window: The Window object (defined in datasets.py) to use.
        Returns:
            List of lists of features.
            One list of features for each token.
            Each list can contain any number of features (including 0).
            Each feature is a string.
        """
        result = []
        for token in window.tokens:
            any_digits = self.regexp_contains_digits.search(token.word) is not None
            result.append(["cD=%d" % (int(any_digits))])
        return result

class ContainsPunctuationFeature(object):
    """Generates a feature that describes, whether a token contains any punctuation."""
    def __init__(self):
        """Instantiates a new object of this feature generator."""
        self.regexp_contains_punctuation = re.compile(r'[\.\,\:\;\(\)\[\]\?\!]+')

    def convert_window(self, window):
        """Converts a Window object into a list of lists of features, where features are strings.
        Args:
            window: The Window object (defined in datasets.py) to use.
        Returns:
            List of lists of features.
            One list of features for each token.
            Each list can contain any number of features (including 0).
            Each feature is a string.
        """
        result = []
        for token in window.tokens:
            any_punct = self.regexp_contains_punctuation.search(token.word) is not None
            result.append(["cP=%d" % (int(any_punct))])
        return result

class OnlyDigitsFeature(object):
    """Generates a feature that describes, whether a token contains only digits."""
    def __init__(self):
        """Instantiates a new object of this feature generator."""
        self.regexp_contains_only_digits = re.compile(r'^[0-9]+$')

    def convert_window(self, window):
        """Converts a Window object into a list of lists of features, where features are strings.
        Args:
            window: The Window object (defined in datasets.py) to use.
        Returns:
            List of lists of features.
            One list of features for each token.
            Each list can contain any number of features (including 0).
            Each feature is a string.
        """
        result = []
        for token in window.tokens:
            only_digits = self.regexp_contains_only_digits.search(token.word) is not None
            result.append(["oD=%d" % (int(only_digits))])
        return result

class OnlyPunctuationFeature(object):
    """Generates a feature that describes, whether a token contains only punctuation."""
    def __init__(self):
        """Instantiates a new object of this feature generator."""
        self.regexp_contains_only_punctuation = re.compile(r'^[\.\,\:\;\(\)\[\]\?\!]+$')

    def convert_window(self, window):
        """Converts a Window object into a list of lists of features, where features are strings.
        Args:
            window: The Window object (defined in datasets.py) to use.
        Returns:
            List of lists of features.
            One list of features for each token.
            Each list can contain any number of features (including 0).
            Each feature is a string.
        """
        result = []
        for token in window.tokens:
            only_punct = self.regexp_contains_only_punctuation.search(token.word) is not None
            result.append(["oP=%d" % (int(only_punct))])
        return result

class WordPatternFeature(object):
    """Generates a feature that describes the word pattern of a feature.
    A word pattern is a rough representation of the word, examples:
        original word | word pattern
        ----------------------------
        John          | Aa+
        Washington    | Aa+
        DARPA         | A+
        2055          | 9+
    """
    def __init__(self):
        """Instantiates a new object of this feature generator."""
        # maximum length of tokens after which to simply cut off
        self.max_length = 15
        # if cut off because of maximum length, use this char at the end of the word to signal
        # the cutoff
        self.max_length_char = "~"

        self.normalization = [
            (r"[A-ZÄÖÜ]", "A"),
            (r"[a-zäöüß]", "a"),
            (r"[0-9]", "9"),
            (r"[\.\!\?\,\;]", "."),
            (r"[\(\)\[\]\{\}]", "("),
            (r"[^Aa9\.\(]", "#")
        ]

        # note: we do not map numers to 9+, e.g. years will still be 9999
        self.mappings = [
            (r"[A]{2,}", "A+"),
            (r"[a]{2,}", "a+"),
            (r"[\.]{2,}", ".+"),
            (r"[\(]{2,}", "(+"),
            (r"[#]{2,}", "#+")
        ]

    def convert_window(self, window):
        """Converts a Window object into a list of lists of features, where features are strings.
        Args:
            window: The Window object (defined in datasets.py) to use.
        Returns:
            List of lists of features.
            One list of features for each token.
            Each list can contain any number of features (including 0).
            Each feature is a string.
        """
        result = []
        for token in window.tokens:
            result.append(["wp=%s" % (self.token_to_wordpattern(token))])
        return result

    def token_to_wordpattern(self, token):
        """Converts a token/word to its word pattern.
        Args:
            token: The token/word to convert.
        Returns:
            The word pattern as string.
        """
        normalized = token.word
        for from_regex, to_str in self.normalization:
            normalized = re.sub(from_regex, to_str, normalized)

        wpattern = normalized
        for from_regex, to_str in self.mappings:
            wpattern = re.sub(from_regex, to_str, wpattern)

        if len(wpattern) > self.max_length:
            wpattern = wpattern[0:self.max_length] + self.max_length_char

        return wpattern

class UnigramRankFeature(object):
    """Generates a feature that describes the rank of the word among a list of unigrams, ordered
    descending, i.e. the most common word would have the rank 1.
    """
    def __init__(self, unigrams):
        """Instantiates a new object of this feature generator.
        Args:
            unigrams: An instance of Unigrams as defined in unigrams.py that can be queried
                to estimate the rank of a word among all unigrams.
        """
        self.unigrams = unigrams

    def convert_window(self, window):
        """Converts a Window object into a list of lists of features, where features are strings.
        Args:
            window: The Window object (defined in datasets.py) to use.
        Returns:
            List of lists of features.
            One list of features for each token.
            Each list can contain any number of features (including 0).
            Each feature is a string.
        """
        result = []
        for token in window.tokens:
            result.append(["ng1=%d" % (self.token_to_rank(token))])
        return result

    def token_to_rank(self, token):
        """Converts a token/word to its unigram rank.
        Args:
            token: The token/word to convert.
        Returns:
            Unigram rank as integer,
            or -1 if it wasn't found among the unigrams.
        """
        return self.unigrams.get_rank_of(token.word, -1)

class PrefixFeature(object):
    """Generates a feature that describes the prefix (the first three chars) of the word."""
    def __init__(self):
        """Instantiates a new object of this feature generator."""
        pass

    def convert_window(self, window):
        """Converts a Window object into a list of lists of features, where features are strings.
        Args:
            window: The Window object (defined in datasets.py) to use.
        Returns:
            List of lists of features.
            One list of features for each token.
            Each list can contain any number of features (including 0).
            Each feature is a string.
        """
        result = []
        for token in window.tokens:
            prefix = re.sub(r"[^a-zA-ZäöüÄÖÜß\.\,\!\?]", "#", token.word[0:3])
            result.append(["pf=%s" % (prefix)])
        return result

class SuffixFeature(object):
    """Generates a feature that describes the suffix (the last three chars) of the word."""
    def __init__(self):
        """Instantiates a new object of this feature generator."""
        pass

    def convert_window(self, window):
        """Converts a Window object into a list of lists of features, where features are strings.
        Args:
            window: The Window object (defined in datasets.py) to use.
        Returns:
            List of lists of features.
            One list of features for each token.
            Each list can contain any number of features (including 0).
            Each feature is a string.
        """
        result = []
        for token in window.tokens:
            suffix = re.sub(r"[^a-zA-ZäöüÄÖÜß\.\,\!\?]", "#", token.word[-3:])
            result.append(["sf=%s" % (suffix)])
        return result

class POSTagFeature(object):
    """Generates a feature that describes the Part Of Speech tag of the word."""
    def __init__(self, pos_tagger):
        """Instantiates a new object of this feature generator.
        Args:
            pos_tagger: An instance of PosTagger as defined in pos.py that can be queried
                to estimate the POS-tag of a word.
        """
        self.pos_tagger = pos_tagger

    def convert_window(self, window):
        """Converts a Window object into a list of lists of features, where features are strings.
        Args:
            window: The Window object (defined in datasets.py) to use.
        Returns:
            List of lists of features.
            One list of features for each token.
            Each list can contain any number of features (including 0).
            Each feature is a string.
        """
        pos_tags = self.pos_tag(window)
        result = []
        
        # catch stupid problems with stanford POS tagger and unicode characters
        if len(pos_tags) == len(window.tokens):
            # _ is the word
            for _, pos_tag in pos_tags:
                result.append(["pos=%s" % (pos_tag)])
        else:
            orig_str = "|".join([token.word for token in window.tokens])
            pos_str = "|".join([word for word, _ in pos_tags])
            print("[Info] Stanford POS tagger got sequence of length %d, returned " \
                  "POS-sequence of length %d. This sometimes happens with special unicode " \
                  "characters. Returning empty list instead." % (len(window.tokens), len(pos_tags)))
            print("[Info] Original sequence was:", orig_str)
            print("[Info] Tagged sequence      :", pos_str)

            # fill with empty feature value lists (one empty list per token)
            for _ in range(len(window.tokens)):
                result.append([])

        return result

    def pos_tag(self, window):
        """Converts a Window (list of tokens) to their POS tags.
        Args:
            window: Window object containing the token list to POS-tag.
        Returns:
            List of POS tags as strings.
        """
        return self.pos_tagger.tag([token.word for token in window.tokens if len(token.word) > 0])
