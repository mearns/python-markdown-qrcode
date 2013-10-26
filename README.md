QRCODE Markdown Extension
=========================

## Installation

1. You need to have python-setuptools installed
`sudo apt-get install python-setuptools`
1. `python ./setup.py install`


## Format

### Traditional Syntax

This is the "traditional" short syntax:

    [-[str data to encode]-]


### Domain Syntax

A second, more verbose but more general and powerful syntax, is called the "domain"
syntax. It looks like this:

    :qr:4:bg=#FF0000:fg=#0000FF:ec=Q:[Encode this as well.]

The domain syntax has the general form:

    :qr:<OPTS>:[<DATA>]

Where OPTS can be used to specify the pixel-size, the foreground and background size,
and the QR Error Correcting Level to use (L, M, H, or Q). (Note that the foreground
color doesn't work real well). All OPTS are optional.

## Config Options

intPixelSize
: Pixel Size of each dark and light bit. _Default is 2_

useShortSyntax
: Enable the use of the original short syntax. _Default is True_

bgColor
: The color to use for background ("light colored") bits. _Default is #FFFFFF (white)_

fgColor
: The color to use for foreground ("dark colored") bits. _Default is #000000 (black)_

ecLevel
: The error correcting level to use. One of L, M, H, or Q. _Default is L_


## Notes

You can try including square brackets in DATA by escaping them with front slashes,
but markdown seems to be replacing them with some strange escape code.

## Legal

### extension.py

+ Copyright (c) 2011 Zenobius Jiricek
+ Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php


### QrCodeLib.py

Ported from Javascript to Python by Sam Curren

Original Project :
+ Copyright (c) 2009 Kazuhiko Arase
+ http://d-project.googlecode.com/svn/trunk/misc/qrcode/js/qrcode.js
+ Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

### Trademarks

The word "QR Code" is registered trademark of DENSO WAVE INCORPORATED

+ http://www.denso-wave.com/qrcode/faqpatent-e.html

