# Test Cases Directory

This directory contains test case configurations and results. Each test case should have:
1. An environment file (e.g., `case123.env`)
2. A results directory (e.g., `results/case123/`)

## Directory Structure
```
cases/
├── README.md
├── templates/
│   └── case.env.template
├── active/
│   ├── case123.env
│   └── case456.env
└── results/
    ├── case123/
    │   ├── 2025-01-22T090425-diagnostic.json
    │   └── 2025-01-22T090425-diagnostic.txt
    └── case456/
        ├── 2025-01-22T085530-diagnostic.json
        └── 2025-01-22T085530-diagnostic.txt
```

## Usage
1. Copy `templates/case.env.template` to `active/caseXXX.env`
2. Edit the new env file with case-specific details
3. Run diagnostics: `python luma_diagnostics.py --case caseXXX`
