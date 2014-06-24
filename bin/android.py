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
    {"name": "xxxhdpi", "size": 192},
    {"name": "xxhdpi",  "size": 144},
    {"name": "xhdpi",   "size": 96},
    {"name": "hdpi",    "size": 72},
    {"name": "mdpi",    "size": 48},
    {"name": "ldpi",    "size": 36}
]

file_name = "icon.png"

try:
    src = Image.open(os.path.join(ROOT, file_name))
except IOError:
    error = "Cannot load source file: %s" % os.path.join(ROOT, file_name)
    sys.exit(error)

original_size = 196

if src.size != (original_size, original_size):
    error = "Wrong source dimension: (%s, %s)" % (src.size[0], src.size[1])
    sys.exit(error)
else:
    print "Source file: %s verified" % file_name
    pass


print "Begin making..."
begin_time = datetime.datetime.now()
count = 0

for spec in specs:
    dest_dir = os.path.join(DEST, "drawable-" + spec["name"])
    dest_path = os.path.join(dest_dir, file_name)

    resized = src.resize((spec["size"], spec["size"]), Image.ANTIALIAS)
    resized.save(dest_path)

    count += 1
    print "Made %s" % spec["name"]


print "Running optimization..."

imgoptim_path = "/Applications/ImageOptim.app/Contents/MacOS/ImageOptim"
dist_path = DEST + "/**.png"
shell_cmd = "%s 2>/dev/null %s" % (imgoptim_path, dist_path)

subprocess.Popen(
    shell_cmd,
    shell=True,
    stdout=subprocess.PIPE
).communicate()

duration = datetime.datetime.now() - begin_time

print "Made %s icons in %s.%s sec" % (
    count, duration.seconds, duration.microseconds
)

sys.exit(0)
