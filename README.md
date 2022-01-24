# Automated Detection of Microscopy Artifacts

## Challenge Description
Multiplex images of tissue contain information on the gene expression, morphology, and spatial distribution of individual cells comprising biologically specialized niches. However, accurate extraction of cell-level features from pixel-level data is hindered by the presence of microscopy artifacts. Manual curation of noisy cell segmentation instances scales poorly with increasing dataset size, and methods capable of automated artifact detection are needed to enhance workflow efficiency, minimize curator burden, and mitigate human bias. In this challenge, participants will draw on classical and/or machine learning approaches to develop probabilistic classifiers for detecting cell segmentation instances in multiplex images of tissue corrupted by microscopy artifacts.

![](schematic.png)

## Data
Test data for this challenge consists of a single 1.6cm<sup>2</sup> section of primary human colorectal adenocarcinoma probed for 21 different tumor, immune, and stromal markers over 8 rounds of t-CyCIF multiplex fluorescence imaging. This dataset, collected as part of the Human Tumor Atlas Network (HTAN), is referred to as SARDANA-097 image consists of a stitched, registered, and segmented 40-channel OME-TIFF pyramid file and corresponding single-cell data for 1,242,756 cells constituting the tissue.

Pixel and cell-level ground truth QC masks detailing multiple classes of microscopy artifacts affecting this multi-channel image have been manually curated and are provided for model training.

All requisite data files for this challenge are available at the Sage Synapse data repository under Synapse ID syn26848598. The following data files are available:

<pre>
<b>01-artifacts</b>
│   markers.csv    
│
└───<b>csv</b>
│   │   ReadMe.txt
│   │   unmicst-WD-76845-097_cellRing.csv
│
└───<b>mask</b>
│   │   ReadMe.txt
│   │   cellRingMask.tif
│
└───<b>qc_masks</b>
│   │   ROI_table.csv
│   │   qcmask_cell.tif
│   │   qcmask_pixel.tif
│   │   polygon_dict.pkl
│
└───<b>seg</b>
│   │   ReadMe.txt
│   │   WD-76845-097.ome.tif
│
└───<b>tif</b>
│   │   ReadMe.txt
│   │   WD-76845-097.ome.tif
</pre>

File descriptions:
* `markers.csv`: channel-to-marker mapping for 40 imaging channels across 10 rounds of t-CyCIF.
* `tif/WD-76845-097.ome.tif`: 40-channel OME-TIFF pyramid file for the SARDANA-097 dataset.
* `mask/WD-76845-097.ome.tif`: cell segmentation mask for the SARDANA-097 dataset.
* `seg/WD-76845-097.ome.tif`: cell segmentation outlines (boundaries) for the SARDANA-097 dataset.
* `csv/unmicst-WD-76845-097_cellRing.csv`: single-cell feature table (CSV format) containing cell IDs, spatial coordinates, integrated fluorescence signal intensities, and nuclear morphology features for 1,242,756 cells constituting the SARDANA-097 image.
* `qc_masks/ROI_table.csv`: ROI metadata file
* `qc_masks/qcmask_cell.csv`: multi-class QC mask annotated at the single-cell level
* `qc_masks/qcmask_pixel.csv`: multi-class QC mask annotated at the single-cell level
* `qc_masks/polygon_dict.pkl`: Python pickle file containing shape types (ellipse/polygon) and vertice coordinates for ROIs specified in `qc_masks/ROI_table.csv`.  

## Output
Classifiers should output a two-column CSV file of CellIDs and corresponding probability scores (0-1) for whether a cell is corrupted by a microscopy artifact.

## Performance Evaluation
Classifier predictions will be scored relative to ground truth annotations using Receiver operating characteristic (ROC) curve analysis by providing CSV files of probability scores and ground truth annotations (`truth.csv`) file to the script `score.py`:

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
