from . import init
from . import global_vars


def read_tracked_pages():
    with open(global_vars._PANBLOGDIR + "/" + global_vars._PAGES, "r") as f:
        lines = f.read().splitlines()

    pages = []
    for line in lines:
        values = line.split(";")
        pages.append({"href": values[0], "template": values[1]})
    return pages


def read_tracked_posts():
    with open(global_vars._PANBLOGDIR + "/" + global_vars._POSTS, "r") as f:
        lines = f.read().splitlines()

    posts = []
    for line in lines:
        values = line.split(";")
        posts.append({"href": values[0], "template": values[1]})
    return posts


def _write_tracked_pages(pages):
    s = ""
    for page in pages:
        s += page["href"] + ";" + page["template"] + "\n"

    with open(global_vars._PANBLOGDIR + "/" + global_vars._PAGES, "w") as f:
        f.write(s)


def _write_tracked_posts(posts):
    s = ""
    for post in posts:
        s += post["href"] + ";" + post["template"] + "\n"

    with open(global_vars._PANBLOGDIR + "/" + global_vars._POSTS, "w") as f:
        f.write(s)


def add_pages(files):
    if not isinstance(files, list):
        files = [files]
    pages = read_tracked_pages()
    for f in files:
        if f not in pages:
            pages.append({"href": f, "template": "page.html"})
        else:
            raise ValueError("{} is already a tracked page.".format(f))
    _write_tracked_pages(pages)


def add_posts(files):
    if not isinstance(files, list):
        files = [files]
    posts = read_tracked_posts()
    for f in files:
        if f not in posts:
            posts.append({"href": f, "template": "post.html"})
        else:
            raise ValueError("{} is already a tracked page.".format(f))
    _write_tracked_posts(posts)


def remove(files):
    if type(files) != list:
        files = [files]

    pages = read_tracked_pages()
    posts = read_tracked_posts()
    for f in files:
        if f in pages:
            pages.remove(f)
        elif f in posts:
            posts.remove(f)
        else:
            raise ValueError("{} is not a tracked site.".format(f))

    _write_tracked_pages(pages)
    _write_tracked_posts(posts)


def list_files():
    config = init.load_config()
    init.check_init(config)

    pages = read_tracked_pages()
    posts = read_tracked_posts()

    print("Pages:")
    for page in pages:
        print("{:<30} {:<30}".format(page["href"], page["template"]))

    print("\nPosts:")
    for post in posts:
        print("{:<30} {:<30}".format(post["href"], post["template"]))
