# Calculation inputs

BDF inputs for NH2, benzyl and Blatter-O. The calculation logs identify the build
by commit `84957bc31d33a27ee8021cb99e3ac3b2e1e953ca` (3 April 2025).
The required X-TDDFT/PCM functionality is available in this build and subsequent
commercial releases. BDF is commercially distributed by HZW; licensing information
and applications for a free trial are available on the
[BDF website](https://www.hzw.ai/bdf/index).

## Coordinates

Coordinates are in angstrom. Optimization inputs contain starting geometries;
excitation inputs contain the geometries used for the reported energies.

| System | Input (`<system>/`) | Coordinates (`../coordinates/`) |
|---|---|---|
| NH2 | `NH2_00_gas_U_X.inp` | `NH2_01.xyz` |
| NH2 | `NH2_01_eps1p1_U_X.inp` | `NH2_01.xyz` |
| NH2 | `NH2_02_eps1p01_U_X.inp` | `NH2_01.xyz` |
| NH2 | `NH2_03_eps1p001_U_X.inp` | `NH2_01.xyz` |
| NH2 | `NH2_04_eps1p0001_U_X.inp` | `NH2_01.xyz` |
| NH2 | `NH2_05_eps1p000001_U_X.inp` | `NH2_01.xyz` |
| NH2 | `NH2_eps20_opt2_U_cLR.inp` | `NH2_01.xyz` |
| NH2 | `NH2_U_ptSS_CE.inp` | `NH2_01.xyz` |
| NH2 | `NH2_eps20_opt2_X_cLR.inp` | `NH2_01.xyz` |
| NH2 | `NH2_X_ptSS_CE.inp` | `NH2_01.xyz` |
| Benzyl | `02_Benzyl_U_B3LYP_TZVP_TD_CHX_CE.inp` | `Benzyl_01.xyz` |
| Benzyl | `02_Benzyl_U_B3LYP_TZVP_TD_CHX_cLR.inp` | `Benzyl_01.xyz` |
| Benzyl | `02_Benzyl_U_B3LYP_TZVP_TD_CHX_r30.inp` | `Benzyl_01.xyz` |
| Benzyl | `02_Benzyl_X_B3LYP_TZVP_TD_CHX_CE.inp` | `Benzyl_01.xyz` |
| Benzyl | `02_Benzyl_X_B3LYP_TZVP_TD_CHX_cLR.inp` | `Benzyl_01.xyz` |
| Benzyl | `02_Benzyl_X_B3LYP_TZVP_TD_CHX_r30.inp` | `Benzyl_01.xyz` |
| Benzyl | `02_Benzyl_RCHX_B3LYP_TZVP_gas_UX_r30.inp` | `Benzyl_01.xyz` |
| BlatterO | `03_BlatterO_RDCM_B3LYP_TZVP_gas_UX_r40.inp` | `BlatterO_01.xyz` |
| BlatterO | `04_BlatterO_Rgas_B3LYP_TZVP_gas_U_r40.inp` | `BlatterO_02.xyz` |
| Benzyl | `05_Benzyl_Rgas_B3LYP_TZVP_gas_UX_r30.inp` | `Benzyl_02.xyz` |
| Benzyl | `01_Benzyl_UKS_B3LYP_D3BJ_SVP_opt_gas.inp` | `Benzyl_01.xyz` |
| BlatterO | `BlatterO_U_B3LYP_TZVP_TD_DCM_r40.inp` | `BlatterO_01.xyz` |
| BlatterO | `BlatterO_X_B3LYP_TZVP_TD_DCM_r40.inp` | `BlatterO_01.xyz` |
| BlatterO | `blatter_o_dcm_ss.inp` | `BlatterO_01.xyz` |
| BlatterO | `blatter_o_dcm_ce.inp` | `BlatterO_01.xyz` |
| BlatterO | `blatter_o_gas_x.inp` | `BlatterO_02.xyz` |
| BlatterO | `02_Blatter_O_UKS_B3LYP_D3BJ_SVP_opt_DCM.inp` | `BlatterO_03.xyz` |
| BlatterO | `02_Blatter_O_UKS_B3LYP_D3BJ_SVP_opt_gas.inp` | `BlatterO_03.xyz` |
