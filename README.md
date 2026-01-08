# Campus Safety Radar Project

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

> An intelligent real-time monitoring system using TI AWR1843 77 GHz FMCW millimeter-wave radar for detecting and classifying pedestrians and electric scooters on campus.

<p align="center">
  <img src="docs/images/radar_detection_demo.gif" alt="Radar Detection Demo" width="600"/>
  <br>
  <i>Real-time pedestrian and e-scooter detection with 3D visualization</i>
</p>

---

## 🎯 Overview

This project develops a **privacy-friendly, all-weather monitoring system** for campus safety using millimeter-wave radar technology. Unlike traditional camera-based systems, it only captures distance and velocity data, ensuring complete privacy while maintaining high detection accuracy.

### Key Capabilities

- **Privacy-Preserving**: No images, no facial recognition, no personal data
- **Weather-Independent**: Works in darkness, rain, fog, and bright sunlight  
- **Real-Time Detection**: <100ms latency with GPU acceleration
- **Multi-Target Tracking**: Tracks multiple pedestrians and e-scooters simultaneously
- **High Accuracy**: 75-80% classification accuracy, 30m detection range

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔒 **Privacy-Friendly** | Only distance and velocity - no visual data |
| 🌦️ **All-Weather** | Unaffected by lighting, rain, or fog |
| 🎯 **Precise Classification** | Distinguishes pedestrians from e-scooters |
| 👥 **Multi-Target Tracking** | Maintains identities in crowded scenarios |
| ⚡ **Real-Time** | <100ms processing latency |
| 📊 **3D Visualization** | Interactive point cloud display |
| 🔄 **Robust** | Handles occlusions and disappearances |

---

## 🚀 Quick Start

### Installation

```bash
# Clone and setup
git clone https://github.com/haowen-EE/Radar-project.git
cd Radar-project
python -m venv .venv311
source .venv311/bin/activate  # Windows: .venv311\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
# Run main application with sample data
python main.py
```

📚 **New to the project?** Start with [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup guide.

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [📘 Complete Documentation](DOCUMENTATION.md) | Full technical documentation and guides |
| [⚡ Quick Start](QUICKSTART.md) | 5-minute setup guide |
| [🔧 Installation](INSTALL.md) | Detailed installation instructions |
| [📖 Usage Guide](USAGE.md) | How to use the system |
| [❓ FAQ](FAQ.md) | Frequently asked questions |
| [🗺️ Roadmap](ROADMAP.md) | Future plans and development |
| [📝 Changelog](CHANGELOG.md) | Version history |

---

## 🏗️ Project Structure

```
Radar-project/
├── main.py                  # Main application entry point
├── escooter_plugin.py       # E-scooter detection plugin
├── read_data_awr1843.py     # Real-time data collection
│
├── utils/                   # Utility scripts
├── visualization/           # Visualization tools
├── experimental/            # Experimental features
│
├── Data/                    # Sample datasets
├── Test/                    # Test scripts
├── Analysis/                # Technical documentation
│
└── docs/                    # Documentation files
```

See [DOCUMENTATION.md](DOCUMENTATION.md) for complete project structure details.

---

## 🧮 How It Works

```
┌─────────────┐
│ AWR1843     │
│ Radar       │ → Raw RF Data
└─────────────┘
       ↓
┌─────────────────────────────────┐
│ Signal Processing               │
│ • Range FFT                     │
│ • Doppler FFT                   │
│ • CFAR Detection                │
└─────────────────────────────────┘
       ↓
┌─────────────────────────────────┐
│ Clustering & Tracking           │
│ • Grid-based DBSCAN             │
│ • Kalman Filtering              │
│ • Data Association              │
└─────────────────────────────────┘
       ↓
┌─────────────────────────────────┐
│ Classification                  │
│ • Speed Analysis                │
│ • Micro-Doppler Features        │
│ • Shape Recognition             │
└─────────────────────────────────┘
       ↓
┌─────────────────────────────────┐
│ Output                          │
│ • 3D Visualization              │
│ • Target Tracking               │
│ • Event Logging                 │
└─────────────────────────────────┘
```

Read more in [DOCUMENTATION.md](DOCUMENTATION.md#algorithm-overview).

---

## 🎓 Research Background

This project addresses campus safety challenges by providing:
- **Privacy-compliant monitoring** without visual surveillance
- **Reliable detection** in all weather conditions
- **Accurate classification** of pedestrians vs. e-scooters
- **Real-time performance** for immediate response

**Technology:** 77 GHz FMCW radar with 3×4 MIMO antenna array provides centimeter-level range resolution and degree-level angular resolution.

See [Proposal/](Proposal/) for detailed research objectives and methodology.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- Development workflow
- How to submit pull requests

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 📖 Citation

If you use this project in your research, please cite:

```bibtex
@misc{radar_project_2026,
  author = {Jiang, Haowen},
  title = {Campus Safety Radar Project: Pedestrian and E-scooter Detection},
  year = {2026},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/haowen-EE/Radar-project}}
}
```

---

## 📧 Contact

**Author**: Haowen Jiang

- GitHub: [@haowen-EE](https://github.com/haowen-EE)
- Email: your.email@example.com
- Project: [github.com/haowen-EE/Radar-project](https://github.com/haowen-EE/Radar-project)

---

## 🙏 Acknowledgments

- Texas Instruments for the AWR1843 mmWave Radar platform
- PyQtGraph for visualization tools
- NumPy and SciPy communities

---

## ⭐ Star History

If you find this project useful, please consider giving it a star ⭐

---

<p align="center">
  <b>Made with ❤️ for campus safety</b>
  <br>
  <sub>Protecting privacy while enhancing security</sub>
</p>
