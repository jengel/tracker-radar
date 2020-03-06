#!/usr/bin/env python3

"""
Generates a uBlock-compatible block list for the tracking domains identified
by the DuckDuckGo Tracker Radar.
"""

import functools
import json
import operator
import pathlib

__copright__ = "Copyright 2020, Jeff Engel"
__license__ = ""

# Directory where the domain files are located.
domains_dir = pathlib.Path("../domains")

# Block file.
output_file = pathlib.Path("tracker-radar-domains-ublock.txt")

preamble = """[Adblock Plus 2.0]
! Title: DuckDuckGo-Tracker-Radar
! Expires: 30 days (update frequency)
! Description: Block tracking websites identified by the DuckDuckGo Tracker Radar
! Homepage: https://github.com/jengel
! Creator: jengel
! License: https://creativecommons.org/licenses/by/4.0/legalcode
!
! Thanks to the folks at DuckDuckGo who generated the domain list at
! https://github.com/duckduckgo/tracker-radar/.
!-------------------------------------------------------------------------------
"""

def read_json_file(file : pathlib.Path) -> str:
    with file.open() as f:
        return json.load(f)

if __name__ == "__main__":
    domain_objects = [read_json_file(file) for file in domains_dir.iterdir()]
    resources = functools.reduce(operator.concat, (obj["resources"] for obj in domain_objects))
    rules = [resource["rule"].replace("\\", "") for resource in resources]

    with output_file.open("w") as f:
        f.writelines(preamble)
        f.writelines("\n|{0}".format(rule) for rule in rules)

    print("Wrote {0} resources to {1}".format(len(rules), output_file))
