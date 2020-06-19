from . import sites
from . import init
from . import global_vars


def _create_make_file(sites, config):
    src_dir = config["DIR"]["source"] + "/"
    build_dir = config["DIR"]["build"] + "/"
    include_dir = config["DIR"]["include"] + "/"
    css_dir = config["DIR"]["css"] + "/"
    asset_dir = config["DIR"]["assets"] + "/"
    blog_dir = config["DIR"]["blog"] + "/"
    blog_pages_dir = config["DIR"]["blogpages"] + "/"
    blog_posts_dir = config["DIR"]["blogposts"] + "/"
    blog_tags_dir = config["DIR"]["blogtags"] + "/"

    obj_src = [src_dir + site[:-5] + ".md" for site in sites]
    obj_build = [build_dir + site for site in sites]

    menu = include_dir + "menu"
    menu_src = src_dir + menu + ".md"
    menu_build = build_dir + menu + ".html"

    footer = include_dir + "footer"
    footer_src = src_dir + footer + ".md"
    footer_build = build_dir + footer + ".html"

    css = css_dir + "style.css"
    css_src = src_dir + css
    css_build = build_dir + css

    blog_index = blog_dir + "index.md"
    blog_index_src = src_dir + blog_index
    blog_index_build = build_dir + blog_index

    blog_pages_src = build_dir + blog_pages_dir + "%.md"
    blog_pages_build = blog_pages_src[:-3] + ".html"

    blog_tags_src = build_dir + blog_tags_dir + "%.md"
    blog_tags_build = blog_tags_src[:-3] + ".html"
    
    blog_posts = blog_posts_dir + "%"
    blog_posts_src = src_dir + blog_posts + ".md"
    blog_posts_build = build_dir + blog_posts + ".html"

    blog_wildcards_src = [blog_index_build, blog_pages_src, blog_tags_src, blog_posts_src]
    blog_wildcards_build = [blog_index_build[:-3] + ".html", blog_pages_build, blog_tags_build, blog_posts_build]

    makefile = ""

    makefile += "ASSETS_SRC = $(wildcard {}{}*)\n".format(src_dir, asset_dir)
    makefile += "ASSETS_BUILD = $(foreach asset, $(ASSETS_SRC), $(patsubst {}%,{}%,$(asset)))\n\n".format(
        src_dir, build_dir
    )

    makefile += "BLOG_POSTS_SRC = $(wildcard {}{}*.md)\n".format(src_dir, blog_posts_dir)
    makefile += "BLOG_POSTS_BUILD = $(foreach post, $(BLOG_POSTS_SRC), $(patsubst {}%.md,{}%.html,$(post)))\n\n".format(
        src_dir, build_dir
    )
    
    makefile += "BLOG_PAGES_SRC = $(wildcard {}{}*.md)\n".format(build_dir, blog_pages_dir)
    makefile += "BLOG_PAGES_BUILD = $(foreach page, $(BLOG_PAGES_SRC), $(patsubst %.md,%.html,$(page)))\n\n".format(
        src_dir, build_dir
    )
    
    makefile += "BLOG_TAGS_SRC = $(wildcard {}{}*.md)\n".format(build_dir, blog_tags_dir)
    makefile += "BLOG_TAGS_BUILD = $(foreach tag, $(BLOG_TAGS_SRC), $(patsubst %.md,%.html,$(tag)))\n\n".format(
        src_dir, build_dir
    )

    # Targets
    makefile += "all: assets html\n\n"

    makefile += "assets: $(ASSETS_BUILD)\n\n"
    makefile += f"{build_dir}{asset_dir}%: {src_dir}{asset_dir}%\n"
    makefile += "\tcp $^ $@\n\n"

    makefile += "html: {} {} {} {} {} $(BLOG_POSTS_BUILD) $(BLOG_PAGES_BUILD) $(BLOG_TAGS_BUILD)\n\n".format(
        css_build, menu_build, footer_build, " ".join(obj_build), blog_index_build
    )

    makefile += f"{menu_build}: {menu_src}\n"
    makefile += (
        '\tpandoc -o $@ -s $^ --filter blog_menu_filter --metadata pagetitle="menu"\n'
    )
    makefile += "\tblog_postprocessor menu $@\n\n"

    makefile += f"{footer_build}: {footer_src}\n"
    makefile += '\tpandoc -o $@ -s $^ --filter blog_footer_filter --metadata pagetitle="footer"\n'
    makefile += "\tblog_postprocessor footer $@\n\n"

    makefile += f"{css_build}: {css_src}\n"
    makefile += "\tcp $^ $@\n\n"

    for o_build, o_src in zip(obj_build, obj_src):
        makefile += f"{o_build}: {o_src} {menu_build} {footer_build} {css_build}\n"
        makefile += f"\tpandoc -o $@ -s $< --filter blog_site_filter --css={css} -B $(word 2,$^) -A $(word 3,$^) --section-divs\n"
        makefile += "\tblog_postprocessor site $@\n\n"
        
    for o_build, o_src in zip(blog_wildcards_build, blog_wildcards_src):
        makefile += f"{o_build}: {o_src} {menu_build} {footer_build} {css_build}\n"
        makefile += f"\tpandoc -o $@ -s $< --filter blog_site_filter --css={css} -B $(word 2,$^) -A $(word 3,$^) --section-divs --metadata active-site=\"{blog_index[:-3]}.html\" \n"
        makefile += "\tblog_postprocessor site $@\n\n"

    makefile += "blog: {}\n\n".format(blog_index_build)

    makefile += "{}: {} $(BLOG_POSTS_SRC)\n".format(blog_index_build, blog_index_src)
    makefile += "\tblog_build {} $^\n\n".format(build_dir)

    makefile += ".PHONY: clean clean_all\n\n"

    makefile += "clean:\n"
    makefile += f"\trm -f {menu_build} {footer_build} {blog_index_build} $(BLOG_PAGES_SRC) $(BLOG_TAGS_SRC)\n\n"

    makefile += "clean_all: clean\n"
    makefile += "\trm -f {} {} $(ASSETS_BUILD)\n\n".format(
        css_build, " ".join(obj_build)
    )

    print(makefile)
    with open(global_vars._MAKEFILE, "w") as f:
        f.write(makefile)


def reload():
    config = init.load_config()
    init.check_init(config)
    tracked_sites = sites.read_tracked_sites()

    _create_make_file(tracked_sites, config)


def make():
    config = init.load_config()
    init.check_init(config)
