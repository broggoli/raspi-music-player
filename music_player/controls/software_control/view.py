from .window.display_control import Display_Control
import ImageDraw
import Image
import ImageFont

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

    def get_image(self, songList, highlightedItem):
        draw = ImageDraw.Draw(self.window_image)
        draw.rectangle((0, 0, self.sizeX, self.sizeY), fill = 255)

        for index, song in enumerate(songList):
            if index < 6:
                yPos = index * self.fSize + 2
                if(highlightedItem == index):
                    draw.rectangle((0, yPos-1, self.sizeX, yPos+self.fSize+1), fill = 0)
                    draw.text((5, yPos), song, font = self.f, fill = 255)
                else:
                    draw.text((5, yPos), song, font = self.f, fill = 0)
            else:
                break

        draw.line((0, self.sizeY-1, self.sizeX, self.sizeY-1), fill = 0, width=2)
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

class List_Title(Window):

    def __init__(self, size, position):
        super(List_Title, self).__init__(size, position, fontSize=16)
        self.s = (self.sizeX, self.sizeY)
        self.list_title_image = Image.new('1', (self.sizeX, self.sizeY), 255)

    def get_image(self, breadcrum):
        draw = ImageDraw.Draw(self.list_title_image)
        draw.rectangle((0, 0, self.sizeX, self.sizeY), fill=255)
        draw.text((5, 1), breadcrum, font = self.f, fill = 0)
        draw.line((0, self.sizeY-2, self.sizeX, self.sizeY-2), fill = 0, width=2)

        return self.list_title_image

class Page_Counter(Window):

    def __init__(self, size, position):
        super(Page_Counter, self).__init__(size, position, fontSize=16)
        self.page_counter_image = Image.new('1', (self.sizeX, self.sizeY), 255)

    def get_image(self, scrollInfo):
        draw = ImageDraw.Draw(self.page_counter_image)
        draw.rectangle((0, 0, self.sizeX, self.sizeY), fill=255)
        pageCounterText = "%i/%i" % scrollInfo
        draw.text((0, 0), pageCounterText, font = self.f, fill = 0)

        return self.page_counter_image

class Scroll_Bar(Window):

    def __init__(self, size, position):
        super(Scroll_Bar, self).__init__(size, position)
        self.scroll_bar_image = Image.new('1', (self.sizeX, self.sizeY), 0)
        self.currentPage, self.totalPages = 1, 1
        self.margin = 1

    def get_image(self, scrollInfo):
        self.currentPage, self.totalPages = scrollInfo

        height = self.sizeY - 2 * self.margin
        pedalHeight = self.calculate_height() - 2 * self.margin + 1
        width = self.sizeX - 2 * self.margin
        pedalWidth = self.sizeX - 4 * self.margin + 1
        #the Position of the pedal
        yPos = 2 * self.margin + (self.currentPage - 1) * pedalHeight

        draw = ImageDraw.Draw(self.scroll_bar_image)
        draw.rectangle((self.margin, self.margin, width, height), fill = 255)

        draw.rectangle((2 * self.margin, yPos, pedalWidth, yPos+pedalHeight), fill = 0)

        return self.scroll_bar_image

    def calculate_height(self):
        return (self.sizeY - 2 * self.margin) / self.totalPages

class Volume_View(Window):
    def __init__(self, size, position):
        super(Volume_View, self).__init__(size, position, fontSize=16)
        self.volume_image = Image.new('1', (self.sizeX, self.sizeY), 255)

    def get_image(self, volume):
        draw = ImageDraw.Draw(self.volume_image)
        draw.text((5, 0), "Volume:"+str(volume), font = self.f, fill = 0)
        return self.volume_image

class View(Display_Control):

    def __init__(self, settings, list_visual):
        super(View, self).__init__()
        self.settings = settings
        self.mainImage = Image.new('1', (200, 168), 255)
        self.status_bar = Battery_Indicator(size = (34, 10), position = (154, 12))

        #Initalizing all the components of the display by giving them a size and position in the main Image
        self.list_title = List_Title(size = (200, 20),  position = (0, 0))
        self.main_window = Main_Winow(size = (190, 125), position = (0, 19))
        self.scroll_bar = Scroll_Bar(size = (10, 126), position = (190, 18))
        self.volume_view = Volume_View(size = (100, 20),  position = (0, 145))
        self.page_counter = Page_Counter(size = (50, 20), position = (170, 150))

        #Handles the lists that need to be displayed
        #   Handles:
        #            * page counter variables
        #            * the part of the list, that is visible
        #            * which of the list items is currently selected
        #            * when to go to the next/previous page
        self.list_visual = list_visual

    def paint(self, imageList):
        """ paints all the given images at once to the main image and draws them to the screen """
        for image, position in imageList:
            self.mainImage.paste(image, position)
        self.draw_partial(self.mainImage, 0, 32)

    def start(self):
        #self.draw_background()
        scrollInfo = self.list_visual.get_scroll_info()
        self.update_view(volume = self.settings["volume"])

    def update_view(self, volume=None, newList=None):
        imageList = []
        if volume:
            imageList.extend(self.update_volume_view(volume))

        imageList.extend(self.update_list(newList))

        self.paint(imageList)

    def update_volume_view(self, volume):
        return [    (self.volume_view.get_image(volume), self.volume_view.position)     ]

    def update_list(self, newList=None):
        if newList:
             self.list_visual.change_list(newList)

        scrollInfo = self.list_visual.get_scroll_info()

        vl, ch = self.list_visual.visibleList, self.list_visual.highlited
        print(vl, ch, scrollInfo)
        imageList = [
                        (self.main_window.get_image(vl, ch), self.main_window.position),
                        (self.scroll_bar.get_image(scrollInfo), self.scroll_bar.position),
                        (self.page_counter.get_image(scrollInfo), self.page_counter.position),
                        (self.list_title.get_image(self.list_visual.listName), self.list_title.position)
                    ]
        return imageList
