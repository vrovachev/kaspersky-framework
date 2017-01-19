import pytest


class TestStable:

    @pytest.mark.stable
    def test_stable(self):
        print("stable test")
