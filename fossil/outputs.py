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


class FileSystemOutput(object):
    def __init__(self, path):
        self.path = os.path.abspath(path)

    def save(self, root, path=None):
        if path is None:
            path = self.path
        if hasattr(root, 'children'):
            if hasattr(root, 'name'):
                # this is a directory
                new_path = os.path.join(path, root.name)
                os.mkdir(new_path)
                for child in root.children:
                    self.save(child, new_path)
            else:
                # this is the root
                for child in root.children:
                    self.save(child, path)
        else:
            # this is a file
            new_path = os.path.join(path, root.name)
            f = open(new_path, 'w')
            f.write(root.content)
