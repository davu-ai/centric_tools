import pytest
from fastapi import Request, HTTPException
from unittest.mock import Mock
from centric_tools.logger import CustomLogger
from centric_tools.permission.decorators import validate_permission
from centric_tools.permission.table import PermissionTable


def test_custom_logger_info():
    mock_context = {"user_id": "123"}
    CustomLogger.info("Test log", context=mock_context)
    assert True  # No exception should be raised


def test_check_permission_granted():
    user_permissions = [PermissionTable.can_manage_project]
    required_permissions = [PermissionTable.can_manage_project]
    try:
        validate_permission(required_permissions)(lambda: True)()
    except HTTPException:
        pytest.fail("Unexpected HTTPException raised")


def test_check_permission_denied():
    user_permissions = []
    required_permissions = [PermissionTable.can_manage_project]
    with pytest.raises(HTTPException) as exc:
        validate_permission(required_permissions)(lambda: True)()
    assert exc.value.status_code == 403


def test_get_request_object():
    mock_request = Mock(spec=Request)
    request = validate_permission([])(lambda request: request)(mock_request)
    assert request == mock_request
