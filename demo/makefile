ASSETS_SRC = $(wildcard src/assets/*)
ASSETS_BUILD = $(foreach asset, $(ASSETS_SRC), $(patsubst src/%,bin/%,$(asset)))

PAGES_BUILD = bin/about.html bin/test.html
POSTS_BUILD = bin/blog/posts/entry2.html bin/blog/posts/entry3.html bin/blog/posts/entry1.html

BLOG_PAGES_SRC = bin/blog/index.md bin/blog/pages/index.md bin/blog/pages/page1.md bin/blog/pages/page2.md bin/blog/tags/index.md bin/blog/tags/tag1.md bin/blog/tags/tag2.md bin/blog/tags/tag3.md

BLOG_PAGES_BUILD = bin/blog/index.html bin/blog/pages/index.html bin/blog/pages/page1.html bin/blog/pages/page2.html bin/blog/tags/index.html bin/blog/tags/tag1.html bin/blog/tags/tag2.html bin/blog/tags/tag3.html

all: assets html

assets: $(ASSETS_BUILD)

bin/assets/%: src/assets/%
	cp $^ $@

html: bin/css/style.css bin/include/footer.html $(PAGES_BUILD) $(POSTS_BUILD) $(BLOG_PAGES_BUILD)

bin/css/style.css: src/css/style.css
	cp $^ $@

bin/include/footer.html: src/include/footer.md
	pandoc -o $@ $< --filter panblog_site_filter

bin/about.html: src/about.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md -A bin/include/footer.html --section-divs --template src/templates/page.html 

bin/test.html: src/test.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md -A bin/include/footer.html --section-divs --template src/templates/page.html 

bin/blog/posts/entry2.html: src/blog/posts/entry2.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md -A bin/include/footer.html --section-divs --template src/templates/post.html --metadata active-site=/blog/index.html

bin/blog/posts/entry3.html: src/blog/posts/entry3.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md -A bin/include/footer.html --section-divs --template src/templates/post.html --metadata active-site=/blog/index.html

bin/blog/posts/entry1.html: src/blog/posts/entry1.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md -A bin/include/footer.html --section-divs --template src/templates/post.html --metadata active-site=/blog/index.html

bin/blog/index.html: src/blog/index.md bin/blog/index.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md --metadata-file bin/blog/index.md -A bin/include/footer.html --section-divs --template src/templates/blog.html --metadata active-site=/blog/index.html

bin/blog/pages/index.html: src/blog/index.md bin/blog/pages/index.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md --metadata-file bin/blog/pages/index.md -A bin/include/footer.html --section-divs --template src/templates/blog.html --metadata active-site=/blog/index.html

bin/blog/pages/page1.html: src/blog/index.md bin/blog/pages/page1.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md --metadata-file bin/blog/pages/page1.md -A bin/include/footer.html --section-divs --template src/templates/blog.html --metadata active-site=/blog/index.html

bin/blog/pages/page2.html: src/blog/index.md bin/blog/pages/page2.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md --metadata-file bin/blog/pages/page2.md -A bin/include/footer.html --section-divs --template src/templates/blog.html --metadata active-site=/blog/index.html

bin/blog/tags/index.html: bin/blog/tags/index.md bin/blog/tags/index.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md --metadata-file bin/blog/tags/index.md -A bin/include/footer.html --section-divs --template src/templates/tag_index.html --metadata active-site=/blog/index.html

bin/blog/tags/tag1.html: bin/blog/tags/tag1.md bin/blog/tags/tag1.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md --metadata-file bin/blog/tags/tag1.md -A bin/include/footer.html --section-divs --template src/templates/tag.html --metadata active-site=/blog/index.html

bin/blog/tags/tag2.html: bin/blog/tags/tag2.md bin/blog/tags/tag2.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md --metadata-file bin/blog/tags/tag2.md -A bin/include/footer.html --section-divs --template src/templates/tag.html --metadata active-site=/blog/index.html

bin/blog/tags/tag3.html: bin/blog/tags/tag3.md bin/blog/tags/tag3.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md --metadata-file bin/blog/tags/tag3.md -A bin/include/footer.html --section-divs --template src/templates/tag.html --metadata active-site=/blog/index.html

.PHONY: clean clean_all

clean:
	rm -f bin/include/footer.html $(BLOG_PAGES_SRC)

clean_all: clean
	rm -f bin/css/style.css $(ASSETS_BUILD) $(PAGES_BUILD) $(POSTS_BUILD) $(BLOG_PAGES_BUILD)