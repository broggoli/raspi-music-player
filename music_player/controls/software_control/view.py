from .window.display_control import Display_Control
import ImageDraw
import Image
import ImageFont
import math

class Window(Display_Control):

    def __init__(self, size, position, fontSize=18):

        super(Window, self).__init__()

        self.sizeX, self.sizeY = size
        self.position = position
        self.positionX, self.positionY = position
        self.fontSize = fontSize

        self.f = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', self.fontSize)

class Main_Winow(Window):

    def __init__(self, size, position):
        self.fSize = 18
        super(Main_Winow, self).__init__(size, position, fontSize=self.fSize)
        self.window_image = Image.new('1', (self.sizeX, self.sizeY), 255)

    def get_image(self, songList):
        draw = ImageDraw.Draw(self.window_image)

        for index, song in enumerate(songList):
            if index < 6:
                yPos = index * self.fSize + 2
                draw.text((5, yPos), song, font = self.f, fill = 0)
        return self.window_image

class Battery_Indicator(Window):

    def __init__(self, size, position):
        super(Battery_Indicator, self).__init__(size, position)
        self.batteryImage = Image.new('1', (self.sizeX, self.sizeY), 255)

    def get_image(self, batteryPrercentage):
        draw = ImageDraw.Draw(self.batteryImage)
        #calculate percentage of width
        fullW = self.sizeX * batteryPrercentage * 0.01
        #Draw the correct battery bar
        draw.rectangle((0, 0, fullW, self.sizeY), fill = 0)

        return self.batteryImage

class Breadcrum(Window):

    def __init__(self, size, position):
        super(Breadcrum, self).__init__(size, position, fontSize=16)
        self.s = (self.sizeX, self.sizeY)
        self.breadcrum_image = Image.new('1', (self.sizeX, self.sizeY), 255)

    def get_image(self, breadcrum):
        draw = ImageDraw.Draw(self.breadcrum_image)
        draw.text((5, 1), breadcrum, font = self.f, fill = 0)
        draw.line((0, self.sizeY-2, self.sizeX, self.sizeY-2), fill = 0, width=2)

        return self.breadcrum_image

class Scroll_Bar(Window):

    def __init__(self, size, position):
        super(Scroll_Bar, self).__init__(size, position)
        self.scroll_bar_image = Image.new('1', (self.sizeX, self.sizeY), 0)
        self.currentPage, self.totalPages = 1, 1
        self.margin = 1

    def get_image(self, scrollInfo):
        self.currentPage, self.totalPages = scrollInfo

        height = self.calculate_height()
        width = self.sizeX - 2 * self.margin
        yPos = self.margin + (self.currentPage - 1) * height

        draw = ImageDraw.Draw(self.scroll_bar_image)
        draw.rectangle((self.margin, yPos, width, height), fill = 255)

        return self.scroll_bar_image

    def calculate_height(self):
        return (self.sizeY - 2 * self.margin) / self.totalPages

class Volume_View(Window):
    def __init__(self, size, position):
        super(Volume_View, self).__init__(size, position, fontSize=16)
        self.volume_image = Image.new('1', (self.sizeX, self.sizeY), 255)

    def get_image(self, volume):
        draw = ImageDraw.Draw(self.volume_image)
        draw.text((5, 0), "Vol: "+str(volume), font = self.f, fill = 0)
        return self.volume_image

class View(Display_Control):

    def __init__(self, settings, playlist):
        super(View, self).__init__()
        self.settings = settings
        self.currentPlaylist = playlist
        self.mainImage = Image.new('1', (200, 168), 255)
        self.status_bar = Battery_Indicator(size = (34, 10), position = (154, 12))

        self.breadcrum = Breadcrum(size = (200, 20),  position = (0, 0))
        self.main_window = Main_Winow(size = (190, 125), position = (0, 20))
        self.scroll_bar = Scroll_Bar(size = (10, 125), position = (190, 20))
        self.volume_view = Volume_View(size = (100, 20),  position = (0, 145))

        self.list_visual = self.List_Visual(self.currentPlaylist.list)

    def paint(self, imageList):
        for image, position in imageList:
            self.mainImage.paste(image, position)
        self.draw_partial(self.mainImage, 0, 32)

    def start(self):
        self.draw_background()
        vl = self.list_visual.visible_list()
        scrollInfo = (self.list_visual.currentPage, self.list_visual.totalPages)
        imageList = [
                        (self.volume_view.get_image(self.settings["volume"]), self.volume_view.position),
                        (self.breadcrum.get_image(self.settings["lastPlaylist"]), self.breadcrum.position),
                        (self.main_window.get_image(vl), self.main_window.position),
                        (self.scroll_bar.get_image(scrollInfo), self.scroll_bar.position)
                    ]
        self.paint(imageList)

    def update_volume_view(self, volume):
        self.paint([(self.volume_view.get_image(volume), self.volume_view.position)])
    def update_breadcrum(self, breadcrum):
        self.paint([(self.breadcrum.get_image(breadcrum), self.breadcrum.position)])
    def update_song_listing(self, songList, scrollInfo):
        self.paint([(self.main_window.get_image(breadcrum), self.main_window.position),
                    (self.scroll_bar.get_image(scrollInfo), self.scroll_bar.position)])

    class List_Visual(object):

        def __init__(self, initalList):
            self.list = initalList
            self.itemsPerPage = 6
            self.currentPage = 1
            self.totalPages = self.amount_pages()

        def amount_pages(self):
            return max(1, int(math.ceil(len(self.list) / self.itemsPerPage)))

        def visible_list(self):
            return [item.split("/")[3].split(".")[0] for index, item in enumerate(self.list)
                    if index >= self.itemsPerPage*(self.currentPage-1) and
                    index < self.itemsPerPage*(self.currentPage)]

        def change_list(self, l):
            self.list = l

        def get_list_image(self, l = None):
            if l:
                self.list = l

            vl = self.visible_list()
            scrollInfo = (self.currentPage, self.totalPages)
            imageList = [
                            (self.main_window.get_image(vl), self.main_window.position),
                            (self.scroll_bar.get_image(scrollInfo), self.scroll_bar.position)
                        ]
            return imageList
