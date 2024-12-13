<h1 align="center">Beat Down: Fists of Vengeance Image Extractor</h1>

This is a tool I wrote to help me with analyzing the .XAF file. There are bugs here and there but I'll fix those later. **I have no experience with 3D or 3D modding so I'm learning as I go.**

<p align="center"><img src="images\extractor.jpg" alt="" /></p>

## Features

- Image Preview
- Texture Extractor
- Texture Patcher
- File Extractor
- File Patcher

## Textrure Replacement

Textures are located in the DATA.XAV file. Open it, pick a texture, click "Export .PNG", edit it and click "Patch Image". Then use Apache to patch the ISO. Here's the result:

<p align="center"><img src="images\Beat Down - Fists of Vengeance_SLUS-21150_20241213104844.png" alt="" /></p>

Make sure the edited texture has no more than 256 colors.

## Export Section

This will export the raw file. For some characters, their textures are inside a .RWS container inside ARCHIVE.XAV. Model data are stored inside .RWS container.

## Editing Models

Currently working on this. Right now, I can make simple changes to the model. I need to create a .RWS editor for more complex modding.
<p align=center><img src=images\Fatima.jpg /></p>

## Todo

- Refactor the code
- Add viewer for .RWS files
- Add model extractor/importer