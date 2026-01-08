# Frequently Asked Questions (FAQ)

## General Questions

### What is this project?

The Campus Safety Radar Project is an intelligent monitoring system that uses millimeter-wave radar to detect and classify pedestrians and electric scooters in real-time, enhancing campus safety while preserving privacy.

### Why use radar instead of cameras?

- **Privacy**: Radar doesn't capture images or personal identities
- **All-weather**: Works in darkness, rain, fog, and bright sunlight
- **Privacy-compliant**: No video recording or facial recognition
- **Reliable**: Not affected by lighting conditions or visual obstructions

### What hardware do I need?

- TI AWR1843 mmWave radar (77 GHz)
- Computer with Python 3.11+ (Windows, macOS, or Linux)
- USB cable for radar connection
- Optional: NVIDIA GPU for acceleration

---

## Installation & Setup

### Do I need a GPU?

No, but it's recommended. The system works without GPU but runs faster with CUDA acceleration. CPU-only mode is sufficient for offline processing and moderate real-time use.

### What if I get "Qt platform plugin" errors?

This is a common PyQt5 issue. The code includes automatic fixes, but if problems persist:

**Windows:**
```bash
set QT_QPA_PLATFORM_PLUGIN_PATH=%VIRTUAL_ENV%\Lib\site-packages\PyQt5\Qt5\plugins
```

**macOS/Linux:**
```bash
export QT_QPA_PLATFORM_PLUGIN_PATH=$VIRTUAL_ENV/lib/python3.11/site-packages/PyQt5/Qt5/plugins
```

### Can I use Python 3.10 or 3.12?

Python 3.11 is recommended, but 3.10 and 3.12 should work. Some dependencies might need version adjustments.

### How do I verify my installation?

```bash
python -c "import numpy; import pyqtgraph; print('Success!')"
```

If this runs without errors, your installation is correct.

---

## Usage

### How do I run the system?

1. Edit `CSV_FILE` path in `main.py` to point to your data
2. Run: `python main.py`
3. A 3D visualization window will appear

### What file format does it use?

CSV files with columns: `FrameID, Timestamp, X, Y, Z, Doppler, SNR`

### Can I use my own data?

Yes! Collect data using `read_data_awr1843.py` or convert existing radar data to the CSV format.

### How do I adjust the radar height?

Edit line ~74 in `main.py`:
```python
RADAR_HEIGHT = 0.45  # Your height in meters
```

### Why aren't pedestrians being detected?

Common causes:
- Speed thresholds too restrictive (adjust `WALK_SPEED_LO` and `WALK_SPEED_HI`)
- Radar height incorrect (update `RADAR_HEIGHT`)
- Minimum cluster size too large (reduce `MIN_POINTS_IN_CLUSTER`)
- Confirmation score too high (lower `CONFIRM_SCORE`)

### Why are e-scooters being missed?

Check `escooter_plugin.py` parameters:
- Speed thresholds might be too narrow
- Point count thresholds might not match your scenario
- Try adjusting detection sensitivity

---

## Performance

### The visualization is slow/laggy

Solutions:
1. Enable GPU acceleration (install CuPy)
2. Reduce `ROLL_WIN` (less history = faster)
3. Increase `GRID_CELL_M` (coarser clustering = faster)
4. Close other applications
5. Reduce visualization quality

### How much RAM do I need?

- Minimum: 8GB
- Recommended: 16GB
- For large datasets or long sessions: 32GB

### What frame rate can I expect?

- With GPU: 10-15 Hz (real-time)
- Without GPU: 5-10 Hz
- Depends on: number of targets, parameter settings, hardware

### Can I process data offline?

Yes! The system works with pre-recorded CSV files. No need for real-time radar connection.

---

## Technical Questions

### What's the detection range?

Approximately 30 meters, depending on:
- Target size and material
- Radar configuration
- Environmental conditions

### What's the accuracy?

Based on testing:
- Classification accuracy: 75-80%
- Position accuracy: ±10cm
- Speed accuracy: ±0.2 m/s

### How does it distinguish pedestrians from e-scooters?

Multiple factors:
- **Speed**: E-scooters typically move faster (>2.5 m/s)
- **Point distribution**: Different spatial patterns
- **Doppler signature**: Wheel rotation vs. limb motion
- **Trajectory characteristics**: Smoothness, acceleration patterns

### What about bicycles or motorcycles?

Current version focuses on pedestrians and e-scooters. Bicycles and motorcycles may be detected but classification is not optimized for them. This could be a future enhancement.

### Does it work indoors?

Yes, but:
- Strong multipath reflections may cause false detections
- Smaller detection range due to clutter
- May need parameter tuning for indoor environments

---

## Data & Privacy

### Is any personal data recorded?

No. The radar only measures:
- Distance (range)
- Velocity (speed)
- Direction (angle)

No images, video, or identifying information is captured.

### Can I share my data?

Yes, but ensure:
- No additional sensors captured identifiable information
- You have permission if on private property
- You comply with local privacy regulations

### What format should I use for sharing datasets?

Use the standard CSV format:
```
FrameID, Timestamp, X, Y, Z, Doppler, SNR
```

Include metadata file with:
- Radar height
- Location type (urban, campus, indoor, etc.)
- Weather conditions
- Ground truth labels (if available)

---

## Troubleshooting

### No radar data received

1. Check USB connection
2. Verify radar is powered on
3. Check COM port (Windows) or `/dev/tty*` (Linux/macOS)
4. Ensure drivers are installed
5. Try different USB port

### "CSV file not found" error

- Use absolute path with `r'...'` prefix
- Check file path is correct
- Ensure file exists and has read permissions

### Tracking is unstable

1. Increase `MAX_MISS` (allow more missed detections)
2. Increase `ROLL_WIN` (more smoothing)
3. Adjust `ASSOC_GATE_BASE_M` (association threshold)
4. Check for environmental clutter

### High false positive rate

1. Increase `CONFIRM_SCORE` (stricter confirmation)
2. Adjust speed thresholds
3. Increase `MIN_DURATION_S` (longer required duration)
4. Enable static object filtering

### Memory usage grows over time

This might indicate a memory leak. Solutions:
- Limit trajectory history length
- Periodically clean old tracks
- Restart application for long sessions
- Report as bug if persistent

---

## Development

### How can I contribute?

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines. Quick steps:
1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

### Where do I report bugs?

Open an issue on [GitHub Issues](https://github.com/haowen-EE/Radar-project/issues) with:
- Detailed description
- Steps to reproduce
- System information
- Error messages/logs

### How do I add new features?

1. Check existing issues/discussions
2. Create feature proposal issue
3. Discuss approach with maintainers
4. Implement and submit PR

### Can I use this in my research?

Yes! Please cite the project:
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

## License & Legal

### What license is this under?

MIT License - you can use, modify, and distribute freely with attribution.

### Can I use this commercially?

Yes, under MIT License terms. Include the license and copyright notice.

### Are there any export restrictions?

Millimeter-wave radar technology may be subject to export controls in some countries. Check local regulations.

---

## Getting Help

### Where can I ask questions?

1. Check this FAQ first
2. Search [GitHub Issues](https://github.com/haowen-EE/Radar-project/issues)
3. Open new issue if problem persists
4. Contact maintainers: your.email@example.com

### Is there a community/forum?

Currently using GitHub Issues and Discussions. May establish dedicated forum if community grows.

### How often is the project updated?

Active development with regular updates. Check [CHANGELOG.md](CHANGELOG.md) for version history.

---

## Additional Resources

- [Installation Guide](INSTALL.md)
- [Usage Guide](USAGE.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Technical Documentation](Analysis/)
- [Project Proposal](Proposal/)

---

**Question not answered?** Open an issue on GitHub or contact us at: your.email@example.com
