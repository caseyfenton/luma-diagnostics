# LUMA Labs API Diagnostics Tool

A comprehensive diagnostic tool for testing and validating the LUMA Dream Machine API, with special focus on image and video generation capabilities.

## Features

### Basic Tests
- Public Access & DNS Resolution
- SSL/TLS Certificate Validation
- Redirect & Response Analysis
- Response Headers & Content Analysis
- Basic Image Validity

### Generation Tests (requires API key)
- Text-to-Image Generation
  - Default prompts with standard settings
  - Custom prompts and configurations
  - Status monitoring and result validation
- Image-to-Image Generation
  - Style transfer testing
  - Image modification capabilities
  - Reference image handling
- Image-to-Video Generation
  - Camera motion validation
  - Video quality assessment
  - Generation status tracking

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

## Quick Start

The easiest way to get started is to use our interactive wizard:

```bash
luma-diagnostics --wizard
```

The wizard will guide you through:
- Selecting an image to test (including a sample image)
- Setting up your API key (if you have one)
- Choosing which tests to run
- Understanding the results

For more advanced usage, you can also use the command line interface:

```bash
# Test a specific image
luma-diagnostics --image-url https://example.com/image.jpg

# Run a specific test case
luma-diagnostics --case my_test_case

# Specify a configuration file
luma-diagnostics --config config.json
```

## Usage

### Interactive Wizard Mode (Recommended for New Users)

The easiest way to use LUMA Diagnostics is through the interactive wizard:

```bash
luma-diagnostics --wizard
```

The wizard will:
1. Guide you through the setup process
2. Help you choose which tests to run
3. Explain the results in a clear, human-readable format
4. Provide suggestions for next steps

### Using Generation Tests

Generation tests require a LUMA API key and are automatically run when the key is available:

1. Text-to-Image:
   ```bash
   # Test with default prompt
   luma-diagnostics --case default_prompt

   # Test with custom prompt
   luma-diagnostics --case custom_prompt --config config.json
   ```

2. Image-to-Image:
   ```bash
   # Test style transfer
   luma-diagnostics --case style_transfer --image-url https://example.com/source.jpg

   # Test image modifications
   luma-diagnostics --case image_mod --config mod_config.json
   ```

3. Image-to-Video:
   ```bash
   # Test video generation
   luma-diagnostics --case video_gen --config video_config.json
   ```

### Understanding Results

Results are saved in both JSON and human-readable text formats:

```
results/
└── case_id/
    ├── diagnostic_results_TIMESTAMP.json  # Machine-readable format
    └── diagnostic_results_TIMESTAMP.txt   # Human-readable format
```

The results include:
- Test status (completed/failed)
- Detailed error messages if applicable
- Generation IDs and status
- Asset URLs when available
- Performance metrics

## Case Management

The wizard can help you create and manage test cases. After running tests, you'll be prompted to create a case if you want to track:
- Test configurations and results
- Customer information
- Technical context and issues
- Priority levels

Cases are stored in the `cases/active` directory with the following structure:
```
cases/
├── active/
│   └── case_20250122_102345/
│       └── CASE_20250122_102345.md
└── archived/
```

Each case file includes:
- Case metadata (ID, creation time, priority)
- Customer information
- Technical description
- Test configuration
- Complete test results

You can also create cases manually or move them to `cases/archived` when resolved.

## API Key Management

Your LUMA API key can be stored in several ways:

1. **Environment Variable (Recommended)**
   ```bash
   # Add to your ~/.bashrc, ~/.zshrc, or similar
   export LUMA_API_KEY=your_api_key_here
   ```
   Or create a `.env` file in your home directory:
   ```bash
   # ~/.env
   LUMA_API_KEY=your_api_key_here
   ```

2. **Settings File**
   When you enter an API key in the wizard, it's saved to:
   ```
   ~/.config/luma-diagnostics/settings.json
   ```
   This allows you to reuse the key in future sessions.

3. **Per-Session**
   You can also enter your API key each time you run the wizard, or pass it directly via the CLI:
   ```bash
   luma-diagnostics --api-key your_api_key_here
   ```

The wizard will automatically detect and offer to use any existing API keys it finds in these locations.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| TEST_IMAGE_URL | Yes | URL of the image to test |
| LUMA_API_KEY | No* | Your LUMA API key (required for generation tests) |
| CASE_ID | No | Unique identifier for this test case |
| OUTPUT_DIR | No | Custom directory for test results |
| CONFIG_PATH | No | Path to custom test configuration |

*Required for generation tests and advanced API features

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
