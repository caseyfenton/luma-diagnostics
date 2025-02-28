# LUMA API Image Diagnostics

An automated diagnostic suite for troubleshooting image processing issues with the LUMA API. This tool provides a user-friendly wizard interface to run comprehensive tests and generate detailed reports.

## Features

- 🧙‍♂️ Interactive CLI wizard
- 🔍 Comprehensive image tests
- 📊 Detailed test reports
- 📁 Case management
- 🔑 Secure API key handling
- 📝 Human-readable outputs
- 🤖 JSON outputs for automation

## Installation

```bash
# Clone the repository
git clone https://github.com/caseyfenton/luma-diagnostics.git
cd luma-diagnostics

# Install dependencies
pip install -e .
```

## Quick Start

```bash
# Run the diagnostic wizard
luma-diagnostics --wizard

# Or run specific tests
luma-diagnostics --image-url https://example.com/image.jpg --test-type basic
```

## Configuration

1. Set your LUMA API key:
   ```bash
   # Option 1: Environment variable
   export LUMA_API_KEY=your_api_key

   # Option 2: Add to ~/.env file
   echo "LUMA_API_KEY=your_api_key" >> ~/.env

   # Option 3: Let the wizard guide you
   luma-diagnostics --wizard
   ```

2. Optional: Configure default test parameters in `~/.config/luma-diagnostics/settings.json`

## Available Tests

### Basic Tests
- URL accessibility
- Certificate validation
- Redirect handling
- MIME type verification
- Image format validation

### Advanced Tests (requires API key)
- Text-to-Image generation
- Image-to-Image generation
- Image-to-Video generation

## Case Management

The tool includes a case management system to track issues and test results:

```
cases/
├── active/          # Active case files
│   └── customer-case-20250122/
│       ├── README.md
│       ├── test_20250122_105752.json
│       └── test_20250122_105752.txt
└── archived/        # Archived cases
```

## Development

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/caseyfenton/luma-diagnostics/issues).
