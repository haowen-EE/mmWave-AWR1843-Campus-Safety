# Changelog

All notable changes to the Campus Safety Radar Project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Machine learning-based classification
- Web-based monitoring dashboard
- Multi-radar fusion
- Mobile app integration

---

## [7.0.0] - 2025-10-07

### Added
- Continuous tracking optimization for e-scooters
- Improved handling of temporary occlusions
- Enhanced trajectory prediction during track loss
- Adaptive association gates based on target speed

### Changed
- Optimized tracking parameters for better stability
- Improved false positive reduction
- Enhanced multi-target scenario handling

### Fixed
- Tracking discontinuity in crowded scenarios
- Ghost track elimination
- ID switching issues

See: `Analysis/V7_Scooter_Optimization_Completion_Summary.md`

---

## [6.0.0] - 2025-09-15

### Added
- Inertia system for tracking stability
- Predictive tracking for occluded targets
- Improved track-to-track association

### Changed
- Enhanced tracking algorithm with motion prediction
- Better handling of target disappearance

### Fixed
- Frequent track ID changes
- Loss of tracking in partial occlusions

See: `Analysis/V6_Improvement_Completion_Summary.md`

---

## [5.0.0] - 2025-08-20

### Added
- Enhanced pedestrian detection algorithm
- Improved walking pattern recognition
- Better static object filtering

### Changed
- Refined speed thresholds for pedestrian classification
- Optimized clustering parameters

### Fixed
- False pedestrian detections from static objects
- Misclassification of slow-moving pedestrians

See: `Analysis/V5_Fix_Completion_Summary.md`

---

## [4.0.0] - 2025-07-10

### Added
- Static object detection and classification
- Object protection zones to prevent false associations
- Enhanced clutter filtering

### Changed
- Improved clustering algorithm efficiency
- Better bounding box visualization

### Fixed
- Memory leaks in long-running sessions
- Clustering instability with sparse point clouds
- GUI rendering issues on macOS

See: `Analysis/V4_Fix_Completion_Summary.md`

---

## [3.0.0] - 2025-06-01

### Added
- E-scooter detection plugin (`escooter_plugin.py`)
- Real-time 3D visualization with PyQtGraph
- Bounding box rendering for detected targets
- Multi-target tracking with Kalman filtering
- Speed estimation and display

### Changed
- Migrated from V2 experimental code to production-ready V3
- Improved CFAR detection algorithm
- Enhanced grid-based clustering
- Better trajectory smoothing (EWMA)

### Fixed
- Major tracking stability issues from V2
- Point cloud coordinate system inconsistencies
- Performance bottlenecks in clustering

See: `Analysis/V3_Ultimate_Fix_Solution.md`

---

## [2.0.0] - 2025-04-15

### Added
- Experimental e-scooter classification
- Basic multi-target tracking
- CSV data format support

### Changed
- Improved signal processing pipeline
- Enhanced DBSCAN clustering

### Known Issues
- Tracking instability in crowded scenarios
- False positives from clutter
- Performance issues with many targets

See: `Analysis/V2_Improvement_Description.md`

---

## [1.0.0] - 2025-03-01

### Added
- Initial proof of concept
- Basic radar data collection (`read_data_awr1843.py`)
- Point cloud visualization
- Simple target detection using CFAR
- Data format conversion utilities

### Features
- Real-time data streaming from AWR1843
- Basic 3D point cloud display
- CSV export functionality

---

## Version Naming Convention

- **Major version (X.0.0)**: Significant new features or breaking changes
- **Minor version (0.X.0)**: New features, backward compatible
- **Patch version (0.0.X)**: Bug fixes and minor improvements

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute to this project.

---

## Documentation

For detailed information about each version, see the corresponding documents in the `Analysis/` directory:

- V7: `V7_Scooter_Optimization_Completion_Summary.md`
- V6: `V6_Improvement_Completion_Summary.md`
- V5: `V5_Fix_Completion_Summary.md`
- V4: `V4_Fix_Completion_Summary.md`
- V3: `V3_Ultimate_Fix_Solution.md`
- V2: `V2_Improvement_Description.md`

[Unreleased]: https://github.com/haowen-EE/Radar-project/compare/v7.0.0...HEAD
[7.0.0]: https://github.com/haowen-EE/Radar-project/compare/v6.0.0...v7.0.0
[6.0.0]: https://github.com/haowen-EE/Radar-project/compare/v5.0.0...v6.0.0
[5.0.0]: https://github.com/haowen-EE/Radar-project/compare/v4.0.0...v5.0.0
[4.0.0]: https://github.com/haowen-EE/Radar-project/compare/v3.0.0...v4.0.0
[3.0.0]: https://github.com/haowen-EE/Radar-project/compare/v2.0.0...v3.0.0
[2.0.0]: https://github.com/haowen-EE/Radar-project/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/haowen-EE/Radar-project/releases/tag/v1.0.0
