# SfMToolKit
Vision Based Creation of Realistic 3D Terrain Profiles

End of studies project by Raphaël Durand-Delacre

## Overview

This repository contains an application called SfMToolKit, which provides the following functionality:

- Reconstruct a mesh from images
- Segment and extract frames from videos
- Match 2 point clouds through ICP


## Installation Instructions

This repository relies on several extrenal tools, and has been tested on Ubuntu 18.04.

- OpenMVG
- OpenMVS
- LibPointMatcher
- ExifTool
- FFmpeg

You need to install of these dependences prior to SfMToolKit.

Here are links to these libraries:
https://github.com/openMVG/openMVG
https://github.com/cdcseacave/openMVS
https://github.com/ethz-asl/libpointmatcher
https://www.sno.phy.queensu.ca/~phil/exiftool/
https://www.ffmpeg.org/

SfMToolKit contains a single module (the ICP) that requires its own installation. It can be installed through Cmake.

## Getting started

Each module can be run independently through a python script or a console command (for the ICP). A GUI that controls it all is found in the __main__ file. 

## Data Sets

Data sets can be found online, and generated with youtube videos. Some useful datasets can be found following these links.
https://www.sensefly.com/education/datasets/
https://dronemapper.com/sample_data/
