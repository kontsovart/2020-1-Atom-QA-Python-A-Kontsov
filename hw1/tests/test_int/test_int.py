from ...conftest import *


class TestInt:
    @pytest.mark.parametrize('abc_init', list(range(3)))
    def test_shift_left(self, abc_init):
        abc = abc_init
        bca = abc << 1
        assert bca == abc_init * 2

    @pytest.mark.parametrize('abc_length', list(range(3)))
    def test_bit_length(self, abc_length):
        abc = 1
        abc = abc << abc_length
        assert abc.bit_length() == abc_length + 1

    @pytest.mark.parametrize('abc_init', list(range(3)))
    def test_bitwize_and(self, abc_init):
        abc = abc_init
        bca = 0 << abc_init
        abc = abc & bca
        assert abc == 0

    @pytest.mark.parametrize('abc_init', list(range(3)))
    def test_abs(self, abc_init):
        abc = -abc_init
        assert abs(abc) == abc_init

    def test_compare(self, generate_int_class):
        abc = generate_int_class
        abc += 1
        assert abc > generate_int_class
