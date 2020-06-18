from bs4 import BeautifulSoup
import argparse
import configparser

import re
import prettifyer


def read_html(file):
    with open(file, "r") as f:
        markup = f.read()
        soup = BeautifulSoup(markup, "html.parser")
    return soup


def get_meta_var(soup, name, default=None, delete_tag=True):
    meta = soup.head.find_all("meta")
    result = None
    for m in meta:
        if m.get("name") == name:
            result = m.get("content")
            if delete_tag:
                m.decompose()
            break

    if not result:
        result = default

    return result


def wrap(soup, to_wrap, wrap_in, **args):
    new_tag = soup.new_tag(wrap_in, **args)
    to_wrap.wrap(new_tag)


def replace(soup, to_replace, replace_with, **args):
    to_replace.name = replace_with
    to_replace.attrs = args


def prettify(soup):
    unformatted_tag_list = []

    for i, tag in enumerate(soup.find_all(["span", "code"])):
        unformatted_tag_list.append(str(tag))
        tag.replace_with("{" + "unformatted_tag_list[{0}]".format(i) + "}")

    pretty_markup = soup.prettify().format(unformatted_tag_list=unformatted_tag_list)
    return pretty_markup


def postprocess_menu(file):
    soup = read_html(file)

    menu = soup.body.ul
    wrap(soup, menu, "nav", **{"id": "menu"})
    menu = soup.body.nav

    with open(file, "w") as f:
        f.write(menu.prettify())


def postprocess_footer(file):
    soup = read_html(file)

    body = soup.body
    replace(soup, soup.body, "footer")
    footer = soup.find("footer")

    with open(file, "w") as f:
        f.write(footer.prettify())


def set_active_site(soup, active_site, menu_id):
    menu = soup.find("nav", id=menu_id)
    if not menu or not active_site:
        return

    links = menu.find_all("a")
    for link in links:
        if link.get("href").endswith(active_site):
            link["class"] = "active"
            break


def create_tags(soup, tags, config):
    if not tags:
        return None
    result = soup.new_tag("ul", attrs={"class": "tags"})
    for tag in tags:
        li = soup.new_tag("li")
        a = soup.new_tag(
            "a",
            attrs={
                "href": "{}{}{}.html".format(
                    config["GENERAL"].get("BaseUrl", ""),
                    config["GENERAL"].get("BlogTagDirectory", "/"),
                    tag,
                )
            },
        )
        a.append(tag)
        li.append(a)
        result.append(li)

    return result


def remove_code_style(soup):
    style = soup.head.find("style")
    content = style.string
    content = re.sub("code[ ]*?\{.*?\}", "", content)
    # style.string.replace_with(content)


def postprocess_site(file, config):
    soup = read_html(file)

    active_site = get_meta_var(soup, "ACTIVE_SITE")
    menu_id = get_meta_var(soup, "MENU_ID")
    ignore_header = get_meta_var(soup, "IGNORE_HEADER", default=False) == "True"
    tags = get_meta_var(soup, "TAGS", default="")
    tags = [t.strip() for t in tags.split(";") if t.strip()]

    header = soup.find("header")
    if ignore_header:
        header.contents = "&nbsp;"
    else:
        tags_ul = create_tags(soup, tags, config)
        if tags_ul:
            header.append(tags_ul)

    set_active_site(soup, active_site, menu_id)

    stylesheet = soup.head.find("link", rel="stylesheet")
    stylesheet["href"] = config["GENERAL"].get("BaseUrl", "") + stylesheet.get("href")

    remove_code_style(soup)

    with open(file, "w") as f:
        html = prettifyer.prettify_html(soup.prettify())
        f.write(html)


def main(file, postprocessor_type, config):
    if postprocessor_type == "menu":
        postprocess_menu(file)
    elif postprocessor_type == "footer":
        postprocess_footer(file)
    elif postprocessor_type == "site":
        postprocess_site(file, config)
    else:
        raise ValueError("Unknown parameter.")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("type")
    parser.add_argument("file")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    config = configparser.ConfigParser()
    config.read("config.ini")

    main(args.file, args.type, config)
