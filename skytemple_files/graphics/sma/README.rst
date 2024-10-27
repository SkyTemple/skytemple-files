SMA File Format
===============
manpu_su.sma and manpu_ma.sma are both found in the /SYSTEM/ folder.  manpu_su.sma contains status effect icon data and has the format detailed in this file.  manpu_ma.sma contains no image data and its structure/use is currently unknown.


The file uses SIR0 headers to store its pointers.  General SIR0 details can be found in the main SIR0 documentation.  The sections below will cover only manpu_su.sma-specific blocks of data.

Name 	Offset 	Size (Per Element) 	# of Elements 	Description
SIR0 Header 	0x00 	16 Bytes 	1 	Details in the SIR0 documentation
Animation Data 	Pointed by Content Header 	12 	Specified by Content Header 	Each element contains animation data of a status icon, including size and number of frames.
Image Data 	Pointed by Content Header 	Varies 	1 	One continuous block of image data that is read nibble-by-nibble.
Palette Data 	Pointed by Content Header 	64 Bytes 	16 	A block of palette data that is separated into 16 palettes, each with 16 colors of 4 bytes each.
Content Header 	Pointed by SIR0 Header 	32 Bytes 	1 	Contains the pointers to Animation Data, Image Data, Palette Data, and the number of animations.
Pointer Offsets List 	Pointed by SIR0 Header 	1 Byte 	Varies 	Details in the SIR0 documentation
SIR0 Padding 	After Pointer Offsets List 	Varies 	--- 	Details in the SIR0 documentation


Content Header
###

The 32-byte header appears to be split into 8 sections, each with 4 bytes:

1. Unknown
2. Pointer to start of Animation Data
3. Number of animations
4. Pointer to image data
5. Unknown
6. Pointer to palette data
7. Unknown
8. Unknown

Animation Data
###

This block contains an array of elements, each 12 bytes and representing an animation.  Contains 7 elements:

AA BB CC CC DD DD 00 00 EE EE FF FF

A: Width of all frames in this animation, in blocks (8 pixels)
B: Height of all frames in this animation, in blocks (8 pixels)
C: Unknown
D: The offset, in bytes, from which to start reading from the image data.
E. The number of frames in this animation.
F. Unknown.  Possibly a mapping table for the destination of where to load in memory?

A fully zeroed out animation exists as the first element.

+---------+---------------------------------------+
| Name    | Offset                                |
+=========+=======================================+
| 0b00    | Wall tile                             |
+---------+---------------------------------------+
| 0b01    | Water / lava / chasm tile             |
+---------+---------------------------------------+
| 0b10    | Ground / floor tile                   |
+---------+---------------------------------------+
| 0b11    | Extra / special tile (see below)      |
+---------+---------------------------------------+

