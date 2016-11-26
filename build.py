#!/usr/bin/env python

import jinja2
import os, fnmatch, shutil

print("building")

# copy all non-template dirs to dist dir
# interpolate all html files
# bob's yer uncle

def walk_files(source):
    for root, dirnames, filenames in os.walk(source):
        #for filename in fnmatch.filter(filenames, '*.html'):
        for filename in filenames:
            path = os.path.join(root, filename)
            relpath = os.path.relpath(path, source)
            yield path, relpath

def copy_file(source_path, rel_path, dest_path):
    print("COPY {} --> {}".format(source_path, dest_path))

    dirname = os.path.dirname(dest_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    if source_path.endswith('.html') and not source_path.startswith('src/scripts'):
        # template vars if needed

        template = template_env.get_template(rel_path)
        contents = template.render()

        with open(dest_path, 'w') as fh:
            fh.write(contents)

    else:
        # simple file copy if non-html
        shutil.copy2(source_path, dest_path)



def copy_files(source, dest):
    for (source_path, relpath) in walk_files(source):
        dest_path = os.path.join(dest, relpath)
        if 'src/templates' not in source_path:
            copy_file(source_path, relpath, dest_path)


template_env = jinja2.Environment(loader=jinja2.FileSystemLoader('./src/'))
copy_files('src', 'dist')
