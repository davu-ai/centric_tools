import os
import pytest
from fastapi import Request, HTTPException
from unittest.mock import Mock
from centric_tools.permission.decorators import check_permission, get_request_object
from centric_tools.permission.table import PermissionTable


os.environ["PERMISSION_CHECK"] = "True"


def test_check_permission_granted():
    user_permissions = ["can_edit", "can_view"]
    required_permissions = ["can_view"]  # User should have at least one

    try:
        check_permission(user_permissions, required_permissions)  # Should NOT raise
    except HTTPException as e:
        assert False, f"Unexpected HTTPException raised: {e}"


def test_check_permission_denied():
    user_permissions = ["can_view"]
    required_permissions = ["can_edit"]  # User lacks this permission

    with pytest.raises(HTTPException) as exc_info:
        check_permission(user_permissions, required_permissions)

    assert (
        exc_info.value.status_code == 403
    ), f"Expected 403, got {exc_info.value.status_code}"


def test_get_request_object():
    mock_request = Mock(spec=Request)
    mock_request.headers = {"x-permissions": "['can_view']"}  # Use a real dictionary

    request = get_request_object(mock_request)

    assert request.headers["x-permissions"] == "['can_view']"
