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
from fossil import virtual_files


class TestVirtualFiles(object):
    virt_file = virtual_files.VirtualFile("test_name", "test_content")

    def test_init(self):
        assert self.virt_file.name == "test_name"
        assert self.virt_file.content == "test_content"

    def test_str(self):
        assert str(self.virt_file) == "test_name\n"
        assert self.virt_file.__str__(level=1) == "    test_name\n"


class TestTemplateFile(TestVirtualFiles):
    virt_file = virtual_files.TemplateFile("test_name", "test_content")

    def test_render(self):
        result_files = self.virt_file.render()
        assert len(result_files) == 1
        assert result_files[0].__class__ == virtual_files.VirtualFile
        assert result_files[0].name == "test_name"
        assert result_files[0].content == "test_content"

        virt_file2 = virtual_files.TemplateFile(
            "test_name,test_name_2",
            "test_content"
        )
        result_files2 = virt_file2.render()
        assert len(result_files2) == 2
        assert result_files2[0].__class__ == virtual_files.VirtualFile
        assert result_files2[0].name == "test_name"
        assert result_files2[0].content == "test_content"
        assert result_files2[1].__class__ == virtual_files.VirtualFile
        assert result_files2[1].name == "test_name_2"
        assert result_files2[1].content == "test_content"

        virt_file3 = virtual_files.TemplateFile(
            "{{test}}name",
            "{{test}}content"
        )
        result_files3 = virt_file3.render(test="test_")
        assert len(result_files3) == 1
        assert result_files3[0].__class__ == virtual_files.VirtualFile
        assert result_files3[0].name == "test_name"
        assert result_files3[0].content == "test_content"

        virt_file4 = virtual_files.TemplateFile("", "content")
        result_files4 = virt_file4.render()
        assert len(result_files4) == 0

        virt_file5 = virtual_files.TemplateFile(
            "{{test}}",
            "{{fossil.file.name}}"
        )
        result_files5 = virt_file5.render(test="test_name")
        assert len(result_files5) == 1
        assert result_files5[0].__class__ == virtual_files.VirtualFile
        assert result_files5[0].name == "test_name"
        assert result_files5[0].content == "test_name"

        virt_file6 = virtual_files.TemplateFile(
            "{{test}}",
            b"asd123"
        )  # simulate binary file
        result_files6 = virt_file6.render(test="test_name")
        assert len(result_files6) == 1
        assert result_files6[0].__class__ == virtual_files.VirtualFile
        assert result_files6[0].name == "test_name"
        assert result_files6[0].content == b"asd123"
