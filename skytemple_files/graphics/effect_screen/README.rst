Screen Effect File Format
===============
The file ``/EFFECT/effect.bin`` contains vfx used for dungeon battle, weather effects, and some ground mode vfx.

The file contains 293 effect entries, most of which are WAN format.
Specifically the files effect0268-00289 are not WAN.
They are used for screen effects in moves and cutscenes.


The file uses SIR0 headers to store its pointers.  General SIR0 details can be found in the main SIR0 documentation.

+-----------------------+-----------------------------+---------------------+------------------------------+--------------------------------------------------------------------------------------------------+
| Name                  | Offset                      | Size (Per Element)  | # of Elements                | Description                                                                                      |
+=======================+=============================+=====================+==============================+==================================================================================================+
| SIR0 Header           | 0x00                        | 16 Bytes            | 1                            | Details in the SIR0 documentation                                                                |
+-----------------------+-----------------------------+---------------------+------------------------------+--------------------------------------------------------------------------------------------------+
| Animation Data        | Pointed by Animation Ptrs   | Varies              | Specified by Content Header  | A 36-byte header with draw parameters, plus a list of draw instructions to put textures onscreen |
+-----------------------+-----------------------------+---------------------+------------------------------+--------------------------------------------------------------------------------------------------+
| Animation Pointers    | Pointed by Content Header   | 4 Bytes             | Specified by Content Header  | List of pointers to each frame of Animation Data                                                 |
+-----------------------+-----------------------------+---------------------+------------------------------+--------------------------------------------------------------------------------------------------+
| Palette Data          | Pointed by Content Header   | 64 Bytes            | 16                           | A block of palette data that is separated into 16 palettes, each with 16 colors of 4 bytes each. |
+-----------------------+-----------------------------+---------------------+------------------------------+--------------------------------------------------------------------------------------------------+
| Image Data            | Pointed by Content Header   | Varies              | 1                            | One continuous block of image data that is read nibble-by-nibble.                                |
+-----------------------+-----------------------------+---------------------+------------------------------+--------------------------------------------------------------------------------------------------+
| Content Header        | Pointed by SIR0 Header      | 32 Bytes            | 1                            | Contains the pointers to Animation Data, Image Data, Palette Data, and the number of animations. |
+-----------------------+-----------------------------+---------------------+------------------------------+--------------------------------------------------------------------------------------------------+
| Pointer Offsets List  | Pointed by SIR0 Header      | 1 Byte              | Varies                       | Details in the SIR0 documentation                                                                |
+-----------------------+-----------------------------+---------------------+------------------------------+--------------------------------------------------------------------------------------------------+
| SIR0 Padding          | After Pointer Offsets List  | Varies              | ---                          | Details in the SIR0 documentation                                                                |
+-----------------------+-----------------------------+---------------------+------------------------------+--------------------------------------------------------------------------------------------------+


Content Header
~~~~~~~~~~~~~~

The 32-byte header appears to be split into 6 sections, each with 4 bytes:

1. Number of frames in the animation
2. Pointer to start of Animation Data
3. Unknown
4. Pointer to image data
5. Pointer to palette data
6. Unknown

Animation Data
~~~~~~~~~~~~~~

Represents one frame of screen animation per element.
It is always a header of 36 bytes, followed by a variable number of 2-byte draw instructions.
This frame of animation is drawn tile-by-tile: Starting from the top-left, row by row, then column by column.
Each tile is 8x8 texture.  First the number of tiles to draw are specified by the header (rows x columns)
Then, by reading each two-byte value and interpreting it as either a draw instruction that advances one tile,
or a skip instruction that advances the specified number of tiles.
Once all tiles (rows x columns) have been traversed, the frame has finished drawing and will not be read any further.

Header
------

The header 36 bytes is split up into the following regions:

AA AA BB BB CC CC DD DD EE EE 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF FF 00 00 00 GG 00 00

A: Always a multiple of section A
B: Always a multiple of section D
C: Number of textures per row.
D: Number of textures per column.
E: Frame duration in 1/60th of a second.
F: Transparency.
G: Unknown. One of various possible numbers: 0x00,0x40,0x60,0x7F,0x80,0xC0,0xF0,0xFF

Draw Instructions
-----------------

Two bytes that tell the game how to draw a single 8x8 texture in the current position, or how many tiles to skip.
The draw instruction is a little endian, 16 bit value made up of 4 parts.

AAA0 BCDD DDDD DDDD

A: If 1, draw the texture specified in D.  If 0, skip a number of tiles specified in D.
B: Flip the source image on Y axis before drawing
C: Flip the source image on X axis before drawing
D: Draw value.  If selected as a tile to draw, interpret this as the point in imgData to start reading an 8x8 texture.


Credits
-------
Thanks to BitDrifter for experimenting and deducing Header and Draw Instructions.