#!/usr/bin/env python3

import sys
import argparse
import json
import cv2

###############################################################################
# Function to parse json file and extract zipiline start & end coordinates 
#
def parseJsonFile(file_name):
    ret = []
    # load file contents to a json
    try:
        data = json.load(file_name)
    except:
        print("An exception occurred while reading source file.") 
    # ziplines are embedded json - getting the data
    try:
        zipiline_manager = json.loads(data['Data']['ZipLineManager'])
    except:
        print("An exception occurred while converting data to json.") 
    # extracting coordinates 
    for zipline in zipiline_manager['Ziplines']:
        ret.append([zipline['_anchorAPosition']['x'], zipline['_anchorAPosition']['z'], zipline['_anchorBPosition']['x'], zipline['_anchorBPosition']['z']])
    return(ret)

###############################################################################
# Function to load clean map and plot lines
#
def createMap(ziplines):
    # X pixel to coordinates ratio
    pixel_index=3.15
    # Y pixel to coordinates ratio
    pixel_index_y=3.05
    # Center of the map coordinates (0,0 in forest map)
    map_center_x=1006
    map_center_y=658

    # load clean image
    clean_map = cv2.imread("img/sotf-clean.png")
    
    for zipline_points in ziplines:
        #get line start and end coordinets - shift by the center of the map and divide by pixel to coordinates ratio
        line_a_x= round(map_center_x+zipline_points[0]/pixel_index)
        line_a_y= round(map_center_y-zipline_points[1]/pixel_index_y)
        line_b_x= round(map_center_x+zipline_points[2]/pixel_index)
        line_b_y= round(map_center_y-zipline_points[3]/pixel_index_y)
        # append line to the map
        cv2.line(clean_map, (line_a_x,line_a_y), (line_b_x,line_b_y), (255,0,0), 4)
        cv2.circle(clean_map, (line_a_x,line_a_y), 4, (255,0,0), 2)
        cv2.circle(clean_map, (line_b_x,line_b_y), 4, (255,0,0), 2)

    return(clean_map)

###############################################################################
# script entrypoint
#
def main():
    # arguments parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input", nargs="?", default="-",
        metavar="INPUT_FILE", type=argparse.FileType("r"),
        help="path to the input file (ZipLineManagerSaveData.json)")

    parser.add_argument(
        "output", nargs="?", default="-",
        metavar="OUTPUT_FILE", type=argparse.FileType("w"),
        help="path to the output file (zipline_map.png)")
    if len(sys.argv) < 3:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    zipline_points = parseJsonFile(args.input)
    final_map = createMap(zipline_points)
    cv2.imwrite(args.output.name, final_map)

if __name__ == "__main__":
    main()
