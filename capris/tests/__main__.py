import sys
import unittest
import capris.tests


def main():
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=0)

    for test in capris.tests.get_tests():
        suite.addTest(test)

    runner.failfast = True
    result = runner.run(suite)

    if not result.wasSuccessful():
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
