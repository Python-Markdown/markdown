#!/usr/bin/env python

import tests
import os
import sys

if len(sys.argv) > 1 and sys.argv[1] == "update":
    if len(sys.argv) > 2:
        config = tests.get_config(os.path.dirname(sys.argv[2]))
        root, ext = os.path.splitext(sys.argv[2])
        if ext == config.get(
            config.get_section(os.path.basename(root)), 'input_ext'
        ):
            tests.generate(root, config)
        else:
            print(
                sys.argv[2],
                'does not have a valid file extension. Check config.'
            )
    else:
        tests.generate_all()
else:
    tests.run()
