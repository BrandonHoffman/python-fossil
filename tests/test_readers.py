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

from fossil import readers, virtual_dirs, virtual_files


class TestFileSystemReader(object):
    reader = readers.FileSystemReader(
        os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)
            ),
            "input",
            "TestFileSystemReader"
        )
    )

    def test_init(self):
        assert self.reader.path == os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)
            ),
            "input",
            "TestFileSystemReader")

    def test_get_template(self):
        template = self.reader.get_template()
        assert template.__class__ == virtual_dirs.TemplateRoot
        assert len(template.children) == 3
        assert template.children[0].__class__ == virtual_dirs.TemplateDir
        assert template.children[0].name == "test_dir"
        assert len(template.children[0].children) == 1
        child = template.children[0].children[0]
        assert child.__class__ == virtual_files.TemplateFile
        assert child.name == "test_file"
        assert child.content == "test\n"
        assert template.children[1].__class__ == virtual_dirs.TemplateDir
        assert template.children[1].name == "test_dir2"
        assert template.children[2].__class__ == virtual_files.TemplateFile
        assert template.children[2].name == "test_file2"
        assert template.children[2].content == "test2\n"
