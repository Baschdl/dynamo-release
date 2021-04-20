from dynamo import LoggerManager
import dynamo.tools
import dynamo as dyn
import pytest
import time
import numpy as np
import os
from test_utils import *

logger = LoggerManager.get_main_logger()


def test_simple_cluster_community_adata(adata):
    dyn.tl.louvain(adata)
    dyn.tl.leiden(adata)
    dyn.tl.infomap(adata)

    try:
        dyn.tl.louvain(adata, directed=True)
    except ValueError as e:
        print("################################################")
        print("PASSED: Value error captured as EXPECTED, Exception info:")
        print(e)
        print("################################################")

    dyn.tl.leiden(adata, directed=True)
    dyn.tl.infomap(adata, directed=True)
    assert np.all(adata.obs["louvain"] != -1)
    assert np.all(adata.obs["leiden"] != -1)
    assert np.all(adata.obs["infomap"] != -1)

    # dyn.pl.louvain(adata, basis="pca")
    # dyn.pl.leiden(adata, basis="pca")
    # dyn.pl.infomap(adata, basis="pca")


def test_simple_cluster_subset(adata):
    print(adata.obs["Cluster"])
    result = dyn.tl.infomap(
        adata,
        directed=True,
        copy=True,
        selected_cluster_subset=["Cluster", [0, 1, 2]],
    )
    print(result.obs["subset_infomap"])
    result = dyn.tl.infomap(
        adata, directed=True, copy=True, selected_cell_subset=np.arange(0, 10)
    )
    print(result.obs["subset_infomap"])


def test_simple_cluster_field(adata):
    dyn.tl.cluster_field(adata, method="louvain")
    dyn.tl.cluster_field(adata, method="leiden")


def test_simple_cluster_keys(adata):
    adata = dyn.tl.infomap(adata, directed=True, copy=True, layer="curvature")
    # adata = dyn.tl.infomap(
    #     adata,
    #     directed=True,
    #     copy=True,
    #     layer="acceleration"
    # )


def test_leiden_membership_input(adata):
    # to-do: fix the following test cases
    initial_membership = np.random.randint(
        low=0, high=min(100, len(adata)), size=len(adata), dtype=int
    )
    print(initial_membership)
    dyn.tl.leiden(adata, initial_membership=initial_membership)

    initial_membership = np.random.randint(
        low=0, high=100, size=len(adata), dtype=int
    )
    dyn.tl.leiden(adata, directed=True, initial_membership=initial_membership)


if __name__ == "__main__":
    # generate data if needed
    if not os.path.exists(test_zebrafish_data_path):
        print("generating test data...")
        gen_zebrafish_test_data()

    print("reading test data...")
    # To-do: use a fixture in future
    adata = dyn.read_h5ad(test_zebrafish_data_path)
    print("******acc layer: ", adata.layers["curvature"])
    print(adata)

    print("tests begin...")
    ######### testing begins here #########
    test_leiden_membership_input(adata)
    test_simple_cluster_community_adata(adata)
    test_simple_cluster_subset(adata)
    test_simple_cluster_keys(adata)
