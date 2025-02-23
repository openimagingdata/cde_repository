# cde_repository

This repository contains scripts and data for managing Common Data Elements (CDEs) for open imaging data.

## Project Structure

- `cde_repository/main.py`: Main script to process CDEs.
- `cde_repository/cde_sets/`: Directory containing valid CDE sets in JSON format.
- `cde_repository/cde_sets_docs/`: Directory containing documentation for CDE sets in Markdown format.
- `cde_repository/invalid_cde_sets/`: Directory containing invalid CDE sets in JSON and text formats.
- `cde_repository/status.log`: Log file for tracking the status of CDE processing.

## Python Environment Setup

### To get list of Python versions
```
py --list
```

### To create Python virtual environment
```
python -m venv .venv
```

### To activate Python environment
```
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On Unix or MacOS
```

### Installing dependencies
```
pip install -r requirements.txt
```

### Export Python dependencies into requirements.txt
```
pip freeze > requirements.txt
```

### To deactivate Python environment
```
deactivate
```

### Current Python Version
This project uses Python 3.12.