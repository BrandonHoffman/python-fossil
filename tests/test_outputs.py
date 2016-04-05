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
import glob
import os

from fossil import outputs, virtual_dirs, virtual_files


class TestFileSystemOutput(object):
    outputer = outputs.FileSystemOutput(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "output"
        )
    )

    def test_init(self):
        assert self.outputer.path == os.path.join(os.path.dirname(__file__),
                                                  "output")

    def test_save(self):
        virt_file = virtual_files.VirtualFile("test.py", "hello")
        virt_file2 = virtual_files.VirtualFile("test2.py", "hello2")
        virt_dir = virtual_dirs.VirtualDir("TestFileSystemOutput",
                                           [virt_file, virt_file2])
        virt_dir2 = virtual_dirs.VirtualDir("TestFileSystemOutput2")
        virt_root = virtual_dirs.VirtualRoot([virt_dir, virt_dir2])
        self.outputer.save(virt_root)
        base_path = os.path.join(os.path.dirname(__file__), "output")
        test_path = os.path.join(base_path, "TestFileSystemOutput")
        assert os.path.isdir(test_path)
        assert os.path.isdir(os.path.join(base_path, "TestFileSystemOutput2"))
        file1_path = os.path.join(test_path, "test.py")
        file2_path = os.path.join(test_path, "test2.py")
        assert os.path.isfile(file1_path)
        assert os.path.isfile(file2_path)
        assert open(file1_path).read() == "hello"
        assert open(file2_path).read() == "hello2"

    @classmethod
    def remove_path(cls, path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            paths = glob.glob(os.path.join(path, "*"))
            for child_path in paths:
                cls.remove_path(child_path)
            os.rmdir(path)

    @classmethod
    def teardown_class(cls):
        paths = glob.glob(
            os.path.join(
                os.path.dirname(__file__),
                "output",
                "TestFileSystemOutput*"
            )
        )
        for path in paths:
            TestFileSystemOutput.remove_path(path)
