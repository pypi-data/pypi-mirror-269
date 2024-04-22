def convert_UOM(quantity, conversion_ratio):
    """
    Convert from one unit of measure to another.

    Parameters:
        quantity (float): The quantity to be converted.
        conversion_ratio (float): The ratio to convert from the source unit to the target unit.

    Returns:
        float: The converted quantity.
    """
    converted_quantity = quantity * conversion_ratio
    return converted_quantity

