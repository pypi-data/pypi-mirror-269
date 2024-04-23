import os

import pytest

from hipscat.pixel_math import HealpixPixel
from hipscat.pixel_tree.pixel_tree_builder import PixelTreeBuilder


@pytest.fixture
def pixel_trees_dir(test_data_dir):
    return os.path.join(test_data_dir, "pixel_trees")


@pytest.fixture
def pixel_tree_1():
    return PixelTreeBuilder.from_healpix([HealpixPixel(0, 11)])


@pytest.fixture
def pixel_tree_2():
    return PixelTreeBuilder.from_healpix(
        [
            HealpixPixel(0, 10),
            HealpixPixel(1, 33),
            HealpixPixel(1, 35),
            HealpixPixel(1, 44),
            HealpixPixel(1, 45),
            HealpixPixel(1, 46),
            HealpixPixel(2, 128),
            HealpixPixel(2, 130),
            HealpixPixel(2, 131),
        ]
    )


@pytest.fixture
def pixel_tree_3():
    return PixelTreeBuilder.from_healpix(
        [
            HealpixPixel(0, 8),
            HealpixPixel(1, 36),
            HealpixPixel(1, 37),
            HealpixPixel(1, 40),
            HealpixPixel(1, 42),
            HealpixPixel(1, 43),
            HealpixPixel(1, 44),
            HealpixPixel(1, 46),
            HealpixPixel(1, 47),
        ]
    )


@pytest.fixture
def aligned_trees_2_3_inner():
    return PixelTreeBuilder.from_healpix(
        [
            HealpixPixel(1, 33),
            HealpixPixel(1, 35),
            HealpixPixel(1, 40),
            HealpixPixel(1, 42),
            HealpixPixel(1, 43),
            HealpixPixel(1, 44),
            HealpixPixel(1, 46),
            HealpixPixel(2, 128),
            HealpixPixel(2, 130),
            HealpixPixel(2, 131),
        ]
    )


@pytest.fixture
def aligned_trees_2_3_left():
    return PixelTreeBuilder.from_healpix(
        [
            HealpixPixel(1, 33),
            HealpixPixel(1, 35),
            HealpixPixel(1, 40),
            HealpixPixel(1, 41),
            HealpixPixel(1, 42),
            HealpixPixel(1, 43),
            HealpixPixel(1, 44),
            HealpixPixel(1, 45),
            HealpixPixel(1, 46),
            HealpixPixel(2, 128),
            HealpixPixel(2, 130),
            HealpixPixel(2, 131),
        ]
    )


@pytest.fixture
def aligned_trees_2_3_right():
    return PixelTreeBuilder.from_healpix(
        [
            HealpixPixel(1, 33),
            HealpixPixel(1, 34),
            HealpixPixel(1, 35),
            HealpixPixel(1, 36),
            HealpixPixel(1, 37),
            HealpixPixel(1, 40),
            HealpixPixel(1, 42),
            HealpixPixel(1, 43),
            HealpixPixel(1, 44),
            HealpixPixel(1, 46),
            HealpixPixel(1, 47),
            HealpixPixel(2, 128),
            HealpixPixel(2, 129),
            HealpixPixel(2, 130),
            HealpixPixel(2, 131),
        ]
    )


@pytest.fixture
def aligned_trees_2_3_outer():
    return PixelTreeBuilder.from_healpix(
        [
            HealpixPixel(1, 33),
            HealpixPixel(1, 34),
            HealpixPixel(1, 35),
            HealpixPixel(1, 36),
            HealpixPixel(1, 37),
            HealpixPixel(1, 40),
            HealpixPixel(1, 41),
            HealpixPixel(1, 42),
            HealpixPixel(1, 43),
            HealpixPixel(1, 44),
            HealpixPixel(1, 45),
            HealpixPixel(1, 46),
            HealpixPixel(1, 47),
            HealpixPixel(2, 128),
            HealpixPixel(2, 129),
            HealpixPixel(2, 130),
            HealpixPixel(2, 131),
        ]
    )
