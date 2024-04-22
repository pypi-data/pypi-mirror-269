from UoMConversion import convert

def test_convert_UOM():
    # Packages to lineItem
    assert convert.convert_UOM(
        5,20
    ) == 100.00