# Static Site Generator

A static site generator written in Python, built as part of the [Boot.dev](https://www.boot.dev) "Build a Static Site Generator" course. It converts Markdown files into a full static HTML website.

Demo content lives in `content/` — a small Tolkien fan site — deployed via GitHub Pages at [aleksa898989.github.io/static_site_generator](https://aleksa898989.github.io/static_site_generator/).

## How it works

- Markdown files in `content/` are parsed into an intermediate node tree (inline text nodes → HTML nodes).
- Each Markdown file is wrapped in `template.html` and written out as an `.html` file, mirroring the `content/` directory structure.
- Static assets (`static/`) are copied alongside the generated pages.

## Usage

```sh
./test.sh    # run the unit test suite
./main.sh    # generate the site into docs/ and serve it locally at http://localhost:8888
./build.sh   # generate a production build with the GitHub Pages base path
```
