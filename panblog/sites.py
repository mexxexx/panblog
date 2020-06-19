from . import init
from . import global_vars


def read_tracked_sites():
    with open(global_vars._PANBLOGDIR + "/" + global_vars._SITES, "r") as f:
        sites = f.read().splitlines()
    return sites


def _write_tracked_sites(sites):
    with open(global_vars._PANBLOGDIR + "/" + global_vars._SITES, "w") as f:
        f.write("\n".join(sites))
    return sites


def add_files(files):
    if type(files) != list:
        files = [files]

    sites = read_tracked_sites()
    for f in files:
        if f not in sites:
            sites.append(f)
        else:
            raise ValueError("{} is already a tracked site.".format(f))
    _write_tracked_sites(sites)


def remove_files(files):
    if type(files) != list:
        files = [files]

    sites = read_tracked_sites()
    for f in files:
        if f in sites:
            sites.remove(f)
        else:
            raise ValueError("{} is not a tracked site.".format(f))

    _write_tracked_sites(sites)


def list_sites(print_sites):
    config = init.load_config()
    init.check_init(config)

    sites = read_tracked_sites()

    if print_sites:
        print("\n".join(sites))
