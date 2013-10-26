#!/usr/bin/env python

"""
QRcode markdown filter
========================

- Copyright (c) 2011 Zenobius Jiricek
    - Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php


## Format

### Traditional Syntax

This is the "traditional" short syntax:

    [-[str data to encode]-]

It renders like this:

[-[str data to encode]-]


### Domain Syntax

A second, more verbose but more general and powerful syntax, is called the "domain"
syntax. It looks like this:

    :qr:4:bg=#FF0000:fg=#0000FF:ec=Q:[Encode this as well.]

Which renders as

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

"""


import markdown
import StringIO
from QrCodeLib import *
from markdown.util import etree
from base64 import b64encode

class QrCodeExtension(markdown.Extension):
  """ QRcode Extension for Python-Markdown. """
  def __init__(self, configs):
    """
    Create an instance of QrCodeExtension

    Keyword arguments:
    * configs: A dict of configuration settings passed in by the user.
    """
    # Set extension defaults
    self.config = {
      "intPixelSize"  : [  "2", "Pixel Size of each dark and light bit" ],
      "useShortSyntax" : [ "true", "Enable the use of the original short syntax ( '[-[data to encode]-]' )"],
      "bgColor" : [ "#FFFFFF", "The color to use for background (\"light colored\") squares."],
      "fgColor" : [ "#000000", "The color to use for foreground (\"dark colored\") squares."],
      "ecLevel" : ["L", "The error correcting level to use. One of L, M, H, or Q."],
    }
    # Override defaults with user settings
    for key, value in configs:
      self.setConfig(key, value)


    self.config["intPixelSize"][0] = int(self.config["intPixelSize"][0])
    self.config["useShortSyntax"][0] = (self.config["useShortSyntax"][0]).lower() in ("true", "yes", "t", "y", "1")


  def add_inline(self, md, name, pattern_class, pattern):
    """
    Add new functionality to the Markdown instance.

    Keyword arguments:
    * md: The Markdown instance.
    * md_globals: markdown's global variables.
    """
    objPattern = pattern_class(pattern, self.config)
    objPattern.md = md
    objPattern.ext = self
    md.inlinePatterns.add(name, objPattern, "<reference")

  def extendMarkdown(self, md, md_globals):
    self.add_inline( md, "qrcode-domain", BasicQrCodePattern, r':(?:qr|QR):(?P<args>[^\[\]]+:)?\[(?P<data>.*)\]')
    if self.config['useShortSyntax'][0]:
        self.add_inline( md, "qrcode", BasicQrCodePattern, r'\[\-\[(?P<data>.*)\]\-\]')

class BasicQrCodePattern(markdown.inlinepatterns.Pattern):
  def __init__(self, pattern, config):
    self.pattern = pattern
    self.config = config
    markdown.inlinepatterns.Pattern.__init__(self, pattern)

  def handleMatch(self, match):

    if match :

      captures = match.groupdict()

      pixel_size = self.config['intPixelSize'][0]
      fg_col = self.config['fgColor'][0]
      bg_col = self.config['bgColor'][0]
      ec_level = self.config['ecLevel'][0]

      if "args" in captures:
        args = captures["args"]
        if args is not None:
            args = args[:-1].split(":")
            for arg in args:
                c = arg.split("=", 1)
                if len(c) == 1:
                    pixel_size = int(c[0])
                else:
                    k, v = c
                    if k.lower() == "fg":
                        fg_col = v
                    elif k.lower() == "bg":
                        bg_col = v
                    elif k.lower() == "ec":
                        ec_level = v

      if ec_level == 'L':
        ec_level = QRErrorCorrectLevel.L
      elif ec_level == 'M':
        ec_level = QRErrorCorrectLevel.M
      elif ec_level == 'H':
        ec_level = QRErrorCorrectLevel.H
      elif ec_level == 'Q':
        ec_level = QRErrorCorrectLevel.Q
      else:
        ec_level = QRErrorCorrectLevel.L

      qrcodeSourceData = str(captures["data"])

      qrCodeObject = QRCode(pixel_size, ec_level)
      qrCodeObject.addData( qrcodeSourceData )
      qrCodeObject.make()
      qrCodeImage = qrCodeObject.makeImage(
        pixel_size = pixel_size,
        dark_colour = fg_col,
        light_colour = bg_col,
      )
      qrCodeImage_File = StringIO.StringIO()
      qrCodeImage.save( qrCodeImage_File , format= 'PNG')

      element = markdown.util.etree.Element('img')
      element.set("src", "data:image/png;base64,%s" % b64encode( qrCodeImage_File.getvalue()) )
      element.set("title", "qrcode for : %s " % qrcodeSourceData )

      qrCodeImage_File.close()

      return element
    else :
      return ""

def makeExtension(configs=None):
  return QrCodeExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    #print doctest.testmod()
    #print "-" * 8
    md = markdown.Markdown(extensions=['qrcode', 'def_list'])
    print md.convert( __doc__ )

