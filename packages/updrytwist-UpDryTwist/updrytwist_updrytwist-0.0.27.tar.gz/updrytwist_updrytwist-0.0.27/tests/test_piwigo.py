import unittest
from updrytwist import piwigo

class PiwigoTest ( unittest.TestCase):

    def test_csvReader ( self ):

        LINE_COUNT=38894
        pics = piwigo.PictureInfos()
        pics.loadFromCsv( 'piwigo-albums.csv')
        self.assertEqual( LINE_COUNT, len(pics.pictures))


if __name__ == '__main__':
    unittest.main()