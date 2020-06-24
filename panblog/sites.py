from . import init
from . import global_vars


def read_tracked_pages():
    with open(global_vars._PANBLOGDIR + "/" + global_vars._PAGES, "r") as f:
        lines = f.read().splitlines()

    pages = []
    for line in lines[1:]:
        values = line.split(";")
        pages.append({"href": values[0], "template": values[1]})
    return pages


def read_tracked_posts():
    with open(global_vars._PANBLOGDIR + "/" + global_vars._POSTS, "r") as f:
        lines = f.read().splitlines()

    posts = []
    for line in lines[1:]:
        values = line.split(";")
        posts.append({"href": values[0], "template": values[1]})
    return posts


def read_tracked_blog_pages():
    with open(global_vars._PANBLOGDIR + "/" + global_vars._BLOG_PAGES, "r") as f:
        lines = f.read().splitlines()

    pages = []
    for line in lines[1:]:
        values = line.split(";")
        pages.append({"href": values[0], "base_file": values[1], "template": values[2]})
    return pages


def _write_tracked_pages(pages):
    s = "href;template\n"
    for page in pages:
        s += page["href"] + ";" + page["template"] + "\n"

    with open(global_vars._PANBLOGDIR + "/" + global_vars._PAGES, "w") as f:
        f.write(s)


def _write_tracked_posts(posts):
    s = "href;template\n"
    for post in posts:
        s += post["href"] + ";" + post["template"] + "\n"

    with open(global_vars._PANBLOGDIR + "/" + global_vars._POSTS, "w") as f:
        f.write(s)


def _write_tracked_blog_pages(pages):
    s = "href;base_file;template\n"
    for page in pages:
        s += page["href"] + ";" + page["base_file"] + ";" + page["template"] + "\n"

    with open(global_vars._PANBLOGDIR + "/" + global_vars._BLOG_PAGES, "w") as f:
        f.write(s)


def add_page(page, template="page.html"):
    if isinstance(page, list):
        page = page[0]
    page = read_tracked_pages()
    if page not in [p["href"] for p in pages]:
        pages.append({"href": page, "template": template})
    else:
        raise ValueError("{} is already a tracked page.".format(f))
    _write_tracked_pages(pages)


def add_post(post, template="post.html"):
    if isinstance(post, list):
        post = post[0]
    posts = read_tracked_posts()
    if post not in [p["href"] for p in posts]:
        posts.append({"href": post, "template": template})
    else:
        raise ValueError("{} is already a tracked page.".format(post))
    _write_tracked_posts(posts)


def add_blog_page(page, base_file, template="blog.html"):
    if isinstance(page, list):
        page = page[0]
    blog_pages = read_tracked_blog_pages()
    if page not in [p["href"] for p in blog_pages]:
        blog_pages.append({"href": page, "base_file": base_file, "template": template})
    else:
        raise ValueError("{} is already a tracked page.".format(page))
    _write_tracked_blog_pages(blog_pages)


def remove(files):
    if type(files) != list:
        files = [files]

    pages = read_tracked_pages()
    posts = read_tracked_posts()
    blog_pages = read_tracked_blog_pages()
    for f in files:
        if f in pages:
            pages.remove(f)
        elif f in posts:
            posts.remove(f)
        elif f in blog_pages:
            blog_pages.remove(f)
        else:
            raise ValueError("{} is not a tracked site.".format(f))

    _write_tracked_pages(pages)
    _write_tracked_posts(posts)
    _write_tracked_blog_pages(blog_pages)


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
