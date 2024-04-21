import unittest

from utilset import linkedin


class TestLinkedin(unittest.TestCase):

    def test_get_vanity_from_linkedin_url(self):
        url = 'https://www.linkedin.com/in/williamhgates/'

        self.assertEqual('williamhgates',
                         linkedin.get_vanity_from_linkedin_url(url))


if __name__ == '__main__':
    unittest.main()