#!/usr/bin/env python
import os
import sys
import datetime
import subprocess

import pip


parent_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(parent_dir, "upgrade.log")

log = open(log_path, "r")
history = log.read()
log.close()
log = open(log_path, "w")
log.truncate()


system_info = os.uname()
cmds = []


if "Darwin" in system_info:
    cmds.append("npm update")
elif "Linux" in system_info:
    cmds.append("apt-get --assume-yes update")
    cmds.append("apt-get --assume-yes upgrade")
else:
    error = "ERROR: Unsupported system. Abort."
    log.write(error)
    log.close()
    sys.exit(1)

for cmd in cmds:
    process = subprocess.Popen(cmd, shell=True).communicate()

system = system_info[0]
version = system_info[2]

log.write("- %s is now at %s\n" % (system, version))


dists = []

for dist in pip.get_installed_distributions():
    dists.append(dist.project_name)

log.write("pip %s\n" % datetime.datetime.now())

for dist_name in sorted(dists, key=lambda s: s.lower()):
    cmd = "sudo pip install --upgrade %s" % dist_name

    process = subprocess.Popen(cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    ).communicate()

    out = process[0]
    print out

    begin_index = out.find("Successfully installed")

    if begin_index < 0:
        pass
    else:
        end_index = out.find("\n", begin_index)
        package = out[begin_index:end_index].split(' ')[-1]

        cmd = "pip freeze | grep %s" % package
        process = subprocess.Popen(cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ).communicate()

        out = process[0]
        version = out.split("==")[-1]

        log.write("- %s is now at %s" % (package, version))


log.write("\n")
log.write(history)
log.close()
