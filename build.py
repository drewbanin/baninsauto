#!/usr/bin/env python

import jinja2
import os, fnmatch, shutil, json

print("building")

# copy all non-template dirs to dist dir
# interpolate all html files
# bob's yer uncle

def get_site_config(cfg_file):
    with open(cfg_file) as fh:
        site_content = json.load(fh)
        return site_content

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
        parts = source_path.split("/")
        context = {}
        context['locations'] = site_config['locations']

        if len(parts) == 4:
            path_parts = parts[1:-1]
            context = site_config["topics"]
            context = context.get(path_parts[0], {})
            context = context.get(path_parts[1], {})
            context['locations'] = site_config['locations']
            context['link_to_locations'] = False
            context['inv_link_to_locations'] = True

        template = template_env.get_template(rel_path)
        contents = template.render(**context)

        # write the "base" html file
        with open(dest_path, 'w') as fh:
            fh.write(contents)

        # then do it for every location! lol
        if len(parts) == 4:
            parts = dest_path.split("/")
            context['link_to_locations'] = True
            for location in site_config["locations"]:
                print(".", end=" ")
                # update context with location information

                # skip the stupid integer subdirs
                try:
                    int(parts[2])
                    continue
                except ValueError:
                    pass

                context.update(location)
                dest_parts = parts[:3] + [location['location']] + parts[3:]
                dest_file = "/".join(dest_parts)
                dest_path = os.path.dirname(dest_file)

                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)

                contents = template.render(**context)

                with open(dest_file, 'w') as fh:
                    fh.write(contents)
            print()

    else:
        # simple file copy if non-html
        shutil.copy2(source_path, dest_path)

def copy_files(source, dest):
    for (source_path, relpath) in walk_files(source):
        dest_path = os.path.join(dest, relpath)
        if 'src/templates' not in source_path:
            copy_file(source_path, relpath, dest_path)


site_config = get_site_config("./src/site.json")
print(site_config)
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader('./src/'))
copy_files('src', 'dist')
