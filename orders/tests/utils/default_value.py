import datetime


def generate_order():

    """
        Must be added to seller and store instance.    
    """
    
    return {
        "created_at": datetime.datetime.utcnow(),
    }
