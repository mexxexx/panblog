from pandocfilters import toJSONFilter, Link, stringify
import re
import configparser

meta_tags_written = []


def add_to_meta(meta, where, x):
    if where not in meta:
        meta[where] = {
            "t": "MetaBlocks",
            "c": [x],
        }
    else:
        meta[where]["c"].append(x)


def write_meta_tag(meta, name, content):
    global meta_tags_written
    if name in meta_tags_written:
        return

    result = {
        "t": "RawBlock",
        "c": ["html", '<meta name="{}" content="{}" />'.format(name, content),],
    }
    add_to_meta(meta, "header-includes", result)
    meta_tags_written.append(name)


def get_meta_string(meta, name, default=""):
    result = meta.get(name, {})
    if result and result["t"] == "MetaInlines":
        t = result["c"][0]["t"]
        result = stringify(result)
    else:
        result = default

    return result


base_url = ""


def parse_menu(k, v, fmt, meta):
    if k == "Link":
        title = v[0]
        text = v[1]
        link = v[2]
        if link[0].endswith(".md"):
            link[0] = base_url + link[0][:-3] + ".html"
        return Link(title, text, link)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    if "BaseUrl" in config["GENERAL"]:
        base_url = config["GENERAL"]["BaseUrl"]

    toJSONFilter(parse_menu)
