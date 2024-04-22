
from PIL import Image, ImageFilter

class ImageTool:
    @staticmethod
    def resize_image(image, width, height):
        return image.resize((width, height))

    @staticmethod
    def rotate_image(image, angle):
        return image.rotate(angle)

    @staticmethod
    def apply_filter(image, filter_type):
        if filter_type == 'grayscale':
            return image.convert('L')
        elif filter_type == 'blur':
            return image.filter(ImageFilter.BLUR)
        elif filter_type == 'edge_enhance':
            return image.filter(ImageFilter.EDGE_ENHANCE)
        else:
            return image

    @staticmethod
    def convert_format(image, new_format):
        new_image = Image.new("RGB", image.size)
        new_image.paste(image)
        output = io.BytesIO()
        new_image.save(output, format=new_format)
        output.seek(0)
        return output
