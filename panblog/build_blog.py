import configparser
import sys
import re
import datetime
import math

from . import global_vars


def parse_blog_post(file):
    with open(file, "r") as f:
        content = f.read()

    lines = content.splitlines()
    in_header = lines[0].startswith("---")

    title = None
    date = None
    content = ""
    tags = []
    for i, line in enumerate(lines):
        if in_header:
            m = re.search('title[ ]*:[ ]*"(.*)"', line)
            if m:
                title = m.group(1)

            m = re.search("date[ ]*:[ ]*(.*)", line)
            if m:
                date = m.group(1)

            m = re.search('tags[ ]*:[ ]*"(.*)"', line)
            if m:
                tags = m.group(1)
                tags = [tag.strip() for tag in tags.split(";") if tag.strip()]

            if i > 0:
                in_header = not line.startswith("---")
        else:
            content += line + "\n"

    if not title:
        raise AttributeError(
            "Blog post {} has no title info. ".format(file)
            + 'Please specify a title with the "title: ..." attribute.'
        )
    elif not date:
        raise AttributeError(
            "Blog post {} has no date info. ".format(file)
            + 'Please specify a date with the "date: ..." attribute.'
        )

    return {
        "file": file.split("/", 1)[1],
        "title": title,
        "date": date,
        "tags": tags,
        "content": content.strip(),
    }


def parse_blog_preview_template(file):
    with open(file, "r") as f:
        content = f.read()

    return content


def get_short_content(content, max_word_count):
    words = content.split(" ")
    if max_word_count < 0:
        max_word_count = len(words)

    short_content = " ".join(words[:max_word_count]).strip()
    if len(words) > max_word_count:
        short_content += "..."
    return short_content


def create_blog_post(post, max_word_count, config):
    title = post["title"]
    date = post["date"]
    content = post["content"]
    link = post["file"]
    tags = post["tags"]

    result = ""
    result += "## [{}]({}) {{.blog_post_preview}}\n\n".format(title, link)

    result += '<p class="date">'
    if date is not None:
        result += date
    result += "</p>\n\n"

    if tags:
        result += '<ul class="tags">\n'
        for tag in tags:
            result += "<li>[{0}]({1}/{0}.md)</li>\n".format(
                tag, config["DIR"]["blogtags"]
            )
        result += "</ul>\n\n"

    content = get_short_content(
        content, max_word_count
    ) + " [read more]({})\n\n".format(link)

    result += content
    return result


def create_blog_preview(posts, page_num, last_page, max_word_count, config):
    result = ""

    result += "::: {#blog_posts}\n"
    for i, post in enumerate(posts):
        if i > 0:
            result += "--------------\n\n"
        result += create_blog_post(post, max_word_count, config)

    result += ":::\n\n"

    result += '<nav id="blog_preview_page_number">\n\n'

    result += "::: {#blog_preview_page_number_prev}\n"
    if not page_num == 1:
        result += "[&#171; {0}]({1}/page{0}.md){{.prev_blog_page}}\n".format(
            str(page_num - 1), config["DIR"]["blogpages"]
        )

    result += ":::\n\n"

    result += "::: {#blog_preview_page_number_current}\n" + str(page_num) + "\n:::\n\n"

    result += "::: {#blog_preview_page_number_next}\n"
    if not last_page:
        result += "[{0} &#187;]({1}/page{0}.md){{.next_blog_page}}\n".format(
            str(page_num + 1), config["DIR"]["blogpages"]
        )
    result += ":::\n\n"

    result += "</nav>\n\n"
    return result


def insert_blog_preview(template, content):
    return template.replace('<div id="blog_previews" />', content)


def get_blog_posts():
    posts = []
    if len(sys.argv) >= 4:
        for f in sys.argv[3:]:
            posts.append(parse_blog_post(f))
    posts.sort(key=lambda x: x["date"], reverse=True)
    return posts


def get_tag_list(entries):
    tags = {}

    for entry in entries:
        for tag in entry["tags"]:
            if tag in tags:
                tags[tag].append(entry)
            else:
                tags[tag] = [entry]

    return tags


def create_blog_pages(
    posts, blog_preview_template, posts_per_page, max_word_count, config
):
    pages = []
    if posts_per_page < 0:
        num_pages = 1
    else:
        num_pages = int(math.ceil(len(posts) / posts_per_page))

    for i in range(num_pages):
        page_num = i + 1
        pages.append(
            (
                page_num,
                create_blog_preview(
                    posts=posts[i * posts_per_page : (i + 1) * posts_per_page],
                    page_num=page_num,
                    last_page=page_num == num_pages,
                    max_word_count=max_word_count,
                    config=config,
                ),
            )
        )

    pages = [
        (page_num, insert_blog_preview(blog_preview_template, page_content))
        for page_num, page_content in pages
    ]
    return pages


def create_tag_page(tag, posts, max_word_count, config):
    result = '---\ntitle: "Tag: {}"\n---\n\n'.format(tag)
    result += '<div id="blog_posts">\n\n'
    for i, post in enumerate(posts):
        if i > 0:
            result += "--------------\n\n"
        result += create_blog_post(post, max_word_count, config)

    result += "</div>\n\n"
    return tag, result


def create_tag_pages(tags, max_word_count, config):
    pages = []

    for tag, posts in tags.items():
        pages.append(create_tag_page(tag, posts, max_word_count, config))

    return pages


def write_pages(pages, build_directory, config):
    for page_num, content in pages:
        filenames = [
            "{0}{1}/page{2}.md".format(
                build_directory,
                config["DIR"]["blogpages"],
                page_num,
            )
        ]
        if page_num == 1:
            filenames.append(
                "{0}{1}/index.md".format(
                    build_directory, config["DIR"]["blog"]
                )
            )

        for filename in filenames:
            with open(filename, "w") as f:
               f.write(content)


def write_tag_pages(tag_pages, build_directory, config):
    for tag, content in tag_pages:
        filename = "{}{}/{}.md".format(
            build_directory, config["DIR"]["blogtags"], tag
        )

        with open(filename, "w") as f:
            f.write(content)


def main():
    config = configparser.ConfigParser()
    config.read(global_vars._CONFIG)

    posts_per_page = int(config["BLOG"].get("PostsPerPage", "-1"))
    max_word_count = int(config["BLOG"].get("MaxWordCount", "-1"))
    build_directory = sys.argv[1]

    blog_preview_template = parse_blog_preview_template(sys.argv[2])

    blog_posts = get_blog_posts()
    tags = get_tag_list(blog_posts)

    pages = create_blog_pages(
        blog_posts, blog_preview_template, posts_per_page, max_word_count, config
    )
    write_pages(pages, build_directory, config)

    tag_pages = create_tag_pages(tags, max_word_count, config)
    write_tag_pages(tag_pages, build_directory, config)


if __name__ == "__main__":
    main()
