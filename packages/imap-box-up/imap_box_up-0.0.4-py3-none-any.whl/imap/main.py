# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2024 porter.pan <porter.pan@outlook.com>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import logging
import sys
from pathlib import Path

import imap.global_var as global_var

from imap.lib.draw import add_editor, show_map
from imap.lib.convertor import Opendrive2Apollo


def convert_map_format(input_path, output_path, relative, junctionbox=False):
    opendrive2apollo = Opendrive2Apollo(input_path, output_path)
    # todo(zero): only lane type is driving add relationship!!!
    opendrive2apollo.set_parameters(only_driving=False)
    opendrive2apollo.convert(relative, junctionbox)
    opendrive2apollo.save_map()


def show_open_drive_map(map_file):
    opendrive2apollo = Opendrive2Apollo(map_file)
    opendrive2apollo.set_parameters(only_driving=False)
    opendrive2apollo.convert()


def main(args=sys.argv):
    parser = argparse.ArgumentParser(
        description="Imap is a tool to display hdmap info on a map.",
        prog="imap_box_up",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='eg:\n \
    1.show appollo map by id: imap_box_up -m data/borregas_ave.txt -l lane_35 \n \
    2.Format conversion with UTM map(opendrive->appollo): imap_box_up -f -i data/town.xodr -o data/apollo_map.txt \n \
    3.Format conversion with relative map(opendrive->appollo.relative map, recommend): imap_box_up -f -r -i data/town.xodr -o data/apollo_map.txt \n \
    4.if you want convert map junction with box(not recommend): imap_box_up -f -r -b -i data/town.xodr -o data/apollo_map.txt \n \
    Notice:\n \
    1.After running the command imap -m data/your_map_file, nothing display and no errors!!! \n \
        step1:Check the permissions: sudo chmod 777 data/your_map_file \n \
    if step1 no solve the problem, you can try sudo pip install xxx again. \n \
    2.Other Problem you can contact porter.pan@outlook.com \n \
    3.code modified from: https://github.com/daohu527/imap '
        )

    parser.add_argument(
        "-m", "--map", action="store", type=str, required=False,
        help="Specify the map(appollo hdmap) file in txt or binary format, to show")
    parser.add_argument(
        "--save_fig", action="store", type=bool, required=False,
        default=False, help="Whether to save the visualization figure (only for .xodr suffix)")
    parser.add_argument(
        "-z", "--enable_z_axis", action="store", type=bool, required=False,
        default=False, help="Whether to extract z-axis coordination information to apollo hd-map")
    parser.add_argument(
        "-l", "--lane", action="store", type=str, required=False,
        help="Find lane by lane id")

    parser.add_argument(
        "-f", "--format", action="store", type=str, required=False,
        nargs='?', const="0", help="Convert opendrive hdmap to appollo format")
    parser.add_argument(
        "-i", "--input", action="store", type=str, required=False,
        help="opendrive hdmap input path")
    parser.add_argument(
        "-o", "--output", action="store", type=str, required=False,
        help="for save appollo hdmap file output path")
    parser.add_argument(
        "-s", "--sampling", action="store", type=float, required=False,
        default=1.0, help="sampling length")
    parser.add_argument(
        "-d", "--debug", action="store", type=bool, required=False,
        nargs='?', const=True, default=False, help="debug mode")
    parser.add_argument(
        "-r", "--relative", action="store", type=bool, required=False,
        nargs='?', const=True, default=False, help="convert opendrive map to appollo map without GIS projection")
    parser.add_argument(
        "-b", "--box", action="store", type=bool, required=False,
        nargs='?', const=True, default=False, help="convert opendrive map to appollo map junction with box(not recommend)")
    args = parser.parse_args(args[1:])

    # 1. Init global var
    global_var._init()
    global_var.set_element_vaule("sampling_length", args.sampling)
    global_var.set_element_vaule("debug_mode", args.debug)
    global_var.set_element_vaule("enable_z_axis", args.enable_z_axis)

    # 2. show map
    if args.map is not None:
        map_file = Path(args.map)
        if not map_file.is_file():
            logging.error("File not exist! '{}'".format(args.map))
            return
        suffix = args.map.split(".")[1]
        if suffix == "bin" or suffix == "txt":
            add_editor()
            show_map(args.map, args.lane)
        elif suffix == "xodr":
            global_var.set_element_vaule("need_save_figure", args.save_fig)
            show_open_drive_map(args.map)
        else:
            pass

    # 3. convert opendrive map to apollo
    if args.format is not None:
        map_file = Path(args.input)
        if not map_file.is_file():
            logging.error("File not exist! '{}'".format(args.input))
            return
        convert_map_format(args.input, args.output, args.relative, args.box)

if __name__ == '__main__':
  main(args=sys.argv)