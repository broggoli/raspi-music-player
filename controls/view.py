#import display_modules.epd1in54
import display_modules.Image
import ImageDraw
import ImageFont

class View(object):

    def __init__(self, batteryPrercentage, displayRotation = 0):

        self.screenSize = screenSize
        self.background = Image.open('mp3-player-background.bmp')
        self.font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 24)
        self.displayRotation = displayRotation

        # Creates an image with all pixle set to 255 (white)
        self.clearingImage = Image.new('1', (epd1in54.EPD_WIDTH, epd1in54.EPD_HEIGHT), 255)
        #self.initialize_screen()
        draw_battery(batteryPrercentage)

    def initialize_screen(self):
        self.draw_background()

    def draw_background(self):
        self.display_full(self.background)

    def draw_battery(self, batteryPrercentage):
        """Draws the given battery status in the battery indicator"""

        #setup
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
        self.display_partial(batteryImage, 154, 12)

    def display_full(self, image):
        epd = epd1in54.EPD()
        epd.init(epd.lut_full_update)
        #Display full frame
        epd.set_frame_memory(image.rotate(self.displayRotation), 0, 0)
        epd.display_frame()
        epd.set_frame_memory(image.rotate(self.displayRotation), 0, 0)
        epd.display_frame()

    def display_partial(self, image, x, y):
        epd = epd1in54.EPD()
        epd.init(epd.lut_partial_update)
        epd.set_frame_memory(image, x, y)
        epd.display_frame()

    """def feedback_flashing(self):
        # falshing bar height = 5 px
        # space from left = 75 px
        # space from top = 195 px

        flashingImage = Image.new('1', (50, 5), 0)
        self.display_partial(flashingImage, 75, 195)
        flashingImage = Image.new('1', (50, 5), 255)
        self.display_partial(flashingImage, 75, 195)"""

class Window(object):

    def __init__(self):
        self.size = (148, 180)
