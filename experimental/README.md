# Experimental Scripts

This directory contains experimental and legacy scripts that are not part of the main application workflow.

⚠️ **Warning**: These scripts may be outdated or incompatible with current data formats.

---

## Scripts

### `csv_boxes_v4.py`
**Purpose**: CSV processing with boxes (version 4)

**Status**: Legacy/Experimental

**Description**:
- Older version of box detection
- May have different parameter settings
- Kept for reference or specific use cases

---

### `csv_boxes_with_bike.py`
**Purpose**: CSV boxes with bicycle detection

**Status**: Experimental

**Description**:
- Experimental bicycle detection algorithm
- Not integrated into main application
- May require specific data format

**Note**: Current main application focuses on pedestrian and e-scooter detection.

---

### `csv_boxes_with_things.py`
**Purpose**: CSV boxes with general object detection

**Status**: Experimental

**Description**:
- Generic object detection experiments
- Broader classification beyond pedestrians/e-scooters
- Research/development code

---

## Usage Notes

### Before Using These Scripts:

1. **Check compatibility**: These scripts may use different data formats
2. **Review parameters**: Parameter names and values may differ from main application
3. **Test with sample data**: Verify output before using with important datasets
4. **Consider alternatives**: Check if main application has needed functionality

### Updating These Scripts:

If you want to use features from these scripts:
- Consider porting the functionality to the main application
- Update to current naming conventions and standards
- Add proper documentation and tests

---

## Migration to Main Application

If you find useful features here that should be in the main application:

1. Extract the relevant algorithm/feature
2. Refactor to match current code style
3. Add tests
4. Integrate into main application or appropriate module
5. Update documentation

---

## Why Keep These Scripts?

- **Historical reference**: Understanding evolution of algorithms
- **Feature mining**: May contain useful experimental features
- **Comparison**: Benchmark against older approaches
- **Recovery**: Restore functionality if needed

---

## Maintenance Policy

- These scripts are **not actively maintained**
- Bug fixes are low priority
- May be removed in future versions if unused
- Contributions to modernize are welcome

---

## See Also

- [Main Application](../main.py) - Current production code
- [Test Scripts](../Test/) - Active testing and analysis
- [CHANGELOG.md](../CHANGELOG.md) - Version history and changes
