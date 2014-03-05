#!/usr/bin/env python
import os
import sys
import datetime
import subprocess

try:
    import Image
except ImportError:
    error = "Failed importing PIL"
    sys.exit(error)


SCRIPT, ROOT, DEST = sys.argv

specs = [
    {"size": 1024,"name": "iTunesArtwork@2x.png"},
    {"size": 512, "name": "iTunesArtwork.png"},
    {"size": 152, "name": "AppIcon76x76@2x~ipad.png"},
    {"size": 76,  "name": "AppIcon76x76~ipad.png"},
    {"size": 144, "name": "AppIcon72x72@2x~ipad.png"},
    {"size": 72,  "name": "AppIcon72x72~ipad.png"},
    {"size": 120, "name": "AppIcon60x60@2x.png"},
    {"size": 114, "name": "AppIcon57x57@2x.png"},
    {"size": 57,  "name": "AppIcon57x57.png"},
    {"size": 100, "name": "AppIcon50x50@2x~ipad.png"},
    {"size": 50,  "name": "AppIcon50x50~ipad.png"},
    {"size": 80,  "name": "AppIcon40x40@2x.png"},
    {"size": 80,  "name": "AppIcon40x40@2x~ipad.png"},
    {"size": 40,  "name": "AppIcon40x40~ipad.png"},
    {"size": 58,  "name": "AppIcon29x29@2x.png"},
    {"size": 29,  "name": "AppIcon29x29.png"},
    {"size": 58,  "name": "AppIcon29x29@2x~ipad.png"},
    {"size": 29,  "name": "AppIcon29x29~ipad.png"}
]

source_name = specs[0]["name"]

try:
    source = Image.open(os.path.join(ROOT, source_name))
except IOError:
    error = "Cannot load source file"
    sys.exit(error)

source_size = specs[0]["size"]

if source.size != (source_size, source_size):
    error = "Wrong source file dimension: (%s, %s)" % (
        source.size[0], source.size[1]
    )
    sys.exit(error)
else:
    print "Source file: %s verified" % source_name
    pass


count = 0
print "Begin making..."

begin_time = datetime.datetime.now()

for index, spec in enumerate(specs):
    dest_path = None

    if index == 0:
        continue
    elif index == 1:
        dest_path = os.path.join(ROOT, spec["name"])
    else:
        dest_path = os.path.join(DEST, spec["name"])

    resized = source.resize((spec["size"], spec["size"]), Image.ANTIALIAS)
    resized.save(dest_path)
    count += 1

    print "Made %s" % spec["name"]


print "Running optimization..."

imgoptim_path = "/Applications/ImageOptim.app/Contents/MacOS/ImageOptim"
dist_path = DEST + "/*.png"
shell_cmd = "%s 2>/dev/null %s" % (imgoptim_path, dist_path)

subprocess.Popen(
    shell_cmd,
    shell=True,
    stdout=subprocess.PIPE
).communicate()

duration = datetime.datetime.now() - begin_time

print "Done. Made %s icons in %s.%s sec." % (
    count, duration.seconds, duration.microseconds)

sys.exit(0)
