#!/usr/bin/env python
import os
import sys
import datetime
import subprocess

try:
    import Image
except ImportError:
    error = "ERROR: Failed importing PIL. Exiting."
    sys.exit(error)


script, root, dest = sys.argv

specs = [{
    "src": "chrome.png",
    "prefix": "droid",
    "sizes": [196, 128]
}, {
    "src": "safari.png",
    "prefix": "apple",
    "sizes": [152, 144, 120, 114, 76, 72, 57]
}, {
    "src": "firefox.png",
    "prefix": "gecko",
    "sizes": [128, 60, 30]
}]

for spec in specs:
    try:
        src_file = Image.open(os.path.join(root, spec["src"]))
    except IOError:
        error = "ERROR: %s failed to load. Exiting." % spec["src"]
        sys.exit(error)

    spec_size = spec["sizes"][0]

    if (spec_size, spec_size) != src_file.size:
        error = "ERROR: %s should be %sx%s, got %sx%s. Aborted." % (
            spec["src"], spec_size, src_file.size[0], src_file.size[1])
        sys.exit(error)
    else:
        print "Verified %s" % spec["src"]
        pass


print "Begin making icons..."

made_count = 0
begin_time = datetime.datetime.now()

for spec in specs:
    icon_prefix = "%s-icon" % spec["prefix"]

    fullcolored = Image.open(os.path.join(root, spec["src"]))
    desaturated = fullcolored.convert("LA")

    for size in spec["sizes"]:
        icon_name = "%s-%sx%s" % (icon_prefix, size, size)
        icon_size = (size, size)

        if spec["prefix"] == "apple":
            icon_name += "-precomposed.png"
        else:
            icon_name += ".png"

        prod = fullcolored.resize(icon_size, Image.ANTIALIAS)
        stag = desaturated.resize(icon_size, Image.ANTIALIAS)

        prod.save(os.path.join(dest, "original", icon_name))
        stag.save(os.path.join(dest, "greyscale", icon_name))

        made_count += 3


print "Running optimization..."

imgoptim_path = "/Applications/ImageOptim.app/Contents/MacOS/ImageOptim"
dist_path = dest + "/*/*.png"
shell_cmd = "%s 2>/dev/null %s" % (imgoptim_path, dist_path)

subprocess.Popen(shell_cmd,
    shell=True,
    stdout=subprocess.PIPE
).communicate()

duration = datetime.datetime.now() - begin_time

print "Done. Made %s icons in %s.%s sec." % (
    made_count, duration.seconds, duration.microseconds
)

sys.exit(0)
