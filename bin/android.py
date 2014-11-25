#!/usr/bin/env python
import subprocess, datetime, sys, os


try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import PIL")


SCRIPT, SOURCE, DEST = sys.argv

specs = [
    {"name": "xxxhdpi", "size": 192},
    {"name": "xxhdpi", "size": 144},
    {"name": "xhdpi", "size": 96},
    {"name": "hdpi", "size": 72},
    {"name": "mdpi", "size": 48},
    {"name": "ldpi", "size": 36}
]

file_name = "ic_launcher.png"

try:
    src = Image.open(SOURCE)
except IOError:
    sys.exit("Cannot load source: %s" % SOURCE)

original_size = 512

if src.size != (original_size, original_size):
    sys.exit("Invalid source size: (%s, %s)" % (src.size[0], src.size[1]))
else:
    pass


print "Begin..."

begin_time = datetime.datetime.now()
count = 0

for spec in specs:
    dest_dir = os.path.join(DEST, "drawable-" + spec["name"])
    dest_path = os.path.join(dest_dir, file_name)

    resized = src.resize((spec["size"], spec["size"]), Image.ANTIALIAS)
    resized.save(dest_path)

    count += 1


print "Optimizing..."

optimizer_path = "/Applications/ImageOptim.app/Contents/MacOS/ImageOptim"
dist_path = DEST + "/**.png"

subprocess.Popen("%s 2>/dev/null %s" % (optimizer_path, dist_path),
    stdout=subprocess.PIPE,
    shell=True
).communicate()

cost = datetime.datetime.now() - begin_time

print "%s icons, %s.%s seconds." % (count, cost.seconds, cost.microseconds)

sys.exit(0)
