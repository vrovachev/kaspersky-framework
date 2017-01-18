import pytest


class TestNetwork:

    @pytest.mark.network
    def test_network(self):
        print("network test")