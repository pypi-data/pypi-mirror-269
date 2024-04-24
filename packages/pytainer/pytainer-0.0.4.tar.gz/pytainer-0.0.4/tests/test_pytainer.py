import httpx
from pytest_httpx import HTTPXMock

from pytainer import Pytainer
from pytainer.models.portainer import AuthAuthenticateResponse, SystemInfoResponse


def test_portainer_init():
    portainer = Pytainer(
        base_url="https://portainer.test/", api_token="debug-auth-token"
    )
    assert portainer.base_url == "https://portainer.test/"
    assert portainer.headers == {}
    assert portainer.api_token == "debug-auth-token"
    assert isinstance(portainer.requester, httpx.Client)


def test_auth_auth(httpx_mock: HTTPXMock):
    jwt = "debug-auth-token"
    httpx_mock.add_response(
        method="POST",
        url="https://portainer.test/api/auth",
        json=AuthAuthenticateResponse(jwt=jwt).model_dump(),
    )
    portainer = Pytainer(
        base_url="https://portainer.test", api_token="debug-auth-token"
    )

    with httpx.Client() as client:
        resp = portainer.auth.auth(username="test-login", password="test-password")
        assert portainer.api_token == jwt
        assert isinstance(resp, AuthAuthenticateResponse)
        assert resp.jwt == jwt


def test_system_info(httpx_mock: HTTPXMock):
    portainer = Pytainer(
        base_url="https://portainer.test/", api_token="debug-auth-token"
    )
    httpx_mock.add_response(
        method="GET",
        url="https://portainer.test/api/system/info",
        json=SystemInfoResponse(agents=0, edgeAgents=0, platform="str").model_dump(),
    )

    with httpx.Client() as client:
        resp = portainer.system.info()
        assert isinstance(resp, SystemInfoResponse)
