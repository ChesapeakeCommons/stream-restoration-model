# Stream Restoration Model (Protocols 1 - 5)

This model estimates nutrient and sediment load reductions using data and algorithms from the [2019/2020 Stream Restoration Expert Panel Report](https://chesapeakestormwater.net/wp-content/uploads/dlm_uploads/2021/10/Unified-Stream-Restoration-Guide_FINAL_9.17.21.pdf).

There are currently five protocols that define the nutrient and sediment removal rates associated with stream restoration practices.

The source code contains separate modules for each of the five protocols. The following sections describe module inputs and outputs.

## Protocol 1: Prevented sediment

Protocol 1 provides credit for projects occurring in first through third order streams with perennial flow that stabilize banks and prevent sediment erosion in actively degrading channels.

See complete [2019 Protocol 1 Guidance](https://chesapeakestormwater.net/wp-content/uploads/dlm_uploads/2020/03/PROTOCOL-1-MEMO_WQGIT-Approved_revised-2.27.20_clean_w-appendices.pdf).

View [source code.](https://github.com/ChesapeakeCommons/stream-restoration-model/blob/master/app/modules/prevented_sediment/utilities.py)

### Inputs

| Name | Type | Description |
| :--- | :--- | :--- |
| `banks` | array | An array of `bank` objects (see below). |

**Bank values**

| Name | Type | Description |
| :--- | :--- | :--- |
| `bulk_density_of_soil` | float/integer | Bulk density of bank soil measured in pounds per cubic foot (lbs/ft<sup>3</sup>). **Default:** 0. |
| `bank_erosion_rate` | float/integer | Bank erosion rate measured in pounds per foot per year (lbs/ft/year). **Default:** 0. |
| `eroding_bank_length` | float/integer | Eroding bank length measured in feet (ft). **Default:** 0. |
| `eroding_bank_height` | float/integer | Eroding bank height measured in feet (ft). **Default:** 0. |
| `nitrogen_concentration` | float/integer | **Default:** 0. |
| `phosphorus_concentration` | float/integer | **Default:** 0. |

### Outputs

| Name | Type | Description |
| :--- | :--- | :--- |
| `tss_lbs_reduced` | float | Annual reduction in pounds of total suspended solids (`tss`). If multiple banks are provided, this number will be the aggregate of all `tss` reductions. |
| `tn_lbs_reduced` | float | Annual reduction in pounds of total nitrogen (`tn`). If multiple banks are provided, this number will be the aggregate of all `tn` reductions. |
| `tp_lbs_reduced` | float | Annual reduction in pounds of total phosphorus (`tp`). If multiple banks are provided, this number will be the aggregate of all `tp` reductions. |

### Formulas

See [design example](https://chesapeakestormwater.net/wp-content/uploads/dlm_uploads/2021/07/Design-Example-for-Protocol-1-recent.pdf).

**Abbreviations**

| Input | Abbreviation |
| :--- | :--- |
| `bulk_density_of_soil` | `bds` |
| `bank_erosion_rate` | `ber` |
| `eroding_bank_length` | `ebl` |
| `eroding_bank_height` | `ebh` |
| `nitrogen_concentration` | `ncon` |
| `phosphorus_concentration` | `pcon` |

```python
# Calculate sediment load.

tss_lbs_reduced = bds * ber * ebl * ebl

# Convert erosion rate to nutrient loading rates.
#
# The measured nutrient values of the sediments are:
#  - 1.05 pounds TP/ton sediment
#  - 2.28 pounds TN/ton sediment

tn_lbs_reduced = (tss_lbs_reduced/2000.0) * nitrogen_concentration

tp_lbs_reduced = (tss_lbs_reduced/2000.0) * phosphorus_concentration

# Estimate stream restoration efficiency.
# Assume the efficiency of the restoration practice to be 50%.

tss_lbs_reduced = tss_lbs_reduced * 0.50

tn_lbs_reduced = tn_lbs_reduced * 0.50

tp_lbs_reduced = tp_lbs_reduced * 0.50
```

## Protocol 2: Hyporheic exchange

Protocol 2 provides credit for projects that include design features to promote denitrification during base flow.

See complete [2020 Protocol 2 Guidance](https://chesapeakestormwater.net/wp-content/uploads/dlm_uploads/2020/10/FINAL-Approved-Group-4-Memo_10.27.20.pdf).

View [source code.](https://github.com/ChesapeakeCommons/stream-restoration-model/blob/master/app/modules/denitrification/utilities.py)

## Site-specific reduction factors

**Site specific discount factors for adjusting the denitrification rate (Parola et al, 2019)**

*Effective hyporheic zone N credit = (Base rate) (EHZ) (Bf) (Hf) (Af)*

| Baseflow reduction factor (B<sub>f</sub>) || Floodplain height factor (H<sub>f</sub>)<sup>1</sup> || Aquifer conductivity reduction factor (A<sub>f</sub>)<sup>2</sup> ||
| :--- | :--- | :--- | :--- | :--- | :--- 
| Perennial baseflow 	| 1.0 | 0 - 0.75 ft | 1.0 | cobbly gravel, gravel, gravelly sand, sand and peat | 1.0 |
| Baseflow in all but late summer/fall | 0.75 | 0.76 ft - 1.00 ft | 0.75 | gravelly silt, silty sand or loamy sand, sandy loam, and organic silt with no coarse material layer connected to the streambed | 0.60 |
| Baseflow in winter/spring | 0.50 | 1.01 ft - 1.25 ft | 0.50 | clayey gravel, sandy silt, sandy clay loam, loam, silt loam, and silt with no coarse material layer connected to the streambed | 0.40 |
| Baseflow only during wet seasons | 0.25 | 1.26 ft - 1.50 ft | 0.10 | sandy clay, clay loam, silty clay loam, organic clay with no coarse material layer connected to the streambed | 0.10 |
| Flow only during runoff events | 0.10 | > 1.50 ft | 0.00 | silty clay and clay with no coarse material layer connected to the streambed | 0.01 |

<strong><sup>1</sup></strong> The floodplain height factor is determined by the restored floodplain height (Hf) above the streambed riffle elevations or low flow water surface elevations. Additional streambed feature elevations, like those at a run in sand bed channels or streambeds comprised of silty clay, also may be used to determine the restored floodplain height. Low base-flow (lowest 10% of flows) could also be used as a suitable alternative.

<strong><sup>2</sup></strong> This refers to an aquifer capacity factor based on the dominant materials within the streambed and below the floodplain soil of the EHZ. Where coarse grain aquifer layers are not directly connected to the channel, the factor should be determined based on the soil texture at the elevation of the streambed using NRCS standard texture classifications (Schoeneberger, et al, 2012).

"Base rate" is the mean areal floodplain denitrification rate (lbs/sq foot/yr), as recommended by Group 4.


### Inputs

| Name | Type | Description |
| :--- | :--- | :--- |
| `floodplain_sq_ft` | float/integer | Area of the restored floodplain measured in square feet (ft<sup>2</sup>).  **Default:** 0. |
| `channel_sq_ft` | float/integer | Area of the restored channel measured in square feet (ft<sup>2</sup>). **Default:** 0. |
| `brf` | float/integer | Baseflow reduction factor. **Default:** 0. |
| `fhf` | float/integer | Floodplain height factor. **Default:** 0. |
| `acrf` | float/integer | Aquifer conductivity reduction factor. **Default:** 0. |

### Outputs

| Name | Type | Description |
| :--- | :--- | :--- |
| `tn_lbs_reduced` | float | Annual reduction in pounds of total nitrogen (`tn`). |

### Formulas

See [design example](https://chesapeakestormwater.net/wp-content/uploads/dlm_uploads/2021/07/P2-DESIGN-EXAMPLE.pdf).

```python
# Apply denitrification rate.

floodplain_tn = floodplain_sq_ft * 0.00269

channel_tn = channel_sq_ft * 0.00269

# Apply site-specific discount factors.

total_floodplain_tn = brf * fhf * acrf * floodplain_tn

total_channel_tn = brf * fhf * acrf * channel_tn

# Calculate total nitrate removed.

tn_lbs_reduced = total_floodplain_tn + total_channel_tn
```

## Protocol 3: Floodplain reconnection

Protocol 3 provides credit for projects that reconnect the stream channel with its natural floodplain, encouraging floodplain deposition, plant uptake and denitrification.

See complete [2020 Protocol 3 Guidance](https://chesapeakestormwater.net/wp-content/uploads/dlm_uploads/2020/10/FINAL-Approved-Group-4-Memo_10.27.20.pdf).

View source code [here](https://github.com/ChesapeakeCommons/stream-restoration-model/blob/master/app/modules/floodplain_reconnection_1/utilities.py), [here](https://github.com/ChesapeakeCommons/stream-restoration-model/blob/master/app/modules/floodplain_reconnection_2/utilities.py), and [here](https://github.com/ChesapeakeCommons/stream-restoration-model/blob/master/app/modules/floodplain_reconnection_3/utilities.py).

### Inputs

Protocol 3 requires multiple input steps to derive values for downstream calculations. The sequence is organized as follows.

**Step 1

| Name | Type | Description |
| :--- | :--- | :--- |
| `floodplain_sq_ft` | float/integer | The number of objects to be returned. Limit can range between 1 and 100. **Default:** 0. |
| `channel_sq_ft` | float/integer | The result set page to be returned. **Default:** 0. |
| `brf` | float/integer | Baseflow reduction factor. **Default:** 0. |
| `fhf` | float/integer | Floodplain height factor. **Default:** 0. |
| `acrf` | float/integer | Aquifer conductivity reduction factor. **Default:** 0. |

### Outputs

| Name | Type | Description |
| :--- | :--- | :--- |
| `tss_lbs_reduced` | float | Annual reduction in pounds of total suspended solids (`tss`). |
| `tn_lbs_reduced` | float | Annual reduction in pounds of total nitrogen (`tn`). |
| `tp_lbs_reduced` | float | Annual reduction in pounds of total phosphorus (`tp`). |

### Formulas

See [design example](https://chesapeakestormwater.net/wp-content/uploads/dlm_uploads/2021/07/P3-Design-Example.pdf).

```
floodplain_tn = floodplain_sq_ft * 0.00269

channel_tn = channel_sq_ft * 0.00269

total_floodplain_tn = brf * fhf * acrf * floodplain_tn

total_channel_tn = brf * fhf * acrf * channel_tn

tn_lbs_reduced = total_floodplain_tn + total_channel_tn
```


