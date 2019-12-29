import math
from datetime import timedelta, datetime

from luma.core.interface.serial import spi
from luma.oled.device import ssd1322
from luma.core.sprite_system import framerate_regulator
from luma.core.render import canvas
from luma.core.virtual import viewport, snapshot

from utils import makeFonts


class Display:
    def __init__(self):
        self._serial = spi()
        self._device = ssd1322(self._serial, mode="1", rotate=2)
        self._fonts = makeFonts()
        self._color = "yellow"  # hardcoded color as it's useless on monochrome screen
        self._WIDTH = 256
        self._HEIGHT = 64
        self._STATUS_APPROACHING = "Train a l'approche"
        self._STATUS_DELAYED = "Train retarde"
        self._STATUS_TERMINATED = "Service termine"
        self._STATUS_PP = "++   "
        self._STATUS_MM = "00 mn"
        self._STATUS_NODATA = "Pas de train a"
        self.regulator = framerate_regulator(fps=10)

    def _renderDestination(self, departure, font):
        def drawText(draw, width, height):
            draw.text(
                (0, 0), text=departure["destination"], font=font, fill=self._color)

        return drawText

    def _renderServiceStatus(self, departure, font):
        status = departure["message"]
        if status == self._STATUS_APPROACHING:
            status = self._STATUS_MM
        elif status in [self._STATUS_DELAYED, self._STATUS_TERMINATED]:
            status = self._STATUS_PP

        def drawText(draw, width, height):
            w, h = draw.textsize(status, font)
            draw.text((width-w, 0), text=status, font=font, fill=self._color)
        return drawText

    def _renderTime(self, draw, width, height):
        rawTime = datetime.now().time()
        hour, minute, second = str(rawTime).split(".")[0].split(":")

        w1, h1 = draw.textsize("{}:{}".format(
            hour, minute), self._fonts["fontBoldLarge"])
        w2, h2 = draw.textsize(":00", self._fonts["fontBoldTall"])

        draw.text(((width - w1 - w2) / 2, 0), text="{}:{}".format(hour, minute),
                  font=self._fonts["fontBoldLarge"], fill=self._color)
        draw.text((((width - w1 - w2) / 2) + w1, 5), text=":{}".format(second),
                  font=self._fonts["fontBoldTall"], fill=self._color)

    def _renderNoDataText(self, xOffset):
        def drawText(draw, width, height):
            draw.text((int(xOffset), 0), text=self._STATUS_NODATA,
                      font=self._fonts["font"], fill=self._color)

        return drawText

    def _renderDepartureStation(self, departureStation, xOffset):
        def drawText(draw, width, height):
            draw.text((int(xOffset), 0), text=departureStation,
                      font=self._fonts["fontBold"], fill=self._color)
        return drawText

    def drawBlankSignage(self, station):
        lineText = "Metro {}".format(station["line"])
        # Maximum text sizes
        with canvas(self._device) as draw:
            welcomeSize = draw.textsize(
                self._STATUS_NODATA, self._fonts["font"])
            stationSize = draw.textsize(
                station["name"], self._fonts["fontBold"])
            lineSize = draw.textsize(
                lineText, self._fonts["fontBold"])

        self._device.clear()
        virtualViewport = viewport(
            self._device, width=self._WIDTH, height=self._HEIGHT)

        width = virtualViewport.width
        rowOne = snapshot(width, 10, self._renderNoDataText(
            (width - welcomeSize[0]) / 2), interval=10)
        rowTwo = snapshot(width, 10, self._renderDepartureStation(
            station["name"], (width - stationSize[0]) / 2), interval=10)
        rowThree = snapshot(width, 10, self._renderDepartureStation(
            lineText, (width - lineSize[0]) / 2), interval=10)
        rowTime = snapshot(width, 14, self._renderTime, interval=1)

        if len(virtualViewport._hotspots) > 0:
            for hotspot, xy in virtualViewport._hotspots:
                virtualViewport.remove_hotspot(hotspot, xy)

        virtualViewport.add_hotspot(rowOne, (0, 0))
        virtualViewport.add_hotspot(rowTwo, (0, 12))
        virtualViewport.add_hotspot(rowThree, (0, 24))
        virtualViewport.add_hotspot(rowTime, (0, 50))

        return virtualViewport

    def drawSignage(self, station, departures):
        self._device.clear()
        virtualViewport = viewport(
            self._device, width=self._WIDTH, height=self._HEIGHT)

        maxWidthStatus = self._STATUS_DELAYED
        width = virtualViewport.width

        # Maximum text size
        with canvas(self._device) as draw:
            w, h = draw.textsize(maxWidthStatus, self._fonts["fontBold"])

        stationText = "{} ({})".format(station["name"], station["line"])
        rowStation = snapshot(
            width, 10, self._renderDepartureStation(stationText, 0), interval=10)

        maxD = min([len(departures), 3])
        c, r = 2, maxD
        rows = [[0 for x in range(c)] for y in range(r)]
        for i in range(maxD):
            f = self._fonts["font"]
            rows[i][0] = snapshot(width - w, 10, self._renderDestination(
                departures[i], f), interval=10)
            rows[i][1] = snapshot(
                w, 10, self._renderServiceStatus(departures[i], f), interval=1)

        rowTime = snapshot(width, 14, self._renderTime, interval=0.1)

        if len(virtualViewport._hotspots) > 0:
            for hotspot, xy in virtualViewport._hotspots:
                virtualViewport.remove_hotspot(hotspot, xy)

        virtualViewport.add_hotspot(rowStation, (0, 0))

        for i in range(maxD):
            virtualViewport.add_hotspot(rows[i][0], (0, (i + 1) * 12))
            virtualViewport.add_hotspot(rows[i][1], (width - w, (i + 1) * 12))

        virtualViewport.add_hotspot(rowTime, (0, 50))

        return virtualViewport
