from . import sites
from . import init
from . import global_vars


def _create_make_file(pages, posts, config):
    panblog_posts_file = global_vars._PANBLOGDIR + "/" + global_vars._POSTS

    src_dir = config["DIR"]["source"] + "/"
    bin_dir = config["DIR"]["build"] + "/"
    include_dir = config["DIR"]["include"] + "/"
    css_dir = config["DIR"]["css"] + "/"
    asset_dir = config["DIR"]["assets"] + "/"
    blog_dir = config["DIR"]["blog"] + "/"
    blog_pages_dir = config["DIR"]["blogpages"] + "/"
    blog_posts_dir = config["DIR"]["blogposts"] + "/"
    blog_tags_dir = config["DIR"]["blogtags"] + "/"
    templates_dir = config["DIR"]["templates"] + "/"

    base_url = config["GENERAL"]["baseurl"]

    pages = [
        (
            src_dir + page["href"],
            bin_dir + page["href"][:-3] + ".html",
            src_dir + templates_dir + page["template"],
        )
        for page in pages
    ]

    posts = [
        (
            src_dir + blog_posts_dir + post["href"],
            bin_dir + blog_posts_dir + post["href"][:-3] + ".html",
            src_dir + templates_dir + post["template"],
        )
        for post in posts
    ]

    # include/menu.html
    menu = include_dir + "menu"
    menu_src = src_dir + menu + ".md"

    # include/footer.html
    footer = include_dir + "footer"
    footer_src = src_dir + footer + ".md"
    footer_bin = bin_dir + footer + ".html"

    # css/style.css
    css = css_dir + "style.css"
    css_src = src_dir + css
    css_bin = bin_dir + css

    # blog/index.md
    # blog_index = blog_dir + "index.md"
    # blog_index_src = src_dir + blog_index
    # blog_index_bin = bin_dir + blog_index

    # blog/pages/%.html
    # blog_pages_src = bin_dir + blog_pages_dir + "%.md"
    # blog_pages_bin = blog_pages_src[:-3] + ".html"

    # blog/tags/%.html
    # blog_tags_src = bin_dir + blog_tags_dir + "%.md"
    # blog_tags_bin = blog_tags_src[:-3] + ".html"

    # blog_wildcards_src = [blog_index_bin, blog_pages_src, blog_tags_src]
    # blog_wildcards_bin = [
    #    blog_index_bin[:-3] + ".html",
    #    blog_pages_bin,
    #    blog_tags_bin,
    # ]

    makefile = ""

    makefile += f"ASSETS_SRC = $(wildcard {src_dir}{asset_dir}*)\n"
    makefile += f"ASSETS_BUILD = $(foreach asset, $(ASSETS_SRC), $(patsubst {src_dir}%,{bin_dir}%,$(asset)))\n\n"

    makefile += f"PAGES_BUILD = {' '.join([page[1] for page in pages])}\n\n"
    makefile += f"POSTS_BUILD = {' '.join([post[1] for post in posts])}\n\n"

    # Targets
    makefile += "all: assets html\n\n"

    makefile += "assets: $(ASSETS_BUILD)\n\n"
    makefile += f"{bin_dir}{asset_dir}%: {src_dir}{asset_dir}%\n"
    makefile += "\tcp $^ $@\n\n"

    makefile += f"html: {css_bin} {footer_bin} $(PAGES_BUILD) $(POSTS_BUILD)\n\n"

    makefile += f"{css_bin}: {css_src}\n"
    makefile += "\tcp $^ $@\n\n"

    makefile += f"{footer_bin}: {footer_src}\n"
    makefile += f"\tpandoc -o $@ $< --filter panblog_site_filter\n\n"

    for src_file, bin_file, template in pages:
        makefile += f"{bin_file}: {src_file} {menu_src} {footer_bin}\n"
        makefile += f"\tpandoc -o $@ -s $< --filter panblog_site_filter --css={base_url + css} --metadata-file {menu_src} -A {footer_bin} --section-divs --template {template} \n\n"

    for src_file, bin_file, template in posts:
        makefile += f"{bin_file}: {src_file} {menu_src} {footer_bin}\n"
        makefile += f"\tpandoc -o $@ -s $< --filter panblog_site_filter --css={base_url + css} --metadata-file {menu_src} -A {footer_bin} --section-divs --template {template} --metadata active-site={blog_dir}index.html\n\n"

    # for o_bin, o_src in zip(posts_bin, posts_src):
    #    makefile += f"{o_bin}: {o_src} {menu_bin} {footer_bin}\n"
    #    makefile += f'\tpandoc -o $@ -s $< --filter panblog_site_filter --css={css} -B $(word 2,$^) -A $(word 3,$^) --section-divs --metadata active-site="{blog_index[:-3]}.html" \n'
    #    makefile += "\tpanblog_postprocessor site $@\n\n"

    # for o_bin, o_src in zip(blog_wildcards_bin, blog_wildcards_src):
    #    makefile += f"{o_bin}: {o_src} {menu_bin} {footer_bin}\n"
    #    makefile += f'\tpandoc -o $@ -s $< --filter panblog_site_filter --css={css} -B $(word 2,$^) -A $(word 3,$^) --section-divs --metadata active-site="{blog_index[:-3]}.html" \n'
    #    makefile += "\tpanblog_postprocessor site $@\n\n"

    # makefile += "blog: {}\n\n".format(blog_index_bin)

    # makefile += f"{blog_index_bin}: {blog_index_src} {' '.join(posts_src)} {panblog_posts_file}\n"
    # makefile += f"\tpanblog_bin {bin_dir} $(wordlist 1,{len(posts_src) + 1},$^)\n\n"

    makefile += ".PHONY: clean clean_all\n\n"

    makefile += "clean:\n"
    makefile += f"\trm -f {footer_bin}\n\n"

    makefile += "clean_all: clean\n"
    makefile += f"\trm -f {css_bin} $(ASSETS_BUILD) $(PAGES_BUILD) $(POSTS_BUILD)"

    # print(makefile)
    with open(global_vars._MAKEFILE, "w") as f:
        f.write(makefile)


def reload():
    config = init.load_config()
    init.check_init(config)
    pages = sites.read_tracked_pages()
    posts = sites.read_tracked_posts()

    _create_make_file(pages, posts, config)


def make():
    config = init.load_config()
    init.check_init(config)
