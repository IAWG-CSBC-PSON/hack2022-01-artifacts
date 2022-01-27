# Automated Detection of Microscopy Artifacts

## Description
Multiplex images of tissue contain information on the gene expression, morphology, and spatial distribution of individual cells comprising biologically specialized niches. However, accurate extraction of cell-level features from pixel-level data is hindered by the presence of microscopy artifacts. Manual curation of noisy cell segmentation instances scales poorly with increasing dataset size, and methods capable of automated artifact detection are needed to enhance workflow efficiency, minimize curator burden, and mitigate human bias. In this challenge, participants will draw on classical and/or machine learning approaches to develop probabilistic classifiers for detecting cell segmentation instances in multiplex images of tissue corrupted by microscopy artifacts.

![](images/schematic.png)

## Data
Test data for this challenge consists of a single 1.6cm<sup>2</sup> section of primary human colorectal adenocarcinoma probed for 21 different tumor, immune, and stromal markers over 8 rounds of t-CyCIF multiplex immunofluorescence imaging. The dataset was collected as part of the Human Tumor Atlas Network (HTAN) and is referred to as SARDANA-097 image.

Multiclass ground truth annotations detailing microscopy artifacts in the SARDNA-097 image have been previously curated and are provided for model training.

Requisite data files for this challenge are available at the Sage Synapse data repository under Synapse ID [syn26848598](https://www.synapse.org/#!Synapse:syn26848598). Available files are as follows:

<pre>
<b>01-artifacts</b>  
│
└───<b>csv</b>
│   │   ReadMe.txt
│   │   unmicst-WD-76845-097_cellRing.csv
│
└───<b>markers</b>
│   │   markers.csv
│
└───<b>mask</b>
│   │   ReadMe.txt
│   │   cellRingMask.tif
│
└───<b>qc_masks</b>
│   │   ROI_table.csv
│   │   polygon_dict.pkl
│   │   qcmask_cell.tif
│   │   qcmask_pixel.tif
│
└───<b>score</b>
│   │   pr.py
│   │   roc.py
│   │   truth.csv
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
* `csv/unmicst-WD-76845-097_cellRing.csv`: single-cell feature table (CSV format) containing cell IDs, spatial coordinates, integrated fluorescence signal intensities, and nuclear morphology features for 1,242,756 cells constituting the SARDANA-097 image
* `markers/markers.csv`: channel-cycle-marker mapping
* `mask/WD-76845-097.ome.tif`: cell segmentation mask
* `qc/ROI_table.csv`: metadata for ROIs used to define multiple classes of artifacts
* `qc/polygon_dict.pkl`: Python pickle file of ROI shape types (ellipse or polygon) and vertices. Order codeorresponds to ROI metadata in `qc/ROI_table.csv`
* `qc/qcmask_cell.csv`: cell segmentation mask labeled by QC annotation: 0=background, 1=clean, 2=fluorescence aberration, 3=slide debris, 4=coverslip air bubble, 5=uneven tissue staining, 6=image blur.  
* `qc/qcmask_pixel.csv`: multiclass artifact ROI mask
* `score/pr.py`: Python script for computing precision and recall binary classification predictions against ground truth labels (see `score/truth.csv` below)
* `score/roc.py`: Python script for performing multiclass Receiver Operating Characteristic (ROC) curve analysis
* `score/truth.csv`: multiclass ground truth annotations for 1,242,756 cells comprising the SARDANA-097 image
* `seg/WD-76845-097.ome.tif`: cell segmentation outlines
* `tif/WD-76845-097.ome.tif`: stitched and registered 40-channel OME-TIFF pyramid file containing t-CyCIF images for the SARDANA-097 image

## Target Channels
Although the SARDANA-097 dataset comprises a total of 40 channels, only 21 were used in the curation of microscopy artifacts, as several channels represented signals from secondary antibodies alone (used to block non-specific antibody binding) or were otherwise determined to be unsuitable for the purposes of this challenge. When developing classifiers, please use the following channels:

```
'Hoechst0', 'anti_CD3', 'anti_CD45RO', 'Keratin_570', 'aSMA_660', 'CD4_488', 'CD45_PE', 'PD1_647', 'CD20_488', 'CD68_555', 'CD8a_660', 'CD163_488', 'FOXP3_570', 'PDL1_647', 'Ecad_488', 'Vimentin_555', 'CDX2_647', 'LaminABC_488',
'Desmin_555', 'CD31_647', 'PCNA_488', 'CollagenIV_647'
```

## Artifact Classes
Examples of 5 microscopy artifact classes found in the SARDANA-097 image:

![](images/schematic.png)

## Classifier Output
Classifier output should consist of a 7-column CSV file containing Cell IDs and probability scores for whether cells are clean (1) or affected by one of 5 classes of artifacts (2-6).

```
CellID,1,2,3,4,5,6
1,0.95,0.23,0.14,0.05,0.39,0.21
2,0.10,0.09,0.56,0.67,0.89,0.01
3,0.03,0.28,0.22,0.17,0.42,0.91
.
.
.
```

## Performance Evaluation
Multiclass classifier predictions will be scored against ground truth annotations using a combination of Receiver operating characteristic (ROC) curve analysis and binary performance metrics of precision and recall using the following scripts: `pr.py` and `roc.py`.

```
$ python roc.py  multiclass.csv truth.csv
```

![](images/roc.png)

```
$ python pr.py pred.csv truth.csv

precision=0.78, recall=0.67
```

## Suggested Computational Resources and Software Packages
* High-level programming language (Python is recommended)
* Data analysis software libraries such as `pandas`, `numpy`, `scipy`
* Software libraries for reading, writing, analyzing, and visualizing multi-channel image files such as `tifffile`, `skimage`, `matplotlib`, `napari`
* Machine learning and artificial intelligence libraries such as `scikit-learn`, `tensorflow`, `keras`, `pytorch`
* access to a GPU
