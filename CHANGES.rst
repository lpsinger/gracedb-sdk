Changelog
=========

0.1.5 (unreleased)
------------------

-   No changes yet.

0.1.4 (2020-02-27)
------------------

-   Work around a bug in GraceDB where normalization of floating-point GPS
    times to fixed-precision decimal representation is applied to JSON-encoded
    requests but not form-encoded requests. This bug caused superevent API
    requests with GPS times specified with more than 6 decimal places to fail.
    See https://git.ligo.org/lscsoft/gracedb/issues/195.

0.1.2 (2020-02-20)
------------------

-   Fix an argument parsing bug: ``client.superevents.update()`` failed to
    treat the keyword argument ``preferred_event=None`` the same as omission of
    the keyword argument.

0.1.1 (2020-02-11)
------------------

-   Fix Python string formatting syntax so that the package is Python 3.5
    compatible.

0.1.0 (2020-02-04)
------------------

-   Skip unit tests if the user's X.509 certificate is not authorized for
    gracedb-test.ligo.org.

-   Track rename of ligo-requests to requests-gracedb.

-   Address all feedback from Pierre Chanial's code review:
    https://git.ligo.org/emfollow/gracedb-sdk/issues/2

0.0.2 (2019-12-12)
------------------

-   Factor out generic HTTP requests support into a separate package,
    ligo-requests.

-   Rename ``fail_noauth`` keyword argument to ``fail_if_noauth`` for
    consistency with gracedb-client.

0.0.1 (2019-12-08)
------------------

-   Initial release.
