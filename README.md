# Automated Detection of Microscopy Artifacts

## Challenge Description
Multiplex images of tissue contain information on the gene expression, morphology, and spatial distribution of individual cells comprising biologically specialized niches. However, accurate extraction of cell-level features from pixel-level data is hindered by the presence of microscopy artifacts. Manual curation of noisy cell segmentation instances scales poorly with increasing dataset size, and methods capable of automated artifact detection are needed to enhance workflow efficiency, minimize curator burden, and mitigate human bias. In this challenge, participants will draw on classical and/or machine learning approaches to develop probabilistic classifiers for detecting cell segmentation instances in multiplex images of tissue corrupted by microscopy artifacts.

![](schematic.png)

## Data
Test data for this challenge consists of a single 1.6cm<sup>2</sup> section of primary human colorectal adenocarcinoma collected as part of the Human Tumor Atlas Network (HTAN) and is referred to as SARDANA-097. This tissue (shown in the image above) was probed for 21 tumor, immune, and stromal markers over over 8 rounds of t-CyCIF. The MCMICRO multiple image processing pipeline was used to produce a stitched, registered, and segmented 40-channel OME-TIFF file file and corresponding single-cell data on the 1,242,756 cell segmentation instances comprising the tissue.

Data files for the SARDANA-097 image plus manually curated quality control masks highlighting regions of the tissue affected by microscopy artifacts are available at the Sage Synapse data repository (Synapse ID: syn26848598) and consist of the following:

```
01-artifacts
│   markers.csv    
│
└───**csv**
│   │   ReadMe.txt
│   │   unmicst-WD-76845-097_cellRing.csv
│   
└───**cylinter_output**
│   │
│   └───**ROIs**
│   │    │   polygon_dict.pkl
│   │
│   └───**checkpoints**
│   │    │   aggregateData.parquet
│   │    │   selectROIs.parquet
│
└───**mask**
│   │   ReadMe.txt
│   │   cellRingMask.tif
│
└───**qc_masks**
│   │   ROI_table.CSV
│   │   qcmask_cell.tif
│   │   qcmask_pixel.tif
│
└───**seg**
│   │   ReadMe.txt
│   │   WD-76845-097.ome.tif
│
└───**tif**
│   │   ReadMe.txt
│   │   WD-76845-097.ome.tif
```

   * 40-channel OME-TIFF image file
   * single-cell feature table (CSV format) with the following columns:
     * `CellID` - a unique identifier for each cell within the tissue
     * `Hoechst0` through `CollagenIV_647` - log10-transformed integrated signal intensities for each of 40 channels.  
     * `X_centroid` and `Y_centroid` - spatial coordinates of cells in the tissue
     * `Area` through `Orientation` - nuclear morphological features extracted from segmented cells
   * cell segmentation mask indexed 0-n, where n is the number of segmented   cells in the tissue (1,242,756)
   * quality control mask indexed 0-5 (0=unknown, 1=fluorescence aberration, 2=slide debris, 3=cover slip air bubble, 4=tissue detachment, 5=image blur)

## Requisite Output
Classifier output must consist of a two-column CSV file of CellIDs and confidence scores (0-1) for whether each cell in the SARDANA-097 image is corrupted by a microscopy artifact.

## Performance Evaluation
Classifier performance will be benchmarked against ground truth annotations using Receiver operating characteristic (ROC) curve analysis. To score predictions, simply provide the two-column CSV file of confidence scores and matching `truth.csv` file to `score.py`:

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
