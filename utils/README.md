# Utilities

This directory contains utility scripts for data processing and conversion.

## Scripts

### `convert_dat_to_csv.py`
**Purpose**: Convert raw radar binary data (.dat) to CSV format

**Usage**:
```bash
python utils/convert_dat_to_csv.py --input raw_data.dat --output processed_data.csv
```

**Description**: 
- Reads binary radar data files
- Converts to human-readable CSV format
- Outputs point cloud data with columns: FrameID, Timestamp, X, Y, Z, Doppler, SNR

---

### `final_identify.py`
**Purpose**: Final target identification and classification

**Usage**:
```bash
python utils/final_identify.py
```

**Description**:
- Advanced identification algorithms
- Target classification refinement
- Post-processing utilities

---

## Adding New Utilities

When adding new utility scripts to this directory:

1. Follow Python naming conventions (snake_case)
2. Include docstrings and comments
3. Add usage examples to this README
4. Keep utilities focused on a single task

---

## See Also

- [Main Application](../main.py) - Core application
- [Visualization](../visualization/) - Visualization scripts
- [Test Scripts](../Test/) - Testing utilities
