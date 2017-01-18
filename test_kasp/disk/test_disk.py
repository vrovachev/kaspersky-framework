import pytest


class TestDisk:

    @pytest.mark.disk
    def test_disk(self):
        print("disk test")