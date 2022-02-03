import sys
import pandas as pd
from os.path import abspath


def binary_pr(calls, truth):

    # check that CellIDs between predictions and truth tables match
    assert set(calls['CellID']) == set(truth['CellID']), \
        'Cell IDs mismatch between predictions table and truth table.'

    # check that PREDICTIONS table only contains valid class labels
    assert set(calls['class_label'].unique()).issubset([0, 1]), \
        'Predictions table contains class labels outside of 0 and 1.'

    # check that TRUTH table only contains valid class labels
    assert set(truth['class_label'].unique()).issubset([0, 1]), \
        'Truth table contains class labels other than 0 and 1.'

    # merge prediction and truth tables
    merge = truth.merge(
        calls, how='inner', on='CellID', suffixes=('_truth', '_pred')
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


# read binarized classifier predictions
calls = abspath(sys.argv[1])
calls = pd.read_csv(calls)

# read truth table and binarize artifact labels
truth = abspath(sys.argv[2])
truth = pd.read_csv(truth)

class_metadata = {
    2: 'Fluor', 3: 'Debris', 4: 'Bubble',
    5: 'Staining', 6: 'Blur', 'Overall': 'Overall'
    }

print()
# loop over individual and combined class labels:
for i in [2, 3, 4, 5, 6, 'Overall']:

    truth_copy = truth.copy()
    calls_copy = calls.copy()

    if i == 'Overall':
        truth_copy.loc[
            truth_copy['class_label'] == 1, 'class_label'] = 0  # clean
        truth_copy.loc[
            truth_copy['class_label'] != 0, 'class_label'] = 1  # noisy

        calls_copy.loc[
            calls_copy['class_label'] == 1, 'class_label'] = 0  # clean
        calls_copy.loc[
            calls_copy['class_label'] != 0, 'class_label'] = 1  # noisy

    else:
        truth_copy.loc[
            truth_copy['class_label'] != i, 'class_label'] = 0  # clean
        truth_copy.loc[
            truth_copy['class_label'] == i, 'class_label'] = 1  # noisy

        calls_copy.loc[
            calls_copy['class_label'] != i, 'class_label'] = 0  # clean
        calls_copy.loc[
            calls_copy['class_label'] == i, 'class_label'] = 1  # noisy

    # compute precision and recall on input
    precision, recall = binary_pr(calls_copy, truth_copy)

    # print precision and recall values
    print(
        f'\033[1m{class_metadata[i]}:\033[0m ' +
        f'precision={precision}, recall={recall}'
        )
