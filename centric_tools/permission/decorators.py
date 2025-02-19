import ast
import asyncio
import functools
from typing import List
from fastapi import Request, HTTPException
from centric_tools.logger import CustomLogger 


def check_permission(user_permissions: List[str], required_permission: List[str]):
    """
    Check if a user has the required permissions.
    """
    if not set(user_permissions).intersection(set(required_permission)):
        context = {
            "required_permission": required_permission,
            "user_permissions": user_permissions,
        }
        CustomLogger.info("Access to resource denied", context=context)
        raise HTTPException(
            detail="You are not allowed to access this resource", status_code=403
        )


def get_request_object(*args, **kwargs) -> Request:
    request: Request = kwargs.get("request")
    if not request:
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                break
    if not request:
        raise HTTPException(status_code=400, detail="Request object not found")
    return request


def get_user_permissions(request: Request) -> List[str]:
    headers = dict(request.headers)
    raw_permissions = headers.get("x-permissions")
    if not raw_permissions or raw_permissions == "None":
        raw_permissions = "[]"
    return ast.literal_eval(raw_permissions)


def validate_permission(required_permissions: List[str]):
    def decorator(func):
        is_async: bool = asyncio.iscoroutinefunction(func)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            request = get_request_object(*args, **kwargs)
            user_permissions = get_user_permissions(request)
            check_permission(user_permissions, required_permissions)
            return await func(*args, **kwargs)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            request = get_request_object(*args, **kwargs)
            user_permissions = get_user_permissions(request)
            check_permission(user_permissions, required_permissions)
            return func(*args, **kwargs)

        return async_wrapper if is_async else sync_wrapper

    return decorator
