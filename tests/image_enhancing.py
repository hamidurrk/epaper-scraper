from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(img_path):
    img = Image.open(img_path)

    current_dpi = img.info.get('dpi', (72, 72))  # Default DPI is 72
    scale_factor = 400 / current_dpi[0]

    new_width = int(img.width * scale_factor)
    new_height = int(img.height * scale_factor)

    img = img.resize((new_width, new_height), resample=Image.LANCZOS)

    img = img.filter(ImageFilter.MedianFilter(size=3))  # Noise reduction

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(6)

    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.2)

    img = img.point(lambda p: p > 170 and 255)

    return img

# Example usage:
image_path = 'C:/Users/hamid/OneDrive/Documents/epaper-scraper/tests/article_10.jpg'
processed_image = preprocess_image(image_path)
processed_image.save('C:/Users/hamid/OneDrive/Documents/epaper-scraper/tests/processed_image.jpg')
