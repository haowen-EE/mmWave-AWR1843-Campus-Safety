# Installation Guide

This guide provides detailed instructions for setting up the Campus Safety Radar Project.

## Table of Contents

- [System Requirements](#system-requirements)
- [Software Installation](#software-installation)
- [Hardware Setup](#hardware-setup)
- [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.11 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 2GB free space for software and data
- **Display**: 1920x1080 resolution recommended

### Recommended Requirements

- **GPU**: NVIDIA GPU with CUDA support (for acceleration)
- **CPU**: Multi-core processor (Intel i5/i7 or AMD equivalent)
- **RAM**: 16GB or more

### Hardware

- **TI AWR1843 mmWave Radar**: Available from Texas Instruments
- **USB Cable**: For radar connection
- **Mounting Equipment**: Tripod or stable mount at ~45cm height

---

## Software Installation

### Step 1: Install Python

#### Windows

1. Download Python 3.11+ from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```bash
   python --version
   ```

#### macOS

```bash
# Using Homebrew
brew install python@3.11

# Verify installation
python3 --version
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Verify installation
python3.11 --version
```

### Step 2: Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/haowen-EE/Radar-project.git

# Navigate to project directory
cd Radar-project
```

### Step 3: Create Virtual Environment

#### Windows

```bash
# Create virtual environment
python -m venv .venv311

# Activate virtual environment
.venv311\Scripts\activate
```

#### macOS/Linux

```bash
# Create virtual environment
python3.11 -m venv .venv311

# Activate virtual environment
source .venv311/bin/activate
```

### Step 4: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

### Step 5: Verify Installation

```bash
# Test imports
python -c "import numpy; import pyqtgraph; print('Installation successful!')"
```

---

## Hardware Setup

### TI AWR1843 Radar Configuration

#### Step 1: Install TI Software

1. Download and install **mmWave Studio** from [TI's website](https://www.ti.com/tool/MMWAVE-STUDIO)
2. Download and install **DCA1000EVM** software (if using DCA1000)
3. Install USB drivers for the radar

#### Step 2: Connect the Radar

1. Connect AWR1843 to your computer via USB
2. Power on the radar
3. Verify connection:
   - Windows: Check Device Manager → Ports (COM & LPT)
   - macOS/Linux: Check `/dev/ttyUSB*` or `/dev/ttyACM*`

#### Step 3: Configure Radar Parameters

The radar configuration file should include:

```json
{
  "frequency": 77,
  "bandwidth": 4000,
  "chirp_duration": 60,
  "idle_time": 7,
  "ramp_end_time": 62,
  "frame_periodicity": 100
}
```

Use mmWave Studio or the provided configuration scripts to load these parameters.

#### Step 4: Mount the Radar

1. Mount radar at **45cm height** (default configuration)
2. Ensure clear line of sight to monitoring area
3. Angle radar slightly downward for optimal coverage
4. Secure mounting to prevent vibrations

### Radar Height Adjustment

If you need to mount the radar at a different height:

1. Measure actual height from ground
2. Update `RADAR_HEIGHT` in `main.py`:
   ```python
   # Line ~74
   RADAR_HEIGHT = 0.45  # Change to your height in meters
   ```

---

## Optional: GPU Acceleration Setup

### CUDA Installation (NVIDIA GPUs)

#### Windows

1. Download CUDA Toolkit from [NVIDIA's website](https://developer.nvidia.com/cuda-downloads)
2. Install CUDA Toolkit
3. Install CuPy:
   ```bash
   # For CUDA 12.x
   pip install cupy-cuda12x
   
   # For CUDA 11.x
   pip install cupy-cuda11x
   ```

#### Linux

```bash
# Install CUDA Toolkit
sudo apt install nvidia-cuda-toolkit

# Install CuPy
pip install cupy-cuda12x  # or cupy-cuda11x
```

### Verify GPU Setup

```bash
python -c "import cupy; print('GPU acceleration available!')"
```

---

## Configuration File Setup

### Create Data Directory Structure

```bash
# Create directories for organized data storage
mkdir -p Data Data_V2 Data_V3 Test Analysis
```

### Configure Data File Path

Edit `main.py` (around line 91):

```python
# Update with your data file path
CSV_FILE = r'/path/to/your/data.csv'
```

**Examples:**

- Windows: `CSV_FILE = r'C:\Users\YourName\Documents\radar_data.csv'`
- macOS/Linux: `CSV_FILE = r'/home/username/radar_data.csv'`

---

## Testing the Installation

### Run Basic Test

```bash
# Test with sample data
python main.py
```

If you see a 3D visualization window, installation is successful!

### Run Unit Tests

```bash
# Run test suite
python -m pytest Test/
```

---

## Troubleshooting

### Common Issues

#### 1. "No module named 'PyQt5'"

**Solution:**
```bash
pip install PyQt5
```

#### 2. "Could not find Qt platform plugin"

**Solution (Windows):**
```bash
set QT_QPA_PLATFORM_PLUGIN_PATH=%VIRTUAL_ENV%\Lib\site-packages\PyQt5\Qt5\plugins
```

**Solution (macOS/Linux):**
```bash
export QT_QPA_PLATFORM_PLUGIN_PATH=$VIRTUAL_ENV/lib/python3.11/site-packages/PyQt5/Qt5/plugins
```

#### 3. Radar Not Detected

**Solution:**
- Check USB connection
- Verify drivers are installed
- Try a different USB port
- Check device permissions (Linux):
  ```bash
  sudo chmod 666 /dev/ttyUSB0
  ```

#### 4. ImportError: DLL load failed (Windows)

**Solution:**
Install Visual C++ Redistributable from [Microsoft](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)

#### 5. Low Frame Rate / High Latency

**Solutions:**
- Enable GPU acceleration (install CuPy)
- Reduce `ROLL_WIN` parameter
- Close other applications
- Use lower visualization quality

### Getting Help

If you encounter issues not listed here:

1. Check the [Issues](https://github.com/haowen-EE/Radar-project/issues) page
2. Search existing discussions
3. Create a new issue with:
   - Your operating system and Python version
   - Complete error message
   - Steps to reproduce the problem

---

## Next Steps

After successful installation:

1. Read the [Usage Guide](USAGE.md) for detailed usage instructions
2. Explore sample data in the `Data/` directory
3. Review configuration parameters in `Analysis/Configuration_Parameters_Detailed_Guide.md`
4. Start collecting your own radar data with `read_data_awr1843.py`

---

## Updating the Software

To update to the latest version:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt
```

---

**Need more help?** Contact us at: your.email@example.com
