
# Historical plotting notebooks

This directory preserves Jupyter notebooks used during the analysis and figure preparation for:

E. Acuna-Yeomans et al. (2023), "Evaluation of ZIF-8 flexible force fields for structural and mechanical properties."

[Publication DOI](https://doi.org/10.1016/j.micromeso.2022.112406)

## Purpose

These notebooks document the original research and plotting workflow.

They have been copied from the historical research archive without changing their contents, including code cells, metadata, and saved outputs.

They are preserved as historical records rather than maintained or validated software.

## Notebook inventory

| Notebook | Main purpose | Related figure |
|---|---|---|
| `PlottingData.ipynb` | Elastic constants and deformation-parameter analysis | Figure 7 (partial match) |
| `ecs/ecs_raspa.ipynb` | Elastic constants obtained from RASPA calculations | Figure 4 (partial match) |
| `pstability/Pstab_definitive.ipynb` | Pressure-dependent structural properties | Figure 3 |
| `tstability/tstab.ipynb` | Temperature-dependent structural properties | Supporting analysis |
| `tstability/tstab-16-june.ipynb` | Temperature-dependent structural properties and experimental comparisons | Figure 2 (partial match) |

These associations were established by examining plotting commands, data references, and saved figures. They do not establish that the current notebook contents exactly reproduce the published figures.

## Historical limitations

The notebooks contain absolute Windows paths pointing to locations in the original research archive.

Some cells were modified or reused during the research, so the notebooks may contain intermediate plotting code rather than the final version used for publication.

Saved outputs and execution counts have been preserved.

Some referenced input files are not included in this directory.

A historical temperature-analysis notebook also contains an explicitly provisional data value, which requires verification before reuse.

The notebooks have not been rerun as part of this repository.

## Reconstructed figures

Newer plotting scripts are maintained separately in:

[`../reconstructed/`](../reconstructed/)

These scripts use relative paths and selected archived datasets, and include automated tests.

The reconstructed implementations should not be confused with the original plotting code.

## Provenance

Source: original PhD research archive, `Documents/Repos/`.

The historical notebooks were copied without modifying their contents. The source archive is retained separately.

The scientific results should be attributed to the associated publication and its cited sources.
