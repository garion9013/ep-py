#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class AbstractPlotter(object):
    def __init__(self, **kwargs):
        self.fig, self.ax = plt.subplots()
        if "ylabel" in kwargs:
            self.ax.set_ylabel(kwargs["ylabel"])
        if "xlabel" in kwargs:
            self.ax.set_xlabel(kwargs["xlabel"])
        if "title" in kwargs:
            self.ax.set_title(kwargs["title"])

        if ("width" in kwargs) & ("height" in kwargs):
            self.fig.set_size_inches(kwargs["width"], kwargs["height"])

        self.manualLegendStyle=False
        self.ax.autoscale(enable=True, axis='y', tight=False)
        self.ax.autoscale(enable=True, axis='x', tight=False)

    def setLegendStyle(self, **kwargs):
        self.manualLegendStyle=True
        if "ncol" in kwargs:
            self.ncol = kwargs["ncol"]
        if "size" in kwargs:
            self.legsize = kwargs["size"]
        if "frame" in kwargs:
            self.frame = kwargs["frame"]

    def drawLegend(self, this, target, legend):
        if self.manualLegendStyle is True:
            leg = this.ax.legend(target, legend, loc="upper center", 
                                 ncol=this.ncol, prop={'size':this.legsize})
            leg.draw_frame(this.frame)
        else:
            this.ax.legend(target, legend)

    def setLimitOn(self, **kwargs):
        # set y-space
        if "y" in kwargs:
            plt.ylim(kwargs["y"])

        # set x-space
        if "x" in kwargs:
            plt.xlim(kwargs["x"])

    def saveToPdf(self, output):
        pp = PdfPages(output)
        plt.savefig(pp, format='pdf')
        pp.close()
        plt.close()

    def showToWindow(self):
        plt.show()
        plt.close()

class tickLabelInit:
    """Initializer of tickLabel class"""
    def __init__(self):
        self.content = [""]

# Back-end plotter
class LinePlotter(AbstractPlotter):
    """Draw line graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)
        self.ax.grid()

    def draw(self, *argv):
        keyLen = len(argv)
        pc = range(keyLen)

        legend = []
        for i in range(keyLen):
            pc[i], = self.ax.plot(argv[i].X, argv[i].Y, linewidth=1, marker=argv[i].marker, color=argv[i].color)
            legend.append(argv[i].legend)

        self.drawLegend(self, pc, legend);

class CBarPlotter(AbstractPlotter):
    """Draw clustered bar graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)

        self.barwidth = 1
        self.tickLabel = [""]
        self.tickAngle = 0

        if "barwidth" in kwargs:
            self.barwidth = kwargs["barwidth"]

    def draw(self, *argv, **kwargs):
        # default 12% margin to entire bar width
        FigSideMargin = 0.12 

        if "figmargin" in kwargs:
            FigSideMargin = kwargs["figmargin"]
        if "ticklabel" in kwargs:
            self.tickLabel = kwargs["ticklabel"]
        if "tickangle" in kwargs:
            self.tickAngle = kwargs["tickangle"]

        keyLen = len(argv)
        datLen = len(argv[0].Y)

        # Interval between clustered bars: 40% of total width in a clustered group
        interClusterOffset = (self.barwidth*keyLen) * 1.4
        base = np.arange(datLen) * interClusterOffset

        legend = []
        rects = []
        for i in range(keyLen):
            rects.append(self.ax.bar(base+i*self.barwidth, argv[i].Y, self.barwidth, color=argv[i].color, hatch=argv[i].hatch))
            if bool(argv[i].legend):
                legend.append(argv[i].legend)

        # set legend
        self.drawLegend(self, rects, legend);

        # set xtick point and label
        self.ax.set_xticks(base+(self.barwidth*keyLen)/2)
        self.ax.set_xticklabels(self.tickLabel.content, rotation=self.tickAngle)


        LengthOfWholeBar = base[-1] + self.barwidth*keyLen
        plt.xlim([-LengthOfWholeBar*FigSideMargin, LengthOfWholeBar*(1+FigSideMargin)])


class CCBarPlotter(AbstractPlotter):
    """Draw clustered*2 bar graph with grouped parsed data"""
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)

        self.barwidth = 1
        self.tickLabel = [""]
        self.tickAngle = 0

        if "barwidth" in kwargs:
            self.barwidth = kwargs["barwidth"]

    def draw(self, *argv, **kwargs):
        # default 12% margin to entire bar width
        FigSideMargin = 0.12 

        if "figmargin" in kwargs:
            FigSideMargin = kwargs["figmargin"]
        if "groupmargin" in kwargs:
            BtwGroupMargin = kwargs["groupmargin"]
        if "ticklabel" in kwargs:
            # merge multiple label list
            temp = []
            for i in kwargs["ticklabel"]:
                temp += i.content
            self.tickLabel = temp
        if "tickangle" in kwargs:
            self.tickAngle = kwargs["tickangle"]

        legend = []
        rects = []
        base = []
        globalBase = np.array([])

        # set margin proportional to the first data
        keyLen = argv[0].length
        datLen = len(argv[0].content[0].Y)

        # Interval between clustered bars: 40% of total width in a clustered group
        interClusterOffset = (self.barwidth * keyLen) * 1.4
        # Interval between clustered group: 
        interGlobalOffset = interClusterOffset * datLen * BtwGroupMargin

        for k, eachGroup in enumerate(argv):
            keyLen = eachGroup.length
            datLen = len(eachGroup.content[0].Y)
            # base calcuation (x position of bar with array)
            base.append(np.arange(datLen) * interClusterOffset + interGlobalOffset * k)

            # Update global accumulative variables
            globalBase = np.concatenate((globalBase, base[k] + (self.barwidth*keyLen)/2)) 

            for i, elem in enumerate(eachGroup.content):
                rects.append(self.ax.bar(base[k]+i*self.barwidth, elem.Y, self.barwidth,
                                         color=elem.color, hatch=elem.hatch))
                if bool(elem.legend):
                    legend.append(elem.legend)

        # set legend
        self.drawLegend(self, rects, legend);

        # set xtick point and label
        self.ax.set_xticks(globalBase)
        self.ax.set_xticklabels(self.tickLabel, rotation=self.tickAngle)

        LengthOfWholeBar = base[-1][-1] + self.barwidth*keyLen
        plt.xlim([-LengthOfWholeBar*FigSideMargin, LengthOfWholeBar*(1+FigSideMargin)])

class BoxPlotter(AbstractPlotter):
    """Draw clustered bar graph with grouped data or column-parsed data"""
    def __init__(self, **kwargs):
        AbstractPlotter.__init__(self, **kwargs)

        # Default properties
        self.boxwidth = 1
        self.vertical = True
        self.timeline = False
        self.tickLabel = tickLabelInit()
        self.tickAngle = 0

        if "boxwidth" in kwargs:
            self.boxwidth = float(kwargs["boxwidth"])
        if "vertical" in kwargs:
            self.vertical = kwargs["vertical"]
        if "timeline" in kwargs:
            self.timeline = kwargs["timeline"]

    def draw(self, *argv, **kwargs):
        # default 12% margin to entire box width
        FigSideMargin = 0.12 

        if "figmargin" in kwargs:
            FigSideMargin = kwargs["figmargin"]
        if "groupmargin" in kwargs:
            BtwGroupMargin = kwargs["groupmargin"]
        if "ticklabel" in kwargs:
            self.tickLabel = kwargs["ticklabel"]
        if "tickangle" in kwargs:
            self.tickAngle = kwargs["tickangle"]

        keyLen = len(argv)

        if self.timeline is True:
            base = np.linspace(0, 0, keyLen)
        else:
            base = np.linspace(0, self.boxwidth*(keyLen+2), keyLen)

        legend = []
        rects = []
        for i in range(keyLen):
            datLen = len(argv[i].X)
            for j in range(datLen):
                if self.vertical is True:
                    rect = plt.Rectangle([base[i], argv[i].X[j]], self.boxwidth, argv[i].Y[j] - argv[i].X[j],
                                         facecolor=argv[i].color, hatch=argv[i].hatch)
                else:
                    rect = plt.Rectangle([argv[i].X[j], base[i]], argv[i].Y[j] - argv[i].X[j], self.boxwidth,
                                         facecolor=argv[i].color, hatch=argv[i].hatch)
                self.ax.add_patch(rect)
            if bool(argv[i].legend):
                rects.append(rect)
                legend.append(argv[i].legend)

        # set legend
        self.drawLegend(self, rects, legend);

        # set xtick point and label
        if self.vertical is True:
            self.ax.set_xticks(base + self.boxwidth/2)
            self.ax.set_xticklabels(self.tickLabel.content, rotation=self.tickAngle)
        else:
            self.ax.set_yticks(base + self.boxwidth/2)
            self.ax.set_yticklabels(self.tickLabel.content, rotation=self.tickAngle)

        # set x / y-range
        if self.vertical is True:
            self.ax.autoscale(enable=True, axis='y', tight=False)
            LengthOfWholeBar = base[-1] + self.boxwidth
            plt.xlim([-LengthOfWholeBar*FigSideMargin, LengthOfWholeBar*(1+FigSideMargin)])
        else:
            self.ax.autoscale(enable=True, axis='x', tight=False)
            LengthOfWholeBar = base[-1] + self.boxwidth
            plt.ylim([-LengthOfWholeBar*FigSideMargin, LengthOfWholeBar*(1+FigSideMargin)])
