import unittest
from updrytwist import strcompress

class StrCompressTest ( unittest.TestCase):

    def test_compressdecompress ( self ):

        testList = [
            [ 'abc', 'defgh', 'ijklmno303'],
            [ 'pqr', '23094820982304984980923#^#^*@(@(@*#$^&$())_///', '02394UU']
        ]

        compressor = strcompress.SetEncoder()

        compressor.addSets( testList )
        compressed = compressor.compressed()
        uncompressed = compressor.decompress( compressed )

        for i in range( 0, len(testList)-1 ):
            for j in range( 0, len(testList[i])- 1 ):
                self.assertEqual( testList[i][j], uncompressed[i][j])

if __name__ == '__main__':
    unittest.main()
