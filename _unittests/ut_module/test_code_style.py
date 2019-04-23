"""
@brief      test log(time=0s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import check_pep8, ExtTestCase


class TestCodeStyle(ExtTestCase):
    """Test style."""

    def test_style_src(self):
        thi = os.path.abspath(os.path.dirname(__file__))
        src_ = os.path.normpath(os.path.join(thi, "..", "..", "src"))
        check_pep8(src_, fLOG=fLOG,
                   pylint_ignore=('C0103', 'C1801', 'R0201', 'R1705', 'W0108', 'W0613',
                                  'C0111', 'W0223', 'W0201', 'W0212'),
                   skip=["Parameters differ from overridden 'fit' method",
                         "Module 'numpy.random' has no 'RandomState' member",
                         "Instance of 'SkLearnParameters' has no '",
                         "kmeans_constraint_.py:66: W0622",
                         " in module 'sklearn.cluster._k_means'",
                         "kmeans_constraint_.py:16: R1710",
                         "Instance of 'Struct' has no '",
                         "kmeans_constraint_.py:328: R1716",
                         ])

    def test_style_test(self):
        thi = os.path.abspath(os.path.dirname(__file__))
        test = os.path.normpath(os.path.join(thi, "..", ))
        check_pep8(test, fLOG=fLOG, neg_pattern="temp_.*",
                   pylint_ignore=('C0103', 'C1801', 'R0201', 'R1705', 'W0108', 'W0613',
                                  'C0111', 'W0612', 'E0632'),
                   skip=["Instance of 'tuple' has no ",
                         ])


if __name__ == "__main__":
    unittest.main()
