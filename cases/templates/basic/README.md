# Basic Test Case Template

This is a basic test case template that uses LUMA's official example images and prompts. It's designed to verify:

1. API Key functionality
2. Network connectivity
3. Basic API operations
4. Image processing capabilities

## Usage

1. Create a new case from this template:
```bash
cp -r cases/templates/basic cases/your_case_name
```

2. Copy the template env file:
```bash
cd cases/your_case_name
cp .env.template .env
```

3. Edit `.env` to add your API key:
```bash
LUMA_API_KEY=your_api_key_here
```

4. Run the diagnostics:
```bash
luma-diagnostics --case your_case_name
```

## Default Test Images

This template uses official example images from LUMA's documentation:

1. Basic Test Image:
   - URL: https://storage.cdn-luma.com/dream_machine/7e4fe07f-1dfd-4921-bc97-4bcf5adea39a/video_0_thumb.jpg
   - Purpose: General API functionality testing

2. Reference Images:
   - Image Reference
   - Style Reference
   - Character Reference

## Default Test Prompts

The template includes example prompts that are known to work well with the API:

1. Text to Image: "A teddy bear in sunglasses playing electric guitar and dancing"
2. Image Reference: "sunglasses"
3. Style Reference: "dog"
4. Character Reference: "man as a warrior"
5. Image Modification: "transform all the flowers to sunflowers"

## Customization

To use your own images or prompts:
1. Edit the `.env` file
2. Replace any of the `*_URL` variables with your image URLs
3. Modify the `*_PROMPT` variables with your custom prompts

Remember to use publicly accessible image URLs that return the image file directly.
