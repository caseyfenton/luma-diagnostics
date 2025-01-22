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

## Case Management

This directory contains test cases for the LUMA API Diagnostics tool. Each case can have its own configuration and test images.

## Default Test Images

By default, the diagnostics tool uses test images from LUMA's official documentation. These images are known to work well with the API and serve as a good baseline for testing your API key and connection setup.

The default images are configured in the `.env` file and include:
- Basic test image for general diagnostics
- Image reference test image
- Style reference test image
- Character reference test image

## Using Custom Images

To test with your own images:

1. Create a new case directory:
```bash
cp -r cases/templates/basic cases/your_case_name
```

2. Edit the case configuration in `cases/your_case_name/.env`:
```bash
# Replace with your image URLs
TEST_IMAGE_URL=https://your-server.com/path/to/image.jpg
IMAGE_REF_URL=https://your-server.com/path/to/ref_image.jpg
STYLE_REF_URL=https://your-server.com/path/to/style_image.jpg
CHARACTER_REF_URL=https://your-server.com/path/to/character_image.jpg

# Customize prompts for your use case
TEXT_TO_IMAGE_PROMPT="Your custom prompt"
IMAGE_REF_PROMPT="Your reference prompt"
STYLE_REF_PROMPT="Your style prompt"
CHARACTER_REF_PROMPT="Your character prompt"
MODIFY_IMAGE_PROMPT="Your modification prompt"
```

3. Run diagnostics with your case:
```bash
luma-diagnostics --case your_case_name
```

## Workflow Recommendation

1. First run the diagnostics with default images to verify:
   - Your API key works
   - Your network can access LUMA's API
   - Basic API functionality works

2. Once the default tests pass, create a new case with your custom images to:
   - Verify your image hosting setup
   - Test specific image types or formats
   - Debug issues with particular images or prompts

## Case Directory Structure

```
cases/
├── templates/          # Template cases
│   └── basic/         # Basic test template
├── results/           # Test results
└── your_case_name/    # Your custom test cases
```

## Tips

- Host test images on a publicly accessible server
- Ensure image URLs are direct links to the image files
- Test with various image formats (JPEG, PNG)
- Keep image sizes reasonable (under 10MB)
- Use descriptive case names for better organization

## Usage
1. Copy `templates/case.env.template` to `active/caseXXX.env`
2. Edit the new env file with case-specific details
3. Run diagnostics: `python luma_diagnostics.py --case caseXXX`
