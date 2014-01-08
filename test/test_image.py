from PIL import Image

from instagram_cl.image import BrailleImage


class TestGrayScaleImage:

    def test_stores_size(self):
        width = 4
        height = 8
        test_image = Image.new('RGB', (width, height))

        braille_image = BrailleImage(test_image, width=width)

        assert braille_image.width == 4
        assert braille_image.height == 2

    def test_returns_braille_chars(self):
        width = 4
        height = 8
        test_image = Image.new('RGB', (width, height))

        braille_image = BrailleImage(test_image, width=20)
        image_array, braille_chars = braille_image.as_array()
        assert len(braille_chars) == 20
        assert len(braille_chars[0]) == 20

