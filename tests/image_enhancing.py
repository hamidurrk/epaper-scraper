from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(img_path, new_dpi):
    # Open the image file
    img = Image.open(img_path)

    # Calculate the scale factor to achieve the desired DPI
    current_dpi = img.info.get('dpi', (72, 72))  # Default DPI is 72
    scale_factor = new_dpi / current_dpi[0]

    # Calculate the new dimensions
    new_width = int(img.width * scale_factor)
    new_height = int(img.height * scale_factor)

    # Resize the image while preserving the aspect ratio
    img = img.resize((new_width, new_height), resample=Image.LANCZOS)

    # Apply noise reduction
    img = img.filter(ImageFilter.MedianFilter(size=3))

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(6)

    # Increase brightness
    # enhancer = ImageEnhance.Brightness(img)
    # img = enhancer.enhance(1.2)

    # Apply sharpening
    # img = img.filter(ImageFilter.SHARPEN)

    # Convert to grayscale
    # img = img.convert('L')

    # Apply adaptive thresholding
    # img = img.point(lambda p: p > 170 and 255)

    return img

# Example usage:
image_path = 'C:/Users/hamid/OneDrive/Documents/epaper-scraper/tests/article_10.jpg'
processed_image = preprocess_image(image_path, 400)
processed_image.save('C:/Users/hamid/OneDrive/Documents/epaper-scraper/tests/processed_image.jpg')
