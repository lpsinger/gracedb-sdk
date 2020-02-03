Changelog
=========

0.0.3 (unreleased)
------------------

-   Skip unit tests if the user's X.509 certificate is not authorized for
    gracedb-test.ligo.org.

-   Track rename of ligo-requests to requests-gracedb.

0.0.2 (2019-12-12)
------------------

-   Factor out generic HTTP requests support into a separate package,
    ligo-requests.

-   Rename ``fail_noauth`` keyword argument to ``fail_if_noauth`` for
    consistency with gracedb-client.

0.0.1 (2019-12-08)
------------------

-   Initial release.
