# LUMA API Test Plan

## Overview
This test plan outlines the API-specific tests to be conducted once we receive the API key. These tests are designed to isolate the "Failed to read user input frames" error and understand its root cause.

## Test Categories

### 1. Authentication & Authorization
- [ ] Validate token format and structure
- [ ] Test token expiration handling
- [ ] Verify permission scopes
- [ ] Test invalid token scenarios
- [ ] Check rate limit headers

### 2. Image Source Testing
- [ ] Test with AWS S3 hosted image
- [ ] Test with Google Cloud Storage hosted image
- [ ] Test with GitHub raw content
- [ ] Test with clean IP (non-blacklisted) host
- [ ] Test with CDN-served images

### 3. Image Quality Variations
- [ ] Test with progressive JPEG
- [ ] Test with standard JPEG
- [ ] Test with varying compression qualities
- [ ] Test with embedded ICC profiles
- [ ] Test with different EXIF metadata

### 4. Request Structure Tests
- [ ] Test frame0 vs frame1 naming
- [ ] Test multiple keyframes
- [ ] Test different aspect ratios
- [ ] Test with/without optional parameters
- [ ] Validate JSON structure variations

### 5. Concurrency & Rate Limits
- [ ] Test concurrent requests (2, 5, 10 simultaneous)
- [ ] Test rapid sequential requests
- [ ] Test rate limit boundaries
- [ ] Test backoff behavior
- [ ] Monitor rate limit headers

### 6. Error Handling
- [ ] Test with invalid image URLs
- [ ] Test with temporary network issues
- [ ] Test with malformed requests
- [ ] Test with oversized images
- [ ] Document all error responses

### 7. Edge Cases
- [ ] Test with maximum allowed image size
- [ ] Test with minimum allowed image size
- [ ] Test with unusual aspect ratios
- [ ] Test with very long URLs
- [ ] Test with special characters in URLs

## Test Matrix

| Test Category | Clean Host | Blacklisted Host | S3/GCS | Local Server |
|--------------|------------|------------------|---------|--------------|
| Basic Auth    | [ ]        | [ ]              | [ ]     | [ ]          |
| Rate Limits   | [ ]        | [ ]              | [ ]     | [ ]          |
| Concurrency   | [ ]        | [ ]              | [ ]     | [ ]          |
| Error Cases   | [ ]        | [ ]              | [ ]     | [ ]          |

## Success Criteria
- Identify specific conditions that trigger the error
- Document any undisclosed API limitations
- Create reproducible test cases
- Generate clear error patterns

## Test Environment Setup
```bash
# Required environment variables
export LUMA_API_KEY="<to-be-provided>"
export TEST_S3_BUCKET="luma-test-images"
export TEST_GCS_BUCKET="luma-test-images"

# Test image preparation
aws s3 cp test_image.jpg s3://$TEST_S3_BUCKET/
gsutil cp test_image.jpg gs://$TEST_GCS_BUCKET/
```

## Reporting
Results will be logged to:
- `api_test_results.json`: Detailed test results
- `api_test_summary.md`: Human-readable summary
- `error_patterns.json`: Categorized error responses

## Notes
- All tests should be run from multiple geographic locations
- Each test should be run multiple times to ensure consistency
- Document any deviations from expected behavior
- Track all rate limit headers and usage metrics
