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

## 📊 Sample Commands

```bash
# Run the interactive wizard (recommended for beginners)
luma-diagnostics --wizard

# Run basic diagnostic tests with your API key
luma-diagnostics --test --api-key your_api_key

# Test a specific image URL and your API key
luma-diagnostics --test --image /path/to/your/image.jpg --api-key your_api_key

# Use API key from environment variable
export LUMA_API_KEY=your_api_key  # (macOS/Linux)
luma-diagnostics --test
```

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
   - The wizard can also save your API key to your `.env` file for future use

> **Note**: Your API key should begin with `luma_` and be at least 32 characters long.

## 🐛 Troubleshooting Common Issues

### "API key is required" error
- Make sure you've set your LUMA API key using one of the methods in the API Key Configuration section
- Verify your API key starts with "luma_" and is at least 32 characters long
- Check if your API key has been properly saved in your environment or .env file

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
