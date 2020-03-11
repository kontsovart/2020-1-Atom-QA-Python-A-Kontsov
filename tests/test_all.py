import pytest
import random
import string


@pytest.fixture()
def generate_int_func():
    return random.randint(0, 100)


@pytest.fixture(scope='class')
def generate_int_class():
    return random.randint(101, 200)


@pytest.fixture(scope='session')
def generate_int_session():
    return random.randint(0, 100)


@pytest.fixture(autouse=True)
def random_list_ascii(generate_int_session):
    letters = string.ascii_lowercase
    list_ascii = []
    for i in range(generate_int_session):
        list_ascii.append(random.choice(letters))
    return list_ascii


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


class TestInt:
    @pytest.mark.parametrize('abc_init', list(range(3)))
    def test_shift_left(self, abc_init):
        abc = abc_init
        abc = abc << 1
        assert abc == abc_init * 2

    @pytest.mark.parametrize('abc_length', list(range(3)))
    def test_multiplication(self, abc_length):
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
