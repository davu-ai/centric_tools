import os

import pytest
from fastapi import Request, HTTPException
from unittest.mock import Mock
from centric_tools.permission.decorators import check_permission, get_request_object, get_user_permissions


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


def test_get_permission_from_request_object_headers():
    mock_request = Mock(spec=Request)
    mock_request.headers = {"x-permissions": "['can_view']"}  # Use a real dictionary

    request = get_request_object(mock_request)

    assert request.headers["x-permissions"] == "['can_view']"

def test_get_permission_from_request_object_state():
    mock_request = Mock(spec=Request)
    mock_request.state.user_data = {"permissions": ["can_view"]}
    request = get_request_object(mock_request)

    assert request.state.user_data["permissions"] == ["can_view"]


def test_get_permissions_when_permission_store_is_headers_returns_empty():
    mock_request = Mock(spec=Request)
    mock_request.headers = {}
    mock_request.state.user_data = {"permissions": ["can_delete"]}
    request = get_request_object(mock_request)
    permissions = get_user_permissions(request)
    assert len(permissions) == 0


def test_get_permissions_when_permission_store_is_headers_returns_permissions():
    mock_request = Mock(spec=Request)
    mock_request.headers = {"x-permissions": "['can_edit']"}
    mock_request.state.user_data = {"permissions": ["can_view"]}
    request = get_request_object(mock_request)
    permissions = get_user_permissions(request)
    assert len(permissions) == 1
    for perm in permissions:
        assert perm == "can_edit"


def test_get_permissions_when_permission_store_is_state_returns_empty():
    os.environ["PERMISSION_STORE"] = "state"
    mock_request = Mock(spec=Request)
    mock_request.state.user_data = {}
    mock_request.headers = {"x-permissions": "['can_view']"}
    request = get_request_object(mock_request)
    permissions = get_user_permissions(request)
    assert len(permissions) == 0


def test_get_permissions_when_permission_store_is_state_returns_permissions():
    os.environ["PERMISSION_STORE"] = "state"
    mock_request = Mock(spec=Request)
    mock_request.headers = {"x-permissions": "['can_edit']"}
    mock_request.state.user_data = {"permissions": ["can_view"]}
    request = get_request_object(mock_request)
    permissions = get_user_permissions(request)
    assert len(permissions) == 1
    for perm in permissions:
        assert perm == "can_view"