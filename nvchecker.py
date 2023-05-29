#!/bin/python
import logging
import os
import sys
import traceback
from pathlib import Path

import toml
import yaml

nvchecker_toml = toml.load("config/__config__.toml")
if not 'GITHUB_TOKEN' in os.environ and 'keyfile' in nvchecker_toml['__config__']:
    del nvchecker_toml['__config__']['keyfile']

for i in [Path(j) for j in sys.argv[1:]] if len(sys.argv) > 1 else Path("config").rglob("*.yaml"):
    if i.stem in ["example"]:
        continue
    try:
        with open(i) as f:
            config = yaml.safe_load(f)
            config = config["nvchecker"]
            config["user_agent"] = "nvchecker"
            nvchecker_toml[i.stem] = config
        print("Loaded", i)
    except:
        print("Failed to load", i)
        traceback.print_exc()

with open("nvchecker.toml", "w") as f:
    toml.dump(nvchecker_toml, f)
