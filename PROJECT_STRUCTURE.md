# Project Structure Reorganization

This document describes the code organization changes made on January 8, 2026.

---

## Overview

The project has been reorganized to improve code organization and maintainability by grouping related files into dedicated directories.

---

## Directory Structure

### Core Files (Root Directory)

The following essential files remain in the root directory for easy access:

```
📄 main.py                  - Main application entry point
📄 escooter_plugin.py       - Core plugin for e-scooter detection  
📄 read_data_awr1843.py     - Real-time data collection from radar
```

**Rationale**: These are the most frequently used files and should be easily accessible.

---

### New Directories

#### 📁 `utils/` - Utility Scripts

**Purpose**: General-purpose utility scripts for data processing and conversion.

**Contents**:
- `convert_dat_to_csv.py` - Convert binary radar data to CSV format
- `final_identify.py` - Target identification utilities

**Usage**:
```bash
python utils/convert_dat_to_csv.py --input data.dat --output data.csv
```

---

#### 📁 `visualization/` - Visualization Scripts

**Purpose**: Scripts dedicated to visualizing radar data and detection results.

**Contents**:
- `clustering_3d.py` - Basic 3D point cloud clustering
- `clustering_3d_boxes.py` - 3D clustering with bounding boxes (recommended)
- `visualize_csv_3d.py` - CSV data 3D visualization
- `visualize_csv_3d_v3.py` - Enhanced CSV 3D visualization

**Usage**:
```bash
python visualization/clustering_3d_boxes.py
```

**Tip**: Use `clustering_3d_boxes.py` for the most feature-complete visualization.

---

#### 📁 `experimental/` - Experimental & Legacy Code

**Purpose**: Experimental features and legacy code not part of the main workflow.

**Contents**:
- `csv_boxes_v4.py` - Legacy CSV boxes implementation
- `csv_boxes_with_bike.py` - Experimental bicycle detection
- `csv_boxes_with_things.py` - Experimental object detection

**⚠️ Warning**: These scripts may be outdated or incompatible with current data formats.

**Usage**: Reference only. Check compatibility before use.

---

## Migration Guide

### Command Updates

If you were using old commands, update them as follows:

| Old Command | New Command |
|-------------|-------------|
| `python convert_dat_to_csv.py` | `python utils/convert_dat_to_csv.py` |
| `python clustering_3d.py` | `python visualization/clustering_3d.py` |
| `python clustering_3d_boxes.py` | `python visualization/clustering_3d_boxes.py` |
| `python visualize_csv_3d.py` | `python visualization/visualize_csv_3d.py` |

### Import Statement Updates

If you're importing from these modules:

**Old**:
```python
from clustering_3d import some_function
```

**New**:
```python
from visualization.clustering_3d import some_function
```

---

## Benefits

### 1. **Improved Organization**
- Related files are grouped together
- Easier to navigate for new contributors
- Clear separation of concerns

### 2. **Better Discoverability**
- Each directory has a README explaining its contents
- Clear categorization of scripts by purpose
- Reduced root directory clutter

### 3. **Maintainability**
- Experimental code clearly separated from production code
- Easier to identify which files are actively maintained
- Simpler to archive or remove obsolete code

### 4. **Scalability**
- Room for future additions without cluttering root
- Easy to add new categories as needed
- Better preparation for packaging/distribution

---

## Directory Guidelines

### When to Add Files to Each Directory

#### `utils/`
- ✅ Data conversion tools
- ✅ General-purpose utilities
- ✅ Helper functions used by multiple scripts
- ❌ Application-specific logic (use root or dedicated directory)

#### `visualization/`
- ✅ Plotting and display scripts
- ✅ 3D visualization tools
- ✅ Data presentation utilities
- ❌ Data processing (use `utils/`)
- ❌ Core algorithms (use root or dedicated directory)

#### `experimental/`
- ✅ Proof-of-concept code
- ✅ Legacy implementations
- ✅ Features under development
- ✅ Alternative approaches for comparison
- ❌ Production-ready code (move to appropriate directory)

---

## Documentation Updates

The following documentation files have been updated to reflect the new structure:

- ✅ `README.md` - Updated project structure section
- ✅ `USAGE.md` - Updated command examples
- ✅ `QUICKSTART.md` - Updated quick start commands
- ✅ `utils/README.md` - Created utilities documentation
- ✅ `visualization/README.md` - Created visualization documentation
- ✅ `experimental/README.md` - Created experimental scripts documentation

---

## Backward Compatibility

### No Breaking Changes

The reorganization does not break existing functionality:
- All scripts work the same way
- Just run from new locations
- Main application (`main.py`) unchanged

### Updating Your Workflow

If you have:
- **Shell scripts**: Update file paths
- **Python imports**: Update import statements
- **Documentation**: Update file references
- **Bookmarks**: Update directory bookmarks

---

## Future Plans

### Potential Additional Directories

As the project grows, consider adding:

```
algorithms/     - Core detection and tracking algorithms
configs/        - Configuration files
models/         - Machine learning models
notebooks/      - Jupyter notebooks for analysis
scripts/        - Automation scripts
tools/          - Development tools
```

---

## Quick Reference

### File Location Lookup

| File | Old Location | New Location |
|------|--------------|--------------|
| `convert_dat_to_csv.py` | Root | `utils/` |
| `final_identify.py` | Root | `utils/` |
| `clustering_3d.py` | Root | `visualization/` |
| `clustering_3d_boxes.py` | Root | `visualization/` |
| `visualize_csv_3d.py` | Root | `visualization/` |
| `visualize_csv_3d_v3.py` | Root | `visualization/` |
| `csv_boxes_v4.py` | Root | `experimental/` |
| `csv_boxes_with_bike.py` | Root | `experimental/` |
| `csv_boxes_with_things.py` | Root | `experimental/` |
| `main.py` | Root | Root (unchanged) |
| `escooter_plugin.py` | Root | Root (unchanged) |
| `read_data_awr1843.py` | Root | Root (unchanged) |

---

## Questions?

If you have questions about the new structure:

1. Check the README in each directory
2. See updated documentation ([README.md](README.md), [USAGE.md](USAGE.md))
3. Open an issue on GitHub
4. Contact the maintainers

---

**Last Updated**: January 8, 2026  
**Related**: See also [FILE_NAMING_CHANGES.md](FILE_NAMING_CHANGES.md) for recent file renaming
