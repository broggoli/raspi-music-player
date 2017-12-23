from .display_modules import epd1in54
import Image
import ImageDraw
import ImageFont

class Display_Control(object):

    def __init__(self, displayRotation = 0):

        self.background = Image.open('../raspi-music-player/bitmaps/mp3-player-background.bmp')

        self.font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 24)
        self.displayRotation = displayRotation

        # Creates an image with all pixle set to 255 (white)
        self.clearingImage = Image.new('1', (epd1in54.EPD_WIDTH, epd1in54.EPD_HEIGHT), 255)

    def start(self):
        self.draw_background()
        self.draw_battery(60)

    def stop(stop):
        #just don't draw anything anymore, maybe usful later on
        pass

    def draw_background(self):
        self.draw_full(self.background)

    def draw_battery(self, batteryPrercentage):
        """Draws the given battery status in the battery indicator"""

        #setup battery dimensions on screen
        batteryW = 34
        batteryH = 10

        #initilize image
        batteryImage = Image.new('1', (batteryW, batteryH), 255)
        draw = ImageDraw.Draw(batteryImage)

        #calculate percentage of width
        fullW = batteryW * batteryPrercentage * 0.01

        #Draw the correct battery bar
        draw.rectangle((0, 0, fullW, batteryH), fill = 0)

        #draw to screen
        self.draw_partial(batteryImage, 154, 12)

    def draw_full(self, image):
        epd = epd1in54.EPD()
        epd.init(epd.lut_full_update)
        #Display full frame
        epd.set_frame_memory(image.rotate(self.displayRotation), 0, 0)
        epd.display_frame()
        epd.set_frame_memory(image.rotate(self.displayRotation), 0, 0)
        epd.display_frame()

    def draw_partial(self, image, x, y):
        epd = epd1in54.EPD()
        epd.init(epd.lut_partial_update)
        epd.set_frame_memory(image, x, y)
        epd.display_frame()

    """def feedback_flashing(self):
        # falshing bar height = 5 px
        # space from left = 75 px
        # space from top = 195 px

        flashingImage = Image.new('1', (50, 5), 0)
        self.draw_partial(flashingImage, 75, 195)
        flashingImage = Image.new('1', (50, 5), 255)
        self.draw_partial(flashingImage, 75, 195)
    """

class Window(object):

    def __init__(self):
        self.size = (148, 180)

    def draw_window(self):
        pass
