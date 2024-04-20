

=========
Changelog
=========




.. towncrier release notes start

6.10.0 (2023-12-19)
===================

Features
--------

- Use ``Authorization`` header instead of adding username/password to URL when fetching from mirror.

- Fix #998: Use the pure Python httpx library instead of aiohttp to prevent delays in supporting newest Python releases.



Bug Fixes
---------

- Fix #996: support hashes other than sha256 in application/vnd.pypi.simple.v1+json responses.

- Only compare hostname instead of full URL prefix when parsing mirror packages to fix mirrors with basic authentication and absolute URLs. See #1006



6.9.2 (2023-08-06)
==================

Bug Fixes
---------

- Prevent duplicates when adding values to lists in index configuration with ``+=`` operator.


6.9.1 (2023-07-02)
==================

Bug Fixes
---------

- Prevent error in find_pre_existing_file in case of incomplete metadata.

- Fix #980: Remove long deprecated backward compatibility for old pluggy versions to fix error with pluggy 1.1.0.


6.9.0 (2023-05-23)
==================

Features
--------

- Support export directory layout for ``--replica-file-search-path`` option.

- Fix #931: Add ``mirror_no_project_list`` setting for mirror indexes that have no full project list like google cloud artifacts or if you want to prevent downloading the full list for huge indexes like PyPI.


Bug Fixes
---------

- Keep a reference to async tasks to avoid their removal mid execution.

- Support changed default of ``enforce_content_length`` in urllib3 >= 2.

- Fix #934: Properly set PATH_INFO when outside URL is used with sub-path.

- Fix #945: Adapt FatalError to be usable as an async HTTP response when updating a project on a mirror.

- Fix wrong hash metadata introduced in 6.5.0 for toxresults which prevents replication. The metadata can be fixed by an export/import cycle.


6.8.0 (2022-12-05)
==================

Features
--------

- Fix #929: Cache normalized project names per transaction on mirror index instances.


Bug Fixes
---------

- Fix #914: add locking to list_projects_perstage of mirror indexes to prevent multiple slow concurrent updates of the full project name list.

- Catch exceptions in async_httpget analog to httpget.

- Add locking to mirror name cache to prevent race condition on updates.

