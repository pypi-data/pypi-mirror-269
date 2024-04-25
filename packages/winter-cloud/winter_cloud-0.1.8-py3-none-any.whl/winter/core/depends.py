import json
from typing import Optional

from fastapi import Header, Request
from fastapi.security import SecurityScopes

from ..authentication import AuthUser
from ..common.exception import UnauthorizedException, NotPermissionException


async def get_auth_user(
        request: Request,
        user_id: Optional[int] = Header(None),
        user_token_id: Optional[int] = Header(None),
        authorities: Optional[str] = Header(None),
):
    """ 通过依赖注入获取当前登录用户 """
    if not user_id:
        raise UnauthorizedException
    try:
        authorities = json.loads(authorities)
    except json.JSONDecodeError:
        authorities = []
    user = AuthUser(
        user_id=user_id,
        user_token_id=user_token_id,
        authorities=authorities
    )
    request.scope['user'] = user


async def as_permission(
        request: Request,
        security_scopes: SecurityScopes,
):
    """ 权限校验 """
    for scope in security_scopes.scopes:
        if scope not in request.user.authorities:
            raise NotPermissionException
    return True
