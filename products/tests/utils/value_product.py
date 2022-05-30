
def product_shirt ():

    """
        The product_shirt function returns a dictionary compatible with the ProductModel instance.
        This function automatically searches the database for the StoreModel and CategoryModel 
        instances, if it finds it returns a product with the foregnkey, otherwise it returns 
        the dictionary with several `storee_id` and `category_id` fields.
        Ensure at least one instance of StoreModel and category Model in the database.
        This function will always take the first one.
    """
    
    return {
        'name': 'Camiseta Casual',
        'cost_value': 15.99,
        'sale_value_retail': 46.99,
        'sale_value_wholesale': 35.99,
        'quantity_wholesale': 10,
    }
