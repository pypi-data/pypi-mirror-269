import package_a.main as main_a
import package_b.main as main_b


def test_multiply():
    assert main_a.multiply(1, 2, 3) == 6


def test_divide():
    assert main_b.divide(1, 2, 3) == 0.16666666666666666
