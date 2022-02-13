# Automated Detection of Microscopy Artifacts

## Description
Multiplex images of tissue contain information on the gene expression, morphology, and spatial distribution of individual cells comprising biologically specialized niches. However, accurate extraction of cell-level features from pixel-level data is hindered by the presence of microscopy artifacts. Manual curation of noisy cell segmentation instances scales poorly with increasing dataset size, and methods capable of automated artifact detection are needed to enhance workflow efficiency, minimize curator burden, and mitigate human bias. In this challenge, participants will draw on classical and/or machine learning approaches to develop probabilistic classifiers for detecting cell segmentation instances in multiplex images of tissue corrupted by microscopy artifacts.

![](images/schematic.png)

## Dataset
Test data for this challenge was collected as part of the Human Tumor Atlas Network (HTAN) and consists of a single 1.6cm<sup>2</sup> section of primary human colorectal adenocarcinoma probed for 21 tumor, immune, and stromal markers over 8 rounds of [CyCIF](https://www.cycif.org/) multiplex immunofluorescence imaging (SARDANA-097).

Multiclass quality control (QC) annotations for microscopy artifacts present in the multi-channels SARDANA-097 image have been manually curated and are provided as training labels for model training. These and other data files for the SARDANA-097 image can be found at the Sage Synapse data repository under [Synapse ID: syn26848598](https://www.synapse.org/#!Synapse:syn26848598).

Data files and descriptions:

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
└───<b>qc</b>
│   │   ROI_table.csv
│   │   polygon_dict.pkl
│   │   qcmask_cell.tif
│   │   qcmask_pixel.tif
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

* `csv/unmicst-WD-76845-097_cellRing.csv`: single-cell feature table containing cell IDs, (x, y) spatial coordinates, integrated fluorescence signal intensities, and various nuclear morphology attributes for 1,242,756 cells constituting the SARDANA-097 image.
* `markers/markers.csv`: immunomarker metadata mapping immunomarkers to image channel numbers and CyCIF cycle numbers.
* `mask/WD-76845-097.ome.tif`: cell segmentation mask for the SARDANA-097 image indexed 0 to 1,242,756 with 0 reserved for background pixels.
* `qc/ROI_table.csv`: ROI metadata for artifacts in the SARDANA-097 image.
* `qc/polygon_dict.pkl`: shape type (ellipse or polygon) and vertex coordinates defining ROIs in `qc/ROI_table.csv`.
* `qc/qcmask_cell.csv`: cell segmentation mask annotated by artifact classes: 0=background, 1=artifact-free, 2=fluorescence aberration, 3=slide debris, 4=coverslip air bubble, 5=uneven immunolabeling, 6=image blur.
* `qc/qcmask_pixel.csv`: equivalent to an ROI mask: 1=no ROI, 2=fluorescence aberration, 3=slide debris, 4=coverslip air bubble, 5=uneven immunolabeling, 6=image blur.
* `qc/truth.csv`: multiclass ground truth annotations for 1,242,756 cells comprising the SARDANA-097 image.
* `seg/WD-76845-097.ome.tif`: segmentation outlines defining cell boundaries in the SARDANA-097 image.
* `tif/WD-76845-097.ome.tif`: stitched and registered 40-channel OME-TIFF file constituting the SARDANA-097 image.

## Target Channels
While the SARDANA-097 image comprises a total of 40 channels, artifacts were curated from only 22 of them, as others either contained signals from secondary antibodies alone or were determined to be unsuitable for the purposes of this hackathon challenge. Please consider the following channels for model training:

```
'Hoechst0', 'anti_CD3', 'anti_CD45RO', 'Keratin_570', 'aSMA_660', 'CD4_488', 'CD45_PE', 'PD1_647', 'CD20_488', 'CD68_555', 'CD8a_660', 'CD163_488', 'FOXP3_570', 'PDL1_647', 'Ecad_488', 'Vimentin_555', 'CDX2_647', 'LaminABC_488',
'Desmin_555', 'CD31_647', 'PCNA_488', 'CollagenIV_647'
```

## Artifact Classes
Examples of artifact classes in the SARDANA-097 image:

![](images/artifacts.png)

## Classifier Output
Classifier output should consist of a CSV file named `scores.csv` containing probability scores for each of the 6 artifact classes for each cell in the dataset: 1=artifact-free, 2=fluorescence aberration, 3=slide debris, 4=coverslip air bubble, 5=uneven immunolabeling, 6=image blur and should be formatted as follows:

```
"CellID","1","2","3","4","5","6"
1,0.95,0.23,0.14,0.05,0.39,0.21
2,0.10,0.09,0.56,0.67,0.89,0.01
3,0.03,0.28,0.22,0.17,0.42,0.91
.
.
.
```

## Performance Evaluation
Classifier predictions will be evaluated against multiclass ground truth annotations (`qc/truth.csv`) using Receiver operating characteristic (ROC) curve analysis by passing `scores.csv` and `qc/truth.csv` as ordered arguments to `roc.py`:

```
$ python roc.py  scores.csv truth.csv
```

<img src="images/roc.png" alt="drawing" width="700"/>

Classifier predictions will also be scored against binary multiclass ground truth labels using measures of precision and recall. This is achieved by first saving artifact class calls to a file named `calls.csv`:

```
"CellID","class_label"
1,1
2,2
3,3
4,1
5,2
.
.
.
```

`calls.csv` and `qc/truth.csv` can then be passed as ordered arguments to `pr.py` for computing precision and recall on individual and combined artifact classes as follows:

<pre>
$ python pr.py calls.csv truth.csv

<b>Fluor:</b> precision=0.78, recall=0.67
<b>Debris:</b> precision=0.61, recall=0.45
<b>Bubble:</b> precision=0.73, recall=0.84
<b>Staining:</b> precision=0.90, recall=0.62
<b>Blur:</b> precision=0.57, recall=0.56
<b>Overall:</b> precision=0.87, recall=0.79
</pre>

## Considerations
1. Ground truth labels can themselves contain inaccuracies. How might classifiers be developed to guard against artifact misclassification, false positives (i.e. artifact-free cells inadvertently being classified as noisy), and false negatives (i.e. artifacts that have gone unannotated)?

2. Which model type achieves superior classifier performance, those trained on single-cell feature tables (i.e. `csv/unmicst-WD-76845-097_cellRing.csv`), or those trained on pixel-level imaging data (`tif/WD-76845-097.ome.tif`)? What about hybrid models trained on both data types?

## Suggested Computational Resources and Software Packages
* High-level programming language (Python 3 is recommended)
* Core data science software packages (e.g. `pandas`, `numpy`, and `scipy`)
* Libraries for reading, writing, analyzing, and visualizing multi-channel TIFF images (e.g. `tifffile`, `skimage`, `matplotlib`, `napari`)
* Machine learning and artificial intelligence libraries (e.g. `scikit-learn`, `tensorflow`, `keras`, `pytorch`)

If using Python 3, the aforementioned libraries can be installed in a new Python virtual environment dedicated to this project by running the following commands:

```
# on Mac

$ python3 -m venv ~/artifacts  # Creates a new Python virtual environment in the home directory
$ source ~/artifacts/bin/activate  # Steps into the newly created virtual environment
$ pip install -r requirements.txt  # Installs software packages using the "requirements.txt" file in this GitHub repo
```

## Team Check-In Times
Virtual check-ins will occur daily at **10am** & **3pm** ([US EST](https://dateful.com/time-zone-converter)) at the following Zoom link:
* https://us02web.zoom.us/j/84722597891?pwd=aVR5VkhBN1hsRHIrRFpTblhzMTI0Zz09.
* For questions outside of these times, please post to the #01-artifacts Slack channel.
