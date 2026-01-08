# Campus Safety Radar Project

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

> An intelligent real-time monitoring system using TI AWR1843 77 GHz FMCW millimeter-wave radar for detecting and classifying pedestrians and electric scooters, enhancing campus safety and situational awareness.

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Algorithm Overview](#-algorithm-overview)
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [Documentation](#-documentation)
- [License](#-license)
- [Citation](#-citation)
- [Contact](#-contact)

---

## ✨ Features

- **🔒 Privacy-Friendly**: Only captures distance and velocity data - no images or personal identities
- **🌦️ All-Weather Operation**: Unaffected by lighting conditions, rain, or fog
- **🎯 High-Precision Classification**: Distinguishes between pedestrians and e-scooters with advanced algorithms
- **👥 Multi-Target Tracking**: Maintains individual target identities in high-density scenarios
- **⚡ Real-Time Processing**: GPU-accelerated signal processing with <100ms latency
- **📊 3D Visualization**: Real-time point cloud visualization with bounding boxes
- **🔄 Robust Tracking**: Handles occlusions and temporary target disappearances

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- TI AWR1843 mmWave Radar
- NVIDIA GPU (optional, for acceleration)
- Operating System: Windows, macOS, or Linux

### Installation

```bash
# Clone the repository
git clone https://github.com/haowen-EE/Radar-project.git
cd Radar-project

# Create virtual environment
python -m venv .venv311
source .venv311/bin/activate  # On Windows: .venv311\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Demo

```bash
# Edit CSV_FILE path in main.py to point to your data
# Then run:
python main.py
```

For detailed installation instructions, see [INSTALL.md](INSTALL.md).

---

## 🔧 Installation

### Quick Install

```bash
pip install -r requirements.txt
```

### Hardware Setup

1. Connect the TI AWR1843 radar to your computer via USB
2. Configure the radar parameters using TI's mmWave Studio
3. Ensure the radar is mounted at the correct height (default: 45cm)

See [INSTALL.md](INSTALL.md) for detailed hardware and software setup instructions.

---

## 📖 Usage

### Basic Usage

```python
# Edit the CSV_FILE path in main.py
CSV_FILE = r'/path/to/your/data.csv'

# Run the application
python main.py
```

### Data Collection

```bash
# Collect real-time data from radar
python read_data_awr1843.py
```

### Data Processing

```bash
# Convert raw radar data to CSV
python utils/convert_dat_to_csv.py

# Visualize 3D point cloud with clustering
python visualization/clustering_3d_boxes.py
```

See [USAGE.md](USAGE.md) for detailed usage instructions, configuration options, and advanced features.

---

## 📁 Project Structure

```
Radar-project/
├── main.py                      # Main application entry point
├── escooter_plugin.py           # E-scooter detection plugin
├── read_data_awr1843.py         # Real-time data collection from radar
│
├── utils/                       # Utility scripts
│   ├── convert_dat_to_csv.py   # Convert binary data to CSV
│   ├── final_identify.py       # Target identification tools
│   └── README.md               # Utils documentation
│
├── visualization/               # Visualization scripts
│   ├── clustering_3d.py        # Basic 3D clustering
│   ├── clustering_3d_boxes.py  # 3D clustering with bounding boxes
│   ├── visualize_csv_3d.py     # CSV 3D visualization
│   ├── visualize_csv_3d_v3.py  # CSV 3D visualization v3
│   └── README.md               # Visualization documentation
│
├── experimental/                # Experimental/legacy scripts
│   ├── csv_boxes_v4.py         # Legacy CSV boxes
│   ├── csv_boxes_with_bike.py  # Bike detection experiments
│   ├── csv_boxes_with_things.py # Object detection experiments
│   └── README.md               # Experimental scripts info
│
├── Test/                        # Test scripts
│   ├── analyze_escooter_data.py
│   ├── test_pedestrian_fix.py
│   └── ...
│
├── Data/                        # Sample datasets
│   ├── escooter_fast_with_RSC.csv
│   ├── man_walking_with_RSC.csv
│   └── README.md
│
├── Data_V2/                     # Version 2 datasets
├── Data_V3/                     # Version 3 datasets
│
├── Analysis/                    # Technical documentation
│   ├── E-scooter_Recognition_Detailed_Guide.md
│   ├── Configuration_Parameters_Detailed_Guide.md
│   └── ...
│
├── Proposal/                    # Project proposal documents
├── Thesis_Draft/                # Thesis drafts
│
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── INSTALL.md                   # Installation guide
├── USAGE.md                     # Usage guide
├── CONTRIBUTING.md              # Contribution guidelines
├── CHANGELOG.md                 # Version history
├── FAQ.md                       # Frequently asked questions
├── QUICKSTART.md                # Quick start guide
├── ROADMAP.md                   # Project roadmap
├── FILE_NAMING_CHANGES.md       # File renaming history
├── LICENSE                      # MIT License
└── .gitignore                   # Git ignore file
```

---

## 🧮 Algorithm Overview

### Signal Processing Pipeline

```
Raw Radar Data → Range FFT → Doppler FFT → CFAR Detection
                                                ↓
                                        Point Cloud
                                                ↓
                        Clustering (Grid-based DBSCAN)
                                                ↓
                                        Target Tracking
                                                ↓
                            Classification (Pedestrian/E-scooter)
                                                ↓
                                        Visualization
```

### Key Algorithms

- **CFAR Detection**: Constant False Alarm Rate for robust target detection
- **Grid-based Clustering**: Efficient spatial clustering for real-time performance
- **Multi-Target Tracking**: Kalman filter with data association (GNN/JPDA)
- **Classification**: Hybrid rule-based and machine learning approach

### Technical Specifications

| Specification | Value |
|--------------|-------|
| Detection Range | ~30 meters |
| Range Resolution | Centimeter-level |
| Angular Resolution | Degree-level |
| Processing Latency | <100ms per frame |
| Classification Accuracy | ≥70% (pedestrian vs. e-scooter) |
| Frame Rate | 10 Hz (configurable) |

For detailed algorithm descriptions, see the [Analysis/](Analysis/) directory.

---

## ⚙️ Configuration

### Key Parameters

```python
# Radar Installation Height
RADAR_HEIGHT = 0.45  # meters (45cm default)

# Clustering Parameters
GRID_CELL_M = 0.7              # Grid cell size for clustering (meters)
MIN_POINTS_IN_CLUSTER = 3      # Minimum points to form a cluster
ASSOC_GATE_BASE_M = 2.4        # Association gate distance (meters)

# Speed Thresholds
WALK_SPEED_LO = 0.3            # m/s: Minimum walking speed
WALK_SPEED_HI = 2.5            # m/s: Maximum pedestrian speed
SPEED_SANITY_MAX = 9.0         # m/s: Maximum reasonable speed

# Tracking Parameters
MAX_MISS = 8                   # Maximum frames to keep track after loss
ROLL_WIN = 40                  # Rolling window size for trajectory
EWMA_ALPHA = 0.35              # Exponential moving average alpha
```

See [Analysis/Configuration_Parameters_Detailed_Guide.md](Analysis/Configuration_Parameters_Detailed_Guide.md) for comprehensive configuration documentation.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Code style guidelines
- Development setup
- How to submit pull requests
- Reporting bugs and suggesting enhancements

### Quick Start for Contributors

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [INSTALL.md](INSTALL.md) | Detailed installation instructions |
| [USAGE.md](USAGE.md) | Comprehensive usage guide |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
| [Analysis/](Analysis/) | Technical specifications and research notes |
| [Proposal/](Proposal/) | Original project proposal |

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📖 Citation

If you use this project in your research, please cite:

```bibtex
@misc{radar_project_2026,
  author = {Jiang, Haowen},
  title = {Campus Safety Radar Project: Pedestrian and E-scooter Detection Using Millimeter-Wave Radar},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/haowen-EE/Radar-project}},
  note = {Accessed: 2026-01-08}
}
```

---

## 📧 Contact

**Author**: Haowen Jiang

- GitHub: [@haowen-EE](https://github.com/haowen-EE)
- Email: your.email@example.com
- Project Link: [https://github.com/haowen-EE/Radar-project](https://github.com/haowen-EE/Radar-project)

---

## 🙏 Acknowledgments

- Texas Instruments for the AWR1843 mmWave Radar platform
- PyQtGraph for visualization tools
- NumPy and SciPy communities

---

<p align="center">
  <b>Made with ❤️ for campus safety</b><br>
  <sub>Protecting privacy while enhancing security</sub>
</p>
