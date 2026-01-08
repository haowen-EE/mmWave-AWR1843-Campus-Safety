# Visualization Scripts

This directory contains scripts for visualizing radar data in various formats.

## Scripts

### `clustering_3d.py`
**Purpose**: Basic 3D point cloud clustering and visualization

**Usage**:
```bash
python visualization/clustering_3d.py
```

**Features**:
- Simple 3D point cloud display
- Basic clustering algorithm
- Real-time or offline visualization

---

### `clustering_3d_boxes.py`
**Purpose**: 3D clustering with bounding boxes

**Usage**:
```bash
python visualization/clustering_3d_boxes.py
```

**Features**:
- Point cloud clustering
- Bounding box generation and display
- Target tracking visualization
- Color-coded classifications

**Recommended**: This is the most feature-complete visualization script.

---

### `visualize_csv_3d.py`
**Purpose**: Visualize CSV data in 3D space

**Usage**:
```bash
python visualization/visualize_csv_3d.py
```

**Features**:
- Load CSV point cloud data
- Interactive 3D visualization
- Basic point rendering

---

### `visualize_csv_3d_v3.py`
**Purpose**: Enhanced CSV 3D visualization (version 3)

**Usage**:
```bash
python visualization/visualize_csv_3d_v3.py
```

**Features**:
- Improved rendering performance
- Additional visualization options
- Enhanced color schemes

---

## Visualization Controls

### Mouse Controls
- **Left Click + Drag**: Rotate view
- **Right Click + Drag**: Pan view
- **Scroll Wheel**: Zoom in/out

### Keyboard Shortcuts
- **Arrow Keys**: Navigate frames (if supported)
- **Space**: Pause/resume (if supported)
- **R**: Reset view
- **Q/Esc**: Quit

---

## Performance Tips

1. **For large datasets**: Use `clustering_3d_boxes.py` with adjusted parameters
2. **For real-time visualization**: Reduce point density or frame rate
3. **For publication-quality figures**: Adjust colors and labels in the scripts

---

## Customization

All visualization scripts can be customized by editing:
- Point size: `POINT_SIZE` parameter
- Colors: `PT_COLOR`, `BOX_COLOR` parameters
- View angles: Initial camera position
- Grid display: Grid on/off toggle

---

## Requirements

These scripts require:
- PyQtGraph
- PyQt5
- NumPy
- PyOpenGL

Install with:
```bash
pip install pyqtgraph PyQt5 PyOpenGL numpy
```

---

## See Also

- [Main Application](../main.py) - Includes integrated visualization
- [Test Scripts](../Test/) - Analysis and testing tools
