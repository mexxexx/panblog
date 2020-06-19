from setuptools import setup


def readme():
    with open("README.md") as readme_file:
        return readme_file.read()


configuration = {
    "name": "panblog",
    "version": "0.1",
    "python_requires": ">=3.6",
    "author": "Max Mihailescu",
    "author_email": "mihailescu.m@gmx.de",
    "description": (),
    "long_description_content_type": "text/x-rst",
    "long_description": readme(),
    "classifiers": [
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3.6",
    ],
    "keywords": "",
    "url": "https://github.com/mexxexx/panblog",
    "license": "MIT",
    "packages": ["panblog"],
    "install_requires": ["pandocfilters"],
    "ext_modules": [],
    "cmdclass": {},
    "tests_require": ["pytest"],
    "data_files": (),
    "extras_require": {},
    "entry_points": {
        "console_scripts": [
            "blog = panblog.__main__:main",
            "blog_menu_filter = panblog.menu_filter:main",
            "blog_footer_filter = panblog.footer_filter:main",
            "blog_site_filter = panblog.site_filter:main",
            "blog_postprocessor = panblog.postprocessor:main",
            "blog_build = panblog.build_blog:main",
        ],
    },
}

setup(**configuration)
