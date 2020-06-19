import os
import configparser

from . import global_vars

_DEFAULTS = {
    "GENERAL": {"baseurl": ("", "What is the Base Url of your blog?"),},
    "DIR": {
        "source": ("src", "Select a source directory."),
        "build": ("bin", "Select a build directory."),
        "css": ("css", "Where do you want to keep the .css files?"),
        "include": (
            "include",
            "Where do you want to keep static include files, e.g. the menu?",
        ),
        "assets": ("assets", "Where do you want to keep assets?"),
        "blog": ("blog", "In which directory do you want to keep the blog?"),
        "blogposts": (
            "blog/posts",
            "In which directory do you want to keep the blog posts?",
        ),
        "blogpages": (
            "blog/pages",
            "In which directory do you want to keep the blog overview pages?",
        ),
        "blogtags": (
            "blog/tags",
            "In which directory do you want to keep the blog tags?",
        ),
    },
    "BLOG": {
        "postsperpage" : (
            "10", "How many posts per page?"
        ),
        "maxwordcount" : (
            "200", "Maximum number of words to display."
        )
    }
}


def create_files(files):
    for f in files:
        with open(f, "w"):
            pass


def check_files(config):
    result = []

    if not os.path.isfile(global_vars._PANBLOGDIR + "/" + global_vars._SITES):
        result.append(global_vars._PANBLOGDIR + "/" + global_vars._SITES)

    menu = config["DIR"]["source"] + "/" + config["DIR"]["include"] + "/menu.md"
    if not os.path.isfile(menu):
        result.append(menu)

    footer = config["DIR"]["source"] + "/" + config["DIR"]["include"] + "/footer.md"
    if not os.path.isfile(footer):
        result.append(footer)

    blog_index = config["DIR"]["source"] + "/" + config["DIR"]["blog"] + "/index.md"
    if not os.path.isfile(blog_index):
        result.append(blog_index)

    return result


def create_dir_structure(dirs):
    for d in dirs:
        os.makedirs(d)


def check_dir_structure(config):
    result = []
    if not os.path.isdir(global_vars._PANBLOGDIR):
        result.append(global_vars._PANBLOGDIR)

    src = config["DIR"]["source"]
    if not os.path.isdir(src):
        result.append(src)

    if not os.path.isdir(src + "/" + config["DIR"]["blog"]):
        result.append(src + "/" + config["DIR"]["blog"])

    if not os.path.isdir(src + "/" + config["DIR"]["blogposts"]):
        result.append(src + "/" + config["DIR"]["blogposts"])

    if not os.path.isdir(src + "/" + config["DIR"]["css"]):
        result.append(src + "/" + config["DIR"]["css"])

    if not os.path.isdir(src + "/" + config["DIR"]["include"]):
        result.append(src + "/" + config["DIR"]["include"])

    if not os.path.isdir(src + "/" + config["DIR"]["assets"]):
        result.append(src + "/" + config["DIR"]["assets"])

    build = config["DIR"]["build"]
    if not os.path.isdir(build):
        result.append(build)

    if not os.path.isdir(build + "/" + config["DIR"]["blog"]):
        result.append(build + "/" + config["DIR"]["blog"])

    if not os.path.isdir(build + "/" + config["DIR"]["blogposts"]):
        result.append(build + "/" + config["DIR"]["blogposts"])

    if not os.path.isdir(build + "/" + config["DIR"]["blogpages"]):
        result.append(build + "/" + config["DIR"]["blogpages"])

    if not os.path.isdir(build + "/" + config["DIR"]["blogtags"]):
        result.append(build + "/" + config["DIR"]["blogtags"])

    if not os.path.isdir(build + "/" + config["DIR"]["css"]):
        result.append(build + "/" + config["DIR"]["css"])

    if not os.path.isdir(build + "/" + config["DIR"]["include"]):
        result.append(build + "/" + config["DIR"]["include"])

    if not os.path.isdir(build + "/" + config["DIR"]["assets"]):
        result.append(build + "/" + config["DIR"]["assets"])

    return result


def load_config():
    config = configparser.ConfigParser()

    if os.path.isfile(global_vars._CONFIG):
        config.read(global_vars._CONFIG)

    return config


def check_config(config):
    result = {"sections": [], "vars": []}

    for section, settings in _DEFAULTS.items():
        if section not in config:
            result["sections"].append(section)

        for k, v in settings.items():
            if section not in config or k not in config[section]:
                result["vars"].append((k, v))
    return result


def create_config(config, config_to_add):
    for section in config_to_add["sections"]:
        config[section] = {}

    for k, v in config_to_add["vars"]:
        selection = input('{} ("{}"):'.format(v[1], v[0])).strip()
        if not selection:
            selection = v[0]
        config[section][k] = selection

    if config_to_add["sections"] or config_to_add["vars"]:
        with open(global_vars._CONFIG, "w") as configfile:
            config.write(configfile)


def check_init(config):
    try:
        config_to_add = check_config(config)
        if config_to_add["sections"] or config_to_add["vars"]:
            raise ValueError()

        dirs_to_create = check_dir_structure(config)
        if dirs_to_create:
            raise ValueError()

        files_to_create = check_files(config)
        if files_to_create:
            raise ValueError()
    except:
        raise ValueError("Directory not correctly initialized. Run init first.")


def init():
    config = load_config()
    config_to_add = check_config(config)
    create_config(config, config_to_add)

    dirs_to_create = check_dir_structure(config)
    create_dir_structure(dirs_to_create)

    files_to_create = check_files(config)
    create_files(files_to_create)
