# Assignment of cell type/state identity {#celltype}

Once segmentation masks have been [quantified](#features), the resulting cell-by-marker matrices can be used to assign cell type/state identity to individual cells. Methods to do this generally fall into two categories. The first set of methods typically begin by clustering cells into distinct subpopulations. The clusters are then inspected for the expression of specific markers, and cell type/state labeles are assigned to all cells belonging to that cluster. More sophisticated methods allow for "soft" assignment of cells to multiple clusters at once, which produces probabilistic assignment of cell types/states.

The second class of methods forgo clustering entirely and work directly with the cell-by-marker matrix on a per-row (i.e., per-cell) basis. In the presence of labels, cell type assignment becomes a standard supervised learning task, where a model can be learned from labeled cells and applied to classify unlabeled ones. In the absence of labels, cell type assignment requires some prior knowledge about which markers map to which cell types/states. Given this mapping, assignment of cell identity can be done directly from marker expression.

**Expected input:**

  * An n-by-p matrix of `n` cells (rows) with quantified expression across `p` markers (columns)
  * [optional] An n-by-1 vector of labels obtained through, e.g., manual curation
  * [optional] A k-by-2 matrix that maps `k` channels to the corresponding cell type

**Expected output:**

  * An n-by-(p+1) matrix that encapsulates the original data with a new additional column denoting cell type assignments made by the method. In the case of probabilistic assigment, the method may output additional columns specifying per-class probabilities.

**Clustering-based methods**

**Traditional supervised learning**

**Method employing prior knowledge**

  * [naivestates](https://github.com/labsyspharm/naivestates) - Inference of cell states using a Naive Bayes framework. The method models each channel / marker as a mixture of two Gaussians. The resulting posterior probabilities of marker expression are combined with a pre-defined marker -> cell type/state mapping to arrive at probabilistic assignment of cells to classes.

  * [IMAAP](https://github.com/labsyspharm/IMAAP) - Cell type annotation and analysis of multiplexed imaging data. The method models each marker as a mixture of two Gaussians and assigns a probability to the regions of uncertainty (where the gaussians intersect) to account for common segmentation errors. The assigned probabilities are then used to determine which cell type / state to which each cell belongs using a combination of user-defined markers. The method also includes data analysis and visualization functions.
