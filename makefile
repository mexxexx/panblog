OBJ = index.html test.html about.html

MENU = menu
FOOTER = footer
CSS = style.css

SRC_DIR = src
BUILD_DIR = build
INCLUDE_DIR = include

CSS_DIR = css
ASSET_DIR = assets

BLOG_DIR = blog
BLOG_POST_DIR = blog/posts
BLOG_PAGES_DIR = blog/pages
BLOG_TAGS_DIR = blog/tags

ASSETS = $(wildcard $(SRC_DIR)/$(ASSET_DIR)/*)
BUILD_ASSETS = $(foreach asset, $(ASSETS), $(patsubst $(SRC_DIR)/%, $(BUILD_DIR)/%, $(asset)))

CSS := $(CSS_DIR)/$(CSS)
BUILD_INCLUDES = $(BUILD_DIR)/$(INCLUDE_DIR)/$(MENU).html $(BUILD_DIR)/$(INCLUDE_DIR)/$(FOOTER).html
BUILD_OBJ = $(foreach obj, $(OBJ), $(BUILD_DIR)/$(obj))
BUILD_CSS = $(BUILD_DIR)/$(CSS)

BLOG_POSTS = $(wildcard $(SRC_DIR)/$(BLOG_POST_DIR)/*.md)
BLOG_POSTS_BUILD = $(foreach post, $(BLOG_POSTS), $(patsubst $(SRC_DIR)/%.md, $(BUILD_DIR)/%.html, $(post)))

BLOG_PAGES = $(BUILD_DIR)/$(BLOG_DIR)/index.md $(wildcard $(BUILD_DIR)/$(BLOG_PAGES_DIR)/page*.md)
BLOG_PAGES_BUILD = $(foreach ov, $(BLOG_PAGES), $(patsubst %.md, %.html, $(ov)))

TAG_PAGES = $(wildcard $(BUILD_DIR)/$(BLOG_TAGS_DIR)/*.md)
TAG_PAGES_BUILD = $(foreach ov, $(TAG_PAGES), $(patsubst %.md, %.html, $(ov)))

all : blog assets html

# Building the menu
$(BUILD_DIR)/$(INCLUDE_DIR)/$(MENU).html : $(SRC_DIR)/$(INCLUDE_DIR)/$(MENU).md
	pandoc -o $@ -s $^ --filter tools/menu_filter.py --metadata pagetitle="menu"
	python tools/postprocessor.py menu $@

# Building the footer
$(BUILD_DIR)/$(INCLUDE_DIR)/$(FOOTER).html : $(SRC_DIR)/$(INCLUDE_DIR)/$(FOOTER).md
	pandoc -o $@ -s $^ --filter tools/footer_filter.py --metadata pagetitle="footer"
	python tools/postprocessor.py footer $@

# Building all html sites
$(BUILD_DIR)/%.html: $(SRC_DIR)/%.md $(BUILD_INCLUDES)
	pandoc -o $@ -s $< --filter tools/site_filter.py --css=$(CSS) -B $(word 2,$^) -A $(word 3,$^) --section-divs
	python tools/postprocessor.py site $@

# Building all blog posts
$(BUILD_DIR)/$(BLOG_POST_DIR)/%.html: $(SRC_DIR)/$(BLOG_POST_DIR)/%.md $(BUILD_INCLUDES)
	pandoc -o $@ -s $< --filter tools/site_filter.py --css=$(CSS) -B $(word 2,$^) -A $(word 3,$^) --metadata active-site="blog/index.html" --section-divs
	python tools/postprocessor.py site $@

# Building all blog previews
$(BUILD_DIR)/$(BLOG_PAGES_DIR)/%.html: $(BUILD_DIR)/$(BLOG_PAGES_DIR)/%.md $(BUILD_INCLUDES)
	pandoc -o $@ -s $< --filter tools/site_filter.py --css=$(CSS) -B $(word 2,$^) -A $(word 3,$^) --metadata active-site="blog/index.html" --section-divs
	python tools/postprocessor.py site $@

# Building blog previews index
$(BUILD_DIR)/$(BLOG_DIR)/index.html: $(BUILD_DIR)/$(BLOG_DIR)/index.md $(BUILD_INCLUDES)
	pandoc -o $@ -s $< --filter tools/site_filter.py --css=$(CSS) -B $(word 2,$^) -A $(word 3,$^) --metadata active-site="blog/index.html" --section-divs
	python tools/postprocessor.py site $@
	
# Building all tag pages
$(BUILD_DIR)/$(BLOG_TAGS_DIR)/%.html: $(BUILD_DIR)/$(BLOG_TAGS_DIR)/%.md $(BUILD_INCLUDES)
	pandoc -o $@ -s $< --filter tools/site_filter.py --css=$(CSS) -B $(word 2,$^) -A $(word 3,$^) --metadata active-site="blog/index.html" --section-divs
	python tools/postprocessor.py site $@

# Copy CSS file
$(BUILD_DIR)/%.css: $(SRC_DIR)/%.css
	cp $^ $@	

# Copy assets
$(BUILD_DIR)/$(ASSET_DIR)/%: $(SRC_DIR)/$(ASSET_DIR)/%
	cp $^ $@

assets: $(BUILD_ASSETS)

html: $(BUILD_CSS) $(BUILD_OBJ) $(BLOG_POSTS_BUILD) $(BLOG_PAGES_BUILD) $(TAG_PAGES_BUILD)

# Build blog overviews
$(BUILD_DIR)/$(BLOG_DIR)/index.md : $(SRC_DIR)/$(BLOG_DIR)/index.md $(BLOG_POSTS)
	python tools/build_blog.py $(BUILD_DIR) $^

blog: $(BUILD_DIR)/$(BLOG_DIR)/index.md

.PHONY: clean clean_build

clean:
	rm -f $(BUILD_INCLUDES) $(BLOG_PAGES) $(TAG_PAGES)

clean_build: clean
	rm -f $(BUILD_OBJ) $(BUILD_ASSETS) $(BUILD_CSS) $(BLOG_PAGES_BUILD) $(BLOG_POSTS_BUILD) $(TAG_PAGES_BUILD)