# Automated Detection of Microscopy Artifacts

## Description
Multiplex images of tissue contain information on the gene expression, morphology, and spatial distribution of individual cells comprising biologically specialized niches. However, accurate extraction of cell-level features from pixel-level data is hindered by the presence of microscopy artifacts. Manual curation of noisy cell segmentation instances scales poorly with increasing dataset size, and methods capable of automated artifact detection are needed to enhance workflow efficiency, minimize curator burden, and mitigate human bias. In this challenge, participants will draw on classical and/or machine learning approaches to develop probabilistic classifiers for detecting cell segmentation instances corrupted by microscopy artifacts in multiplex images of tissue.

<object data="https://github.com/IAWG-CSBC-PSON/hack2022-01-artifacts.git/schematic.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="https://github.com/IAWG-CSBC-PSON/hack2022-01-artifacts.git/schematic.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="https://github.com/IAWG-CSBC-PSON/hack2022-01-artifacts.git/schematic.pdf">Download PDF</a>.</p>
    </embed>
</object>

## Training Data
Training data for this challenge consists of a single 1.6cm2 section of primary human colorectal adenocarcinoma (referred to as SARDANA-097) probed for 21 tumor, immune, and stromal markers imaged over 8 rounds of t-CyCIF at 20x resolution.

Data files for this challenge are available at Sage Synapse (Synapse ID: syn26848598) and consist of the following files:

   * 40-channel OME-TIFF image file
   * corresponding single-cell CSV feature table
    - `CellID` - a unique identifier of each cell within the tissue specimen
    - `Hoechst0` through `CollagenIV_647` - log10-transformed average signal intensities of each cell comprising the tissue.  
    - `X_centroid` and `Y_centroid` - coordinates of the cell in tissue specimen.
    - `Area` through `Orientation` - morphological features extracted from segmented cell populations
   * cell segmentation mask
   * cell quality control (QC) mask (i.e. ground truth labels)

## Requisite Output
Classifier output must consist of a two-column CSV file consisting of CellIDs and confidence scores (0-1) for whether each cell is corrupted by a microscopy artifact.

## Performance Evaluation
Classifier confidence scores will be benchmarked against ground truth annotations using Receiver operating characteristic (ROC) curve analysis. To score predictions, simply provide the two-column CSV file of confidence scores and matching `truth.csv` file to `score.py`:

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
