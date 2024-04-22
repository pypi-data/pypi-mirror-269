#  Copyright (c) 2024. All rights reserved.

from updrytwist import piwigo

def test_csvReader (  ):

    LINE_COUNT=37325
    pics = piwigo.PictureInfos()
    pics.loadFromCsv( 'piwigo-albums.csv')
    assert LINE_COUNT == len(pics.pictures)
