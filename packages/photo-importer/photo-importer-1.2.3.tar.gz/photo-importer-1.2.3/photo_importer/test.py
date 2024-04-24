#!/usr/bin/python3

import glob
import re
import os


def __get_removable_devices():
    res = []
    for path in glob.glob('/sys/block/*/device'):
        dev = re.sub('.*/(.*?)/device', '\g<1>', path)
        with open('/sys/block/%s/removable' % (dev,)) as f:
            if f.read(1) != '1':
                continue
        for ppath in glob.glob('/sys/block/%s/%s*' % (dev, dev)):
            pdev = os.path.split(ppath)[1]
            res.append(pdev)
    return res


for d in __get_removable_devices():
    print(d)
