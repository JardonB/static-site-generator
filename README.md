# static-site-generator
This is a static site generator based on the boot.dev static site generator project

## Usage
This project contains two bash files, `main.sh` and `build.sh`

**_main.sh_**
- Copies the content from the static folder
- Generates the site based on the files in the content directory
- Opens an http server on port 8888

**_build.sh_**
- Contains a base path variable for the base path of the site
- Generates the site using the base path

## Structure
**static-site-generator**
┣content        _--main directory of the site, this is where the markdown files go :)_
┃┣index.md      _--homepage content_
┃┗subdirectory  _--additional page directory_
┃ ┗index.md     _--additional page content_
┣static         _--directory for all of the static site content, such as images, stylesheets, etc_
┣docs           _--generated content will appear within this directory
┗src            _--program source code files_

## Configuration
**main.sh**
- PORT=8888                         _--the port that the http server will run on_

**main.py**
- dest_path = "docs"                _--filepath for where the generated content should be created_
- static_path = "static"            _--filepath where the static site content is located_
- content_path = "content"          _--filepath where the site content is located_
- template_path = "template.html"   _--filepath of the template file_
- base_path = "/"                   _--the "base" filepath, or the base directory for the website, used to generate links_