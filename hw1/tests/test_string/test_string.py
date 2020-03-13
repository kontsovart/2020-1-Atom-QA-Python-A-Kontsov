from ...conftest import *


class TestString:
    @pytest.mark.parametrize('abc_init', [10, 50, 100])
    def test_join(self, abc_init):
        string_int = ''.join(list(str(random.randint(0, 1)) for _ in range(abc_init)))
        assert len(string_int) == abc_init

    def test_concatenation(self, generate_int_func, generate_int_class):
        string1 = ''.join(list(str(random.randint(0, 1)) for _ in range(generate_int_func)))
        string2 = ''.join(list(str(random.randint(0, 1)) for _ in range(generate_int_class)))
        string3 = string1 + string2
        assert len(string3) == generate_int_func + generate_int_class

    def test_split(self, generate_int_func):
        string_space = ' '.join(list(str(random.randint(0, 1)) for _ in range(generate_int_func)))
        assert len(string_space.split()) == generate_int_func

    def test_zfill(self, generate_int_func, generate_int_class):
        string_int = ''.join(list(str(random.randint(0, 1)) for _ in range(generate_int_func)))
        string_int = string_int.zfill(generate_int_class)
        assert len(string_int) == generate_int_class

    def test_replace(self, generate_int_func):
        string_space = ' '.join(list(str(random.randint(0, 1)) for _ in range(generate_int_func)))
        assert len(string_space.replace(' ', '')) == generate_int_func
