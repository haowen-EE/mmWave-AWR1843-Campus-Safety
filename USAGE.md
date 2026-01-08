# Usage Guide

This guide explains how to use the Campus Safety Radar Project for various tasks.

## Table of Contents

- [Quick Start](#quick-start)
- [Data Collection](#data-collection)
- [Data Processing](#data-processing)
- [Real-Time Monitoring](#real-time-monitoring)
- [Configuration](#configuration)
- [Advanced Usage](#advanced-usage)
- [Performance Tuning](#performance-tuning)

---

## Quick Start

### Running with Sample Data

1. **Activate your virtual environment:**
   ```bash
   # Windows
   .venv311\Scripts\activate
   
   # macOS/Linux
   source .venv311/bin/activate
   ```

2. **Configure data file path in `main.py`:**
   ```python
   # Line ~91
   CSV_FILE = r'/path/to/Data/escooter_fast_with_RSC.csv'
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

4. **View the visualization:**
   - A 3D window will open showing the point cloud
   - Green boxes: Pedestrians
   - Purple boxes: E-scooters
   - Blue boxes: Static objects

### Controls

- **Mouse Left Button**: Rotate view
- **Mouse Right Button**: Pan view
- **Mouse Wheel**: Zoom in/out
- **Arrow Keys**: Navigate frames (if implemented)

---

## Data Collection

### Real-Time Data Collection from Radar

1. **Connect the AWR1843 radar** via USB

2. **Configure radar parameters** (if needed):
   ```python
   # Edit read_data_awr1843.py
   CONFIG_FILE = 'path/to/radar_config.cfg'
   ```

3. **Start data collection:**
   ```bash
   python read_data_awr1843.py
   ```

4. **Data will be saved** in the current directory as CSV files

### Recording Sessions

For organized data collection:

```bash
# Create a session directory
mkdir -p Data_V3/session_$(date +%Y%m%d_%H%M%S)

# Start recording with custom output
python read_data_awr1843.py --output Data_V3/session_*/radar_data.csv
```

---

## Data Processing

### Convert Raw Data to CSV

If you have binary radar data files:

```bash
# Convert .dat files to CSV
python utils/convert_dat_to_csv.py --input raw_data.dat --output processed_data.csv
```

### Basic 3D Visualization

```bash
# Simple point cloud visualization
python visualization/clustering_3d.py
```

### Advanced Visualization with Bounding Boxes

```bash
# Clustering with bounding boxes
python visualization/clustering_3d_boxes.py
```

### Batch Processing

Process multiple files:

```bash
# Create a batch processing script
for file in Data/*.csv; do
    python main.py --input "$file" --output "Results/$(basename $file)"
done
```

---

## Real-Time Monitoring

### Main Application (main.py)

The main application provides real-time monitoring with advanced features:

#### Key Features

1. **Pedestrian Detection**: Tracks walking, running, and standing persons
2. **E-scooter Detection**: Identifies electric scooters based on speed and signature
3. **Static Object Detection**: Recognizes stationary objects
4. **Multi-target Tracking**: Maintains identities across frames

#### Configuration Options

Edit parameters in `main.py`:

```python
# === Clustering Parameters ===
GRID_CELL_M = 0.7              # Grid cell size (meters)
MIN_POINTS_IN_CLUSTER = 3      # Minimum points to form a cluster

# === Speed Thresholds ===
WALK_SPEED_LO = 0.3            # Minimum walking speed (m/s)
WALK_SPEED_HI = 2.5            # Maximum pedestrian speed (m/s)

# === Tracking Parameters ===
MAX_MISS = 8                   # Maximum frames before losing track
ROLL_WIN = 40                  # Rolling window for trajectory smoothing
```

### E-scooter Plugin

The `escooter_plugin.py` provides specialized e-scooter detection:

```python
from escooter_plugin import EscooterPlugin

# Initialize plugin
plugin = EscooterPlugin()

# Process frame
results = plugin.process_frame(point_cloud, frame_id)

# Get detected e-scooters
for escooter in results['escooters']:
    print(f"E-scooter at position: {escooter['position']}")
    print(f"Speed: {escooter['speed']} m/s")
```

---

## Configuration

### Radar Installation Height

**Critical**: Adjust for your radar mounting height

```python
# In main.py, line ~74
# Default: 45cm above ground
RADAR_HEIGHT = 0.45  # meters
```

All Y-coordinates in point cloud are relative to this height.

### Coordinate System Rotation

If your radar is oriented differently:

```python
# Line ~94
ROTATE_Y_PLUS_90_FOR_X_ALIGNED_WALK = True  # or False
```

- `True`: Rotates coordinates +90° around Y-axis
- `False`: No rotation (default)

### Detection Sensitivity

#### Pedestrian Detection

```python
# Minimum duration to confirm detection
MIN_DURATION_S = 0.5           # seconds

# Height extent threshold
Y_EXTENT_MIN = 0.35            # meters (minimum vertical extent)

# Speed range for pedestrians
WALK_SPEED_LO = 0.3            # m/s
WALK_SPEED_HI = 2.5            # m/s
```

#### E-scooter Detection

Configured in `escooter_plugin.py`:

```python
# Speed thresholds for e-scooters
ESCOOTER_SPEED_MIN = 2.0       # m/s
ESCOOTER_SPEED_MAX = 15.0      # m/s

# Size characteristics
ESCOOTER_MIN_POINTS = 5
ESCOOTER_MAX_POINTS = 30
```

#### Static Object Detection

```python
# Object detection parameters
OBJ_SPEED_MAX = 0.20           # m/s (nearly stationary)
OBJ_MIN_DURATION_S = 0.5       # seconds
OBJ_MAX_POINTS = 15            # Maximum point count
OBJ_MAX_VOL = 0.50             # m³ (maximum volume)
```

### Tracking Parameters

```python
# Association gate (how close to link to existing track)
ASSOC_GATE_BASE_M = 2.4        # meters

# Maximum missed frames before track termination
MAX_MISS = 8                   # frames

# Trajectory smoothing
EWMA_ALPHA = 0.35              # Exponential smoothing factor
ROLL_WIN = 40                  # Rolling window size
```

### Display Settings

```python
# Point cloud rendering
POINT_SIZE = 3                 # pixels
PT_COLOR = (1, 0, 0, 1)        # Red (R, G, B, Alpha)

# Bounding box colors
BOX_COLOR = (0, 1, 0, 1)       # Green for pedestrians
OBJ_BOX_COLOR = (0, 0.6, 1, 1) # Blue for objects

# Box line width
BOX_WIDTH = 2                  # pixels

# Display speed labels
LABEL_SPEED = True             # Show speed above boxes
```

---

## Advanced Usage

### Custom Classification

Implement custom classification logic:

```python
def custom_classifier(cluster, trajectory):
    """
    Custom classification function.
    
    Args:
        cluster: Current cluster data
        trajectory: Historical trajectory data
        
    Returns:
        str: Classification label ('pedestrian', 'escooter', 'object', 'unknown')
    """
    # Your logic here
    speed = calculate_speed(trajectory)
    height = cluster['y_extent']
    
    if speed < 0.5 and height < 0.5:
        return 'object'
    elif 0.3 < speed < 2.5 and height > 0.35:
        return 'pedestrian'
    elif speed > 2.5:
        return 'escooter'
    else:
        return 'unknown'
```

### Export Tracking Data

Save tracking results to file:

```python
import csv

def export_tracks(tracks, output_file):
    """Export tracking data to CSV."""
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Frame', 'TrackID', 'X', 'Y', 'Z', 'Speed', 'Class'])
        
        for frame_id, frame_tracks in tracks.items():
            for track in frame_tracks:
                writer.writerow([
                    frame_id,
                    track['id'],
                    track['position'][0],
                    track['position'][1],
                    track['position'][2],
                    track['speed'],
                    track['classification']
                ])
```

### Integration with Other Systems

#### REST API Example

```python
from flask import Flask, jsonify
import threading

app = Flask(__name__)
current_detections = {}

@app.route('/api/detections')
def get_detections():
    """API endpoint for current detections."""
    return jsonify(current_detections)

# Run Flask in separate thread
def run_api():
    app.run(port=5000)

threading.Thread(target=run_api, daemon=True).start()
```

#### WebSocket Streaming

```python
import asyncio
import websockets
import json

async def stream_detections(websocket, path):
    """Stream detection results via WebSocket."""
    while True:
        # Get current detections
        data = get_current_detections()
        await websocket.send(json.dumps(data))
        await asyncio.sleep(0.1)  # 10 Hz update rate

# Start WebSocket server
start_server = websockets.serve(stream_detections, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
```

---

## Performance Tuning

### Optimize for Speed

1. **Enable GPU Acceleration:**
   ```bash
   pip install cupy-cuda12x  # or cupy-cuda11x
   ```

2. **Reduce Rolling Window:**
   ```python
   ROLL_WIN = 20  # Smaller window = faster processing
   ```

3. **Increase Grid Cell Size:**
   ```python
   GRID_CELL_M = 1.0  # Larger cells = fewer clusters
   ```

4. **Reduce Max Tracking:**
   ```python
   MAX_MISS = 5  # Drop tracks faster
   ```

### Optimize for Accuracy

1. **Increase Rolling Window:**
   ```python
   ROLL_WIN = 60  # More history = smoother tracking
   ```

2. **Decrease Grid Cell Size:**
   ```python
   GRID_CELL_M = 0.5  # Finer granularity
   ```

3. **Tighter Association Gate:**
   ```python
   ASSOC_GATE_BASE_M = 1.5  # Stricter matching
   ```

4. **Longer Confirmation:**
   ```python
   CONFIRM_SCORE = 5  # Require more evidence
   ```

### Memory Optimization

For long-running sessions:

```python
# Limit trajectory history
MAX_TRAJECTORY_LENGTH = 100  # Keep only recent history

# Periodic cleanup
if frame_id % 1000 == 0:
    cleanup_old_tracks()
    gc.collect()  # Force garbage collection
```

### Benchmark Your System

```bash
# Run performance test
python Test/test_conversion_simulation.py

# Check processing time per frame
python -m cProfile main.py > performance.txt
```

---

## Testing and Validation

### Run Test Suite

```bash
# Run all tests
python -m pytest Test/

# Run specific test
python Test/analyze_escooter_data.py
```

### Validate Detection Accuracy

```bash
# Analyze pedestrian detection
python Test/analyze_pedestrian.py

# Analyze e-scooter detection
python Test/analyze_escooter_data.py

# Check walking detection
python Test/analyze_walk.py
```

### Compare Versions

```bash
# Test optimizations
python Test/test_scooter_optimization.py

# Test pedestrian fixes
python Test/test_pedestrian_fix.py
```

---

## Common Use Cases

### Case 1: Campus Monitoring

```python
# High accuracy, moderate speed
GRID_CELL_M = 0.6
ROLL_WIN = 50
CONFIRM_SCORE = 4
```

### Case 2: Traffic Analysis

```python
# Fast processing, basic tracking
GRID_CELL_M = 1.0
ROLL_WIN = 20
CONFIRM_SCORE = 2
```

### Case 3: Research/Analysis

```python
# Maximum detail and accuracy
GRID_CELL_M = 0.4
ROLL_WIN = 80
CONFIRM_SCORE = 5
LABEL_SPEED = True  # Show all information
```

---

## Troubleshooting

### Low Detection Rate

1. Check radar mounting height and angle
2. Verify speed thresholds match your scenario
3. Increase sensitivity: lower `CONFIRM_SCORE`
4. Check data quality

### False Positives

1. Increase `CONFIRM_SCORE` for stricter detection
2. Adjust speed thresholds
3. Enable static object filtering
4. Review and adjust `MIN_DURATION_S`

### Tracking Instability

1. Increase `ROLL_WIN` for smoother tracking
2. Adjust `ASSOC_GATE_BASE_M` for better association
3. Increase `MAX_MISS` to handle occlusions
4. Check for environmental interference

### Performance Issues

1. Enable GPU acceleration
2. Reduce `ROLL_WIN`
3. Increase `GRID_CELL_M`
4. Close unnecessary applications
5. Check system resources (CPU, RAM, GPU usage)

---

## Additional Resources

- **Configuration Guide**: [Analysis/Configuration_Parameters_Detailed_Guide.md](Analysis/Configuration_Parameters_Detailed_Guide.md)
- **E-scooter Recognition**: [Analysis/E-scooter_Recognition_Detailed_Guide.md](Analysis/E-scooter_Recognition_Detailed_Guide.md)
- **Technical Specs**: [Analysis/Technical_Specification_2025-10-07.md](Analysis/Technical_Specification_2025-10-07.md)

---

**Questions?** Open an issue on [GitHub](https://github.com/haowen-EE/Radar-project/issues) or contact: your.email@example.com
