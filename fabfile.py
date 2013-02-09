"""
Common maintenance commands for the Python-Markdown package.
"""

from fabric.api import local, lcd, settings, hide, prefix, prompt, abort
from sys import version as _pyversion
from sys import platform


def _get_versions():
    """ Find and comfirm all supported versions of Python. """
    vs = []
    for v in ['2.5', '2.6', '2.7', '3.1', '3.2']:
        with settings(
            hide('warnings', 'running', 'stdout', 'stderr'),
            warn_only=True
        ):
            result = local('hash python%s' % v)
            if not result.failed:
                vs.append(v)
    return vs
confirmed_versions = _get_versions()

def clean():
    """ Clean up dir. """
    local('git clean -dfx')

def list_versions():
    """ List all supported versions of Python. """
    print('Supported Python versions available on this system:')
    print('    Python ' + '\n    Python '.join(confirmed_versions))

def test(version=_pyversion[:3]):
    """ Run tests with given Python Version. Defaults to system default. """
    if version in confirmed_versions:
        build_tests(version=version)
        #with prefix('bash $HOME/.virtualenvs/md%s/bin/activate' % version):
        with lcd('build/test.%s/' % version):
            local('python%s run-tests.py' % version)
    else:
        print('Python %s is not an available supported version.' % version)
        list_versions()

def test_all():
    """ Run tests in all available supported versions. """
    for v in confirmed_versions:
        test(v)

def build_tests(version=_pyversion[:3]):
    """ Build tests for given Python Version. """
    local('python%s setup.py build --build-purelib build/test.%s' % \
                                                            (version, version))
    local('rm -rf build/test.%s/tests' % version)
    local('mkdir build/test.%s/tests' % version)
    local('cp -r tests/* build/test.%s/tests' % version)
    local('cp run-tests.py build/test.%s/run-tests.py' % version)
    local('cp setup.cfg build/test.%s/setup.cfg' % version)
    if version.startswith('3'):
        # Do 2to3 conversion
        local('2to3-%s -w -d build/test.%s/markdown' % (version, version))


def generate_test(file):
    """ Generate a given test. """
    import sys, os
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    import tests
    config = tests.get_config(os.path.dirname(file))
    root, ext = os.path.splitext(file)
    if ext == config.get(tests.get_section(os.path.basename(root), config), 
                         'input_ext'):
        tests.generate(root, config)
    else:
        print file, 'does not have a valid file extension. Check config.'

def generate_tests():
    """ Generate all outdated tests. """
    import sys, os
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    from tests import generate_all
    generate_all()

def build_env(version=_pyversion[:3]):
    """ Build testing environment for given Python version. """
    if version in confirmed_versions:
        if version == '2.4':
            local('sudo pip%s install ElementTree' % version)
        local('sudo pip%s install nose' % version)

def build_envs():
    """ Build testing env in all supported versions. """
    for v in confirmed_versions:
        build_env(v)

def build_release():
    """ Build a package for distribution. """
    ans = prompt('Have you updated the version_info in __version__.py?', default='Y')
    if ans.lower() == 'y':
        local('./setup.py sdist --formats zip,gztar')
        if platform == 'win32':
            local('./setup.py bdist_wininst')
    else:
        abort('Try again after updating the version numbers.')

def deploy_release():
    """ Register and upload release to PyPI and Github. """
    build_release()
    local('./setup.py register')
    local('./setup.py upload')
