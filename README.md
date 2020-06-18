# Panblog

Panblog helps you to create a simple blog using only `markdown` files! Everything is statically built to html using pandoc, no `js` is required for the user.

## Installation

First, make sure you have the newest version of [pandoc](https://pandoc.org/) installed. Then, create a `pip` or `conda` environment and pip install `pandocfilters` and `beautifulsoup4`. Then, clone the repository and make sure you start with the following folder structure:

```
root
   makefile
   config.ini
-- tools
-- src
   index.md
   -- assets
   -- css
   -- blog
      index.md
      -- posts
   -- include
      menu.md
      footer.md
-- build
   -- assets
   -- css
   -- blog
      -- posts
      -- pages
      -- tags
   -- include
```

## Directory structure

You can change the directory structure by changing the apropriate paths in `config.ini` and `makefile`. 

### `src` and `build`

Inside the `src` directory you will write all your pages using markdown. When you run `make` and `make blog`, 
all pages will be statically compiled to `html` inside the same directories in `build`. When you link to any
page or asset from yur markdown file, make sure to link relative to the `src` path. For example ifyou want to
link to the file `src/blog/index.md` from `src/index.md`, you would use `[your link](blog/index.md)`. This
will get compiled as a absolute path to the resulting `html` file, so `<a href="[config.ini.BaseUrl]blog/index.html>`.

#### `index.md`

This is your main page

### `assets`

Place all images, PDFs or other assets inside of this directory and reference them with `assets/file.ext`.

### `css`

This is where the stylesheet `style.css` is. It can be edited to fit your needs.

### `include`

Inside of this directory you find the menu and footer. Edit them to fit your pages needs.

### `blog`

Here is where your your blog goes. `index.html` is the first page of the archive. You can write whatever text
you like, a summary of the blog entries will be displayed where the `<div id="blog_previews" />` tag is.

Any markdown file you create inside the `blog/posts` directory will be treated as a blog post. Make sure you include
a `title` and a `date` attribute for every post inside the markdown files header. You can also add tags using the 
`tags` attribute. Separete multiple tags with a semicolon `;`.

## Features

TODO: Explain Features

## Licence

The project is under the MIT licence. If you use it to write your blog, you don't need to include a reference to this
project, although it is appreciated. 