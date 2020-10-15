#!/usr/bin/env python3
import sys, os, time
from waveshare_epd import epd2in13_V2
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path

rfile = '/tmp/eink'

if os.path.exists(rfile) is False:
  Path(rfile).touch()

# Default fonts and path on raspbian
ttfdate = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-Regular.ttf', 20)
ttftime = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-Bold.ttf', 40)
ttfother = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-Regular.ttf', 18)

epd = epd2in13_V2.EPD()
epd.init(epd.FULL_UPDATE)
epd.Clear(0xFF)
W = epd.width
H = epd.height

M = time.strftime('%M')
F = os.path.getmtime(rfile)

while (True):
  image = Image.new('1', (H, W), 255)
  draw = ImageDraw.Draw(image)

  textdate = False
  texttime = False
  textA = False
  textB = False
  textC = False

  with open(rfile) as fp:
    lines = fp.readlines()

    for line in lines:
      cmd = line[0]
      text = line[1:].strip()

      if cmd == 'D':
        textdate = text
      elif cmd == 'T':
        texttime = text
      elif cmd == 'A':
        textA = text
      elif cmd == 'B':
        textB = text
      elif cmd == 'C':
        textC = text
      else:
        print('Unknown command code: ' + cmd + ' [' + line + ']')

  if texttime is False:
    texttime = time.strftime('%-I:%M %p')

  if textdate is False:
    textdate = time.strftime('%A - %B %-d')

  aW, aH = draw.textsize(textdate, font=ttfdate)
  draw.text(( W-(aW/2), 0), textdate, font=ttfdate, fill=0)

  bW, bH = draw.textsize(texttime, font=ttftime)
  draw.text(( W-(bW/2), aH), texttime, font=ttftime, fill=0)

  pad = 60

  if textA is not False:
    tW, tH = draw.textsize(textA, font=ttfdate)
    if tW > W:
      print('Text 3 too long: [' + textA + ']')
    else:
      if textA[0] == '$':
        textA = textA[1:]
        tW = W-(tW/2)
      else:
        tW = 0

      draw.text((tW, pad), textA, font=ttfother, fill=0)

  if textB is not False:
    tW, tH = draw.textsize(textB, font=ttfdate)
    if tW > W:
      print('Text 3 too long: [' + textB + ']')
    else:
      if textB[0] == '$':
        textB = textB[1:]
        tW = W-(tW/2)
      else:
        tW = 0

      draw.text((tW, pad+18), textB, font=ttfother, fill=0)

  if textC is not False:
    tW, tH = draw.textsize(textC, font=ttfdate)
    if tW > W:
      print('Text 3 too long: [' + textC + ']')
    else:
      if textC[0] == '$':
        textC = textC[1:]
        tW = W-(tW/2)
      else:
        tW = 0

      draw.text((tW, pad+18+18), textC, font=ttfother, fill=0)

  epd.display(epd.getbuffer(image))

  while M == time.strftime('%M') and F == os.path.getmtime(rfile):
    time.sleep( 10 )

  M = time.strftime('%M')
  F = os.path.getmtime(rfile)

epd.init(epd.FULL_UPDATE)
epd.Clear(0xFF)
epd.Dev_exit()
