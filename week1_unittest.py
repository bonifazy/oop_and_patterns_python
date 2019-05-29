import unittest


class TestFactorize(unittest.TestCase):  # наследуюсь от unittest.testCase

    def test_wrong_types_raise_exception(self):  # все методы, начинающиеся со слова test являются тестирующими
        for i in ('string', 1.5):
            with self.subTest(x=i):
                self.assertRaises(TypeError, factorize, i)  # выбрасываем исключение для некорректных вводных данных

    def test_negative(self):
        for i in (-1, -10, -100):
            with self.subTest(x=i):
                self.assertRaises(ValueError, factorize, i)

    def test_zero_and_one_cases(self):
        cases = ([0, (0,)], [1, (1,)])
        for i in cases:
            with self.subTest(x=i[0]):
                self.assertEqual(factorize(i[0]), i[1])  # проверка функция(параметр) factorize(i[0]) == с вывод i[1]

    def test_simple_numbers(self):
        cases = ([3, (3,)], [13, (13,)], [29, (29,)])
        for i in cases:
            with self.subTest(x=i[0]):
                self.assertEqual(factorize(i[0]), (i[0],))

    def test_two_simple_multipliers(self):
        cases = ([6, (2, 3)], [26, (2, 13)], [121, (11, 11)])
        for i in cases:
            with self.subTest(x=i[0]):
                self.assertEqual(factorize(i[0]), i[1])

    def test_many_multipliers(self):
        cases = ([1001, (7, 11, 13)], [9699690, (2, 3, 5, 7, 11, 13, 17, 19)])
        for i in cases:
            with self.subTest(x=i[0]):
                self.assertEqual(factorize(i[0]), i[1])


def factorize(x: int) -> tuple:
    """ Factorize positive integer and return its factors.
        :type x: int,>=0
        :rtype: tuple[N],N>0
    """

    if not isinstance(x, int):
        raise TypeError

    if x < 0:
        raise ValueError

    if x in (0, 1):
        answer = (x,)
        return answer

    a = x
    t = True
    factors = []
    while t:
        for i in range(2, a + 1):
            if a % i == 0:
                factors.append(i)
                a = a // i
                break
        if a == 1:
            t = False
    return tuple(factors)


if __name__ == "__main__":
    print(factorize(1))
