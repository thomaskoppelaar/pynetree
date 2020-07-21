# Pynetree

Markdown + Base HTML + Python -> HTML Page

## Goal

Generate HTML using Markdown, an HTML template and a Python script.

Designed for personal use on linux; I can't guarantee this will work on any other platform.

## Usage

1. Clone this repo
2. `cd` to root
3. `python generate.py`

## Syntax

The python script operates on 5 variables: 

```py
inputfolder_name = "input"
outputfolder_name = "output"

basefile_name = "base.html"

bodyfile_name = "body.md"

outputfile_name = "index.html"
```

`basefile_name` is the base HTML template that will be scanned through first for any occurances of the following regex: 

`\{\{(.*)\.md\}\}`

Examples: `{{body.md}}`, `{{post,md}}`. `{{file.md}}`.

Once it finds this line, it will **replace the entire line** with the contents of the file, and convert the markdown into HTML.

The markdown conversion mainly consists of (poorly hand-tested) regex, and doesn't work flawlessly. Example: `this **bold** text shouldn't officially be rendered bold.` 

Feel free to try it out. It's a few lines of Python, have fun with it.