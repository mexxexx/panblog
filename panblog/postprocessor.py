from bs4 import BeautifulSoup
import argparse
import configparser

import re
from . import prettifyer


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
    nav = soup.new_tag("nav", attrs={"id": "menu"})
    if menu:
        menu.wrap(nav)
    else:
        soup.body.append(nav)

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
                "href": "{}{}/{}.html".format(
                    config["GENERAL"]["baseurl"], config["DIR"]["blogtags"], tag,
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


def main():
    args = parse_args()

    config = configparser.ConfigParser()
    config.read("config.ini")

    if args.type == "menu":
        postprocess_menu(args.file)
    elif args.type == "footer":
        postprocess_footer(args.file)
    elif args.type == "site":
        postprocess_site(args.file, config)
    else:
        raise ValueError("Unknown parameter.")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("type")
    parser.add_argument("file")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
