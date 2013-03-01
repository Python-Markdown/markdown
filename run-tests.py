#!/usr/bin/env python

import tests
import os, sys, getopt

opts, args = getopt.getopt(sys.argv[1:], '')

if args and args[0] == "update":
    if len(args) > 1:
        config = tests.get_config(os.path.dirname(args[1]))
        root, ext = os.path.splitext(args[1])
        if ext == config.get(tests.get_section(os.path.basename(root), config), 'input_ext'):
            tests.generate(root, config)
        else:
            print(file, 'does not have a valid file extension. Check config.')
    else:
        tests.generate_all()
else:
    tests.run()
