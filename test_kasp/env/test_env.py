import pytest


class TestEnv:

    @pytest.mark.env
    def test_env(self):
        print("env test")