#!/usr/bin/python

# import sys
# sys.dont_write_bytecode = True;

# library for ep.py
import epic as ep

args = ep.parseCommandArgs() 

# color macro dictionary
mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292",
      "blue":"#4455D2",
      "white":"#FFFFFF", "dwhite":"#DFDFDF", "ddwhite":"#B3B3B3",
      "gray":"#888888", "wgray":"#CECECE", "dgray":"#909090", "ddgray":"#5F5F5F",
      "black":"#000000"}

# output file name
output = "cbar.pdf"
if bool(args.outFile) == True:
    output = args.outFile

if bool(args.inFile) == True:
    text = ep.tRead(args.inFile)

if bool(args.style) == True:
    style = args.style


# Clustered bar graph =======================================================================
# ===========================================================================================

# Parse ======================================================================

# Polybench
PP = ep.PatternParser(ep.tRead("../dat/cbar-line/poly.dat"))
PP.PickKeyWith("row")
PP.ParseWith("\t")
PP.datNormTo("col1", "col2", select="min")

PD = []
PD.append(ep.Group(PP, "col1", color=mc["white"], hatch=""))
PD.append(ep.Group(PP, "col2", color=mc["ddwhite"], hatch=""))
PD.append(ep.Group(PP, "col3", color=mc["black"], hatch=""))

PD[0].setLegend("FluidiCL")
PD[1].setLegend("Boyer et al.")
PD[2].setLegend("jAWS")

# WebCL
PP = ep.PatternParser(ep.tRead("../dat/cbar-line/webcl.dat"))
PP.PickKeyWith("row")
PP.ParseWith("\t")
PP.datNormTo("col1", "col2", select="min")

WD = []
WD.append(ep.Group(PP, "col1", color=mc["white"], hatch=""))
WD.append(ep.Group(PP, "col2", color=mc["ddwhite"], hatch=""))
WD.append(ep.Group(PP, "col3", color=mc["black"], hatch=""))

# Geomean
PP = ep.PatternParser(ep.tRead("../dat/cbar-line/geomean-best.dat"))
PP.PickKeyWith("row")
PP.ParseWith("\t")

GD = []
GD.append(ep.Group(PP, "col1", color=mc["white"], hatch=""))
GD.append(ep.Group(PP, "col2", color=mc["ddwhite"], hatch=""))
GD.append(ep.Group(PP, "col3", color=mc["black"], hatch=""))

# label lists
poly_list = ["ATAX", "BICG", "SYRK", "SYR2K", "GEMM", "2MM", "CORR"]
webcl_list = ["Mandelbrot", "Nbody", "Sobel-CorG", "Random"]
geo_list = ["geomean"]


# Draw ======================================================================

CB = ep.CBarPlotter(ylabel="Speedup over Best Device", ylpos=[-.035, 0.5],
                    width=30, height=6.8)

# Set Ticks
L1 = ep.TickLabel(None, poly_list + webcl_list + geo_list)
CB.setTicks(yspace=[0, 0.5, 1, 1.5], label=L1)
CB.annotate(["Polybench", "WebKit-WebCL"], [[27.5, -.30], [85, -.30]], fontsize=30)

# Figure style
CB.setLegendStyle(ncol=3, size=28, pos=[0.59, 1.18], frame=False)
CB.setFigureStyle(ylim=[0, 1.5], bottomMargin=0.18, fontsize=25,
                  interCmargin=.7, figmargin=0.02)

CB.draw(*PD, barwidth=2)
CB.setBaseOffset(14)
CB.draw(*WD, barwidth=2)
CB.setBaseOffset(14)
CB.draw(*GD, barwidth=2)

CB.saveToPdf(output)
