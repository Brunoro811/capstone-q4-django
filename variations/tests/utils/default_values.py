

from uuid import UUID


def generate_variation_for_size(size: str = "P"):

    """
        this function return one variation of product.
    """

    return {
        "size": size.upper() ,
        "quantity": 10,
        "color": 'Azul',
    } 

