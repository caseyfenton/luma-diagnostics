# LUMA Labs API Diagnostics Tool

A comprehensive diagnostic tool for troubleshooting LUMA Dream Machine API issues, particularly focusing on the "Failed to read user input frames" error.

## Features

### Basic Tests
- Public Access & DNS Resolution
- SSL/TLS Certificate Validation
- Redirect & Response Analysis
- Response Headers & Content Analysis
- Basic Image Validity

### Advanced Tests
- Advanced Image Analysis
  - Progressive JPEG detection
  - Color profile validation
  - Compression quality assessment
  - Metadata examination
- Network Diagnostics
  - Full traceroute implementation
  - IP reputation checking
  - GeoIP location verification
- Security Tests
  - CORS validation
  - Firewall detection
  - Proxy detection
  - HSTS verification

### API Tests (requires API key)
- Authentication flow
- Rate limiting behavior
- Error response patterns
- Concurrent request handling

## Installation

### Option 1: Install from PyPI (Recommended)
```bash
pip install luma-diagnostics
```

### Option 2: Install from Source
1. Clone the repository:
   ```bash
   git clone https://github.com/lumalabs/api-diagnostics.git
   cd api-diagnostics
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### For Customers

1. Quick single test:
   ```bash
   # Set your image URL directly
   export TEST_IMAGE_URL="https://example.com/path/to/your/image.jpg"
   python luma_diagnostics.py
   ```

2. Using a configuration file:
   ```bash
   # Copy the template
   cp env.example .env
   
   # Edit .env with your settings
   nano .env
   
   # Run diagnostics
   python luma_diagnostics.py
   ```

### For Support Team

1. Create a new case:
   ```bash
   # Copy the case template
   cp cases/templates/case.env.template cases/active/case123.env
   
   # Edit the case configuration
   nano cases/active/case123.env
   
   # Run diagnostics for this case
   python luma_diagnostics.py --case case123
   ```

2. View results:
   ```bash
   # Results are saved in cases/results/case123/
   # Named with timestamp: YYYY-MM-DDTHHMMSS-diagnostic.json
   ```

3. Running multiple cases:
   ```bash
   # Test multiple cases sequentially
   for case in case123 case456 case789; do
     python luma_diagnostics.py --case $case
   done
   ```

## Case Management

### Directory Structure
```
cases/
├── templates/          # Templates for new cases
│   ├── case.env.template
│   └── example_customer_case.env.example
├── active/            # Active case configurations
│   ├── case123.env
│   └── case456.env
└── results/           # Test results by case
    ├── case123/
    │   ├── 2025-01-22T090425-diagnostic.json
    │   └── 2025-01-22T090425-diagnostic.txt
    └── case456/
        ├── 2025-01-22T085530-diagnostic.json
        └── 2025-01-22T085530-diagnostic.txt
```

### Case Configuration
Each case configuration file (`cases/active/caseXXX.env`) includes:
- Case metadata (ID, customer info, priority)
- Test configuration
- API settings
- Output preferences

See `cases/templates/case.env.template` for all available options.

### Results
- Results are automatically saved with timestamps
- Each case has its own results directory
- Both JSON (machine-readable) and TXT (human-readable) formats
- Customer information can be included/excluded

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| TEST_IMAGE_URL | Yes | URL of the image to test |
| LUMA_API_KEY | No | Your LUMA API key for advanced tests |
| CASE_ID | No | Unique identifier for this test case |
| CUSTOMER_ID | No | Customer identifier |
| PRIORITY | No | Case priority (low/medium/high/critical) |

See `env.example` or `cases/templates/case.env.template` for all available options.

## Common Issues & Solutions

### "Failed to read user input frames"
Common causes:
1. Image not publicly accessible
2. Image server IP blacklisted
3. Network filtering/blocking
4. Image format/quality issues

### SSL/TLS Issues
- Check certificate validity
- Verify SNI support
- Confirm HTTPS configuration

### Network Issues
- Check firewall rules
- Verify DNS resolution
- Test with alternative image hosts

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please:
1. Check the [Issues](https://github.com/lumalabs/api-diagnostics/issues) page
2. Review our [API Documentation](https://lumalabs.ai/docs)
3. Contact [LUMA Support](https://lumalabs.ai/support)

## Acknowledgments

- LUMA Labs Support Team
- Contributors to the project
- The Python community

---
Made with ❤️ by LUMA Labs
