"""
Copyright 2016 Brandon Michael Hoffman

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import copy

from jinja2 import Template


class VirtualFile(object):
    __slots__ = ('name', 'content')

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __str__(self, level=0):
        return "    "*level+self.name+"\n"


class TemplateFile(VirtualFile):
    __slots__ = ('name_template', 'template')

    def __init__(self, *args, **kwargs):
        super(TemplateFile, self).__init__(*args, **kwargs)
        self.template = Template(self.content)
        self.name_template = Template(self.name)

    def render(self, **kwargs):
        new_files = []
        new_names = self.name_template.render(kwargs)
        for new_name in new_names.split(","):
            new_name = new_name.strip()
            if new_name == "":
                continue
            context = copy.deepcopy(kwargs)
            if 'fossil' not in context:
                context['fossil'] = {}
            context['fossil']['file'] = {
                'name': new_name
            }
            new_content = self.template.render(context)
            new_file = VirtualFile(new_name, new_content)
            new_files.append(new_file)
        return new_files
