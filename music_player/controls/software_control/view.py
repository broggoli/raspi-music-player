from .window.display_control import Display_Control
import ImageDraw
import Image
import ImageFont

class Window(Display_Control):

    def __init__(self, size, position):

        super(Window, self).__init__()

        self.sizeX, self.sizeY = size
        self.positionX, self.positionY = position

    def paint(self, image):
        self.draw_partial(image, self.positionX, self.positionY)

class Main_Winow(Window):

    def __init__(self, size, position):
        super(Main_Winow, self).__init__(size, position)

class Starus_Bar(Window):

    def __init__(self, size, position):
        super(Starus_Bar, self).__init__(size, position)

        #setup battery size in pixels
        self.batteryW = 34
        self.batteryH = 10

    def draw_battery(self, batteryPrercentage):
        """Draws the given battery status in the battery indicator"""

        #initilize image
        batteryImage = Image.new('1', (self.batteryW, self.batteryH), 255)
        draw = ImageDraw.Draw(batteryImage)

        #calculate percentage of width
        fullW = self.batteryW * batteryPrercentage * 0.01
        #Draw the correct battery bar
        draw.rectangle((0, 0, fullW, self.batteryH), fill = 0)
        #draw to screen
        self.draw_partial(batteryImage, 154, 12)

class Breadcrum(Window):

    def __init__(self, size, position):
        super(Breadcrum, self).__init__(size, position)

class Volume_View(Window):
    def __init__(self, size, position):
        super(Volume_View, self).__init__(size, position)
        self.volume_image = Image.new('1', (self.sizeX, self.sizeY), 255)
        self.f = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18)

    def show(self, volume):
        draw = ImageDraw.Draw(self.volume_image)
        draw.rectangle((0, 0, self.sizeX, self.sizeY), fill = 255)
        draw.text((0, 0), str(volume), font = self.f, fill = 0)
        self.paint(self.volume_image)

class View(Display_Control):

    def __init__(self):
        super(View, self).__init__()
        self.main_window = Main_Winow(size = (180, 134), position = (10, 61))
        self.status_bar = Starus_Bar(size = (200, 32), position = (0, 0))
        self.breadcrum = Breadcrum(size = (190, 24),  position = (5, 37))
        self.volume_view = Volume_View(size = (40, 20),  position = (5, 180))


    def start(self, settings):
        self.draw_background()
        self.volume_view.show(settings["volume"])
