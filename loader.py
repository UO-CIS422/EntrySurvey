"""
Load a poll specification from an
external spec (currently YAML)
"""
import yaml
import json
import sys

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def load(poll_name: str):
    f = open(poll_name, 'r')
    struct = yaml.safe_load(f)
    return struct

def indent(lv: int) -> str:
    return " " * 4 * lv

def decode(poll: list):
    """Based on schema from team_formation.yaml:
    # poll ::= section*
    # section ::= title prologue content
    # content ::= range  range-element*
    #          |  text text-element*
    # range-element ::=  name title value-names
    # text-element ::= name title kind required
    """
    lv = 0
    for section in poll:
        print(f"Section {section['title']}")
        print(section["prologue"])
        lv += 1
        kind = section["content-type"]
        for el in section["content"]:
            print(f"{indent(lv)}{el['name']} -- {el['title']}")
            if kind == "text":
                print(f"{indent(lv)}  text({el['format']}")
            elif kind == "range":
                print(f"{indent(lv)}  choose from range {el['values']}")
        lv -= 1


if __name__ == "__main__":
    sample = load("polls/team_formation.yaml")
    print(sample)
    json.dump(sample, sys.stdout, indent=4)
    print("=====")
    decode(sample)



