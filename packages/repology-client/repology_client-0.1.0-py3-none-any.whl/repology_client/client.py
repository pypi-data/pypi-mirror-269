# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>

""" Asynchronous wrapper for Repology API """

import json
import warnings
from pathlib import PurePosixPath
from typing import Any

import aiohttp

from repology_client.constants import (
    API_URL,
    HARD_LIMIT,
    MAX_PROJECTS,
    TOOL_PROJECT_BY_URL,
)
from repology_client.exceptions import (
    EmptyResponse,
    InvalidInput,
)
from repology_client.exceptions.resolve import (
    MultipleProjectsFound,
    ProjectNotFound,
)
from repology_client.types import (
    Package,
    ProjectsRange,
    ResolvePackageType,
    _ResolvePkg,
)
from repology_client.utils import ensure_session, limit


@limit(calls=1, period=1.0)
async def _call(location: str, params: dict | None = None, *,
                session: aiohttp.ClientSession | None = None) -> bytes:
    """
    Do a single rate-limited request.

    :param location: URL location
    :param params: URL query string parameters
    :param session: :external+aiohttp:py:module:`aiohttp` client session

    :raises repology.exceptions.EmptyResponse: on empty response
    :raises aiohttp.ClientResponseError: on HTTP errors

    :returns: raw response
    """

    async with ensure_session(session) as aiohttp_session:
        async with aiohttp_session.get(location, params=params or {},
                                       raise_for_status=True) as response:
            data = await response.read()
            if not data:
                raise EmptyResponse

    return data


async def api(endpoint: str, params: dict | None = None, *,
              session: aiohttp.ClientSession | None = None) -> Any:
    """
    Do a single API request.

    :param endpoint: API endpoint (example: ``/projects``)
    :param params: URL query string parameters
    :param session: :external+aiohttp:py:module:`aiohttp` client session

    :raises repology.exceptions.EmptyResponse: on empty response
    :raises aiohttp.ClientResponseError: on HTTP errors
    :raises json.JSONDecodeError: on JSON decode failure

    :returns: decoded JSON response
    """

    raw_data = await _call(API_URL + endpoint, params, session=session)
    data = json.loads(raw_data)
    if not data:
        raise EmptyResponse

    return data


async def get_packages(project: str, *,
                       session: aiohttp.ClientSession | None = None) -> set[Package]:
    """
    Access the ``/api/v1/project/<project>`` endpoint to list packages for a
    single project.

    :param project: project name on Repology
    :param session: :external+aiohttp:py:module:`aiohttp` client session

    :raises repology.exceptions.EmptyResponse: on empty response
    :raises repology.exceptions.InvalidInput: if ``project`` is an empty string
    :raises aiohttp.ClientResponseError: on HTTP errors

    :returns: set of packages
    """

    if not project:
        raise InvalidInput(f"Not a valid project name: {project}")

    async with ensure_session(session) as aiohttp_session:
        endpoint = PurePosixPath("/project") / project
        data = await api(str(endpoint), session=aiohttp_session)
    return {Package(**package) for package in data}


async def get_projects(start: str = "", end: str = "", count: int = 200, *,
                       session: aiohttp.ClientSession | None = None,
                       **filters: Any) -> dict[str, set[Package]]:
    """
    Access the ``/api/v1/projects/`` endpoint to list projects.

    If both ``start`` and ``end`` are given, only ``start`` is used.

    :param start: name of the first project to start with
    :param end: name of the last project to end with
    :param count: maximum number of projects to fetch
    :param session: :external+aiohttp:py:module:`aiohttp` client session

    :raises repology.exceptions.EmptyResponse: on empty response
    :raises aiohttp.ClientResponseError: on HTTP errors

    :returns: project to packages mapping
    """

    if count > HARD_LIMIT:
        warnings.warn(f"Resetting count to {HARD_LIMIT} to prevent API abuse")
        count = HARD_LIMIT

    proj_range = ProjectsRange(start, end)
    if start and end:
        warnings.warn("The 'start..end' range format is not supported by Repology API")
        proj_range.end = ""

    result: dict[str, set[Package]] = {}
    async with ensure_session(session) as aiohttp_session:
        while True:
            endpoint = PurePosixPath("/projects")
            if proj_range:
                endpoint /= str(proj_range)

            batch = await api(f"{endpoint}/", filters, session=aiohttp_session)
            for project in batch:
                result[project] = set()
                for package in batch[project]:
                    result[project].add(Package(**package))

            if len(result) >= count:
                break
            if len(batch) == MAX_PROJECTS:
                # we probably hit API limits, so…
                # …choose lexicographically highest project as a new start
                proj_range.start = max(batch)
                # …make sure we haven't already hit the requested end
                if end and proj_range.start >= end:
                    break
                # …and drop end condition as unsupported
                proj_range.end = ""
            else:
                break

    return result


async def resolve_package(repo: str, name: str,
                          name_type: ResolvePackageType = ResolvePackageType.SOURCE,
                          *, autoresolve: bool = True,
                          session: aiohttp.ClientSession | None = None) -> set[Package]:
    """
    If you don't know how a project is named on Repology and therefore cannot
    use the :py:func:`get_packages` function, use this instead.

    This function uses the ``/tools/project-by`` utility to resolve a package
    name into ``/api/v1/project/<project>`` project information.

    If you disable autoresolve, ambigous package names will raise the
    :py:class:`MultipleProjectsFound` exception. It will however contain all
    matching project names, so you can continue.

    :param repo: repository name on Repology
    :param name: package name in the repository
    :param name_type: which name is used, "source" or "binary"
    :param autoresolve: enable automatic ambiguity resolution

    :raises repology.exceptions.resolve.MultipleProjectsFound: on ambigous
    package names when automatic resolution is disabled
    :raises repology.exceptions.resolve.ProjectNotFound: on failed resolve
    resulting in the "404 Not Found" HTTP error
    :raises aiohttp.ClientResponseError: on HTTP errors (except 404)

    :returns: set of packages
    """

    params = {
        "repo": repo,
        "name": name,
        "name_type": name_type,
        "target_page": "api_v1_project",
    }
    if not autoresolve:
        params["noautoresolve"] = "on"

    pkg = _ResolvePkg(repo, name, name_type)
    try:
        async with ensure_session(session) as aiohttp_session:
            raw_data = await _call(TOOL_PROJECT_BY_URL, params,
                                   session=aiohttp_session)
    except aiohttp.ClientResponseError as err:
        if err.status == 404:
            raise ProjectNotFound(pkg) from err
        raise

    data = json.loads(raw_data)
    if (
        isinstance(data, dict)
        and (targets := data.get("targets")) is not None
    ):
        raise MultipleProjectsFound(pkg, targets.keys())

    return {Package(**package) for package in data}
