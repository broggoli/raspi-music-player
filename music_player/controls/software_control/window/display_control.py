from .display_modules import epd1in54
import Image
import ImageDraw
import ImageFont

class Display_Control(object):

    def __init__(self, displayRotation = 0):

        self.background = Image.open('../raspi-music-player/bitmaps/mp3-player-background.bmp')
        #self.gray-bg = Image.open('../raspi-music-player/bitmaps/gray-background.bmp')

        self.font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 24)
        self.displayRotation = displayRotation

        # Creates an image with all pixle set to 255 (white)
        self.clearingImage = Image.new('1', (epd1in54.EPD_WIDTH, epd1in54.EPD_HEIGHT), 255)
        self.epd = epd1in54.EPD()

    def stop(stop):
        #just don't draw anything anymore, maybe usful later on
        pass

    def get_gray_background(self, size):
        width, height = size
        background = Image.new('1', (width, height), 255)
        for i in range(int(height/2)):
            background.paste(Image.open('../raspi-music-player/bitmaps/gray-background.bmp'), (0, i*2))
        return background

    def draw_background(self):
        self.draw_full(self.background)


    def draw_full(self, image):
        self.epd.init(self.epd.lut_full_update)
        #Display full frame
        self.epd.set_frame_memory(image.rotate(self.displayRotation), 0, 0)
        self.epd.display_frame()
        self.epd.set_frame_memory(image.rotate(self.displayRotation), 0, 0)
        self.epd.display_frame()

    def draw_partial(self, image, x, y):
        self.epd.init(self.epd.lut_partial_update)
        self.epd.set_frame_memory(image.rotate(self.displayRotation), x, y)
        self.epd.display_frame()
        self.epd.set_frame_memory(image.rotate(self.displayRotation), x, y)
        self.epd.display_frame()
