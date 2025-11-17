# static-site-generator

## [Home](/) [About](/about/) [Plumbing](/plumbing/) [Contact](/contact/)

This is a static site generator based on the [boot.dev](https://www.boot.dev) [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) project

## Usage

This project contains two bash files, `main.sh` and `build.sh`

#### **_main.sh_**

- Copies the content from the static folder
- Generates the site based on the files in the content directory
- Opens an http server on port 8888

#### **_build.sh_**

- Contains a base path variable for the base path of the site
- Generates the site using the base path

## Structure

```
static-site-generator
>content        --main directory of the site, this is where the markdown files go :)
->index.md      --homepage content
->subdirectory  --additional page directory
-->index.md     --additional page content
>static         --directory for all of the static site content, such as images, stylesheets, etc
>docs           --generated content will appear within this directory
>src            --program source code files
```

## Configuration

### **main.sh**

```
PORT=8888                         #the port that the http server will run on
basepath = "/"                    #the "base" filepath, or the base directory for the website, used to generate links
```

### **main.py**

```
dest_path = "docs"                #filepath for where the generated content should be created
static_path = "static"            #filepath where the static site content is located
content_path = "content"          #filepath where the site content is located
template_path = "template.html"   #filepath of the template file
```