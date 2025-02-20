import os
import pytest
from fastapi import HTTPException
from centric_tools.permission.decorators import check_permission, get_request_object


def test_check_permission_granted_even_without_required_permissions():
    user_permissions = ["can_edit", "can_view"]
    required_permissions = ["can_delete"]

    original_value = os.environ.get("PERMISSION_CHECK")
    os.environ["PERMISSION_CHECK"] = "False"

    try:
        check_permission(user_permissions, required_permissions)
    except HTTPException as e:
        pytest.fail(f"Unexpected HTTPException raised: {e}")
    finally:
        if original_value is not None:
            os.environ["PERMISSION_CHECK"] = original_value
        else:
            del os.environ["PERMISSION_CHECK"]
