# Contributing to Python-Markdown

The following is a set of guidelines for contributing to Python-Markdown and its
extensions, which are hosted in the [Python-Markdown Organization] on GitHub.
These are mostly guidelines, not rules. Use your best judgment, and feel free to
propose changes to this document in a pull request.

## Code of Conduct

This project and everyone participating in it is governed by the
[Python-Markdown Code of Conduct]. By participating, you are expected to uphold
this code. Please report unacceptable behavior to <python.markdown@gmail.com>.

## Project Organization

The core Python-Markdown code base and any built-in extensions are hosted in the
[Python-Markdown/markdown] project on GitHub. Other extensions maintained by the
Python-Markdown project may be hosted as separate repositories in the
[Python-Markdown Organization] on GitHub and must follow best practices for
third-party extensions.

The [Python-Markdown/markdown] project is organized as follows:

* Branch `master` should generally be stable and release-ready at all times.
* Version branches should be used for bug-fixes back-ported to the most recent
  PATCH release.
* No other branches should be created. Any other branches which exist are
  preserved for historical reasons only.

## Issues

Feature requests, bug reports, usage questions, and other issues can all be
raised on the GitHub [issue tracker].

When describing issues try to phrase your ticket in terms of the behavior you
think needs to change rather than the code you think needs to change.

Make sure you're running the latest version of Python-Markdown before reporting
an issue.

Search the issue list first for related items. Be sure to check closed issues
and pull requests. GitHub's search only checks open issues by default.

You may want to check the [syntax rules] and/or [Babelmark] to confirm that your
expectations align with the rules and/or other implementations of Markdown.

If reporting a syntax bug, you must provide the minimal input which exhibits the
behavior, the actual output and the output you expected. All three items must be
provided as textual code blocks (screen-shots are not helpful). It may also be
helpful to point to the [syntax rules] which specifically address the area of
concern.

Feature requests will often be closed with a recommendation that they be
implemented as third party extensions outside of the core Python-Markdown
library. Keeping new feature requests implemented as third party extensions
allows us to keep the maintenance overhead of Python-Markdown to a minimum, so
that the focus can be on continued stability, bug fixes, and documentation.

Closing an issue does not necessarily mean the end of a discussion. If you
believe your issue has been closed incorrectly, explain why and we'll consider
if it needs to be reopened.

## Pull Requests

A pull request often represents the start of a discussion, and does not
necessarily need to be the final, finished submission. In fact, if you discover
an issue and intend to provide a fix for it, there is no need to open an issue
first. You can report the issue and provide the fix together in a pull request.

All pull requests should be made from your personal fork of the library hosted
in your personal GitHub account. Do not create branches on the
[Python-Markdown/markdown] project for pull requests. All pull requests should
be implemented in a new branch with a unique name. Remember that if you have an
outstanding pull request, pushing new commits to the related branch of your
GitHub repository will also automatically update the pull request. It may help
to review GitHub's documentation on [Creating a pull request from a fork].

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
request. After making a pull request, check the build status in the
GitHub interface to ensure that all tests are running as expected. If any checks
fail, you may push additional commits to your branch. GitHub will add those
commits to the pull request and rerun the checks.

## Style Guides

In an effort to maintain consistency, Python-Markdown adheres to the following
style guides in its code and documentation. A pull request may be rejected if it
fails to match the relevant style guides.

### Code Style Guide

Except as noted below, all pull requests should follow Python's standard [PEP8
Style Guide] and are run through [Flake8] to ensure that the style guide is
followed.

Legacy code which does not follow the guidelines should only be updated if and
when other changes (bug fix, feature addition, etc.) are being made to that
section of code. While new features should be given names that follow modern
Python naming conventions, existing names should be preserved to avoid backward
incompatible changes.

Line length is limited to a maximum of 119 characters.

When a line of code does not fit within the line length limit, continuation
lines should align elements wrapped inside parentheses, brackets and braces
using a *hanging indent*. When using a hanging indent there should be no
arguments on the first line and further indentation should be used to clearly
distinguish itself as a continuation line. The closing parenthesis, bracket or
brace should be on a line by itself and should line up under the first character
of the line that starts the multi-line construct.

```python
my_list = [
    1, 2, 3,
    4, 5, 6,
]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
)
```

When the conditional part of an `if`-statement is long enough to require that it
be written across multiple lines, extra indentation should be included on the
conditional continuation line.

```python
if (this_is_one_thing
        and that_is_another_thing):
    do_something()
```

### Documentation Style Guide

Documentation should be in American English. The tone of the documentation
should be simple, plain, objective and well-balanced where possible.

Keep paragraphs reasonably short.

With the exception of code blocks, limit line length to 79 characters. You may
want to use your editor's tools to automatically hard wrap lines of text.

Don't use abbreviations such as 'e.g.' but instead use the long form, such as
'For example'.

The documentation is built from the [Markdown] source files in the [`docs`
directory][docs directory] by the [MkDocs] static site generator. In addition to
the basic Markdown syntax, the following extensions are supported: [extra],
[admonition], [smarty], [codehilite], and [toc].

There are a few conventions you should follow when working on the
documentation.

#### Headers

Headers should use the hash style. For example:

```md
## Some important topic
```

The underline style should not be used. Don't do this:

```md
Some important topic
====================
```

#### Links

Links should always use the reference style, with the referenced hyperlinks kept
at the end of the document.

```md
Here is a link to [some other thing][other-thing].

More text...

[other-thing]: http://example.com/other/thing
```

This style helps keep the documentation source consistent and readable.

If you are linking to another document within Python-Markdown's documentation,
you should use a relative link, and link to the `.md` suffix. If applicable, it
is preferred that the link includes a hash fragment pointing to the specific
section of the page. For example:

```md
[authentication]: reference.md#Markdown
```

Linking in this style ensures that the links work when browsing the
documentation on GitHub. If your Markdown editor makes links clickable, they
will work there as well. When the documentation is built, these links will be
converted into regular links which point to the built HTML pages.

#### Notes and Warnings

If you want to draw attention to a note or warning, use the syntax defined in
Python-Markdown's [Admonition Extension]:

```md
!!! note

    This is the content of the note.
```

### Commit Message Style Guide

Use the present tense ("Add feature" not "Added feature").

Use the imperative mood ("Move item to..." not "Moves item to...").

Limit the first line to 72 characters or less.

Reference issues and pull requests liberally after the first line. Include a
summary of the changes/additions made without replicating the content of the
documentation or release notes. This is where an explanation of the choices made
should be found. References to issues and pull requests should only provide the
context in which a choice was made. However, the commit should be able to stand
on its own.

## Development Environment

To start developing on Python-Markdown is it best to create a [fork] of the
project on GitHub. After [cloning your fork] to your local system, you will want
to [configure a remote] that points to the upstream repository so that you can
[sync changes] made in the original repository with your fork.

It is recommended that all development be done from within a Python [virtual
environment], which isolates any experimental code from the general system. To
create a virtual environment, use the following command from the root of the
local working copy of your GitHub fork:

```sh
virtualenv venv
```

That creates a virtual environment which is contained in the `venv` directory
within your local working copy. Note that the repository is configured so that
git will ignore any files within a directory named `venv` or `ENV` for this
very reason.

On Posix systems (Linux, BSD, MacOS, etc.), use the following command to
activate the environment:

```sh
source venv/bin/activate
```

On Windows, use this command instead:

```sh
venv/Scripts/activate
```

See the [User Guide] for more information on using virtual environments.

To be able to run the Markdown library directly while working on it, install the
working copy into the environment in [Development Mode] after activating the
virtual environment for the first time:

```sh
pip install --editable .
```

Now any saved changes will immediately be available within the virtual
environment.

You can run the command line script with the following command:

```sh
python -m markdown
```

And you can directly run the tests with:

```sh
python -m unittest discover tests
```

!!! note

    Some tests require the [PyTidyLib] library, which depends on the [HTML Tidy]
    library. If you do not have PyTidyLib installed, the tests which depend upon
    it will be skipped. Given the difficulty in installing the HTML Tidy library
    on many systems, you may choose to leave both libraries uninstalled and
    depend on the Travis server to run those tests when you submit a pull
    request.

The above setup will only run tests against the code in one version of Python.
However,  Python-Markdown supports multiple versions of Python. Therefore, a
[tox] configuration is included in the repository, which includes test
environments for all supported Python versions, a [Flake8] test environment, and
a spellchecker for the documentation. While it is generally fine to leave those
tests for the Travis server to run when a pull request is submitted, for more
advanced changes, you may want to run those tests locally. To do so, simply
install tox:

```sh
pip install tox
```

Then, to run all configured test environments, simply call the command `tox`
with no arguments. See help (`tox -h`) for more options.

!!! note

    The tox environments expect that some dependencies are already installed on
    your system. For example, by default, any Python version specific
    environment will fail if that version of Python is not installed.
    Additionally, the tox environments assume that the [HTML Tidy] library is
    installed and may fail when attempting to install [PyTidyLib] if it is not.
    Finally, the `spellchecker` environment requires [aspell] and the
    `aspell-en` dictionary to be installed. Unfortunately, installing those
    dependencies may differ significantly from system to system and is outside
    the scope of this guide.

!!! seealso "See Also"

    Python-Markdown provides [test tools] which simply testing Markdown syntax.
    Understanding those tools will often help in understanding why a test may be
    failing.

## Versions

Python-Markdown follows [Semantic Versioning] and uses the
`MAJOR.MINOR.PATCH[.dev#|a#|b#|rc#]` format for identifying releases. The status
of the `master` branch should always be identified in the `__version_info__`
tuple defined in [`markdown/__meta__.py`][markdown/__meta__.py]. The contents of
that tuple will automatically be converted into a normalized version which
conforms to [PEP 440]. An invalid `__version_info__` tuple will raise an error,
preventing the library from running and the package from building.

### Version Status

A MAJOR version is in development status when the MINOR version is `0`, the
PATCH version is `0`, and the version includes a `dev` segment.

A MINOR version is in development status when the MINOR version is not `0`, the
PATCH version is `0`, and the version includes a `dev` segment.

At all other times, the code is considered stable and release-ready.

MAJOR and MINOR releases may or may not get pre-releases (alpha, beta, release
candidate, etc.) at the discretion of the project maintainers.

### Version Workflow

Bug fixes may be merged from a pull request to the `master` branch at any time
so long as all tests pass, including one or more new tests which would have
failed prior to the change.

New features and backward incompatible changes may only be merged to the
`master` branch when the MAJOR and/or MINOR version is in development status
pursuant to [Semantic Versioning].

A separate commit to the `master` branch should be made to bump up the MAJOR
and/or MINOR version and set development status. Only then will any pull
requests implementing new features or backward incompatible changes be accepted.

If a bug fix is deemed to be important and the `master` branch is in development
status, a back-port of the fix should be committed to a version branch. If the
appropriate version branch does not exist, then it should be created and a pull
request back-porting the fix made against that branch. The version branch should
be named with the most recently released MINOR version. For example, if the
`master` branch is at `3.1.dev0` and the most recent MINOR release was `3.0.4`,
then the version branch would be named `3.0` and any releases from that branch
would increment the PATCH version only (`3.0.5`, `3.0.6`...).

## Release Process

When a new release is being prepared, the release manager should follow the
following steps:

1. Verify that all outstanding issues and pull requests related to the release
   have been resolved.

2. Confirm that the release notes and change log have been updated and indicate
   the date of the new release.

3. Update the version defined in [`markdown/__meta__.py`][markdown/__meta__.py].

4. Build a local copy of the documentation, browse through the pages and
   confirm that no obvious issues exist with the documentation.

5. Create a pull request with a commit message in the following format:

        Bump version to X.X.X

6. After all checks have passed, merge the pull request.

7. Create a git tag with the new version as the tag name and push to the
   [Python-Markdown/markdown] repository. The new tag should trigger a GitHub
   workflow which will automatically deploy the release to PyPI and update the
   documentation.

    In the event that the deployment fails, the following steps can be taken to
    deploy manually:

    - Deploy the release to [PyPI] with the command `make deploy`.

    - Deploy an update to the documentation using [MkDocs]. The following example
      assumes that local clones of the [Python-Markdown/markdown] and
      [Python-Markdown/Python-Markdown.github.io] repositories are in sibling
      directories named `markdown` and `Python-Markdown.github.io` respectively.

            cd Python-Markdown.github.io
            mkdocs gh-deploy --config-file ../markdown/mkdocs.yml --remote-branch master

## Issue and Pull Request Labels

Below are the labels used to track and manages issues and pull requests. The
labels are loosely grouped by their purpose, but it is not necessary for every
issue to have a label from every group, and an issue may have more than one
label from the same group.

### Type of Issue or Pull Request

| Label name                   | Description      |
| ---------------------------- | ---------------- |
| `bug`{ .label .bug }         | Bug report.      |
| `feature`{ .label .feature } | Feature request. |
| `support`{ .label .support } | Support request. |
| `process`{ .label .process } | Discussions regarding policies and development process. |

### Category of Issue or Pull Request

| Label name                       | Description                              |
| -------------------------------- | ---------------------------------------- |
| `core`{ .label .core }           | Related to the core parser code.                   |
| `extension`{ .label .extension } | Related to one or more of the included extensions. |
| `docs`{ .label .docs }           | Related to the project documentation.              |

### Status of Issue

| Label name                              | Description                       |
| --------------------------------------- | --------------------------------- |
| `more-info-needed`{ .label .pending }   | More information needs to be provided.              |
| `needs-confirmation`{ .label .pending } | The alleged behavior needs to be confirmed.         |
| `needs-decision`{ .label .pending }     | A decision needs to be made regarding request.      |
| `confirmed`{ .label .approved }         | Confirmed bug report or approved feature request.   |
| `someday-maybe`{ .label .low }          | Approved **low priority** request.                  |
| `duplicate`{ .label .rejected }         | The issue has been previously reported.             |
| `wontfix`{ .label .rejected }           | The issue will not be fixed for the stated reasons. |
| `invalid`{ .label .rejected }           | Invalid report (user error, upstream issue, etc).   |
| `3rd-party`{ .label .rejected }         | Should be implemented as a third party extension.   |


### Status of Pull Request

| Label name                            | Description                         |
| ------------------------------------- | ----------------------------------- |
| `work-in-progress`{ .label .pending } | A partial solution. More changes will be coming.     |
| `needs-review`{ .label .pending }     | Needs to be reviewed and/or approved.                |
| `requires-changes`{ .label .pending } | Awaiting updates after a review.                     |
| `approved`{ .label .approved }        | The pull request is ready to be merged.              |
| `rejected`{ .label .rejected }        | The pull request is rejected for the stated reasons. |

[Python-Markdown Organization]: https://github.com/Python-Markdown
[Python-Markdown Code of Conduct]: https://github.com/Python-Markdown/markdown/blob/master/CODE_OF_CONDUCT.md
[Python-Markdown/markdown]: https://github.com/Python-Markdown/markdown
[issue tracker]: https://github.com/Python-Markdown/markdown/issues
[syntax rules]: https://daringfireball.net/projects/markdown/syntax
[Babelmark]: https://johnmacfarlane.net/babelmark2/
[Creating a pull request from a fork]: https://help.github.com/articles/creating-a-pull-request-from-a-fork/
[action words]: https://help.github.com/articles/closing-issues-using-keywords/
[PEP8 Style Guide]: https://www.python.org/dev/peps/pep-0008/
[Flake8]: http://flake8.pycqa.org/en/latest/index.html
[Markdown]: https://daringfireball.net/projects/markdown/basics
[docs directory]: https://github.com/Python-Markdown/markdown/tree/master/docs
[MkDocs]: https://www.mkdocs.org/
[extra]: extensions/extra.md
[admonition]: extensions/admonition.md
[smarty]: extensions/smarty.md
[codehilite]: extensions/code_hilite.md
[toc]: extensions/toc.md
[Admonition Extension]: extensions/admonition.md#syntax
[fork]: https://help.github.com/articles/about-forks
[cloning your fork]: https://help.github.com/articles/cloning-a-repository/
[configure a remote]: https://help.github.com/articles/configuring-a-remote-for-a-fork
[sync changes]: https://help.github.com/articles/syncing-a-fork
[virtual environment]: https://virtualenv.pypa.io/en/stable/
[User Guide]: https://virtualenv.pypa.io/en/stable/user_guide.html
[Development Mode]: https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode
[PyTidyLib]: https://countergram.github.io/pytidylib/
[HTML Tidy]: https://www.html-tidy.org/
[tox]: https://tox.readthedocs.io/en/latest/
[aspell]: http://aspell.net/
[test tools]: test_tools.md
[Semantic Versioning]: https://semver.org/
[markdown/__meta__.py]: https://github.com/Python-Markdown/markdown/blob/master/markdown/__meta__.py#L29
[PEP 440]: https://www.python.org/dev/peps/pep-0440/
[PyPI]: https://pypi.org/project/Markdown/
[Python-Markdown/Python-Markdown.github.io]: https://github.com/Python-Markdown/Python-Markdown.github.io

<style type="text/css">
    /* GitHub Label Styles */

    code.label {
        color: #000000;
        font-weight: 600;
        line-height: 15px;
        display: inline-block;
        padding: 4px 6px;
    }
    code.bug {
        background-color: #c45b46;
    }
    code.feature {
        background-color: #7b17d8;
        color: #ffffff;
    }
    code.support {
        background-color: #efbe62;
    }
    code.process {
        background-color: #eec9ff;
    }
    code.core {
        background-color: #0b02e1;
        color: #ffffff;
    }
    code.extension {
        background-color: #709ad8;
    }
    code.docs {
        background-color: #b2ffeb;
    }
    code.approved {
        background-color: #beed6d;
    }
    code.low {
        background-color: #dddddd;
    }
    code.pending {
        background-color: #f0f49a;
    }
    code.rejected {
        background-color: #f7c7be;
    }
</style>
