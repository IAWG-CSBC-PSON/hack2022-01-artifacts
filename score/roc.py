import sys
from os.path import abspath

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle

from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import roc_auc_score

###############################################################################

# read classifier predictions
pred = abspath(sys.argv[1])
pred = pd.read_csv(pred)
pred.sort_values(by='CellID', inplace=True)
y_pred = pred.loc[:, ['1', '2', '3', '4', '5', '6']].values

# read truth table and binarize class labels
truth = abspath(sys.argv[2])
truth = pd.read_csv(truth)
truth.sort_values(by='CellID', inplace=True)
y_truth = truth['class_label'].values
y_truth = label_binarize(y_truth, classes=[1, 2, 3, 4, 5, 6])

# number of classes
n_classes = y_truth.shape[1]

###############################################################################

# compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i+1], tpr[i+1], _ = roc_curve(y_truth[:, i], y_pred[:, i])
    roc_auc[i+1] = auc(fpr[i+1], tpr[i+1])

# compute micro-average ROC curve and ROC area
fpr['micro'], tpr['micro'], _ = roc_curve(y_truth.ravel(), y_truth.ravel())
roc_auc['micro'] = auc(fpr['micro'], tpr['micro'])

# compute macro-average ROC curve and ROC area
# first aggregate all false positive rates
all_fpr = np.unique(np.concatenate([fpr[i+1] for i in range(n_classes)]))

# then interpolate all ROC curves at this points
mean_tpr = np.zeros_like(all_fpr)
for i in range(n_classes):
    mean_tpr += np.interp(all_fpr, fpr[i+1], tpr[i+1])

# finally average it and compute AUC
mean_tpr /= n_classes

fpr['macro'] = all_fpr
tpr['macro'] = mean_tpr
roc_auc['macro'] = auc(fpr['macro'], tpr['macro'])

###############################################################################

# class metadata
class_metadata = {
    2: ('Fluor', 'tab:blue'), 3: ('Debris', 'tab:orange'),
    4: ('Bubble', 'tab:pink'), 5: ('Staining', 'tab:olive'),
    6: ('Blur', 'tab:purple'), 'micro': ('Micro', 'tab:red'),
    'macro': ('Macro', 'tab:green'), 'random': ('Random', 'tab:gray'),
    }

# plot ROC curves
plt.figure()

# line width
lw = 2

for cls, data in class_metadata.items():

    if cls == 'random':
        plt.plot(
            [0, 1], [0, 1], color='tab:gray', alpha=0.5, lw=lw, linestyle='--',
            label=f'{data[0]} (area = %0.2f)' % 0.5
            )
    else:
        plt.plot(
            fpr[cls], tpr[cls], color=data[1], lw=lw,
            label=f'{data[0]} (area = %0.2f)' % roc_auc[cls]
            )

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic (ROC) curve')
plt.legend(loc='lower right')
plt.show()
