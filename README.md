# LUMA API Image Diagnostics

Welcome to the LUMA API Diagnostics tool, a community-created helper for LUMA Dream Machine API users! This user-friendly tool helps you diagnose and fix common issues when working with the LUMA API for image generation.

> **Note**: This is an independent, community-created tool and is not officially affiliated with or supported by LUMA Labs. While it's designed to help LUMA API users diagnose issues, it's maintained by the community.

## 🌟 Welcome to the LUMA Community!

The LUMA community is filled with amazing creators, artists, and developers exploring the cutting edge of AI-generated imagery. This diagnostic tool was built to support everyone in the community by making it easier to troubleshoot common issues with the LUMA API. We want to ensure everyone can focus on creating amazing art rather than debugging technical problems!

If you have ideas for improving this tool or want to contribute, please reach out. Together, we can make the LUMA experience even better for everyone.

## ✨ What This Tool Does

This diagnostic wizard helps you identify and fix issues when using the LUMA API by:

- Testing your API key and connection
- Validating your images before submission
- Checking for common configuration errors
- Generating detailed reports to help diagnose problems
- Providing helpful suggestions for fixing issues
- Displaying a helpful welcome message with quick start commands

## 🚀 Installation Guide

### Windows Users

1. **Install Python** (if not already installed):
   - Download the latest Python installer from [python.org](https://www.python.org/downloads/windows/)
   - Run the installer and **make sure to check "Add Python to PATH"**
   - Verify installation by opening Command Prompt and typing: `python --version`

2. **Install LUMA Diagnostics**:
   - Open Command Prompt (search for "cmd" in the Start menu)
   - Run: `pip install luma-diagnostics`

3. **Run the tool**:
   - In Command Prompt, run: `luma-diagnostics --wizard`
   - Follow the on-screen instructions

### macOS Users

1. **Install Python** (if not already installed):
   - Modern Macs come with Python, but it's recommended to install the latest version
   - The easiest way is with Homebrew:
     ```
     # Install Homebrew (if not installed)
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     
     # Install Python
     brew install python
     ```
   - Alternatively, download from [python.org](https://www.python.org/downloads/macos/)

2. **Install LUMA Diagnostics**:
   - Open Terminal (from Applications > Utilities)
   - Run: `pip3 install luma-diagnostics`

3. **Run the tool**:
   - In Terminal, run: `luma-diagnostics --wizard`
   - Follow the on-screen instructions

### Linux Users

1. **Install Python** (if not already installed):
   - Most Linux distributions come with Python pre-installed
   - If needed, install Python using your distribution's package manager:
     ```
     # Ubuntu/Debian
     sudo apt update
     sudo apt install python3 python3-pip
     
     # Fedora
     sudo dnf install python3 python3-pip
     
     # Arch Linux
     sudo pacman -S python python-pip
     ```

2. **Install LUMA Diagnostics**:
   - Open a terminal
   - Run: `pip3 install luma-diagnostics`

3. **Run the tool**:
   - In the terminal, run: `luma-diagnostics --wizard`
   - Follow the on-screen instructions

## 🧙‍♂️ Using the Diagnostic Wizard

The easiest way to use this tool is with the interactive wizard:

1. Open your terminal/command prompt
2. Run: `luma-diagnostics --wizard`
3. Follow the on-screen prompts

The wizard will guide you through:
- Setting up your LUMA API key (required for all tests)
- Testing your connection
- Validating your images
- Diagnosing any issues
- Generating a detailed report

## 🎮 Demo Mode (No API Key Required)

Want to see how the tool works without an API key? Try the demo mode:

```bash
# Run the interactive wizard in demo mode
luma-diagnostics --wizard --demo

# Try the basic tests in demo mode
luma-diagnostics --demo

# Test a specific image in demo mode
luma-diagnostics --demo --image /path/to/your/image.jpg
```

Demo mode provides simulated test results to show you how the tool looks and functions without requiring LUMA API credentials. It's perfect for:
- Getting familiar with the tool before obtaining an API key
- Training purposes and demonstrations
- Testing the tool in environments where API access is not available

## 📊 Sample Commands

```bash
# Run the interactive wizard (recommended for beginners)
luma-diagnostics --wizard

# Try the demo mode (no API key required)
luma-diagnostics --demo

# Test a specific image URL
luma-diagnostics --image-url https://example.com/image.jpg --test-type basic

# Create a case to track troubleshooting
luma-diagnostics --create-case "My Test Case"

# Test a local image file
luma-diagnostics --image /path/to/your/image.jpg --test-type full

# Get help with all available commands
luma-diagnostics --help
```

## 🆕 New in Version 1.0.2

The latest version includes a helpful welcome message that appears when you first install and import the package. This message provides:

- Quick start commands for common tasks
- Basic usage instructions
- An overview of the main functionality

The welcome message appears automatically on first use, but won't interrupt your workflow for subsequent imports.

## 🔑 API Key Configuration

Your LUMA API key is **required** for all tests, including basic diagnostics. You can provide it in several ways:

1. **Environment variable** (recommended):
   ```bash
   # Set temporarily for current session
   # Windows Command Prompt:
   set LUMA_API_KEY=your_api_key
   
   # Windows PowerShell:
   $env:LUMA_API_KEY="your_api_key"
   
   # macOS/Linux:
   export LUMA_API_KEY=your_api_key
   ```

2. **Configuration file**:
   - Create a file named `.env` in your home directory
   - Add the line: `LUMA_API_KEY=your_api_key`

3. **Command line argument**:
   - Pass your API key with each command: `luma-diagnostics --api-key your_api_key --test`

4. **Wizard input**:
   - The wizard will prompt you to enter your API key if needed

## 🐛 Troubleshooting Common Issues

### "Command not found" error
- Ensure Python is installed and added to your PATH
- Try reinstalling with: `pip install --user luma-diagnostics`
- For Windows, you might need to use: `py -m luma_diagnostics.cli`

### API key issues
- Verify your API key is correct
- Check if your API key has reached its usage limit
- Make sure the API key is properly formatted (no extra spaces)

### Image processing problems
- Ensure your image is in a supported format (JPG, PNG, WebP)
- Check that the image size is within allowed limits
- Verify the image URL is publicly accessible

## 🆘 Getting Help

If you encounter any issues:

1. Run the tool with the `--test` flag to perform basic diagnostics
2. Check the troubleshooting section above
3. Create a case with `--create-case` to save your test results
4. Report the issue on the [GitHub issue tracker](https://github.com/caseyfenton/luma-diagnostics/issues)

## 💬 Feedback and Contributions

Your feedback helps make this tool better for everyone in the LUMA community!

- Report bugs or request features on the [GitHub issue tracker](https://github.com/caseyfenton/luma-diagnostics/issues)
- Contribute to the codebase by submitting a pull request
- Share your experiences and suggestions with the community

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
