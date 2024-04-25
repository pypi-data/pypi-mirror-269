# Copyright 2023 Inductor, Inc.
"""Functions for interfacing with the Inductor backend."""

from typing import Any, Dict, Literal, Optional, Union

import httpx
import pydantic

from inductor import config
from inductor.backend_client import wire_model


# TODO: Cleanup these globals.
_MOCK_ENDPOINTS = False


def _send_request(
    method: Literal["get", "post", "put", "delete"],
    endpoint: str,
    auth_access_token: str,
    request_body: Optional[Union[pydantic.BaseModel, Dict[str, Any]]] = None
) -> httpx.Response:
    """Sends a request to the backend with the given method and endpoint.

    Args:
        method: The HTTP method to use. Can be one of "get", "post", "put", or
            "delete".
        endpoint: The endpoint to send the request to. This should not begin
            with a slash.
        auth_access_token: Auth0 access token. This is included in the request
            header.
        request_body: The request body to send. If get or delete, the request
            body is ignored.

    Returns:
        The response from the backend.

    Raises:
        RuntimeError: If the response status code is not a successful response
            (i.e., if the response status code is not in the range (200 – 299)).
    """
    if isinstance(request_body, pydantic.BaseModel):
        request_body_json = request_body.model_dump(mode="json")
    else:
        request_body_json = request_body

    response = httpx.request(
        method,
        f"{config.settings.inductor_api_url}/api/client/v1/{endpoint}",
        headers={
            "Authorization": f"Bearer {auth_access_token}",
            **(config.settings.custom_request_headers or {}),
        },
        json=request_body_json,
    )
    # TODO: #433 - These print statements should be available in --verbose
    # mode.
    # print(f"Request: {request_body_json}")
    # print(f"Response: {response.text}")
    # print(f"Status code: {response.status_code}")
    # print(f"JSON: {response.json()}")
    if response.status_code < 200 or response.status_code >= 300:
        raise RuntimeError(
            f"{method} request to `{endpoint}` failed with status code "
            f"{response.status_code} and response text: {response.text}.")
    return response


def create_api_key(
    request: wire_model.CreateApiKeyRequest,
    auth_access_token: str):
    """POST request to create an API key.
    
    Args:
        request: CreateApiKeyRequest object
        auth_access_token: Auth0 access token.
    """
    if _MOCK_ENDPOINTS:
        return
    _send_request("post", "create-api-key", auth_access_token, request)


def create_test_suite(
    request: wire_model.CreateTestSuiteRequest,
    auth_access_token: str
) -> wire_model.CreateTestSuiteResponse:
    """POST request to create a test suite.

    Args:
        request: CreateTestSuiteRequest object
        auth_access_token: Auth0 access token.
    
    Returns:
        CreateTestSuiteResponse object.
    """
    if _MOCK_ENDPOINTS:
        return wire_model.CreateTestSuiteResponse(id=123)
    response = _send_request(
        "post", "create-test-suite", auth_access_token, request)
    return wire_model.CreateTestSuiteResponse(**response.json())


def create_test_suite_run(
    request: wire_model.CreateTestSuiteRunRequest,
    auth_access_token: str
) -> wire_model.CreateTestSuiteRunResponse:
    """POST request to create a test suite run.
    
    Args:
        request: CreateTestSuiteRunRequest object
        auth_access_token: Auth0 access token.
    
    Returns:
        CreateTestSuiteRunResponse object.
    """
    if _MOCK_ENDPOINTS:
        return wire_model.CreateTestSuiteRunResponse(
            test_suite_run_id=123,
            test_case_ids=[1, 2, 3, 4, 5, 6],
            quality_measure_ids=[7, 8, 9, 10, 11, 12],
            hparam_spec_ids=[13, 14, 15, 16, 17, 18],
            url="http://localhost:5000/MOCK_URL",
        )
    response = _send_request(
        "post", "create-test-suite-run", auth_access_token, request)
    return wire_model.CreateTestSuiteRunResponse(**response.json())


def log_test_case_execution(
    request: wire_model.LogTestCaseExecutionRequest,
    auth_access_token: str):
    """POST request to log test case execution.

    Args:
        request: LogTestCaseExecutionRequest object
        auth_access_token: Auth0 access token.
    """
    if _MOCK_ENDPOINTS:
        return
    _send_request(
        "post", "log-test-case-execution", auth_access_token, request)


def complete_test_suite_run(
    request: wire_model.CompleteTestSuiteRunRequest,
    auth_access_token: str):
    """POST request to complete test suite run.

    Args:
        request: CompleteTestSuiteRunRequest object
        auth_access_token: Auth0 access token.
    """
    if _MOCK_ENDPOINTS:
        return
    _send_request(
        "post", "complete-test-suite-run", auth_access_token, request)


def log_llm_program_execution(
    request: wire_model.LogLlmProgramExecutionRequest,
    auth_access_token: str):
    """POST request to log LLM program execution.

    Args:
        request: LogLlmProgramExecutionRequest object
        auth_access_token: Auth0 access token.
    """
    if _MOCK_ENDPOINTS:
        return
    _send_request(
        "post", "log-llm-program-execution", auth_access_token, request)


def create_live_deployment(
    request: wire_model.CreateLiveDeploymentRequest,
    auth_access_token: str) -> wire_model.CreateLiveDeploymentResponse:
    """POST request to create live deployment.

    Args:
        request: `CreateLiveDeploymentRequest` object.
        auth_access_token: Auth0 access token.

    Returns:
        `CreateLiveDeploymentResponse` object.
    """
    response = _send_request(
        "post", "create-live-deployment", auth_access_token, request)
    return wire_model.CreateLiveDeploymentResponse(**response.json())


def get_test_suite_run_quality_measures(
    test_suite_run_id: int,
    request: wire_model.GetTestSuiteRunQualityMeasuresRequest,
    auth_access_token: str
) -> wire_model.GetTestSuiteRunQualityMeasuresResponse:
    """POST request to get a test suite run's quality measures.

    Args:
        test_suite_run_id: Test suite run ID.
        request: `GetTestSuiteRunQualityMeasuresRequest` object.
        auth_access_token: Auth0 access token.

    Returns:
        `GetTestSuiteRunQualityMeasuresResponse` object.
    """
    response = _send_request(
        "post",
        f"test-suite-run/{test_suite_run_id}/get-quality-measures",
        auth_access_token,
        request)
    return wire_model.GetTestSuiteRunQualityMeasuresResponse(**response.json())
