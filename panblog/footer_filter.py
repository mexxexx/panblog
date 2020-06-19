from pandocfilters import toJSONFilter, Link
import configparser

from . import global_vars

config = None


def parse_footer(k, v, fmt, meta):
    if k == "Link":
        title = v[0]
        text = v[1]
        link = v[2]

        base_url = config["GENERAL"]["baseurl"]
        if link[0].endswith(".md"):
            link[0] = base_url + link[0][:-3] + ".html"
        return Link(title, text, link)


def main():

    global config

    config = configparser.ConfigParser()
    config.read(global_vars._CONFIG)

    toJSONFilter(parse_footer)


if __name__ == "__main__":
    main()
