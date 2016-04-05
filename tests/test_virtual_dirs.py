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
from fossil import version, virtual_dirs, virtual_files


class TestVirtualDirs(object):
    virt_dir = virtual_dirs.VirtualDir("test_dir1", [
        virtual_dirs.VirtualDir("test_dir2")
    ])

    def test_init(self):
        assert self.virt_dir.name == "test_dir1"
        assert len(self.virt_dir.children) == 1
        assert self.virt_dir.children[0].name == "test_dir2"

    def test_str(self):
        assert str(self.virt_dir) == "test_dir1\n    test_dir2\n"
        expected_results = "    test_dir1\n        test_dir2\n"
        assert self.virt_dir.__str__(level=1) == expected_results


class TestTemplateDirs(TestVirtualDirs):
    virt_dir = virtual_dirs.TemplateDir("test_dir1", [
        virtual_dirs.TemplateDir("test_dir2")
    ])

    def test_render(self):
        results = self.virt_dir.render()
        assert len(results) == 1
        assert results[0].__class__ == virtual_dirs.VirtualDir
        assert results[0].name == "test_dir1"
        assert len(results[0].children) == 1
        assert results[0].children[0].__class__ == virtual_dirs.VirtualDir
        assert results[0].children[0].name == "test_dir2"

        virt_dir2 = virtual_dirs.TemplateDir("test_dir1,test_dir2", [
            virtual_dirs.TemplateDir("test_dir3,test_dir4"),
            virtual_files.TemplateFile("test_file1,test_file2", "test_content")
        ])
        results2 = virt_dir2.render()
        assert len(results2) == 2
        assert results2[0].__class__ == virtual_dirs.VirtualDir
        assert results2[0].name == "test_dir1"
        assert results2[1].__class__ == virtual_dirs.VirtualDir
        assert results2[1].name == "test_dir2"
        assert len(results2[0].children) == 4
        assert len(results2[1].children) == 4

        virt_dir3 = virtual_dirs.TemplateDir("{{name}}_dir1,{{name}}_dir2", [
            virtual_dirs.TemplateDir(
                "{{name}}_dir3,{{fossil.directory.name}}.test"
            ),
            virtual_files.TemplateFile(
                "{{fossil.directory.name}}.{{name}}_file1,test",
                "{{fossil.directory.name}}.{{fossil.file.name}}")
        ])
        results3 = virt_dir3.render(name="test")
        assert len(results3) == 2
        assert results3[0].__class__ == virtual_dirs.VirtualDir
        assert results3[0].name == "test_dir1"
        assert results3[1].__class__ == virtual_dirs.VirtualDir
        assert results3[1].name == "test_dir2"
        assert len(results3[0].children) == 4
        assert len(results3[1].children) == 4
        assert results3[1].children[1].name == "test_dir2.test"
        assert results3[1].children[2].name == "test_dir2.test_file1"
        expected_result = "test_dir2.test_dir2.test_file1"
        assert results3[1].children[2].content == expected_result
        assert results3[1].children[3].content == "test_dir2.test"

        virt_dir4 = virtual_dirs.TemplateDir(" ", [
            virtual_dirs.TemplateDir("test"),
        ])
        results4 = virt_dir4.render(name="test")
        assert len(results4) == 0


class TestVirtualRoot(object):
    virt_root = virtual_dirs.VirtualRoot([
        virtual_dirs.VirtualDir("test_dir")
    ])

    def test_init(self):
        assert len(self.virt_root.children) == 1
        assert self.virt_root.children[0].name == 'test_dir'

    def test_str(self):
        assert str(self.virt_root) == "-root\n    test_dir\n"
        expected_result = "    -root\n        test_dir\n"
        assert self.virt_root.__str__(level=1) == expected_result


class TestTemplateRoot(TestVirtualRoot):
    virt_root = virtual_dirs.TemplateRoot([
        virtual_dirs.TemplateDir("test_dir")
    ])

    def test_render(self):
        results = self.virt_root.render()
        assert results.__class__ == virtual_dirs.VirtualRoot
        assert len(results.children) == 1

        virt_root2 = virtual_dirs.TemplateRoot([
            virtual_dirs.TemplateDir("{{name}}_dir"),
            virtual_files.TemplateFile("{{name}}_file", "")
        ])
        results2 = virt_root2.render(name="test")
        assert len(results2.children) == 2
        assert results2.children[0].name == "test_dir"
        assert results2.children[1].name == "test_file"

        virt_file = virtual_files.TemplateFile(
            "file_{{fossil.version}}",
            "{{fossil.directory.name}}.{{fossil.file.name}}.{{fossil.version}}"
        )

        virt_root3 = virtual_dirs.TemplateRoot([
            virtual_dirs.TemplateDir("test_dir_{{fossil.version}}", [
                virt_file
            ])
        ])
        results3 = virt_root3.render(name="test")
        assert len(results3.children) == 1
        assert results3.children[0].name == "test_dir_" + str(version.VERSION)
        expected_result = "file_" + str(version.VERSION)
        assert results3.children[0].children[0].name == expected_result
        expected_result = "test_dir_{version}.file_{version}.{version}".format(
            version=version.VERSION
        )
        assert results3.children[0].children[0].content == expected_result
