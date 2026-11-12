# Analysis and plotting

| Script | Figures |
|---|---|
| `plot_NH2.py` | Figures 4–6; vacuum-limit fits |
| `plot_solvent_shifts.py` | Figures 7–8 |
| `plot_BlatterO.py` | Figure 9 |
| `plot_window_integrals.py` | SI Figure S1; window integrals |

The scripts read CSV files from `../data/` using `read_data.py` and save PNG/SVG
figures in `figures/`. Dependencies
are listed in [requirements.txt](../requirements.txt).

## Optional experimental data for Blatter-O

`plot_BlatterO.py` runs without third-party experimental data and then plots the theoretical spectra only. To include the experimental overlay, obtain the source spectrum as described in `data/THIRD_PARTY_DATA.md` (see also `data/README.md`), digitize it into a CSV file with columns `wavelength_nm` and `log10_extinction`, and run:

```bash
python scripts/plot_BlatterO.py --experimental-data /path/to/BlatterO_experiment.csv
```
