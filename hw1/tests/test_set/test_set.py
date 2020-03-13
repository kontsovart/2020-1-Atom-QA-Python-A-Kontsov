from ...conftest import *


class TestSet:
    @pytest.mark.parametrize('len_list', list(range(3)))
    def test_add(self, len_list):
        abc_len = len_list
        abc = set()
        for i in range(abc_len):
            abc.add(i)
        assert len(abc) == abc_len

    def test_sub_super_set(self, generate_int_func, generate_int_class):
        abc_len = generate_int_func
        abc = {i for i in range(abc_len)}
        bca_len = generate_int_class
        bca = {i for i in range(bca_len)}
        assert abc.issubset(bca) == bca.issuperset(abc)

    def test_copy(self, generate_int_func):
        abc_len = generate_int_func
        abc = {i for i in range(abc_len)}
        bca = abc.copy()
        assert abc == bca

    def test_union(self, generate_int_func, generate_int_class):
        abc_len = generate_int_func
        abc = {i for i in range(abc_len)}
        bca_len = generate_int_class
        bca = {i for i in range(bca_len)}
        abc_bca = abc.copy()
        abc_bca = abc_bca.union(bca)
        assert abc.issubset(abc_bca) == bca.issubset(abc_bca)

    def test_pop(self, generate_int_func):
        abc = {i for i in range(generate_int_func)}
        while abc:
            abc.pop()
        with pytest.raises(KeyError):
            abc.pop()
