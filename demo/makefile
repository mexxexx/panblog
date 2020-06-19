ASSETS_SRC = $(wildcard src/assets/*)
ASSETS_BUILD = $(foreach asset, $(ASSETS_SRC), $(patsubst src/%,bin/%,$(asset)))

BLOG_POSTS_SRC = $(wildcard src/blog/posts/*.md)
BLOG_POSTS_BUILD = $(foreach post, $(BLOG_POSTS_SRC), $(patsubst src/%.md,bin/%.html,$(post)))

BLOG_PAGES_SRC = $(wildcard bin/blog/pages/*.md)
BLOG_PAGES_BUILD = $(foreach page, $(BLOG_PAGES_SRC), $(patsubst %.md,%.html,$(page)))

BLOG_TAGS_SRC = $(wildcard bin/blog/tags/*.md)
BLOG_TAGS_BUILD = $(foreach tag, $(BLOG_TAGS_SRC), $(patsubst %.md,%.html,$(tag)))

all: assets html

assets: $(ASSETS_BUILD)

bin/assets/%: src/assets/%
	cp $^ $@

html: bin/css/style.css bin/include/menu.html bin/include/footer.html bin/about.html bin/index.html bin/test.html bin/blog/index.md $(BLOG_POSTS_BUILD) $(BLOG_PAGES_BUILD) $(BLOG_TAGS_BUILD)

bin/include/menu.html: src/include/menu.md
	pandoc -o $@ -s $^ --filter blog_menu_filter --metadata pagetitle="menu"
	blog_postprocessor menu $@

bin/include/footer.html: src/include/footer.md
	pandoc -o $@ -s $^ --filter blog_footer_filter --metadata pagetitle="footer"
	blog_postprocessor footer $@

bin/css/style.css: src/css/style.css
	cp $^ $@

bin/about.html: src/about.md bin/include/menu.html bin/include/footer.html bin/css/style.css
	pandoc -o $@ -s $< --filter blog_site_filter --css=css/style.css -B $(word 2,$^) -A $(word 3,$^) --section-divs
	blog_postprocessor site $@

bin/index.html: src/index.md bin/include/menu.html bin/include/footer.html bin/css/style.css
	pandoc -o $@ -s $< --filter blog_site_filter --css=css/style.css -B $(word 2,$^) -A $(word 3,$^) --section-divs
	blog_postprocessor site $@

bin/test.html: src/test.md bin/include/menu.html bin/include/footer.html bin/css/style.css
	pandoc -o $@ -s $< --filter blog_site_filter --css=css/style.css -B $(word 2,$^) -A $(word 3,$^) --section-divs
	blog_postprocessor site $@

bin/blog/index.html: bin/blog/index.md bin/include/menu.html bin/include/footer.html bin/css/style.css
	pandoc -o $@ -s $< --filter blog_site_filter --css=css/style.css -B $(word 2,$^) -A $(word 3,$^) --section-divs --metadata active-site="blog/index.html" 
	blog_postprocessor site $@

bin/blog/pages/%.html: bin/blog/pages/%.md bin/include/menu.html bin/include/footer.html bin/css/style.css
	pandoc -o $@ -s $< --filter blog_site_filter --css=css/style.css -B $(word 2,$^) -A $(word 3,$^) --section-divs --metadata active-site="blog/index.html" 
	blog_postprocessor site $@

bin/blog/tags/%.html: bin/blog/tags/%.md bin/include/menu.html bin/include/footer.html bin/css/style.css
	pandoc -o $@ -s $< --filter blog_site_filter --css=css/style.css -B $(word 2,$^) -A $(word 3,$^) --section-divs --metadata active-site="blog/index.html" 
	blog_postprocessor site $@

bin/blog/posts/%.html: src/blog/posts/%.md bin/include/menu.html bin/include/footer.html bin/css/style.css
	pandoc -o $@ -s $< --filter blog_site_filter --css=css/style.css -B $(word 2,$^) -A $(word 3,$^) --section-divs --metadata active-site="blog/index.html" 
	blog_postprocessor site $@

blog: bin/blog/index.md

bin/blog/index.md: src/blog/index.md $(BLOG_POSTS_SRC)
	blog_build bin/ $^

.PHONY: clean clean_all

clean:
	rm -f bin/include/menu.html bin/include/footer.html bin/blog/index.md $(BLOG_PAGES_SRC) $(BLOG_TAGS_SRC)

clean_all: clean
	rm -f bin/css/style.css bin/about.html bin/index.html bin/test.html $(ASSETS_BUILD)

