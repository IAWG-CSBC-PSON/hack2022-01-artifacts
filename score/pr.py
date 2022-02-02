import sys
import pandas as pd
from os.path import abspath


def binary_pr(pred, truth):

    # check that CellIDs between predictions and truth tables match
    assert set(pred['CellID']) == set(truth['CellID']), \
        'Cell IDs mismatch between predictions table and truth table.'

    # check that PREDICTIONS table only contains valid class labels
    assert set(pred['class_label'].unique()).issubset([0, 1]), \
        'Predictions table contains class labels outside of 0 and 1.'

    # check that TRUTH table only contains valid class labels
    assert set(truth['class_label'].unique()).issubset([0, 1]), \
        'Truth table contains class labels other than 0 and 1.'

    # merge prediction and truth tables
    merge = truth.merge(
        pred, how='inner', on='CellID', suffixes=('_truth', '_pred')
        )

    # Identify true positives, true negatives,
    # false positives, and false negatives
    true_pos = merge[
        (merge['class_label_truth'] == 1) & (merge['class_label_pred'] == 1)]
    true_neg = merge[
        (merge['class_label_truth'] == 0) & (merge['class_label_pred'] == 0)]
    false_pos = merge[
        (merge['class_label_truth'] == 0) & (merge['class_label_pred'] == 1)]
    false_neg = merge[
        (merge['class_label_truth'] == 1) & (merge['class_label_pred'] == 0)]

    # compute precision and recall
    precision = round(len(true_pos)/(len(true_pos) + len(false_pos)), 2)
    recall = round(len(true_pos)/(len(true_pos) + len(false_neg)), 2)

    return precision, recall


# read prediction table
pred = abspath(sys.argv[1])
pred = pd.read_csv(pred)

# read truth table
truth = abspath(sys.argv[2])
truth = pd.read_csv(truth)

# compute precision and recall on input
precision, recall = binary_pr(pred, truth)

# print precision and recall values
print()
print(f'precision={precision}, recall={recall}')
