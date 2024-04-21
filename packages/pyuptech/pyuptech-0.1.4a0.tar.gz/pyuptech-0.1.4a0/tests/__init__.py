import unittest

import display_tests
import perf_tests

loader = unittest.TestLoader()
tests = loader.loadTestsFromModule(display_tests, perf_tests)

runner = unittest.TextTestRunner(verbosity=5)
runner.run(tests)

if __name__ == "__main__":
    pass
