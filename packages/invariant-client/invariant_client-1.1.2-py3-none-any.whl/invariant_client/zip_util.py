#   Copyright 2018 The Batfish Open Source Project
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# Modified 2024 Invariant Technology, Inc
# The following modifications were made from the original file:
# 1. Retrieved from https://github.com/batfish/pybatfish/blob/e23829854c70446b4e68a3f8ef2a25410daad167/pybatfish/util.py
# 2. All code except function zip_dir, its imports, and constant _MIN_ZIP_TIMESTAMP was excluded

import os
import tempfile
from typing import IO
import zipfile

# Minimum timestamp supported by ZIP format
# See issue https://bugs.python.org/issue34097
_MIN_ZIP_TIMESTAMP = 315561600.0


def zip_dir(dir_path: str, out_file: str | IO):
    """
    ZIP a specified directory and write it to the given output file path.

    :param dir_path: path to the directory to be zipped up
    :type dir_path: str
    :param out_file: path to the resulting zipfile
    :type out_file: str
    """
    with zipfile.ZipFile(out_file, "w", zipfile.ZIP_DEFLATED) as zipWriter:
        rel_root = os.path.abspath(os.path.join(dir_path, os.path.pardir))

        for root, _dirs, files in os.walk(dir_path):
            zipWriter.write(root, os.path.relpath(root, rel_root), zipfile.ZIP_STORED)
            for f in files:
                filename = os.path.join(root, f)
                arcname = os.path.join(os.path.relpath(root, rel_root), f)

                # Zipped files must be from 1980 or later
                # So copy any file older than that to a tempfile to bump the timestamp
                if os.path.getmtime(filename) < _MIN_ZIP_TIMESTAMP:
                    with tempfile.NamedTemporaryFile("w+b") as temp_file, open(
                        filename, "rb"
                    ) as file_src:
                        temp_file.write(file_src.read())
                        temp_file.flush()
                        zipWriter.write(temp_file.name, arcname)
                else:
                    zipWriter.write(filename, arcname)
