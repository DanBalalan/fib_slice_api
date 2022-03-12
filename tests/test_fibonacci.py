from utils.fibonacci import fibonacci, get_by_value_range, get_by_position_range


class TestFibonacci:

    def test_fibonacci(self):
        for pos, expected in (
                (5, 5), (0, 0), (367, 22334640661774067356412331900038009953045351020683823507202893507476314037053)
        ):
            assert fibonacci(pos) == expected, 'Actual != expected'

    def test_range_by_pos(self):
        for args, expected in (
                ((0, 5), [0, 1, 1, 2, 3, 5]),
                ((8, 13), [21, 34, 55, 89, 144, 233]),
                ((8, 7), []),
        ):
            assert get_by_position_range(*args) == expected, 'Actual != expected'

    def test_range_by_val(self):
        for args, expected in (
                ((0, 5), [0, 1, 1, 2, 3, 5]),
                ((8, 13), [8, 13]),
                ((11, 50), [13, 21, 34]),
                ((11, 10), []),
        ):
            assert get_by_value_range(*args) == expected, 'Actual != expected'
