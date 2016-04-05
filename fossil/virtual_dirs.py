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
from os import environ

from jinja2 import Template

from .version import VERSION


class VirtualDir(object):
    __slots__ = ('name', 'children')

    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []

    def __str__(self, level=0):
        ret = "    "*level+self.name+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret


class TemplateDir(VirtualDir):
    __slots__ = ('name_template')

    def __init__(self, *args, **kwargs):
        super(TemplateDir, self).__init__(*args, **kwargs)
        self.name_template = Template(self.name)

    def render(self, **kwargs):
        new_names = self.name_template.render(kwargs)
        new_directories = []
        for new_name in new_names.split(","):
            new_name = new_name.strip()
            if new_name == "":
                continue
            new_directory = VirtualDir(new_name)
            context = copy.deepcopy(kwargs)
            if "fossil" not in context:
                context["fossil"] = {}

            context['fossil']['directory'] = {
                'name': new_name
            }

            for child in self.children:
                new_child = child.render(**context)
                new_directory.children.extend(new_child)
            new_directories.append(new_directory)

        return new_directories


class VirtualRoot(object):
    __slots__ = ('children')

    def __init__(self, children=None):
        self.children = children or []

    def __str__(self, level=0):
        ret = "    "*level+"-root\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret


class TemplateRoot(VirtualRoot):
    def render(self, **kwargs):
        new_children = []
        for child in self.children:
            context = copy.deepcopy(kwargs)
            context['fossil'] = {
                'version': VERSION,
                'env': environ
            }
            new_children.extend(child.render(**context))
        return VirtualRoot(new_children)
