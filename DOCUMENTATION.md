# Complete Documentation

**Campus Safety Radar Project - Technical Documentation**

This document provides comprehensive technical information about the Campus Safety Radar Project.

> 📘 **For a quick overview**, see [README.md](README.md)  
> ⚡ **To get started quickly**, see [QUICKSTART.md](QUICKSTART.md)

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Algorithm Details](#algorithm-details)
- [Configuration](#configuration)
- [Data Formats](#data-formats)
- [API Reference](#api-reference)
- [Performance](#performance)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [Version History](#version-history)

---

## Project Overview

### Introduction

The Campus Safety Radar Project is an intelligent real-time monitoring system that uses millimeter-wave radar technology to detect and classify pedestrians and electric scooters. Unlike traditional camera-based surveillance systems, this solution is completely privacy-friendly, operating in all weather conditions.

### Key Features

| Feature | Description | Benefit |
|---------|-------------|---------|
| 🔒 **Privacy-Preserving** | Only captures distance and velocity | No visual data, no facial recognition |
| 🌦️ **Weather-Independent** | Works in all conditions | 24/7 reliable operation |
| 🎯 **Accurate Classification** | Distinguishes targets | 75-80% accuracy rate |
| 👥 **Multi-Target** | Tracks multiple objects | Handles crowded scenarios |
| ⚡ **Real-Time** | <100ms latency | Immediate detection |
| 📊 **Visual Feedback** | 3D visualization | Easy monitoring |
| 🔄 **Robust** | Handles occlusions | Continuous tracking |

### Technology Stack

- **Hardware**: TI AWR1843 77 GHz FMCW mmWave Radar
- **Language**: Python 3.11+
- **Core Libraries**: NumPy, SciPy, PyQtGraph, PyQt5
- **Optional**: CuPy (GPU acceleration), TensorFlow/PyTorch (ML models)

### Use Cases

1. **Campus Safety Monitoring**
   - Detect pedestrians and e-scooters in real-time
   - Identify potential safety hazards
   - Generate alerts for abnormal behavior

2. **Traffic Analysis**
   - Count pedestrian and e-scooter traffic
   - Analyze movement patterns
   - Optimize pathway design

3. **Research & Development**
   - Radar signal processing research
   - Machine learning for classification
   - Tracking algorithm development

---

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 10/11, macOS 10.15+, Ubuntu 20.04+ |
| **Python** | 3.11 or higher |
| **RAM** | 8GB |
| **Storage** | 2GB free space |
| **Display** | 1920x1080 |

### Recommended Requirements

| Component | Requirement |
|-----------|-------------|
| **CPU** | Multi-core (Intel i5/i7 or AMD equivalent) |
| **RAM** | 16GB or more |
| **GPU** | NVIDIA GPU with CUDA support |
| **Storage** | 10GB+ for data |

### Hardware

- **TI AWR1843 mmWave Radar** (required)
- **USB Cable** for radar connection
- **Mounting Equipment** (tripod or stable mount)

---

## Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/haowen-EE/Radar-project.git
cd Radar-project
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv .venv311
.venv311\Scripts\activate
```

**macOS/Linux:**
```bash
python3.11 -m venv .venv311
source .venv311/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Hardware Setup

1. **Connect Radar**: Connect AWR1843 to computer via USB
2. **Install Drivers**: Install TI mmWave Studio and drivers
3. **Configure Radar**: Load configuration file to radar
4. **Mount Radar**: Install at 45cm height (adjustable)

### Step 5: Verify Installation

```bash
python -c "import numpy, pyqtgraph; print('✓ Installation successful!')"
```

📖 **Detailed guide**: See [INSTALL.md](INSTALL.md)

---

## Usage

### Basic Usage

#### 1. Run Main Application

```bash
# Edit CSV_FILE path in main.py
python main.py
```

#### 2. Collect Real-Time Data

```bash
python read_data_awr1843.py
```

#### 3. Convert Data Format

```bash
python utils/convert_dat_to_csv.py --input data.dat --output data.csv
```

#### 4. Visualize Data

```bash
python visualization/clustering_3d_boxes.py
```

### Advanced Usage

#### Custom Configuration

Edit parameters in `main.py`:

```python
# Radar height
RADAR_HEIGHT = 0.45  # meters

# Clustering
GRID_CELL_M = 0.7
MIN_POINTS_IN_CLUSTER = 3

# Speed thresholds
WALK_SPEED_LO = 0.3
WALK_SPEED_HI = 2.5

# Tracking
MAX_MISS = 8
ROLL_WIN = 40
```

#### Batch Processing

```bash
for file in Data/*.csv; do
    python main.py --input "$file" --output "Results/$(basename $file)"
done
```

#### Integration Example

```python
from escooter_plugin import EscooterPlugin

plugin = EscooterPlugin()
results = plugin.process_frame(point_cloud, frame_id)

for escooter in results['escooters']:
    print(f"Position: {escooter['position']}, Speed: {escooter['speed']}")
```

📖 **Complete guide**: See [USAGE.md](USAGE.md)

---

## Project Structure

### Directory Layout

```
Radar-project/
├── main.py                      # Main application
├── escooter_plugin.py           # Detection plugin
├── read_data_awr1843.py         # Data collection
│
├── utils/                       # Utilities
│   ├── convert_dat_to_csv.py
│   ├── final_identify.py
│   └── README.md
│
├── visualization/               # Visualization
│   ├── clustering_3d.py
│   ├── clustering_3d_boxes.py
│   ├── visualize_csv_3d.py
│   └── README.md
│
├── experimental/                # Experimental code
│   ├── csv_boxes_v4.py
│   └── README.md
│
├── Test/                        # Tests
├── Data/                        # Data files
├── Analysis/                    # Technical docs
├── Proposal/                    # Proposals
└── docs/                        # Documentation
```

### Core Files

| File | Purpose | Usage Frequency |
|------|---------|-----------------|
| `main.py` | Main entry point | ⭐⭐⭐⭐⭐ |
| `escooter_plugin.py` | Detection algorithm | ⭐⭐⭐⭐⭐ |
| `read_data_awr1843.py` | Data collection | ⭐⭐⭐⭐ |

### Utility Scripts

Located in `utils/`:
- `convert_dat_to_csv.py` - Format conversion
- `final_identify.py` - Identification tools

### Visualization Scripts

Located in `visualization/`:
- `clustering_3d.py` - Basic 3D view
- `clustering_3d_boxes.py` - **Recommended** - Full featured
- `visualize_csv_3d.py` - CSV visualization
- `visualize_csv_3d_v3.py` - Enhanced version

📖 **Structure details**: See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

## Algorithm Details

### Signal Processing Pipeline

```
┌──────────────────┐
│  Raw RF Data     │
│  (AWR1843)       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Range FFT       │
│  - 2048 points   │
│  - Window: Hann  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Doppler FFT     │
│  - 256 chirps    │
│  - Zero padding  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  CFAR Detection  │
│  - 2D CA-CFAR    │
│  - Threshold: 15 │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Point Cloud     │
│  (X, Y, Z, V)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Clustering      │
│  - Grid DBSCAN   │
│  - Cell: 0.7m    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Tracking        │
│  - Kalman Filter │
│  - Data Assoc.   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Classification  │
│  - Speed         │
│  - Shape         │
│  - Micro-Doppler │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Output          │
│  - Visualization │
│  - Logging       │
└──────────────────┘
```

### Clustering Algorithm

**Grid-based DBSCAN**:
1. Divide space into grid cells (0.7m × 0.7m × 0.7m)
2. Group points within same cell
3. Merge adjacent cells with sufficient points
4. Apply minimum point threshold (3 points)

**Advantages**:
- O(n) complexity vs O(n²) for traditional DBSCAN
- Real-time performance
- Adjustable granularity

### Tracking Algorithm

**Kalman Filter + Data Association**:

1. **Prediction**: 
   - Predict next position using constant velocity model
   - Update uncertainty

2. **Association**:
   - Calculate distance between predictions and detections
   - Use GNN (Global Nearest Neighbor) for assignment
   - Gate distance: 2.4m (adjustable)

3. **Update**:
   - Update track with associated detection
   - Apply exponential smoothing (α=0.35)
   - Maintain trajectory history (40 frames)

4. **Track Management**:
   - Create new tracks for unassociated detections
   - Delete tracks after 8 missed frames
   - Merge duplicate tracks

### Classification Method

**Hybrid Approach**:

**Rule-based**:
```python
if speed < 0.3:
    class = "static_object"
elif 0.3 <= speed < 2.5 and height > 0.35:
    class = "pedestrian"
elif speed >= 2.5:
    class = "escooter"
else:
    class = "unknown"
```

**Feature-based** (optional):
- Speed statistics (mean, std, max)
- Point distribution (height, width, depth)
- Micro-Doppler signature
- Trajectory characteristics

📖 **Algorithm details**: See [Analysis/](Analysis/) directory

---

## Configuration

### Main Parameters

#### Radar Configuration

```python
RADAR_HEIGHT = 0.45              # m: Installation height
ROTATE_Y_PLUS_90 = False         # Coordinate rotation
```

#### Clustering Parameters

```python
GRID_CELL_M = 0.7                # m: Grid cell size
MIN_POINTS_IN_CLUSTER = 3        # Minimum points per cluster
ASSOC_GATE_BASE_M = 2.4          # m: Association threshold
```

#### Speed Thresholds

```python
# Pedestrians
WALK_SPEED_LO = 0.3              # m/s: Minimum
WALK_SPEED_HI = 2.5              # m/s: Maximum
MIN_DURATION_S = 0.5             # s: Minimum duration
Y_EXTENT_MIN = 0.35              # m: Minimum height

# E-scooters (in escooter_plugin.py)
ESCOOTER_SPEED_MIN = 2.0         # m/s
ESCOOTER_SPEED_MAX = 15.0        # m/s

# Static objects
OBJ_SPEED_MAX = 0.20             # m/s
OBJ_MIN_DURATION_S = 0.5         # s
OBJ_MAX_POINTS = 15              # points
```

#### Tracking Parameters

```python
MAX_MISS = 8                     # frames: Max missed before deletion
ROLL_WIN = 40                    # frames: Trajectory window
EWMA_ALPHA = 0.35                # Smoothing factor (0-1)
SPEED_WIN_PAIR = 10              # Frame pairs for speed estimation
```

#### Display Parameters

```python
POINT_SIZE = 3                   # pixels
PT_COLOR = (1, 0, 0, 1)          # Red (RGBA)
BOX_COLOR = (0, 1, 0, 1)         # Green for pedestrians
OBJ_BOX_COLOR = (0, 0.6, 1, 1)   # Blue for objects
BOX_WIDTH = 2                    # pixels
LABEL_SPEED = True               # Show speed labels
```

### Performance Tuning

#### For Speed

```python
ROLL_WIN = 20                    # Smaller window
GRID_CELL_M = 1.0                # Larger cells
MAX_MISS = 5                     # Drop tracks faster
```

#### For Accuracy

```python
ROLL_WIN = 60                    # More history
GRID_CELL_M = 0.5                # Finer granularity
ASSOC_GATE_BASE_M = 1.5          # Stricter matching
CONFIRM_SCORE = 5                # More confirmation
```

📖 **Full configuration**: See [Analysis/Configuration_Parameters_Detailed_Guide.md](Analysis/Configuration_Parameters_Detailed_Guide.md)

---

## Data Formats

### CSV Format

Point cloud data in CSV format:

```csv
FrameID,Timestamp,X,Y,Z,Doppler,SNR
1,2026-01-08T10:30:45.123456,2.5,0.3,0.1,1.2,25.3
1,2026-01-08T10:30:45.123456,2.6,0.4,0.0,1.3,24.8
2,2026-01-08T10:30:45.223456,2.7,0.3,0.1,1.4,26.1
...
```

**Columns**:
- `FrameID`: Frame number (sequential integer)
- `Timestamp`: ISO 8601 format timestamp
- `X`: Range (meters) - forward distance
- `Y`: Height (meters) - vertical distance (relative to radar)
- `Z`: Lateral (meters) - horizontal distance
- `Doppler`: Velocity (m/s) - positive approaching, negative receding
- `SNR`: Signal-to-Noise Ratio (dB)

### Binary Format

Raw radar data in binary format (vendor-specific).

Conversion:
```bash
python utils/convert_dat_to_csv.py --input data.dat --output data.csv
```

---

## API Reference

### Main Application

```python
# main.py - Entry point
# Configuration at top of file
CSV_FILE = r'/path/to/data.csv'
RADAR_HEIGHT = 0.45

# Run: python main.py
```

### E-scooter Plugin

```python
from escooter_plugin import EscooterPlugin

# Initialize
plugin = EscooterPlugin()

# Process frame
results = plugin.process_frame(
    point_cloud,      # np.ndarray: Nx3 or Nx4 points
    frame_id,         # int: Frame number
    timestamp=None    # optional: datetime
)

# Results dictionary:
# {
#     'escooters': [
#         {
#             'id': int,
#             'position': tuple (x, y, z),
#             'speed': float,
#             'confidence': float
#         },
#         ...
#     ],
#     'pedestrians': [...],
#     'objects': [...]
# }
```

### Data Collection

```python
# read_data_awr1843.py
# Configure COM port and baud rate
# Run: python read_data_awr1843.py
```

---

## Performance

### Benchmarks

System: Intel i7-10700K, 16GB RAM, NVIDIA RTX 3060

| Operation | Time | FPS |
|-----------|------|-----|
| Point cloud processing | 40ms | 25 |
| Clustering | 15ms | 67 |
| Tracking | 10ms | 100 |
| Classification | 5ms | 200 |
| Visualization | 30ms | 33 |
| **Total (CPU)** | **80ms** | **12** |
| **Total (GPU)** | **50ms** | **20** |

### Real-World Performance

Based on testing:

| Metric | Value |
|--------|-------|
| Detection range | 30m |
| Range accuracy | ±10cm |
| Speed accuracy | ±0.2 m/s |
| Classification accuracy | 75-80% |
| False positive rate | 5-8% |
| Max simultaneous targets | 15-20 |

---

## Troubleshooting

### Common Issues

#### 1. No radar data

**Problem**: No data received from radar

**Solutions**:
- Check USB connection
- Verify COM port settings
- Install TI drivers
- Test with TI mmWave Studio

#### 2. Qt platform plugin error

**Problem**: `qt.qpa.plugin: Could not find the Qt platform plugin`

**Solution**:
```bash
export QT_QPA_PLATFORM_PLUGIN_PATH=$VIRTUAL_ENV/lib/python3.11/site-packages/PyQt5/Qt5/plugins
```

#### 3. Low detection rate

**Problem**: Missing targets

**Solutions**:
- Lower `CONFIRM_SCORE`
- Adjust speed thresholds
- Check radar height
- Reduce `MIN_POINTS_IN_CLUSTER`

#### 4. High false positives

**Problem**: Too many detections

**Solutions**:
- Increase `CONFIRM_SCORE`
- Tighten speed thresholds
- Increase `MIN_DURATION_S`
- Enable clutter filtering

#### 5. Tracking instability

**Problem**: IDs changing frequently

**Solutions**:
- Increase `MAX_MISS`
- Increase `ROLL_WIN`
- Adjust `ASSOC_GATE_BASE_M`
- Check for environmental clutter

📖 **More troubleshooting**: See [FAQ.md](FAQ.md)

---

## Development

### Setting Up Development Environment

```bash
# Clone and setup
git clone https://github.com/haowen-EE/Radar-project.git
cd Radar-project
python -m venv .venv311
source .venv311/bin/activate

# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run tests
python -m pytest Test/

# Format code
black .

# Lint
flake8 .
```

### Code Style

Follow PEP 8 with:
- Line length: 100 characters
- Indentation: 4 spaces
- Use type hints
- Write docstrings (Google style)

### Testing

```bash
# Run all tests
python -m pytest Test/

# Run specific test
python Test/analyze_escooter_data.py

# With coverage
python -m pytest --cov=. Test/
```

### Adding Features

1. Create feature branch
2. Implement with tests
3. Update documentation
4. Submit pull request

📖 **Development guide**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Contributing

We welcome contributions!

### How to Contribute

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to branch (`git push origin feature/AmazingFeature`)
5. **Open** Pull Request

### Areas for Contribution

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🧪 Tests
- 🎨 Visualization enhancements
- 🚀 Performance optimizations

📖 **Contribution guide**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Version History

### V7.0 (Current) - October 2025
- Continuous tracking optimization
- Improved occlusion handling
- Enhanced e-scooter detection

### V6.0 - September 2025
- Inertia system for tracking
- Predictive tracking

### V5.0 - August 2025
- Enhanced pedestrian detection
- Improved classification

### V4.0 - July 2025
- Static object detection
- Bug fixes

### V3.0 - June 2025
- Initial public release
- Core functionality

📖 **Complete history**: See [CHANGELOG.md](CHANGELOG.md)

---

## Additional Resources

### Documentation Files

- [README.md](README.md) - Project overview
- [QUICKSTART.md](QUICKSTART.md) - 5-minute guide
- [INSTALL.md](INSTALL.md) - Installation
- [USAGE.md](USAGE.md) - Usage guide
- [FAQ.md](FAQ.md) - Common questions
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [ROADMAP.md](ROADMAP.md) - Future plans

### Technical Documentation

- [Analysis/](Analysis/) - Technical details
- [Proposal/](Proposal/) - Project proposal
- [FILE_NAMING_CHANGES.md](FILE_NAMING_CHANGES.md) - File naming history
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Structure documentation

### Community

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and discussions
- **Email**: your.email@example.com

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Citation

```bibtex
@misc{radar_project_2026,
  author = {Jiang, Haowen},
  title = {Campus Safety Radar Project},
  year = {2026},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/haowen-EE/Radar-project}}
}
```

---

## Contact

**Haowen Jiang**
- GitHub: [@haowen-EE](https://github.com/haowen-EE)
- Email: your.email@example.com

---

<p align="center">
  <b>Campus Safety Radar Project</b><br>
  <i>Complete Technical Documentation</i><br>
  Last Updated: January 8, 2026
</p>
