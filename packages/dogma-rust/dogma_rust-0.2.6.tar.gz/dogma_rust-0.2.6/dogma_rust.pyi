import numpy as np
from numpy.typing import NDArray

def parse_fasta(path: str, mapping: NDArray[np.uint8], is_rna: bool) -> tuple[NDArray[np.uint8], NDArray[np.int64], NDArray[np.int64]]:
    ...

def concatenate_numpy(arrays: list[NDArray]) -> tuple[NDArray[np.uint8], NDArray[np.int64]]:
    ...

def concatenate_awkward(awkwards: list[tuple[NDArray, NDArray[np.int64]]]):
    ...
    
def awkward_from_list_of_numpy(arrays: list[NDArray]) -> tuple[NDArray[np.uint8], NDArray[np.int64]]:
    ...
