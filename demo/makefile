ASSETS_SRC = $(wildcard src/assets/*)
ASSETS_BUILD = $(foreach asset, $(ASSETS_SRC), $(patsubst src/%,bin/%,$(asset)))

PAGES_BUILD = bin/index.html bin/about.html bin/test.html

POSTS_BUILD = bin/blog/posts/entry1.html

all: assets html

assets: $(ASSETS_BUILD)

bin/assets/%: src/assets/%
	cp $^ $@

html: bin/css/style.css bin/include/footer.html $(PAGES_BUILD) $(POSTS_BUILD)

bin/css/style.css: src/css/style.css
	cp $^ $@

bin/include/footer.html: src/include/footer.md
	pandoc -o $@ $< --filter panblog_site_filter

bin/index.html: src/index.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md -A bin/include/footer.html --section-divs --template src/templates/page.html 

bin/about.html: src/about.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md -A bin/include/footer.html --section-divs --template src/templates/page.html 

bin/test.html: src/test.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md -A bin/include/footer.html --section-divs --template src/templates/page.html 

bin/blog/posts/entry1.html: src/blog/posts/entry1.md src/include/menu.md bin/include/footer.html
	pandoc -o $@ -s $< --filter panblog_site_filter --css=/css/style.css --metadata-file src/include/menu.md -A bin/include/footer.html --section-divs --template src/templates/post.html --metadata active-site=blog/index.html

.PHONY: clean clean_all

clean:
	rm -f bin/include/footer.html

clean_all: clean
	rm -f bin/css/style.css $(ASSETS_BUILD) $(PAGES_BUILD) $(POSTS_BUILD)