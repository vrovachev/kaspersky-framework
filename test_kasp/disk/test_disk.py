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

    @pytest.mark.disk
    @pytest.mark.storage
    def test_disk_space_storage(self):
        assert DiskIO().all_free_disk_space_gb() > 3000

    @pytest.mark.disk
    @pytest.mark.workstation
    def test_disk_space_ws(self):
        assert DiskIO().all_free_disk_space_gb() > 30

    @pytest.mark.disk
    @pytest.mark.mailserver
    def test_disk_space_mailserver(self):
        assert DiskIO().all_free_disk_space_gb() > 1000

    @pytest.mark.disk
    @pytest.mark.storage
    def test_io_storage(self):
        io = DiskIO().io_calculate()
        assert io[0] > 200
        assert io[1] > 200

    @pytest.mark.disk
    @pytest.mark.workstation
    def test_io_ws(self):
        io = DiskIO().io_calculate()
        assert io[0] > 100
        assert io[1] > 100

    @pytest.mark.disk
    @pytest.mark.mailserver
    def test_io_mailserver(self):
        io = DiskIO().io_calculate()
        assert io[0] > 150
        assert io[1] > 150
