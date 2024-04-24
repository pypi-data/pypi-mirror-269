# -*- coding: utf-8 -*-
# Copyright (c) 2021-2024 Salvador E. Tropea
# Copyright (c) 2021-2024 Instituto Nacional de Tecnología Industrial
# Copyright (c) 2018-2024 @whitequark
# License: AGPL-3.0
# Project: KiBot (formerly KiPlot)
# Adapted from: https://github.com/whitequark/kicad-boardview
import re
from pcbnew import SHAPE_POLY_SET
from .gs import GS
from .out_base import VariantOptions
from .macros import macros, document, output_class  # noqa: F401
from . import log

logger = log.get_logger()


def skip_module(module, tp=False):
    if module.GetPadCount() == 0:
        return True
    refdes = module.Reference().GetText()
    if tp and not refdes.startswith("TP"):
        return True
    if not tp and refdes.startswith("TP"):
        return True
    return False


def coord(nanometers):
    milliinches = nanometers * 5 // 127000
    return milliinches


def y_coord(maxy, y, flipped):
    # Adjust y-coordinate to start from the bottom of the board and account for flipped components
    return coord(maxy - y) if not flipped else coord(y)


def natural_sort_key(s):
    is_blank = s.strip() == ''
    return (is_blank, [int(text) if text.isdigit() else text.casefold()
                       for text in re.compile('([0-9]+)').split(s)])


def convert(pcb, brd):
    # Board outline
    outlines = SHAPE_POLY_SET()
    if GS.ki5:
        pcb.GetBoardPolygonOutlines(outlines, "")
        outline = outlines.Outline(0)
        outline_points = [outline.Point(n) for n in range(outline.PointCount())]
    else:
        pcb.GetBoardPolygonOutlines(outlines)
        outline = outlines.Outline(0)
        outline_points = [outline.GetPoint(n) for n in range(outline.GetPointCount())]
    outline_maxx = max((p.x for p in outline_points))
    outline_maxy = max((p.y for p in outline_points))

    brd.write("0\n")  # unknown

    brd.write("BRDOUT: {count} {width} {height}\n"
              .format(count=len(outline_points) + outline.IsClosed(),
                      width=coord(outline_maxx),
                      height=coord(outline_maxy)))
    for point in outline_points:
        brd.write("{x} {y}\n"
                  .format(x=coord(point.x),
                          y=y_coord(outline_maxy, point.y, False)))
    if outline.IsClosed():
        brd.write("{x} {y}\n"
                  .format(x=coord(outline_points[0].x),
                          y=y_coord(outline_maxy, outline_points[0].y, False)))
    brd.write("\n")

    # Nets
    net_info = pcb.GetNetInfo()
    net_items = [net_info.GetNetItem(n) for n in range(1, net_info.GetNetCount())]

    brd.write("NETS: {count}\n"
              .format(count=len(net_items)))
    for net_item in net_items:
        code = net_item.GetNet() if GS.ki5 else net_item.GetNetCode()
        brd.write("{code} {name}\n"
                  .format(code=code,
                          name=net_item.GetNetname().replace(" ", u"\u00A0")))
    brd.write("\n")

    # Parts
    module_list = GS.get_modules()
    modules = []
    for m in sorted(module_list, key=lambda mod: mod.GetReference()):
        if not skip_module(m):
            modules.append(m)

    brd.write("PARTS: {count}\n".format(count=len(modules)))
    pin_at = 0
    for module in modules:
        module_bbox = module.GetBoundingBox()
        flipped = module.IsFlipped()
        brd.write("{ref} {x1} {y1} {x2} {y2} {pin} {side}\n"
                  .format(ref=module.GetReference(),
                          x1=coord(module_bbox.GetLeft()),
                          y1=y_coord(outline_maxy, module_bbox.GetTop(), flipped),
                          x2=coord(module_bbox.GetRight()),
                          y2=y_coord(outline_maxy, module_bbox.GetBottom(), flipped),
                          pin=pin_at,
                          side=1 + flipped))
        pin_at += module.GetPadCount()
    brd.write("\n")

    # Pins
    pads = []
    for m in modules:
        pads_list = m.Pads()
        for pad in sorted(pads_list, key=lambda pad: natural_sort_key(pad.GetName())):
            pads.append(pad)

    brd.write("PINS: {count}\n".format(count=len(pads)))
    for pad in pads:
        pad_pos = pad.GetPosition()
        flipped = pad.IsFlipped()
        brd.write("{x} {y} {net} {side}\n"
                  .format(x=coord(pad_pos.x),
                          y=y_coord(outline_maxy, pad_pos.y, flipped),
                          net=pad.GetNetCode(),
                          side=1 + flipped))
    brd.write("\n")

    # Nails
    module_list = GS.get_modules()
    testpoints = []
    for m in sorted(module_list, key=lambda mod: mod.GetReference()):
        if not skip_module(m, tp=True):
            pads_list = m.Pads()
            for pad in sorted(pads_list, key=lambda pad: natural_sort_key(pad.GetName())):
                testpoints.append((m, pad))

    brd.write("NAILS: {count}\n".format(count=len(testpoints)))
    for module, pad in testpoints:
        pad_pos = pad.GetPosition()
        flipped = pad.IsFlipped()
        brd.write("{probe} {x} {y} {net} {side}\n"
                  .format(probe=module.GetReference()[2:],
                          x=coord(pad_pos.x),
                          y=y_coord(outline_maxy, pad_pos.y, flipped),
                          net=pad.GetNetCode(),
                          side=1 + flipped))
    brd.write("\n")


class BoardViewOptions(VariantOptions):
    def __init__(self):
        with document:
            self.output = GS.def_global_output
            """ *Filename for the output (%i=boardview, %x=brd) """
        super().__init__()
        self._expand_id = 'boardview'
        self._expand_ext = 'brd'
        self.help_only_sub_pcbs()

    def run(self, output):
        super().run(output)
        self.filter_pcb_components()
        with open(output, 'wt') as f:
            convert(GS.board, f)
        self.unfilter_pcb_components()

    def get_targets(self, out_dir):
        return [self._parent.expand_filename(out_dir, self.output)]


@output_class
class BoardView(BaseOutput):  # noqa: F821
    """ BoardView
        Exports the PCB in board view format.
        This format allows simple pads and connections navigation, mainly for circuit debug.
        The output can be loaded using Open Board View (https://openboardview.org/) """
    def __init__(self):
        super().__init__()
        self._category = ['PCB/repair', 'PCB/fabrication/assembly']
        with document:
            self.options = BoardViewOptions
            """ *[dict] Options for the `boardview` output """

    @staticmethod
    def get_conf_examples(name, layers):
        return BaseOutput.simple_conf_examples(name, 'Board View export', 'Assembly')  # noqa: F821
