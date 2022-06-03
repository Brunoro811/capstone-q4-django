from variations.tests.utils.gen_variation_functions import (
    get_post_variation_payload,
    get_product_payload,
    get_variation_payload,
)
from variations.tests.utils.patch_utils import (
    required_fields_in_response,
    variation_creation_model,
    variation_update_route,
)
from variations.tests.utils.post_vars_utils import (
    create_variation_201_response_fields,
    list_variations_200_response_fields,
)

from .default_values import generate_variation_for_size
