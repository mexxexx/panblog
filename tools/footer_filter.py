from pandocfilters import toJSONFilter, Link
import configparser

base_url = ""


def parse_footer(k, v, fmt, meta):
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

    toJSONFilter(parse_footer)
