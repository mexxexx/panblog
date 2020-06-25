import configparser
import sys
import re
import datetime
import math
import textwrap

from . import global_vars
from . import sites


def parse_blog_post(file):
    with open(file, "r") as f:
        content = f.read()

    lines = content.splitlines()
    in_header = lines[0].startswith("---")

    result = {
        "file": file.split("/", 1)[1],
        "title": None,
        "author": [],
        "subtitle": None,
        "date": None,
        "tags": [],
        "content": "",
    }

    intags = False
    for i, line in enumerate(lines):
        if in_header:
            m = re.search("title[ ]*:[ ]*(.*)", line)
            if m:
                result["title"] = m.group(1)

            m = re.search("subtitle[ ]*:[ ]*(.*)", line)
            if m:
                result["subtitle"] = m.group(1)

            m = re.search("author[ ]*:[ ]*(.*)", line)
            if m:
                result["author"].append(m.group(1))

            m = re.search("date[ ]*:[ ]*(.*)", line)
            if m:
                result["date"] = m.group(1)

            if intags:
                m = re.search("- (.*)", line)
                if m:
                    result["tags"].append(m.group(1))
                elif line.strip():
                    intags = False

            m = re.search("tags[ ]*:", line)
            if m:
                intags = True

            if i > 0:
                in_header = not line.startswith("---")
        else:
            result["content"] += line + "\n"

    if not result["title"]:
        raise AttributeError(
            "Blog post {} has no title info. ".format(file)
            + 'Please specify a title with the "title: ..." attribute.'
        )
    elif not result["date"]:
        raise AttributeError(
            "Blog post {} has no date info. ".format(file)
            + 'Please specify a date with the "date: ..." attribute.'
        )

    result["content"] = result["content"].strip()
    return result


def get_short_content(content, max_word_count):
    words = content.split(" ")
    if max_word_count < 0:
        max_word_count = len(words)

    short_content = " ".join(words[:max_word_count]).strip()
    if len(words) > max_word_count:
        short_content += "..."
    return short_content

def tag_url(tag, base_url, tags_dir, extension="html"):
    return base_url + tags_dir + tag.lower().strip().replace(" ", "-") + "." + extension

def get_tag_list(posts):
    tags = {}

    for post in posts:
        for tag in post["tags"]:
            if tag in tags:
                tags[tag].append(post)
            else:
                tags[tag] = [post]

    return tags


def create_tag_index(tags, config):
    base_url = config["GENERAL"]["baseurl"]
    tags_dir = config["DIR"]["blogtags"] + "/"

    result = '---\ntitle: Tags\n'
    result += 'tags-list:\n'
    for tag, _ in tags.items():
        href = tag_url(tag, base_url, tags_dir)
        result += '  - {{ text : {}, href : {} }}\n'.format(tag, href)
    result += "---\n"
    return result


def create_tag_page(tag_name, posts, config):
    max_word_count = int(config["BLOG"]["maxwordcount"])
    base_url = config["GENERAL"]["baseurl"]
    tags_dir = config["DIR"]["blogtags"] + "/"
    blog_pages_dir = config["DIR"]["blogpages"] + "/"

    result = "---\n"
    result += "title: {}\n".format(tag_name)
    result += "posts:\n"
    for post in posts:
        url = base_url + post["file"][:-3] + ".html"
        title = post["title"]
        result += "- id: {}\n".format(url.split("/")[-1][:-5])
        result += "  url: {}\n".format(url)
        result += "  title: {}\n".format(title)
        if post["subtitle"]:
            result += "  subtitle: {}\n".format(post["subtitle"])
        result += "  author:\n"
        for author in post["author"]:
            result += "  - {}\n".format(author)
        result += "  date: {}\n".format(post["date"])
        result += "  tags:\n"
        for tag in post["tags"]:
            href = tag_url(tag, base_url, tags_dir)
            result += '  - {{ text : {}, href : {} }}\n'.format(tag, href)
        content = get_short_content(
            post["content"], max_word_count
        ) + " [read more]({})".format(url)
        result += "  content: |\n{}".format(textwrap.indent(content, "    "))
        result += "\n"
    
    result += "tags-index: {}\n".format(base_url + tags_dir + "index.html")
    result += "---\n"

    return tag_name, result


def build_tag_pages(posts, config):
    pages = []

    tags = get_tag_list(posts)

    tag_index = create_tag_index(tags, config)
    for tag, posts in tags.items():
        pages.append(create_tag_page(tag, posts, config))

    return tag_index, pages


def write_tag_index(content, config):
    bin_dir = config["DIR"]["build"] + "/"
    tags_dir = config["DIR"]["blogtags"] + "/"
    
    filename = "{}{}.md".format(tags_dir, "index")
    filename_bin = "{0}{1}".format(bin_dir, filename)

    sites.add_blog_page(filename, filename_bin, "tag_index.html")
    with open(filename_bin, "w") as f:
        f.write(content)


def write_tag_pages(tag_pages, config):
    bin_dir = config["DIR"]["build"] + "/"
    tags_dir = config["DIR"]["blogtags"] + "/"

    for tag, content in tag_pages:
        filename = tag_url(tag, "", tags_dir, "md")
        filename_bin = "{0}{1}".format(bin_dir, filename)

        sites.add_blog_page(filename, filename_bin, "tag.html")
        with open(filename_bin, "w") as f:
            f.write(content)


def write_blog_pages(pages, config):
    src_dir = config["DIR"]["source"] + "/"
    bin_dir = config["DIR"]["build"] + "/"
    pages_dir = config["DIR"]["blogpages"] + "/"
    blog_dir = config["DIR"]["blog"] + "/"

    filenames_saved = []
    for page_num, content in pages:
        filenames = ["{}page{}.md".format(pages_dir, page_num)]
        if page_num == 1:
            filenames.insert(0, "{}index.md".format(blog_dir))
            filenames.insert(1, "{}index.md".format(pages_dir))
        filenames_saved += filenames

        for filename in filenames:
            with open("{0}{1}".format(bin_dir, filename), "w") as f:
                f.write(content)

    base_file = src_dir + blog_dir + "index.md"
    for f in filenames_saved:
        sites.add_blog_page(f, base_file)


def create_blog_page(num, num_pages, posts, config):
    max_word_count = int(config["BLOG"]["maxwordcount"])
    base_url = config["GENERAL"]["baseurl"]
    tags_dir = config["DIR"]["blogtags"] + "/"
    blog_pages_dir = config["DIR"]["blogpages"] + "/"

    result = "---\n"
    result += "posts:\n"
    for post in posts:
        url = base_url + post["file"][:-3] + ".html"
        title = post["title"]
        result += "- id: {}\n".format(url.split("/")[-1][:-5])
        result += "  url: {}\n".format(url)
        result += "  title: {}\n".format(title)
        if post["subtitle"]:
            result += "  subtitle: {}\n".format(post["subtitle"])
        result += "  author:\n"
        for author in post["author"]:
            result += "  - {}\n".format(author)
        result += "  date: {}\n".format(post["date"])
        result += "  tags:\n"
        for tag in post["tags"]:
            href = tag_url(tag, base_url, tags_dir)
            result += '  - {{ text : {}, href : {} }}\n'.format(tag, href)
        content = get_short_content(
            post["content"], max_word_count
        ) + " [read more]({})".format(url)
        result += "  content: |\n{}".format(textwrap.indent(content, "    "))
        result += "\n\n"

    if num >= 2:
        result += "prev-page:\n"
        result += "  num: {0}\n  href: {1}page{0}.html\n".format(
            num - 1, base_url + blog_pages_dir
        )
    result += "current-page:\n".format()
    result += "  num: {0}\n".format(num)
    if num < num_pages:
        result += "next-page:\n"
        result += "  num: {0}\n  href: {1}page{0}.html\n".format(
            num + 1, base_url + blog_pages_dir
        )
    result += "tags-index: {}\n".format(base_url + tags_dir + "index.html")

    result += "---\n"

    return num, result


def build_blog_pages(posts, config):
    posts_per_page = int(config["BLOG"]["postsperpage"])
    max_word_count = int(config["BLOG"]["maxwordcount"])

    src_dir = config["DIR"]["source"] + "/"
    bin_dir = config["DIR"]["build"] + "/"
    post_dir = config["DIR"]["blogposts"] + "/"
    pages_dir = config["DIR"]["blogpages"] + "/"

    base_url = config["GENERAL"]["baseurl"]

    num_pages = max(1, int(math.ceil(len(posts) / posts_per_page)))

    if num_pages == 1:
        pages = [slice(None)]
    else:
        pages = [
            slice(i * posts_per_page, (i + 1) * posts_per_page)
            for i in range(num_pages)
        ]

    pages = [
        create_blog_page(i + 1, num_pages, posts[p], config)
        for i, p in enumerate(pages)
    ]

    return pages


def build_blog(posts, config):
    src_dir = config["DIR"]["source"] + "/"
    post_dir = config["DIR"]["blogposts"] + "/"

    posts_parsed = [
        parse_blog_post(src_dir + post_dir + post["href"]) for post in posts
    ]
    posts_parsed.sort(key=lambda x: x["date"], reverse=True)

    blog_pages = build_blog_pages(posts_parsed, config)
    tag_index, tag_pages = build_tag_pages(posts_parsed, config)

    with open(global_vars._PANBLOGDIR + "/" + global_vars._BLOG_PAGES, "w") as f:
        pass

    write_blog_pages(blog_pages, config)
    write_tag_index(tag_index, config)
    write_tag_pages(tag_pages, config)
