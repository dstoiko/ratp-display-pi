from datetime import timedelta, datetime

from luma.core.interface.serial import spi
from luma.oled.device import ssd1322
from luma.core.sprite_system import framerate_regulator
from luma.core.render import canvas
from luma.core.virtual import viewport, snapshot

from utils import makeFonts


class Display:
    def __init__(self, color):
        self._serial = spi()
        self._device = ssd1322(self._serial, mode="1", rotate=2)
        self._fonts = makeFonts()
        self._color = color
        self._WIDTH = 256
        self._HEIGHT = 64
        self._STATUS_APPROACHING = "Train a l'approche"
        self._STATUS_DELAYED = "Train retarde"
        self.regulator = framerate_regulator(fps=10)

    def _renderDestination(self, departure, font):
        def drawText(draw, width, height):
            draw.text(
                (0, 0), text=departure["destination"], font=font, fill=self._color)

        return drawText

    def _renderServiceStatus(self, departure, font):
        status = departure["message"]
        if status == self._STATUS_APPROACHING:
            status = "00 mn"
        elif status == self._STATUS_DELAYED:
            status = "++    "

        def drawText(draw, width, height):
            w, h = draw.textsize(status, font)
            draw.text((width-w, 0), text=status, font=font, fill=self._color)
        return drawText

    def _renderTime(self, draw, width, height):
        rawTime = datetime.now().time()
        hour, minute, second = str(rawTime).split('.')[0].split(':')

        w1, h1 = draw.textsize("{}:{}".format(
            hour, minute), self._fonts["fontBoldLarge"])
        w2, h2 = draw.textsize(":00", self._fonts["fontBoldTall"])

        draw.text(((width - w1 - w2) / 2, 0), text="{}:{}".format(hour, minute),
                  font=self._fonts["fontBoldLarge"], fill=self._color)
        draw.text((((width - w1 - w2) / 2) + w1, 5), text=":{}".format(second),
                  font=self._fonts["fontBoldTall"], fill=self._color)

    def _renderWelcomeTo(self, xOffset):
        def drawText(draw, width, height):
            text = "Bienvenue à"
            draw.text((int(xOffset), 0), text=text,
                      font=self._fonts["fontBold"], fill=self._color)

        return drawText

    def _renderDepartureStation(self, departureStation, xOffset):
        def draw(draw, width, height):
            text = departureStation
            draw.text((int(xOffset), 0), text=text,
                      font=self._fonts["fontBold"], fill=self._color)

        return draw

    def _renderDots(self, draw, width, height):
        text = ".  .  ."
        draw.text((0, 0), text=text,
                  font=self._fonts['fontBold'], fill=self._color)

    def drawBlankSignage(self, departureStation):
        with canvas(self._device) as draw:
            welcomeSize = draw.textsize("Welcome to", self._fonts["fontBold"])

        with canvas(self._device) as draw:
            stationSize = draw.textsize(
                departureStation, self._fonts["fontBold"])

        self._device.clear()

        virtualViewport = viewport(
            self._device, width=self._WIDTH, height=self._HEIGHT)

        width = virtualViewport.width
        rowOne = snapshot(width, 10, self._renderWelcomeTo(
            (width - welcomeSize[0]) / 2), interval=10)
        rowTwo = snapshot(width, 10, self._renderDepartureStation(
            departureStation, (width - stationSize[0]) / 2), interval=10)
        rowThree = snapshot(width, 10, self._renderDots, interval=10)
        rowTime = snapshot(width, 14, self._renderTime, interval=1)

        if len(virtualViewport._hotspots) > 0:
            for hotspot, xy in virtualViewport._hotspots:
                virtualViewport.remove_hotspot(hotspot, xy)

        virtualViewport.add_hotspot(rowOne, (0, 0))
        virtualViewport.add_hotspot(rowTwo, (0, 12))
        virtualViewport.add_hotspot(rowThree, (0, 24))
        virtualViewport.add_hotspot(rowTime, (0, 50))

        return virtualViewport

    def drawSignage(self, departures):
        self._device.clear()

        virtualViewport = viewport(
            self._device, width=self._WIDTH, height=self._HEIGHT)

        maxWidthStatus = self._STATUS_DELAYED
        width = virtualViewport.width

        # Maximum text size
        with canvas(self._device) as draw:
            w, h = draw.textsize(maxWidthStatus, self._fonts["fontBold"])

        maxD = len(departures)
        r, c = 2, maxD
        rows = [[0 for x in range(r)] for y in range(c)]
        for i in range(maxD):
            dw = (width - w - 5) if i == 0 else (width - w)
            f = self._fonts["fontBold"] if i == 0 else self._fonts["font"]
            rows[i][0] = snapshot(dw, 10, self._renderDestination(
                departures[i], f), interval=10)
            rows[i][1] = snapshot(
                w, 10, self._renderServiceStatus(departures[i], f), interval=1)

        rowTime = snapshot(width, 14, self._renderTime, interval=0.1)

        if len(virtualViewport._hotspots) > 0:
            for hotspot, xy in virtualViewport._hotspots:
                virtualViewport.remove_hotspot(hotspot, xy)

        for i in range(maxD):
            virtualViewport.add_hotspot(rows[i][0], (0, i * 12))
            virtualViewport.add_hotspot(rows[i][1], (width - w, i * 12))

        virtualViewport.add_hotspot(rowTime, (0, 50))

        return virtualViewport
