# Numerical data

Numerical precision is retained for analysis; the manuscript rounds displayed values.

| Files | Contents |
|---|---|
| `NH2_vacuum_limit.csv` | Dielectric constants and maximum gas-to-PCM energy differences across the 20 roots for U and X (eV); corresponding root indices |
| `NH2_excitation_energies.csv` | Gas, frozen-field (`fr`) and LR excitation energies, oscillator strengths and spin diagnostics |
| `NH2_state_specific.csv` | Frozen-field, LR, cLR, ptSS and ptSS+CE energies and corrections |
| `NH2_transition_dipoles.csv` | Frozen-field transition-dipole magnitudes (atomic units) |
| `NH2_difference_dipoles.csv` | Unrelaxed, orbital-relaxation (`Z`) and total relaxed dipole differences, in debye, for frozen-field and LR response densities |
| `Benzyl_solvent_shifts.csv` | Gas/solution comparisons, geometry effects and total solvent shifts |
| `Benzyl_state_specific.csv` | Frozen-field, LR, cLR and ptSS+CE energies, LR oscillator strengths and U spin diagnostics |
| `BlatterO_LR_spectrum.csv` | The 40 formal LR roots for each method used in the absorption spectra and window integrals |
| `BlatterO_gas_LR_energies.csv` | Gas and formal LR energies at the DCM-optimized geometry |
| `BlatterO_solvent_shifts.csv` | Selected frozen-field/LR paired calculations and their gas-reference shifts |
| `BlatterO_state_specific.csv` | Selected cLR and ptSS+CE energies, with separate frozen-field and LR root indices |
| `*_excitation_channels.csv` | Printed orbital-channel amplitudes and percentage contributions; method/treatment or state columns identify the parent state |

Energy columns (`E`, `E_eV`, `E_*`, `fr`, `LR`, `cLR`, `CE`, `ptSS_CE`,
`gas_*`) and energy differences are in eV. `CE` denotes ptSS+CE.
`f` is dimensionless oscillator strength; `nm` is wavelength in nanometres.
`D` denotes the program's spin diagnostic: U-state spin contamination for U,
and the hypothetical U-description diagnostic for X, not residual X-state contamination.
`DU` is the U diagnostic where supplied. Root indices are local to each calculation.

`gas_Rsolv` and `gas_Rgas` denote gas-phase energies at the solution- and
gas-optimized geometries, respectively. `geometry_shift` = `gas_Rgas` − `gas_Rsolv`;
`reference_shift` = `fr` − `gas_Rsolv`; `LR_kernel_shift` = `LR` − `fr`.
`total_*` denotes the corresponding energy minus `gas_Rsolv`.
In the state-specific tables, `delta_*` denotes the energy correction relative
to the frozen-field reference, except where an explicit difference is named.

Dipole columns marked `_D` are in debye; `_au` indicates atomic units.
The trailing `x`, `y` and `z` identify Cartesian components.
`occ` and `virt` identify the orbitals in the printed excitation channel;
`percent` is the printed percentage and `amplitude` is its signed amplitude.
The `dominant` columns retain the leading-channel description from the calculation.
The complete manuscript and SI define the response methods and state assignments.

For the Blatter-O spectral comparison, the digitized log10 extinction values
are interpolated, exponentiated and normalized. U and X theoretical spectra
share a common maximum at each broadening width. Window integrals use
unnormalized, unit-area Gaussians weighted by oscillator strengths.
The benzyl 258 nm and Blatter-O 616 nm reference band positions are taken
from the experimental sources cited in the manuscript.

## Third-party experimental spectrum

The digitized experimental Blatter-O spectrum used for the experimental overlay in the manuscript is not redistributed in this repository. The source is the Supporting Information (Figure S8) associated with the publication at https://doi.org/10.1002/anie.201605612. To reproduce the experimental overlay, obtain the original article and its Supporting Information from the publisher's article page, digitize Figure S8, and save the resulting data as a CSV file with the columns `wavelength_nm` and `log10_extinction`. Pass that file to `scripts/plot_BlatterO.py` using the `--experimental-data` option. The remaining theoretical spectra and numerical results are provided in this repository.
