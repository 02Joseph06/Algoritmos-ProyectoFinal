import pytest

from C6.c6_pac_perceptron import Perceptron, generate_linear_data, pac_sample_bound


def test_pac_bound_increases_when_accuracy_or_confidence_is_stricter():
    assert pac_sample_bound(2, 0.1, 0.05) > pac_sample_bound(2, 0.2, 0.05)
    assert pac_sample_bound(2, 0.1, 0.01) > pac_sample_bound(2, 0.1, 0.05)


def test_perceptron_learns_realizable_linear_sample():
    points, labels = generate_linear_data(100, seed=10)
    model = Perceptron(2)
    model.fit(points, labels)
    assert all(model.predict(point) == label for point, label in zip(points, labels))


def test_sample_bound_validates_parameters():
    with pytest.raises(ValueError):
        pac_sample_bound(0, 0.1, 0.05)
