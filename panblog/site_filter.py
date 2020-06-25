from pandocfilters import toJSONFilter, Link, Image, Str, walk, stringify, elt
import re
import configparser

from . import global_vars

meta_tags_written = []
config = None

MetaBool = elt("MetaBool", 1)
MetaMap = elt("MetaMap", 1)
MetaInlines = elt("MetaInlines", 1)


def get_meta_list(meta, name, default=None):
    result = meta.get(name, {})
    if not result or result["t"] != "MetaList":
        result = default

    return result


def get_meta_string(meta, name, default=""):
    result = meta.get(name, {})
    if result and result["t"] == "MetaInlines":
        result = stringify(result)
    elif result and result["t"] == "MetaString":
        result = result["c"]
    else:
        result = default

    return result


def walk_menu(k, v, fmt, meta):
    base_url = meta["base_url"]
    active_site = meta["active_site"]

    if "href" in v:
        link = v["href"]["c"][0]["c"]
        if link.endswith(".md"):
            link = base_url + link[:-3] + ".html"
            v["href"]["c"][0]["c"] = link

        if active_site and link == active_site:
            v["active"] = MetaBool(True)


def parse_menu(menu, base_url, active_site):
    if not menu:
        return
    walk(menu, walk_menu, None, {"base_url": base_url, "active_site": active_site})


def create_meta_map(x):
    c = {}
    for k, v in x.items():
        c[k] = MetaInlines([Str(v)])
    return c


def parse_tags(tags, base_url, config):
    tagsdir = config["DIR"]["blogtags"]
    if not tags:
        return

    for tag in tags["c"]:
        value = stringify(tag)
        link = base_url + tagsdir + "/" + value.lower().strip().replace(" ", "-") + ".html"
        tag["t"] = "MetaMap"
        tag["c"] = create_meta_map({"text": value, "href": link})


def parse_site(k, v, fmt, meta):
    base_url = config["GENERAL"]["baseurl"]

    if "MENU" not in meta_tags_written:
        active_site = get_meta_string(meta, "active-site", None)
        menu = get_meta_list(meta, "menu")
        parse_menu(menu, base_url, active_site)
        meta_tags_written.append("MENU")
    if "TAGS" not in meta_tags_written:
        tags = get_meta_list(meta, "tags", None)
        parse_tags(tags, base_url, config)
        meta_tags_written.append("TAGS")

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


def main():
    global config

    config = configparser.ConfigParser()
    config.read(global_vars._CONFIG)

    toJSONFilter(parse_site)


if __name__ == "__main__":
    main()
