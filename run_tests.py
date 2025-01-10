import unittest

if __name__ == "__main__":
    # Автоматически находит все тесты в папке "tests"
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
