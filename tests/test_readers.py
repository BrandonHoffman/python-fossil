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
import mock
import os
import pytest

from fossil import readers, virtual_dirs


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
        assert len(template.children) == 2
        names = [item.name for item in template.children]
        assert "test_dir" in names
        assert "test_file2" in names

        if template.children[0].name == "test_dir":
            test_dir = template.children[0]
            test_file = template.children[1]
        else:
            test_file = template.children[0]
            test_dir = template.children[1]
        assert len(test_dir.children) == 1
        assert test_file.content == "test2\n"

        self.reader.skip = ["test_dir", "test_file2"]
        template = self.reader.get_template()
        names = [item.name for item in template.children]
        assert "test_dir" not in names
        assert "test_file2" not in names


class TestGitRepoReader(object):
    reader = readers.GitRepoReader("git://test/hello.git")

    def test_init(self):
        assert self.reader.path == os.path.expanduser(
            os.path.join(
                "~",
                ".fossil",
                "hello")
        )
        assert '.git' in self.reader.skip
        assert self.reader.repo_url == "git://test/hello.git"
        assert self.reader.repo_name == "hello"

    def test_get_template(self):
        with pytest.raises(Exception):
            with mock.patch('subprocess.check_call', lambda cmd, cwd: 1):
                self.reader.get_template()

        with mock.patch('os.path.isdir', lambda x: True):
            with mock.patch('fossil.readers.FileSystemReader.get_template',
                            lambda x: True):
                result = self.reader.get_template()
                assert result
