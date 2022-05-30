from stores.tests.utils.error_detail_vars import (forbidden_details,
                                                  not_found_details,
                                                  store_name_conflict_detais,
                                                  unauthorized_details)
from stores.tests.utils.gen_store_functions import get_store_payload
from stores.tests.utils.patch_vars_utils import \
    update_store_200_response_fields
from stores.tests.utils.values_store import (
    fields_request_create_store, fields_response_create_store,
    get_store_by_id_200_response_fields, store_correct, store_success)
