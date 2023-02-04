"""
@brief      test log(time=150s)
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
                   pylint_ignore=('C0103', 'C1801', 'R1705', 'W0108', 'W0613',
                                  'C0111', 'W0223', 'W0201', 'W0212', 'C0415',
                                  'C0209', 'R1735'),
                   skip=["Parameters differ from overridden 'fit' method",
                         "Module 'numpy.random' has no 'RandomState' member",
                         "Instance of 'SkLearnParameters' has no '",
                         " in module 'sklearn.cluster._k_means'",
                         "Instance of 'Struct' has no '",
                         ])

    def test_style_test(self):
        thi = os.path.abspath(os.path.dirname(__file__))
        test = os.path.normpath(os.path.join(thi, "..", ))
        check_pep8(test, fLOG=fLOG, neg_pattern="temp_.*",
                   pylint_ignore=('C0103', 'C1801', 'R1705', 'W0108', 'W0613',
                                  'C0111', 'W0612', 'E0632', 'C0415', 'C0209',
                                  'R1735'),
                   skip=["Instance of 'tuple' has no ",
                         ])


if __name__ == "__main__":
    unittest.main()
