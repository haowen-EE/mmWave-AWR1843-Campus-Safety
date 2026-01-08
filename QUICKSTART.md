# Quick Start Guide

Get up and running with the Campus Safety Radar Project in minutes!

## Prerequisites Check

Before you begin, ensure you have:

- [ ] Python 3.11 or higher installed
- [ ] TI AWR1843 radar hardware (or sample data for testing)
- [ ] 8GB+ RAM
- [ ] 2GB free disk space

---

## Installation (5 minutes)

### Step 1: Clone the Repository

```bash
git clone https://github.com/haowen-EE/Radar-project.git
cd Radar-project
```

### Step 2: Set Up Virtual Environment

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

**Verify installation:**
```bash
python -c "import numpy, pyqtgraph; print('✓ Installation successful!')"
```

---

## First Run (2 minutes)

### Option A: Run with Sample Data

1. **Configure data path** in `main.py` (line ~91):
   ```python
   CSV_FILE = r'/full/path/to/Radar-project/Data/escooter_fast_with_RSC.csv'
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **You should see:**
   - A 3D visualization window
   - Point clouds in red
   - Green boxes around detected pedestrians
   - Purple boxes around e-scooters
   - Blue boxes around static objects

### Option B: Collect Real-Time Data

1. **Connect your AWR1843 radar** via USB

2. **Configure radar** (if not already done):
   - Use TI mmWave Studio
   - Load provided configuration

3. **Start data collection:**
   ```bash
   python read_data_awr1843.py
   ```

4. **Data will be saved** as CSV in the current directory

---

## Understanding the Interface

### 3D Visualization Controls

- **Left Mouse Button**: Rotate view
- **Right Mouse Button**: Pan view
- **Mouse Wheel**: Zoom in/out
- **Arrow Keys**: Navigate (if implemented)

### Color Coding

- **Red points**: Raw radar detections
- **Green boxes**: Pedestrians
- **Purple boxes**: E-scooters
- **Blue boxes**: Static objects

### Information Display

Labels above boxes show:
- Target ID
- Classification
- Speed (if enabled)

---

## Basic Configuration (Optional)

### Adjust Radar Height

If your radar is not at 45cm:

```python
# In main.py, line ~74
RADAR_HEIGHT = 0.60  # Your height in meters
```

### Adjust Detection Sensitivity

For more sensitive detection:
```python
MIN_POINTS_IN_CLUSTER = 2  # Down from 3
CONFIRM_SCORE = 2          # Down from 3
```

For fewer false positives:
```python
MIN_POINTS_IN_CLUSTER = 4  # Up from 3
CONFIRM_SCORE = 4          # Up from 3
```

---

## Quick Tests

### Test 1: Verify Point Cloud Display

```bash
python visualization/clustering_3d.py
```

Should show: Basic point cloud visualization

### Test 2: Check Clustering

```bash
python visualization/clustering_3d_boxes.py
```

Should show: Point clouds with bounding boxes

### Test 3: Analyze Sample Data

```bash
python Test/analyze_escooter_data.py
```

Should show: Statistics about e-scooter detections

---

## Common Issues & Quick Fixes

### Issue: "No module named 'PyQt5'"

**Fix:**
```bash
pip install PyQt5
```

### Issue: "Qt platform plugin could not be initialized"

**Fix (Windows):**
```bash
set QT_QPA_PLATFORM_PLUGIN_PATH=%VIRTUAL_ENV%\Lib\site-packages\PyQt5\Qt5\plugins
python main.py
```

**Fix (macOS/Linux):**
```bash
export QT_QPA_PLATFORM_PLUGIN_PATH=$VIRTUAL_ENV/lib/python3.11/site-packages/PyQt5/Qt5/plugins
python main.py
```

### Issue: "CSV file not found"

**Fix:**
- Use absolute path with `r'...'` prefix
- Check file actually exists
- Ensure no typos in path

Example:
```python
# Windows
CSV_FILE = r'C:\Users\YourName\Desktop\Radar-project\Data\escooter_fast_with_RSC.csv'

# macOS/Linux
CSV_FILE = r'/Users/yourname/Desktop/Radar-project/Data/escooter_fast_with_RSC.csv'
```

### Issue: Radar not detected

**Fix:**
1. Check USB connection
2. Verify radar is powered
3. Install TI drivers
4. Try different USB port

### Issue: Slow performance

**Quick fixes:**
```python
ROLL_WIN = 20        # Reduce from 40
GRID_CELL_M = 1.0    # Increase from 0.7
```

---

## Next Steps

### 1. Read the Documentation

- **Full guide**: [USAGE.md](USAGE.md)
- **Installation details**: [INSTALL.md](INSTALL.md)
- **Configuration**: [Analysis/Configuration_Parameters_Detailed_Guide.md](Analysis/Configuration_Parameters_Detailed_Guide.md)

### 2. Explore Sample Data

Try different datasets in the `Data/` directory:
- Walking pedestrian data
- Running pedestrian data
- Fast/slow e-scooter data

### 3. Collect Your Own Data

```bash
python read_data_awr1843.py
```

Then process with:
```bash
python main.py
```

### 4. Tune Parameters

Experiment with parameters in `main.py`:
- Speed thresholds
- Clustering parameters
- Tracking parameters

See [USAGE.md](USAGE.md) for detailed parameter descriptions.

### 5. Contribute

Found a bug? Have an idea? See [CONTRIBUTING.md](CONTRIBUTING.md)!

---

## Useful Commands

### Update the Project

```bash
git pull origin main
pip install --upgrade -r requirements.txt
```

### Run Tests

```bash
python -m pytest Test/
```

### Check System Performance

```bash
python -m cProfile main.py > performance_report.txt
```

### Process Multiple Files

```bash
# Create a script or use a loop
for file in Data/*.csv; do
    python main.py --input "$file"
done
```

---

## Learning Path

### Beginner

1. ✅ Install and run with sample data
2. ✅ Understand the visualization
3. ✅ Try different datasets
4. ✅ Read [USAGE.md](USAGE.md)

### Intermediate

1. Collect your own data
2. Adjust parameters for your scenario
3. Understand the algorithm (see [Algorithm Overview](README.md#-algorithm-overview))
4. Read technical documentation in `Analysis/`

### Advanced

1. Modify detection algorithms
2. Implement custom classification
3. Integrate with other systems
4. Contribute improvements

---

## Getting Help

### Self-Help Resources

1. **FAQ**: [FAQ.md](FAQ.md)
2. **Documentation**: [USAGE.md](USAGE.md), [INSTALL.md](INSTALL.md)
3. **Examples**: `Test/` directory
4. **Technical details**: `Analysis/` directory

### Community Help

1. **Search Issues**: [GitHub Issues](https://github.com/haowen-EE/Radar-project/issues)
2. **Ask a Question**: Open a new issue
3. **Discussion**: GitHub Discussions (if available)

### Direct Contact

Email: your.email@example.com

---

## Quick Reference Card

### Essential Files

| File | Purpose |
|------|---------|
| `main.py` | Main application |
| `escooter_plugin.py` | E-scooter detection |
| `read_data_awr1843.py` | Data collection |
| `utils/` | Utility scripts |
| `visualization/` | Visualization tools |

### Key Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `RADAR_HEIGHT` | 0.45m | Radar mounting height |
| `GRID_CELL_M` | 0.7m | Clustering grid size |
| `WALK_SPEED_HI` | 2.5 m/s | Max pedestrian speed |
| `CONFIRM_SCORE` | 3 | Detection confidence |

### Common Commands

```bash
# Run main app
python main.py

# Collect data
python read_data_awr1843.py

# Visualize
python visualization/clustering_3d_boxes.py

# Run tests
python -m pytest Test/
```

---

## Success Checklist

- [ ] Python 3.11+ installed
- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Sample data runs successfully
- [ ] Visualization window appears
- [ ] Can see point clouds and bounding boxes
- [ ] Read USAGE.md for next steps

---

**Congratulations!** You're now ready to use the Campus Safety Radar Project! 🎉

For detailed information, see [README.md](README.md) and [USAGE.md](USAGE.md).

**Questions?** Check [FAQ.md](FAQ.md) or open an issue on GitHub.
