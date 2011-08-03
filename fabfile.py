"""
Common maintenance commands for the Python-Markdown package.
"""

from fabric.api import local, lcd, settings, hide, prefix, prompt, abort
from sys import version as _pyversion
from sys import platform


def _get_versions():
    """ Find and comfirm all supported versions of Python. """
    vs = []
    for v in ['2.4', '2.5', '2.6', '2.7', '3.1', '3.2']:
        with settings(
            hide('warnings', 'running', 'stdout', 'stderr'),
            warn_only=True
        ):
            result = local('hash python%s' % v)
            if not result.failed:
                vs.append(v)
    return vs
confirmed_versions = _get_versions()

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
        local('2to3-%s -w build/test.%s/tests' % (version, version))
        local('2to3-%s -w build/test.%s/run-tests.py' % (version, version))

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
    ans = prompt('Have you updated the version in both setup.py and __init__.py?', default='Y')
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
    upload_to_github()

def upload_to_github():
    """ Upload release to Github. """
    # We need github API v3 but no python lib exists yet. So do it manually.
    import os
    import urllib2
    import base64
    import simplejson
    import getpass
    # Setup Auth
    url = 'https://api.github.com/repos/waylan/Python-Markdown/downloads'
    user = prompt('Github username:', default=getpass.getuser())
    password = prompt('Github password:')
    authstring = base64.encodestring('%s:%s' % (user, password))
    # Loop through files and upload
    base = 'dist/'
    for file in os.listdir(base):
        file = os.path.join(base, file)
        if os.path.isfile(file):
            ans = prompt('Upload: %s' % file, default='Y')
            if ans.lower() == 'y':
                # Create document entry on github
                desc = prompt('Description for %s:' % file)
                data1 = simplejson.dumps({
                    'name': os.path.basename(file),
                    'size': os.path.getsize(file),
                    'description' : desc,
                    #'content_type': 'text/plain' # <-  let github determine
                })
                req = urllib2.Request(url, data1, 
                                      {'Content-type': 'application/json'})
                req.add_header('Authorization', 'Basic %s' % authstring)
                try:
                    response = urllib2.urlopen(req)
                except urllib2.HTTPError, e:
                    error = simplejson.loads(e.read())
                    if error['errors'][0]['code'] == 'already_exists':
                        print 'Already_exists, skipping...'
                        continue
                    else:
                        print e.read()
                        raise
                data2 = simplejson.loads(response.read())
                response.close()
                # Upload document (using curl because it is easier)
                data2['file'] = file
                curl = """curl \\
                -F "key=%(path)s" \\
                -F "acl=%(acl)s" \\
                -F "success_action_status=201" \\
                -F "Filename=%(name)s" \\
                -F "AWSAccessKeyId=%(accesskeyid)s" \\
                -F "Policy=%(policy)s" \\
                -F "Signature=%(signature)s" \\
                -F "Content-Type=%(mime_type)s" \\
                -F "file=@%(file)s" \\
                %(s3_url)s""" % data2
                print 'Uploading...'
                local(curl)
        else:
            print 'Skipping...'
