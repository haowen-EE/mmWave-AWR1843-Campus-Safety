# Contributing to Campus Safety Radar Project

Thank you for your interest in contributing to the Campus Safety Radar Project! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Bug Reports](#bug-reports)
- [Feature Requests](#feature-requests)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of age, body size, disability, ethnicity, gender identity, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behaviors include:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Accepting constructive criticism gracefully
- Focusing on what's best for the community
- Showing empathy towards others

**Unacceptable behaviors include:**
- Harassment, trolling, or derogatory comments
- Publishing others' private information without permission
- Other conduct that would be inappropriate in a professional setting

---

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report:
1. Check the [Issues](https://github.com/haowen-EE/Radar-project/issues) page to avoid duplicates
2. Collect relevant information about the bug

When creating a bug report, include:
- **Clear title** describing the issue
- **Detailed description** of the problem
- **Steps to reproduce** the behavior
- **Expected vs. actual behavior**
- **Screenshots** (if applicable)
- **Environment details**:
  - OS and version
  - Python version
  - Package versions (`pip list`)
  - Radar model and configuration

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear, descriptive title**
- **Provide detailed description** of the proposed functionality
- **Explain why** this enhancement would be useful
- **List any alternative solutions** you've considered
- **Include mockups or examples** if applicable

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**
6. **Push to your fork**
7. **Open a Pull Request**

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/Radar-project.git
cd Radar-project

# Add upstream remote
git remote add upstream https://github.com/haowen-EE/Radar-project.git
```

### 2. Create Development Environment

```bash
# Create virtual environment
python -m venv .venv311
source .venv311/bin/activate  # Windows: .venv311\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

### 3. Create Feature Branch

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 100 characters maximum
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Single quotes for strings (unless avoiding escape)
- **Imports**: Grouped and sorted (standard library, third-party, local)

### Code Formatting

Use [Black](https://github.com/psf/black) for automatic formatting:

```bash
# Format all Python files
black .

# Check formatting without changes
black --check .
```

### Linting

Use [Flake8](https://flake8.pycqa.org/) for code quality:

```bash
# Run linter
flake8 .

# Configuration in .flake8 or setup.cfg
```

### Type Hints

Use type hints where possible:

```python
from typing import List, Dict, Optional, Tuple

def process_cluster(
    points: np.ndarray,
    min_points: int = 3
) -> Optional[Dict[str, any]]:
    """
    Process a cluster of points.
    
    Args:
        points: Nx3 array of point coordinates
        min_points: Minimum points required for valid cluster
        
    Returns:
        Dictionary with cluster properties, or None if invalid
    """
    if len(points) < min_points:
        return None
        
    return {
        'centroid': np.mean(points, axis=0),
        'size': len(points)
    }
```

### Documentation

#### Docstrings

Use Google-style docstrings:

```python
def calculate_speed(trajectory: List[Tuple[float, float, float]], 
                   dt: float) -> float:
    """
    Calculate speed from trajectory.
    
    Args:
        trajectory: List of (x, y, z) positions
        dt: Time step between positions in seconds
        
    Returns:
        Calculated speed in meters per second
        
    Raises:
        ValueError: If trajectory has fewer than 2 points
        
    Example:
        >>> traj = [(0, 0, 0), (1, 0, 0), (2, 0, 0)]
        >>> calculate_speed(traj, dt=0.1)
        10.0
    """
    if len(trajectory) < 2:
        raise ValueError("Need at least 2 points")
    
    # Implementation...
    return speed
```

#### Comments

- Write clear, concise comments
- Explain **why**, not **what**
- Update comments when code changes
- Use TODO comments for temporary code:

```python
# TODO(username): Implement GPU acceleration for this function
# BUG(username): Function fails when input is empty array
# FIXME(username): Memory leak in loop, needs investigation
```

---

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```
feat(tracking): Add Kalman filter for trajectory smoothing

Implement Kalman filter to smooth noisy trajectories and improve
tracking stability in crowded scenarios.

Closes #42
```

```
fix(clustering): Handle empty point clouds gracefully

Previously crashed when processing frames with no detected points.
Now returns empty cluster list instead.

Fixes #123
```

### Atomic Commits

- Each commit should be a single logical change
- Don't mix unrelated changes in one commit
- Commit early and often during development
- Squash commits before final PR if needed

---

## Pull Request Process

### Before Submitting

1. **Update your branch** with latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**:
   ```bash
   python -m pytest Test/
   ```

3. **Check code quality**:
   ```bash
   black --check .
   flake8 .
   ```

4. **Update documentation** if needed

5. **Test thoroughly** with various scenarios

### Submitting Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open PR on GitHub**:
   - Use clear, descriptive title
   - Reference related issues
   - Provide detailed description
   - Include screenshots/videos for UI changes
   - List test scenarios covered

3. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Related Issues
   Fixes #123
   Related to #456
   
   ## Changes Made
   - Added feature X
   - Fixed bug Y
   - Refactored module Z
   
   ## Testing
   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Manual testing completed
   - [ ] Performance tested
   
   ## Screenshots
   (if applicable)
   
   ## Additional Notes
   Any additional context
   ```

### Review Process

1. **Maintainer review**: Usually within 1-3 days
2. **Address feedback**: Make requested changes
3. **Approval**: Once approved, maintainer will merge

### After Merge

1. **Delete your branch**:
   ```bash
   git branch -d feature/your-feature-name
   git push origin --delete feature/your-feature-name
   ```

2. **Update your fork**:
   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```

---

## Testing Guidelines

### Writing Tests

Place tests in the `Test/` directory:

```python
# Test/test_clustering.py
import pytest
import numpy as np
from clustering_module import cluster_points

def test_cluster_basic():
    """Test basic clustering functionality."""
    points = np.array([[0, 0, 0], [0.1, 0, 0], [5, 5, 5]])
    clusters = cluster_points(points, max_dist=1.0)
    
    assert len(clusters) == 2
    assert len(clusters[0]) == 2

def test_cluster_empty():
    """Test clustering with empty input."""
    points = np.array([]).reshape(0, 3)
    clusters = cluster_points(points)
    
    assert len(clusters) == 0

def test_cluster_single_point():
    """Test clustering with single point."""
    points = np.array([[0, 0, 0]])
    clusters = cluster_points(points, min_points=1)
    
    assert len(clusters) == 1
```

### Running Tests

```bash
# Run all tests
python -m pytest Test/

# Run specific test file
python -m pytest Test/test_clustering.py

# Run with coverage
python -m pytest --cov=. Test/

# Run with verbose output
python -m pytest -v Test/
```

---

## Documentation Guidelines

### README Updates

When adding features:
1. Update feature list
2. Add usage examples
3. Update configuration section if needed

### Creating New Documentation

1. Place in appropriate directory (`docs/` or `Analysis/`)
2. Use Markdown format
3. Include table of contents for long documents
4. Add links from main README

### Documentation Structure

```markdown
# Document Title

Brief description

## Table of Contents
- [Section 1](#section-1)
- [Section 2](#section-2)

## Section 1

Content...

### Subsection

Content...

## Examples

```python
# Code example
```

## See Also

- [Related Doc 1](link)
- [Related Doc 2](link)
```

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Requests**: Code contributions

### Getting Help

- Check existing documentation
- Search closed issues
- Ask in GitHub Discussions
- Contact maintainers

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Acknowledged in project documentation

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

## Questions?

If you have questions about contributing:
- Open a [GitHub Discussion](https://github.com/haowen-EE/Radar-project/discussions)
- Contact the maintainers
- Check existing documentation

Thank you for contributing to Campus Safety Radar Project! 🎉
