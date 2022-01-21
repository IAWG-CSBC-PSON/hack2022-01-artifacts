# Challenge
Automated Detection of Microscopy Artifacts

## Task
Challenge Participants will use classical and/or machine learning approaches to develop probabilistic classifiers for detecting cell segmentation instances impacted by microscopy artifacts in multiplex images of tissue.

## Data
40-channel t-CyCIF data, a cell segmentation mask, and corresponding single-cell feature table for a 1.6cm2 section of primary human colorectal adenocarcinoma imaged at 20x resolution (SARDANA-097 image) reside at the Sage Synapse data repository under the following ID: syn26848598. The interpretation of columns is as follows:

  * `CellID` - a unique identifier of each cell within the tissue specimen
  * `Area` through `Orientation` - morphological features extracted from segmented cell populations
  * `X_posiiton` and `Y_position` - coordinates of the cell in tissue specimen.


## Performance Evaluation
Binary ground truth annotations for the ~1.2M cells comprising the SARDANA-097 image have been denoted as either 0 (unknown) or 1 (affected by a microscopy artifact) using an existing QC tool for multiplex image analysis (CyLinter; https://github.com/labsyspharm/cylinter). Using these ground truth annotations, algorithm performance will be benchmarked comparing them to those predicted by automated QC methods using Receiver operating characteristic (ROC) curve analysis. To score predictions, we simply provide the two-column CSV file together with the matching "ground truth" file to `score.py`:

```
$ Rscript score.R Lung3-xgboost.csv.gz data/Lung3.csv.gz
Probability-based AUC values

Probability-based AUC for Immune : 0.6778014
Probability-based AUC for Stroma : 0.7163537
Probability-based AUC for  Tumor : 0.7331163

Confusion Matrix and Statistics

          Reference
Prediction Immune Stroma Tumor
    Immune  53953  19481 13484
    Stroma   3792   6920  1600
    Tumor    3508   1492  6333

...
```

Intuitively, we would like a predictor to be more accurate on cells where we are more confident in our ground truth. Conversely, if we are uncertain that a given cell is noisy (based on marker expression), it would be unfair to penalize a morphology-based predictor that misclassifies this cell as Stroma or Immune. This is the intuition behind probability-based AUC metrics, which rank all cells according to the correpsonding posterior probability values and compute area under the ROC curve from the matching predictions.

The remaining metrics are more standard and treat predictions and true labels as discrete class calls.
