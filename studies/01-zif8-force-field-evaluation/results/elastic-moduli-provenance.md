# Provenance of the recovered RASPA elastic moduli

This note documents the relationship between the elastic moduli
recovered from historical RASPA calculations and those reported in
Table 1 of:

E. Acuna-Yeomans, J. J. Gutierrez-Sevillano, S. Calero, and
D. Dubbeldam, "Evaluation of ZIF-8 flexible force fields for
structural and mechanical properties," *Microporous and Mesoporous
Materials* **348** (2023), 112406.

[Publication DOI](https://doi.org/10.1016/j.micromeso.2022.112406)

The same published values appear in Table 3.1 of Chapter 3 of my
PhD thesis, *Advanced Computational Methods for Stability Assessment
of Metal-Organic Frameworks* (2025).

## Recovered results

The file `raspa_elastic_summary.csv` preserves Hill bulk and shear
moduli recovered from archived RASPA calculations.

The recovered values are compared below with those reported in
Table 1 of the publication.

All values are in GPa.

| Force field | Archived bulk modulus K | Published K | Archived shear modulus G | Published G |
|---|---:|---:|---:|---:|
| Zheng (FF1) | 8.355778 | 8.36 | 2.608902 | 2.61 |
| Hu (FF2) | 7.383523 | 7.27 | 0.475649 | 0.66 |
| Zhang (FF3) | 8.360771 | 8.42 | 0.794013 | 0.83 |
| Wu (FF4) | 8.408425 | 8.36 | 0.817191 | 0.79 |
| Weng–Schmidt (FF5) | 5.211075 | 5.21 | 0.945383 | 0.95 |

The Zheng and Weng–Schmidt results agree with the publication
within the reported precision.

The Hu, Zhang, and Wu results differ from the corresponding
published entries.

## Investigation of the differences

For Hu, Zhang, and Wu, I compared the recovered values against
the original RASPA output files in the historical
`ZIF-8/22March/0Pa_RASPA_minimizations` archive.

The results were read directly from the RASPA output, including
the full elastic stiffness matrices and the reported Hill moduli.

Calculations at 0 Pa and 1 atm produced nearly identical values.
The pressure difference therefore does not explain the discrepancies.

Additional zero-pressure calculations in
`ZIF-8/22March/RASPA_wLAMMPS_output` gave consistent results.

### Zhang and Wu

The archived results suggest that the FF3 and FF4 entries may have
been interchanged while preparing the published table.

The recovered Zhang values are close to those reported under FF4,
while the recovered Wu values are close to those reported under FF3.

This pattern is visible in both the elastic constants and the
derived Hill moduli.

However, the values do not all agree exactly at the reported
precision. A table-row interchange is therefore a plausible
explanation, not a confirmed correction.

### Hu

The archived Hu results do not reproduce the published values.

The historical RASPA output gives approximately:

- K = 7.3835 GPa
- G = 0.4756 GPa

Table 1 reports:

- K = 7.27 GPa
- G = 0.66 GPa

The recovered Figure 4 elastic constants are closer to the archived
RASPA calculation than to the values in Table 1.

I also examined alternative Hu minimizations before and after MD.
The available zero-pressure calculations gave consistent results.

The original calculation responsible for the published Table 1
entry has not been identified.

## Scope and limitations

The archived CSV has been retained unchanged. It documents
recovered historical results rather than a corrected version
of the publication.

The analysis script `analysis/check_raspa_elastic.py` calculates
Voigt bulk and shear moduli from a RASPA stiffness matrix. The
CSV contains Hill moduli reported by RASPA, which combine the
Voigt and Reuss estimates. The two should not be confused.

The temperature labels preserved in the CSV are historical
simulation metadata. They should not be interpreted as the
temperature at which the reported 0 K elastic constants were
evaluated.

The available evidence does not establish whether the published
discrepancies arose from manuscript preparation, selection of
different simulation results, or other changes in the historical
calculation workflow.

The original RASPA outputs remain in private research backups.
They have not been added to this public repository.
