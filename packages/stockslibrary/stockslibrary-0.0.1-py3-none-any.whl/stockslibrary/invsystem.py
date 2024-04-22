def calculate_total_quantity(products):
    """
    Function to calculate the total quantity for products in the inventory.
    Takes a dictionary of products with their quantities as input.
    Returns the total quantity of all products.
    """
    total_quantity = sum(products.values())
    return total_quantity