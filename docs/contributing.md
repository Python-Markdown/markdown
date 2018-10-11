# Contributing to Python-Markdown

The following is a set of guidelines for contributing to Python-Markdown and its
extensions, which are hosted in the [Python-Markdown Organization] on GitHub.
These are mostly guidelines, not rules. Use your best judgment, and feel free to
propose changes to this document in a pull request.

## Code of Conduct

This project and everyone participating in it is governed by the
[Python-Markdown Code of Conduct]. By participating, you are expected to uphold
this code. Please report unacceptable behavior to <markdown@freewisdom.org>.

## Project Organization

The core Python-Markdown code base and any built-in extensions are hosted in the
[Python-Markdown/markdown] project on GitHub. Other extensions maintained by the
Python-Markdown project may be hosted as separate repositories in the
[Python-Markdown Organization] on GitHub and must follow best practices for
third-party extensions.

The [Python-Markdown/markdown] project is organized as follows:

* Branch `master` should generally be stable and release-ready at all times.
* Version branches should be used for bug-fixes back-ported to the most recent
  point release.
* No other branches should be created. Any other branches which exist are
  preserved for historical reasons only.

## Issues

Please address issues on the correct channel. Usage questions should be directed
to the discussion group. Feature requests, bug reports and other issues should
be raised on the GitHub [issue tracker].

Some tips on good issue reporting:

* When describing issues try to phrase your ticket in terms of the behavior you
  think needs to change rather than the code you think needs to change.
* Make sure you're running the latest version of Python-Markdown before
  reporting an issue.
* Search the issue list first for related items. Be sure to check closed issues
  and pull requests. GitHub's search only checks open issues by default.
* You may want to check the [syntax rules] and/or [Babelmark] to confirm that
  your expectations align with the rules and/or other implementations of
  Markdown.
* If reporting a syntax bug, you must provide the minimal input which exhibits
  the behavior, the actual output and the output you expected. All three items
  must be provided as textual code blocks (screen-shots are not helpful). It may
  also be helpful to point to the [syntax rules] which specifically address the
  area of concern.
* Feature requests will often be closed with a recommendation that they be
  implemented as third party extensions outside of the core Python-Markdown
  library. Keeping new feature requests implemented as third party extensions
  allows us to keep the maintenance overhead of Python-Markdown to a minimum, so
  that the focus can be on continued stability, bug fixes, and documentation.
* Closing an issue does not necessarily mean the end of a discussion. If you
  believe your issue has been closed incorrectly, explain why and we'll consider
  if it needs to be reopened.

## Pull Requests

A pull request often represents the start of a discussion, and does not
necessarily need to be the final, finished submission. In fact, if you discover
an issue and intend to provide a fix for it, there is no need to open an issue
first. You can report the issue and provide the fix together in a pull request.

All pull requests should be made from your personal clone of the library hosted
in your personal GitHub account. Do not create branches on the
[Python-Markdown/markdown] project for pull requests. All pull requests should
be implemented in a new branch with a unique name. Remember that if you have an
outstanding pull request, pushing new commits to the related branch of your
GitHub repository will also automatically update the pull request. If may help
to review GitHub's documentation on [Using Pull Requests].

If you are providing a fix for a previously reported issue, you must reference
the issue in your commit message. Be sure to prefix the reference with one of
GitHub's [action words] which will automatically close the issue when the pull
request is merged. For example, `fixes #42` and `closes #42` would be
acceptable, whereas `ref #42` would not. Of course, if merging a pull request
should not cause an issue to be closed, then the action word should not be
included when referencing that issue.

Before being accepted, each pull request must include the applicable code, new
tests of all new features, updated tests for any changed features, documentation
updates, and an appropriate update to the release notes. All changes must follow
the applicable style guides. Failure to meet any one of the requirements is
likely to delay any serious consideration of your pull request and may even
cause it to be closed. Of course, if you are in the early stages of development,
you may include a note in the pull request acknowledging that it is incomplete
along with a request for feedback.

Pull requests will generally not be accepted if any tests are failing.
Therefore, it is recommended that you run the tests before submitting your pull
request, ideally using `tox` in order to check that your modifications are
compatible with all supported versions of Python. After making a pull request,
check the Travis build status in the GitHub interface to ensure that all tests
are running as expected.

## Style Guides

### Code Style Guide

### Documentation Style Guide

### Commit Message Style Guide

## Versions

Python-Markdown follows [Semantic Versioning] and uses the
`MAJOR.MINOR.POINT(PRERELEASE/DEV)` format for specifying releases. The status
of the `master` branch should always be identified in the `__version_info__`
variable defined in [`markdown/__init__.py`][markdown/__init__.py] and should
conform to [PEP 440].

### Version Status

A MAJOR version is in development status when the MINOR version is `0`, the
POINT version is `0`, and the version includes a `DEV` segment.

A MINOR version is in development status when the MINOR version is not `0`, the
POINT version is `0`, and the version includes a `DEV` segment.

At all other times, the code is considered stable and release-ready.

MAJOR and MINOR releases may or may not get pre-releases (beta, release
candidate, etc.) at the discretion of the project maintainers.

### Version Workflow

Bug fixes may be committed to the `master` branch at any time.

New features and backward incompatible changes may only be committed to the
`master` branch when the MAJOR and/or MINOR version is in development status.

A separate commit to the `master` branch should be made to bump up the MAJOR
and/or MINOR version and set the development status. Only then will any pull
requests implementing new features or backward incompatible changes be accepted.

If a bug fix is deemed to be important and the `master` branch is in development
status, a back-port of the fix should be committed to a version branch. If the
appropriate version branch does not exist, then it should be created and a pull
request back-porting the fix made against that branch. The version branch should
be named with the most recently released MINOR version. For example, if the
`master` branch is at `3.1.0dev` and the most recent MINOR release was `3.0.4`,
then the version branch would be named `3.0` and any releases from that branch
would increment the POINT version only (`3.0.5`, `3.0.6`...).


[Python-Markdown Organization]: https://github.com/Python-Markdown
[Python-Markdown Code of Conduct]: https://github.com/Python-Markdown/markdown/blob/master/CODE_OF_CONDUCT.md
[Python-Markdown/markdown]: https://github.com/Python-Markdown/markdown
[issue tracker]: https://github.com/Python-Markdown/markdown/issues
[syntax rules]: http://daringfireball.net/projects/markdown/syntax
[Babelmark]: http://johnmacfarlane.net/babelmark2/
[Using Pull Requests]: https://help.github.com/articles/using-pull-requests
[action words]: https://help.github.com/articles/closing-issues-using-keywords/
[Semantic Versioning]: https://semver.org/
[markdown/__init__.py]: https://github.com/Python-Markdown/markdown/blob/master/markdown/__init__.py#L36
[PEP 440]:https://www.python.org/dev/peps/pep-0440/
