# LUMA Generation Tests

This document describes the generation tests available in the LUMA Diagnostics tool. These tests validate LUMA's image and video generation capabilities.

## Prerequisites

- LUMA API key (required)
- Test image URL (for image-to-image and video tests)
- Configuration file (optional, for custom settings)

## Test Categories

### 1. Text-to-Image Generation

Tests LUMA's ability to generate images from text prompts.

#### Default Tests
- Basic prompt generation
- Style variations
- Aspect ratio tests
- Model comparison tests

#### Configuration Options
```json
{
    "text_to_image": {
        "prompt": "A serene mountain lake at sunset with reflections in the water",
        "aspect_ratio": "16:9",
        "model": "photon-1",
        "style": "photographic"
    }
}
```

### 2. Image-to-Image Generation

Tests LUMA's ability to modify or transform existing images.

#### Default Tests
- Style transfer
- Image modifications
- Reference-based generation
- Character reference tests

#### Configuration Options
```json
{
    "image_to_image": {
        "prompt": "Make it more vibrant and colorful",
        "image_ref": {
            "url": "https://example.com/reference.jpg",
            "weight": 0.85
        },
        "style_ref": null,
        "character_ref": null
    }
}
```

### 3. Image-to-Video Generation

Tests LUMA's video generation capabilities.

#### Default Tests
- Static camera
- Basic camera motions
- Complex camera paths
- Duration variations

#### Configuration Options
```json
{
    "image_to_video": {
        "prompt": "Add dynamic movement",
        "camera_motion": "Orbit Left",
        "duration": 3.0,
        "fps": 24
    }
}
```

## Test Results

### Success Criteria

A test is considered successful when:
1. The generation request is accepted (status 201)
2. The generation completes without errors
3. The resulting assets are accessible
4. The output matches the input parameters

### Result Format

Results are provided in both JSON and human-readable formats:

```json
{
    "test_name": "Text to Image Generation",
    "status": "completed",
    "details": {
        "generation_id": "8e87f674-f07b-47b9-a37e-ae23be32d42a",
        "state": "completed",
        "assets": {
            "image": "https://api.lumalabs.ai/images/8e87f674-f07b-47b9-a37e-ae23be32d42a.jpg"
        },
        "request": {
            "prompt": "A serene mountain lake at sunset",
            "model": "photon-1",
            "aspect_ratio": "16:9"
        }
    }
}
```

## Common Issues

### Generation Failures
1. **Invalid API Key**
   - Ensure your API key is valid and has the correct permissions
   - Check for any rate limiting or quota issues

2. **Image Access Issues**
   - Verify the image URL is publicly accessible
   - Check for any IP restrictions or geoblocking
   - Ensure the image format is supported

3. **Parameter Issues**
   - Verify all required parameters are provided
   - Check parameter values are within allowed ranges
   - Ensure prompt text follows guidelines

### Performance Issues
1. **Long Generation Times**
   - Check network connectivity
   - Monitor API status
   - Consider reducing complexity of request

2. **Resource Usage**
   - Monitor rate limits
   - Track quota usage
   - Consider batch processing for multiple tests

## Best Practices

1. **Test Organization**
   - Use meaningful case IDs
   - Group related tests together
   - Document test configurations

2. **Error Handling**
   - Implement appropriate timeouts
   - Handle transient failures gracefully
   - Log detailed error information

3. **Result Management**
   - Save all test results
   - Track generation IDs
   - Monitor long-running generations

4. **Configuration Management**
   - Use version control for configurations
   - Document parameter changes
   - Share successful configurations
