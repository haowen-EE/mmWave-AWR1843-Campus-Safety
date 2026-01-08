# Data Directory

This directory contains sample radar data for testing and development.

## Data Format

Each CSV file contains point cloud data with the following columns:

```
FrameID, Timestamp, X, Y, Z, Doppler, SNR
```

- **FrameID**: Frame number (sequential)
- **Timestamp**: ISO format timestamp (e.g., "2025-01-08T10:30:45.123456")
- **X**: Range (meters) - forward distance from radar
- **Y**: Height (meters) - vertical distance from radar
- **Z**: Lateral (meters) - horizontal distance from radar
- **Doppler**: Velocity (m/s) - positive = approaching, negative = receding
- **SNR**: Signal-to-Noise Ratio (dB)

## Sample Datasets

### With RSC (Range-Speed Correction)

- `escooter_fast_with_RSC.csv` - Fast-moving e-scooter (~8-10 m/s)
- `escooter_slow_with_RSC.csv` - Slow-moving e-scooter (~3-5 m/s)
- `man_run_with_RSC.csv` - Running person (~3-4 m/s)
- `man_walking_with_RSC.csv` - Walking person (~1.5 m/s)

### Without RSC

- `escooter_fast_without_RSC.csv` - Fast e-scooter (raw data)
- `escooter_slow_without_RSC.csv` - Slow e-scooter (raw data)
- `man_run_without_RSC.csv` - Running person (raw data)
- `man_walking_without_RSC.csv` - Walking person (raw data)

## Usage

To use these datasets:

```python
# In main.py
CSV_FILE = r'/path/to/Radar-project/Data/escooter_fast_with_RSC.csv'
```

## Collecting Your Own Data

See `read_data_awr1843.py` for real-time data collection from the radar.

## Notes

- RSC (Range-Speed Correction) data has been processed to correct for velocity-induced range errors
- All measurements are relative to the radar position
- Radar was mounted at 45cm height during data collection
- Data collected at 10 Hz frame rate

## Data Size

These are sample datasets. Full datasets may be several hundred MB to GB in size.

For privacy and repository size reasons, only representative samples are included.
