from pandocfilters import toJSONFilter, Link, Image, stringify
import re
import configparser

meta_tags_written = []
base_url = ""


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
        result = stringify(result)
    elif result and result["t"] == "MetaString":
        result = result["c"]
    else:
        result = default

    return result


def get_meta_bool(meta, name, default=False):
    result = meta.get(name, {})
    if result and result["t"] == "MetaBool":
        result = result["c"]
    else:
        result = default

    return result


def parse_site(k, v, fmt, meta):
    ignore_header = get_meta_bool(meta, "ignore-header")
    write_meta_tag(meta, "IGNORE_HEADER", ignore_header)

    active_site = get_meta_string(meta, "active-site")
    write_meta_tag(meta, "ACTIVE_SITE", active_site)

    menu_id = get_meta_string(meta, "menu-id", "menu")
    write_meta_tag(meta, "MENU_ID", menu_id)

    tags = get_meta_string(meta, "tags")
    write_meta_tag(meta, "TAGS", tags)

    if k == "Link":
        title = v[0]
        text = v[1]
        link = v[2]
        if link[0].endswith(".md"):
            link[0] = base_url + link[0][:-3] + ".html"
        return Link(title, text, link)
    elif k == "Image":
        title = v[0]
        text = v[1]
        link = v[2]
        link[0] = base_url + link[0]
        return Image(title, text, link)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    if "BaseUrl" in config["GENERAL"]:
        base_url = config["GENERAL"]["BaseUrl"]

    toJSONFilter(parse_site)
