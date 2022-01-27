# Automated Detection of Microscopy Artifacts

## Description
Multiplex images of tissue contain information on the gene expression, morphology, and spatial distribution of individual cells comprising biologically specialized niches. However, accurate extraction of cell-level features from pixel-level data is hindered by the presence of microscopy artifacts. Manual curation of noisy cell segmentation instances scales poorly with increasing dataset size, and methods capable of automated artifact detection are needed to enhance workflow efficiency, minimize curator burden, and mitigate human bias. In this challenge, participants will draw on classical and/or machine learning approaches to develop probabilistic classifiers for detecting cell segmentation instances in multiplex images of tissue corrupted by microscopy artifacts.

![](images/schematic.png)

## Dataset
Test data for this challenge consist of a single 1.6cm<sup>2</sup> section of primary human colorectal adenocarcinoma probed for 21 different tumor, immune, and stromal markers over 8 rounds of multiplex immunofluorescence imaging by [CyCIF](https://www.cycif.org/). This dataset was collected as part of the Human Tumor Atlas Network (HTAN) and is referred to as the SARDANA-097 image.

Multiclass quality control (QC) annotations flagging microscopy artifacts in the SARDANA-097 image have been manually curated and are provided as a reference for model training along with other data files pertinent to this challenge  at the Sage Synapse data repository under [Synapse ID: syn26848598](https://www.synapse.org/#!Synapse:syn26848598). Files are organized as follows:

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
* `csv/unmicst-WD-76845-097_cellRing.csv`: single-cell feature table containing cell IDs, spatial coordinates (x, y), integrated fluorescence signal intensities, and nuclear morphology attributes for 1,242,756 cells constituting the SARDANA-097 image.
* `markers/markers.csv`: immunomarker metadata. Maps immunomarkers to image channel and CyCIF cycle numbers.
* `mask/WD-76845-097.ome.tif`: cell segmentation mask indexed 0 (background) to N (total number of segmented cells in the image).
* `qc/ROI_table.csv`: metadata for ROIs used to curate multiple classes of artifacts in the SARDANA-097 image.
* `qc/polygon_dict.pkl`: shape type (ellipse or polygon) and vertices defining each ROI. Order corresponds to that in `qc/ROI_table.csv`.
* `qc/qcmask_cell.csv`: cell segmentation mask annotated with multiclass QC labels: 0=background, 1=artifact-free, 2=fluorescence aberration, 3=slide debris, 4=coverslip air bubble, 5=uneven immunolabeling, 6=image blur.  
* `qc/qcmask_pixel.csv`: multiclass artifact ROI mask: 1=no ROI, 2=fluorescence aberration, 3=slide debris, 4=coverslip air bubble, 5=uneven immunolabeling, 6=image blur.
* `qc/truth.csv`: multiclass ground truth annotations for 1,242,756 cells comprising the SARDANA-097 image in long-table format.
* `seg/WD-76845-097.ome.tif`: cell segmentation outlines. Defines boundaries of segmented cells in `mask/WD-76845-097.ome.tif`.
* `tif/WD-76845-097.ome.tif`: stitched and registered 40-channel OME-TIFF file of CyCIF data for the SARDANA-097 image.

## Target Channels
The raw SARDANA-097 dataset comprises a total of 40 channels; however, only 21 were used in the curation of microscopy artifacts to this challenge, as several of its channels represent signals from secondary antibodies used to block non-specific antibody binding or those which were otherwise determined to be unsuitable for the purposes of this challenge. While all channels may be used in classifier development, please use the following channels:

```
'Hoechst0', 'anti_CD3', 'anti_CD45RO', 'Keratin_570', 'aSMA_660', 'CD4_488', 'CD45_PE', 'PD1_647', 'CD20_488', 'CD68_555', 'CD8a_660', 'CD163_488', 'FOXP3_570', 'PDL1_647', 'Ecad_488', 'Vimentin_555', 'CDX2_647', 'LaminABC_488',
'Desmin_555', 'CD31_647', 'PCNA_488', 'CollagenIV_647'
```

## Artifact Classes
Examples of different artifact classes found in the SARDANA-097 image:

![](images/artifacts.png)

## Classifier Output
The output of each classifier should consist of a CSV file consisting of cell IDs and probability scores for each of 6 classes (1=artifact-free, 2=fluorescence aberration, 3=slide debris, 4=coverslip air bubble, 5=uneven immunolabeling, 6=image blur):

```
CellID,1,2,3,4,5,6
1,0.95,0.23,0.14,0.05,0.39,0.21
2,0.10,0.09,0.56,0.67,0.89,0.01
3,0.03,0.28,0.22,0.17,0.42,0.91
.
.
.
```
* Cell IDs can be found in `csv/unmicst-WD-76845-097_cellRing.csv` and `mask/WD-76845-097.ome.tif`. A mapping of cell IDs to cell classes can be found in `qc/truth.csv`.

## Performance Evaluation
Classifier predictions will be scored against ground truth annotations `qc/truth_multiclass.csv` and `qc/truth_binary.csv` using a combination of multiclass Receiver operating characteristic (ROC) curve analysis and binary performance metrics of precision and recall using the following Python scripts: `score/roc.py` and `score/pr.py`.

To score classifier predictions by multiclass Receiver Operating Characteristic (ROC) curve analysis, pass multiclass predictions formatted as in the "Classifier Output" section above and `qc/truth_multiclass.csv` to `score/roc.py` as follows:

```
$ python roc.py  pred_multiclass.csv truth_multiclass.csv
```

![](images/roc.png)

To score binarized classifier predictions using metrics of precision and recall, pass binary predictions (0=clean, 1=artifact) and `qc/truth_binary.csv` to `score/pr.py` as follows:

```
$ python pr.py pred_binary.csv truth_binary.csv

precision=0.78, recall=0.67
```

## Considerations
1. Ground truth labels can themselves be inaccurate. How might classifiers be trained to be become robust to misclassified artifacts, false positives (artifact-free cells inadvertently classified as noisy), or false negatives (artifacts which have gone unannotated)?

2. Are pixel-level classifiers superior to those developed using derived single-cell data (i.e. feature tables)? What about models that integrate information at both the pixel and cell levels?

## Suggested Computational Resources and Software Packages
* A high-level programming language (Python 3 is recommended)
* Software packages including data analysis libraries such as `pandas`, `numpy`, and `scipy`; libraries for reading, writing, analyzing, and visualizing multi-channel TIFF files like `tifffile`, `skimage`, `matplotlib`, `napari`, `scikit-learn`; and various machine learning and artificial intelligence libraries such as `tensorflow`, `keras`, and `pytorch`. If using Python 3, the aforementioned libraries can all be installed at once in a clean Python virtual environment dedicated to this project by running the following commands:
```
$ python3 -m venv ~/artifacts  # Creates a new Python virtual environment
$ source ~/artifacts/bin/activate  # Step into the new virtual environment
$ pip install -r requirements.txt  # Install software packages from "requirements.txt"
```

## Team Check-in Times (all times US EST)
Virtual check-ins will occur daily at 10am & 3pm at the following Zoom link:
* https://us02web.zoom.us/j/84722597891?pwd=aVR5VkhBN1hsRHIrRFpTblhzMTI0Zz09.

For questions outside of dedicated check-in times, please post to the #01-artifacts Slack channel.
