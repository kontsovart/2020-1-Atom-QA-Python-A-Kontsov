from ...conftest import *


class TestDict:
    @pytest.mark.parametrize('abc_init', [10, 50, 100])
    def test_values_keys(self, abc_init):
        abc = {i: i for i in range(abc_init)}
        assert list(abc.keys()) == list(abc.values())

    def test_clear(self, generate_int_func):
        abc = {i: i for i in range(generate_int_func)}
        abc.clear()
        assert abc == {}

    def test_copy(self, generate_int_func):
        abc = {i: i for i in range(generate_int_func)}
        bca = abc.copy()
        assert abc == bca

    def test_popitem(self, generate_int_func):
        abc = {i: i for i in range(generate_int_func)}
        while abc:
            abc.popitem()
        with pytest.raises(KeyError):
            abc.popitem()

    def test_update(self, generate_int_func, generate_int_class):
        abc = {i: i for i in range(generate_int_func)}
        bca_len = generate_int_class
        bca = {i: i for i in range(generate_int_class)}
        abc.update(bca)
        for i in range(bca_len):
            abc.popitem()
        with pytest.raises(KeyError):
            abc.popitem()
