#!/usr/bin/env python

"""
QRcode markdown filter
========================

- Copyright (c) 2011 Zenobius Jiricek
    - Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php


## Format

[-[strDataToEncode]-]

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
      "intPixelSize"  : [  2, "Pixel Size of each dark and light bit" ],
      "useDomainSyntax" : [ True, "Use the alternative \"domain\" style syntax (:qr:`data`)"],
      "bgColor" : [ "#FFFFFF", "The color to use for background (\"light colored\") squares."],
      "fgColor" : [ "#000000", "The color to use for foreground (\"dark colored\") squares."],
    }
    # Override defaults with user settings
    for key, value in configs:
      self.setConfig(key, value)

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
    if self.config['useDomainSyntax']:
        self.add_inline( md, "qrcode", BasicQrCodePattern, r':(?:qr|QR):(?P<pix>[0-9]+:)?(?:(?:fg|FG)=(?P<fg>[^:]*):)?(?:(?:bg|BG)=(?P<bg>[^:]*):)?\[(?P<data>.*)\]')
    else:
        self.add_inline( md, "qrcode", BasicQrCodePattern, r'\[\-\[(?P<data>.*)\]\-\]')

class BasicQrCodePattern(markdown.inlinepatterns.Pattern):
  def __init__(self, pattern, config):
    self.pattern = pattern
    self.config = config
    markdown.inlinepatterns.Pattern.__init__(self, pattern)

  def handleMatch(self, match):

    if match :

      captures = match.groupdict()
      print captures

      pixel_size = self.config['intPixelSize'][0]
      fg_col = self.config['fgColor'][0]
      bg_col = self.config['bgColor'][0]

      if "pix" in captures:
        pix = captures["pix"]
        if pix is not None:
            pixel_size = int(captures["pix"][:-1])
      if "fg" in captures:
        fg = captures["fg"]
        if fg is not None:
            fg_col = fg
      if "bg" in captures:
        bg = captures["bg"]
        if bg is not None:
            bg_col = bg

      qrcodeSourceData = str(captures["data"])

      qrCodeObject = QRCode(pixel_size, QRErrorCorrectLevel.L)
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
    print doctest.testmod()
    print "-" * 8
    md = markdown.Markdown(extensions=['qrcode'])
    print md.convert( __doc__ )

