# File Naming Changes

This document records the file renaming performed to comply with Python naming conventions (PEP 8).

## Date: January 8, 2026

---

## Python Naming Convention

**Standard**: Use lowercase with underscores (snake_case) for module names.

**Avoid**: 
- Starting with numbers
- Capital letters (unless for constants)
- Mixed case (camelCase)
- Special prefixes like "AAA_"

---

## Files Renamed

### Main Application Files

| Old Name | New Name | Purpose |
|----------|----------|---------|
| `AAA_V3.py` | `main.py` | Main application entry point |
| `readData_AWR1843.py` | `read_data_awr1843.py` | Real-time data collection from AWR1843 radar |
| `dat_to_csv_manual.py` | `convert_dat_to_csv.py` | Convert binary radar data to CSV format |

### Visualization Files

| Old Name | New Name | Purpose |
|----------|----------|---------|
| `3D_clustering.py` | `clustering_3d.py` | Basic 3D point cloud clustering |
| `3D_clustering_with_boxes.py` | `clustering_3d_boxes.py` | 3D clustering with bounding boxes |
| `csv_to_3d.py` | `visualize_csv_3d.py` | Visualize CSV data in 3D |
| `csv_to_3d3.py` | `visualize_csv_3d_v3.py` | Visualize CSV data in 3D (version 3) |

### Processing Scripts

| Old Name | New Name | Purpose |
|----------|----------|---------|
| `1_Final_Identify_Code.py` | `final_identify.py` | Final identification code |
| `csv_boxs_4.py` | `csv_boxes_v4.py` | CSV boxes processing (version 4) |
| `csv_boxs_withbike.py` | `csv_boxes_with_bike.py` | CSV boxes with bike detection |
| `csv_boxs_withthings.py` | `csv_boxes_with_things.py` | CSV boxes with object detection |

### Files Unchanged (Already Compliant)

| File Name | Purpose |
|-----------|---------|
| `escooter_plugin.py` | E-scooter detection plugin |

---

## Updated Documentation

The following documentation files have been updated to reflect the new file names:

- ✅ `README.md`
- ✅ `QUICKSTART.md`
- ✅ `INSTALL.md`
- ✅ `USAGE.md`
- ✅ `FAQ.md`
- ✅ `CHANGELOG.md`
- ✅ `Data/README.md`
- ✅ `DOCUMENTATION_SUMMARY.md`

---

## Migration Guide

If you have existing scripts or configurations that reference the old file names, update them as follows:

### Example: Update Import Statements

**Old:**
```python
from AAA_V3 import some_function
```

**New:**
```python
from main import some_function
```

### Example: Update Command Line Usage

**Old:**
```bash
python AAA_V3.py
python readData_AWR1843.py
python 3D_clustering.py
```

**New:**
```bash
python main.py
python read_data_awr1843.py
python clustering_3d.py
```

### Example: Update Configuration Files

**Old:**
```yaml
script: AAA_V3.py
data_collector: readData_AWR1843.py
```

**New:**
```yaml
script: main.py
data_collector: read_data_awr1843.py
```

---

## Why These Changes?

### 1. **PEP 8 Compliance**
Python's official style guide (PEP 8) recommends:
- Module names should be short, lowercase, with underscores
- Avoid starting with numbers
- Avoid special prefixes

### 2. **Improved Readability**
- `main.py` is clearer than `AAA_V3.py`
- `read_data_awr1843.py` is more descriptive than `readData_AWR1843.py`
- `clustering_3d.py` is clearer than `3D_clustering.py`

### 3. **Better Tool Compatibility**
- Some tools sort files incorrectly with numbers/capital letters
- Better tab completion in terminals
- Improved IDE support

### 4. **Professional Standards**
- Follows industry best practices
- Makes the project more accessible to new contributors
- Aligns with other open-source Python projects

---

## Quick Reference

### Main Commands Updated

| Task | Old Command | New Command |
|------|-------------|-------------|
| Run main application | `python AAA_V3.py` | `python main.py` |
| Collect data | `python readData_AWR1843.py` | `python read_data_awr1843.py` |
| Convert data | `python dat_to_csv_manual.py` | `python convert_dat_to_csv.py` |
| Visualize 3D | `python 3D_clustering.py` | `python clustering_3d.py` |
| Visualize with boxes | `python 3D_clustering_with_boxes.py` | `python clustering_3d_boxes.py` |

---

## Git History Note

If you're tracking changes in Git, the rename history is preserved. Use:

```bash
# View file history across renames
git log --follow main.py

# View what happened to old file
git log --all --full-history -- AAA_V3.py
```

---

## Questions?

If you encounter any issues with the renamed files:

1. Check this document for the correct mapping
2. Search and replace old names in your local scripts
3. Report any documentation inconsistencies as GitHub issues

---

**Last Updated**: January 8, 2026
