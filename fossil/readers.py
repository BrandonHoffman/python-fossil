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
import os

from .virtual_dirs import TemplateDir, TemplateRoot
from .virtual_files import TemplateFile


class FileSystemReader(object):
    def __init__(self, directory):
        self.path = os.path.abspath(directory)

    def get_template(self):
        templates = self._get_children(self.path)
        return TemplateRoot(templates)

    def _get_children(self, path):
        templates = []
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isfile(full_path):
                content = open(full_path).read()
                template = TemplateFile(item, content)
                templates.append(template)
            else:
                children = self._get_children(full_path)
                template = TemplateDir(item, children)
                templates.append(template)
        return templates
