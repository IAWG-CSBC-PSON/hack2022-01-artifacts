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

# Import some data to play with
iris = datasets.load_iris()

y = iris.target  # class_labels

# format class labels
# truth = pd.read_csv('/Users/greg/projects/QC_challenge/truth.csv')
# truth = truth.sample(n=1000000, random_state=random_state)
# truth.sort_values(by='CellID', inplace=True)
# y = truth['class_label'].values

# Binarize the output
y = label_binarize(y, classes=[0, 1, 2])
n_classes = y.shape[1]

###############################################################################

# format single-cell data
# X = pd.read_csv(
#     '/Users/greg/projects/QC_challenge/csv/unmicst-WD-76845-097_cellRing.csv'
#     )
# X = X[X['CellID'].isin(truth['CellID'])]
# X.sort_values(by='CellID', inplace=True)
#
# # select 21 channels in which artifact annotations were made
# X = X[['Hoechst0', 'anti_CD3', 'anti_CD45RO', 'Keratin_570', 'aSMA_660',
#        'CD4_488', 'CD45_PE', 'PD1_647', 'CD20_488', 'CD68_555', 'CD8a_660',
#        'CD163_488', 'FOXP3_570', 'PDL1_647', 'Ecad_488', 'Vimentin_555',
#        'CDX2_647', 'LaminABC_488', 'Desmin_555', 'CD31_647', 'PCNA_488',
#        'CollagenIV_647']].values

X = iris.data

# Add noisy features to make the problem harder
random_state = np.random.RandomState(0)
n_samples, n_features = X.shape
X = np.c_[X, random_state.randn(n_samples, 200 * n_features)]

###############################################################################

# shuffle and split training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, random_state=0
    )

###############################################################################

# Learn to predict each class against the other
classifier = OneVsRestClassifier(
    svm.SVC(kernel='linear', probability=True, random_state=random_state)
    )
y_score = classifier.fit(X_train, y_train).decision_function(X_test)

###############################################################################
# Compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Compute micro-average ROC curve and ROC area
fpr['micro'], tpr['micro'], _ = roc_curve(y_test.ravel(), y_score.ravel())
roc_auc['micro'] = auc(fpr['micro'], tpr['micro'])

# Compute macro-average ROC curve and ROC area
# First aggregate all false positive rates
all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))
# Then interpolate all ROC curves at this points
mean_tpr = np.zeros_like(all_fpr)
for i in range(n_classes):
    mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])
# Finally average it and compute AUC
mean_tpr /= n_classes

fpr["macro"] = all_fpr
tpr["macro"] = mean_tpr
roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

###############################################################################

# Plot of an ROC curve for a specific class
plt.figure()
lw = 2
# class_metadata = {
#     0: ('blobs', 'tab:blue'), 1: ('debris', 'tab:orange'),
#     2: ('bubbles', 'tab:green'), 'micro': ('micro', 'tab:red'),
#     'macro': ('macro', 'tab:purple')
#     }

class_metadata = {
    0: ('Class 0', 'tab:blue'), 1: ('Class 1', 'tab:orange'),
    2: ('Class 2', 'tab:green'), 'micro': ('micro', 'tab:red'),
    'macro': ('macro', 'tab:purple')
    }

for cls, data in class_metadata.items():
    plt.plot(
        fpr[cls], tpr[cls], color=data[1], lw=lw,
        label=f"{data[0]} (area = %0.2f)" % roc_auc[cls]
        )

plt.plot([0, 1], [0, 1], color='tab:gray', alpha=0.5, lw=lw, linestyle="--")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic (ROC) curve')
plt.legend(loc='lower right')
plt.show()
