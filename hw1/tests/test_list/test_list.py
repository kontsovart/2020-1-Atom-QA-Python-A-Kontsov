from ...conftest import *


class TestList:
    @pytest.mark.parametrize('len_list', list(range(3)))
    def test_reverse(self, len_list):
        abc = [i for i in range(len_list)]
        cba = abc.copy()
        cba.reverse()
        for item in range((len(abc)) // 2):
            abc[item], abc[-item - 1] = abc[-item-1], abc[item]
        assert abc == cba

    def test_extend(self, generate_int_func, generate_int_class):
        abc_len = generate_int_func
        abc = [i for i in range(abc_len)]
        bca_len = generate_int_class
        bca = [i for i in range(bca_len)]
        abc.extend(bca)
        assert len(abc) == abc_len + bca_len

    def test_pop(self, generate_int_func, generate_int_class):
        abc_len = generate_int_func
        abc = [i for i in range(abc_len)]
        bca_len = generate_int_class
        bca = [i for i in range(bca_len)]
        with pytest.raises(IndexError):
            abc.pop(bca_len)
        bca.pop(abc_len)
        assert len(bca) == bca_len - 1

    def test_count(self, random_list_ascii, generate_int_session):
        item = random_list_ascii[random.randint(0, generate_int_session - 1)]
        counter = 0
        for i in random_list_ascii:
            if i == item:
                counter += 1
        assert random_list_ascii.count(item) == counter

    def test_clear(self, generate_int_func):
        abc_len = generate_int_func
        abc = [i for i in range(abc_len)]
        abc.clear()
        assert abc == []
