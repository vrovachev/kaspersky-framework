# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# THIS FILE IS MANAGED BY THE GLOBAL REQUIREMENTS REPO - DO NOT EDIT

import pytest

from utils.disk_utils import DiskIO


class TestDisk:

    def __init__(self):
        self.WRITE_MB = 128
        self.WRITE_BLOCK_KB = 1024
        self.READ_BLOCK_B = 512

    @staticmethod
    def all_free_disk_space_gb():
        return reduce(lambda res, x: res+x[1], DiskIO().disks, 0)

    @pytest.mark.disk
    @pytest.mark.storage
    def test_disk_space_storage(self):
        assert self.all_free_disk_space_gb() > 3000
