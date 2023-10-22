import sys
sys.path.append("/home/kevin/code/kmip_poc/shared_ciphers_investigation/extending_python_with_c/build/lib.linux-x86_64-cpython-311")

import spam
import unittest
import io
import pathlib

def callback():
    return 123

class TestSpam(unittest.TestCase):
    def setUp(self):
        self.num_callback_calls = 0

    def test_system(self):
        filename = "foo.txt"
        path = pathlib.Path(filename)
        path.unlink(missing_ok=True)
        spam.system("echo 'hi' > {}".format(filename))
        self.assertTrue(path.exists(), "expected file '{}' to exist but did not".format(filename))
        self.assertEqual(path.read_text(), "hi\n")
        # Clean up
        path.unlink(missing_ok=True)

    def method_callback (self):
        self.num_callback_calls += 1

    def test_callme(self):
        got = spam.callme(callback)
        self.assertEqual (got, 123)

        self.assertEqual(self.num_callback_calls, 0)
        spam.callme(self.method_callback)
        self.assertEqual(self.num_callback_calls, 1)

    def test_rewrite_string (self):
        s = "abc"
        got = spam.rewrite_string(s)
        self.assertEqual("bbc", s)
        self.assertEqual(got, 123)

    def test_goof (self):
        got = spam.goof()
        self.assertEqual(got, 123)


if __name__ == "__main__":
    unittest.main()