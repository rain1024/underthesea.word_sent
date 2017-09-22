# -*- coding: utf-8 -*-
import pycrfsuite
from os.path import join
from os.path import dirname

from models.crf_2.transformer import Transformer, sent2labels


def train():
    transformer = Transformer()
    train_sents = transformer.load_train_sents()
    matrix = []
    for sentence in train_sents:
        matrix.append(transformer.list_to_tuple(transformer.format_word(sentence)))
    train_sents = matrix
    X_train = [Transformer.extract_features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]
    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)
    trainer.set_params({
        'c1': 1.0,  # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 2000,  #
        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    })
    trainer.train(join(dirname(__file__), "crf-model-2"))


if __name__ == '__main__':
    train()
