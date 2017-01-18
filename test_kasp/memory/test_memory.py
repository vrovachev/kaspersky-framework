import pytest


class TestMemory:

    @pytest.mark.memory
    def test_memory(self):
        print("memory test")