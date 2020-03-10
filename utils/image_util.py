from PIL import Image


def format_image(image, path1, path2):
    width, height = image.size
    crop_dim = width
    if width < height:
        crop_dim = height
    min_dimension = min(height, width)
    if min_dimension < 500:
        return False

    height_1 = (240 / min_dimension)*crop_dim

    height_2 = (720 / min_dimension)* crop_dim

    image.thumbnail((width, height_1), Image.ANTIALIAS)
    image.save(path2)
    image.thumbnail((width, height_2), Image.ANTIALIAS)
    image.save(path1)
    return True

