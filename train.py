# -*- coding: utf-8 -*-
"""
Main training file for the CRF.
This file trains a CRF model and saves it under the filename provided via an 'identifier' command
line argument.

Usage example:
    python train.py --identifier="my_experiment"
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import random
import pycrfsuite

from model.datasets import load_windows, load_articles, generate_examples
import model.features as features

# All capitalized constants come from this file
import config as cfg

random.seed(42)

def main():
    """This function handles the command line arguments and then calls the train() method."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--identifier", required=True,
                        help="A short name/identifier for your experiment, e.g. 'ex42b'.")
    args = parser.parse_args()

    train(args)

def train(args):
    """Main training method.
    """
    trainer = pycrfsuite.Trainer(verbose=True)

    # Create/Initialize the feature generators
    # this may take a few minutes
    print("Creating features...")
    feature_generators = features.create_features()

    # Initialize the window generator
    # each window has a fixed maximum size of tokens
    print("Loading windows...")
    windows = load_windows(load_articles(cfg.ARTICLES_FILEPATH), cfg.WINDOW_SIZE,
                           feature_generators, only_labeled_windows=True)

    # Add chains of features (each list of lists of strings)
    # and chains of labels (each list of strings)
    # to the trainer.
    print("Adding example windows (up to max %d)..." % (cfg.COUNT_WINDOWS_TRAIN))

    examples = generate_examples(windows, nb_append=cfg.COUNT_WINDOWS_TRAIN,
                                 nb_skip=cfg.COUNT_WINDOWS_TEST, verbose=True)
    for feature_values_lists, labels, tokens in examples:
        trainer.append(feature_values_lists, labels)

    # Train the model
    # this may take several hours
    print("Training...")
    if cfg.MAX_ITERATIONS is not None and cfg.MAX_ITERATIONS > 0:
        # set the maximum number of iterations of defined in the config file
        # the optimizer stops automatically after some iterations if this is not set
        trainer.set_params({'max_iterations': cfg.MAX_ITERATIONS})
    trainer.train(args.identifier)

# ----------------

if __name__ == "__main__":
    main()
