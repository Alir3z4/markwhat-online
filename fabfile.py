import os
from time import gmtime, strftime
from contextlib import contextmanager
from functools import wraps
from fabric.api import env, local, lcd, run, prefix, cd
from fabric.colors import green


# Leveraging native SSH config files
from fabric.operations import prompt

env.use_ssh_config = True

# Project
env.root = os.path.abspath(os.path.dirname(__file__))
env.project_name = 'markwhat'
env.django_project_dir = 'markwhat'
env.project_path = env.root
env.repo_prod = 'heroku'
env.repo_stage = 'staging'


# Config
env.venv_name = "%(project_name)sEnv" % env
env.venv_path = "%(project_path)s/%(venv_name)s" % env
env.venv_python_path = "%(venv_path)s/lib/python2.7/site-packages" % env
env.activate = 'source %(venv_path)s/bin/activate' % env
env.python = 'python'
env.utc_ts = gmtime()
env.utc_ts_str = strftime('%Y%m%d_%H%M%S', env.utc_ts)

# Local
env.lvenv_path = '../%(venv_name)s' % env
env.lactivate = "source %(lvenv_path)s/bin/activate"

# Env names
env.env_name = '<MAIN_APP_ENV>'


apps = [
    'whatwhat',
]

localization_dirs = apps + [
    'templates',
    'markwhat',
]


def grint(msg):
    """
    print in green with bold text.
    """
    print(green('-------> {0}'.format(msg.strip()), True))


def grintify(method):
    """
    Take the docstring from the method
    and print-out with green font with help of
    grint()
    """

    @wraps(method)
    def _wrapped_method(*args, **kwrags):
        grint(method.__doc__)
        return method(*args, **kwrags)

    return _wrapped_method


@grintify
def set_env(env_name):
    """
    Set `env.env_name`.
    """
    grint('Set env_name to {0}'.format(env_name))
    env.env_name = env_name


@grintify
def coverage():
    """
    Code coverage report.
    """
    local("coverage run --source='.' manage.py test {0}".format(' '.join(apps)))
    local("coverage report")


@grintify
def make_msg():
    """
    Make messages for the whole project for each app
    """
    for app in localization_dirs:
        with lcd(app):
            grint("makemessage for: {0}".format(app))
            local('mkdir -p locale')
            local('django-admin.py makemessages -l en')
    # git_add_dot()
    # local("git commit -m 'Makes translation files'")


@grintify
def compile_msg():
    """
    Compile messages for whole project for each app
    """
    for app in apps:
        with lcd(app):
            local('django-admin.py compilemessages')
    # git_add_dot()
    # local("git commit -m 'Compiles translation files'")


@grintify
def tx_push():
    """
    Push Translation to transifex
    """
    local('tx push --source')


@grintify
def tx_pull():
    """
    Pull translation from transifex
    """
    local('tx pull -a')


@grintify
def syncdb():
    """
    Syncd db, mean sync the db
    """
    manage_pro('syncdb')


@grintify
def syncdb_all():
    """
    Syncd db, mean sync the db [--all]
    """
    manage_pro('syncdb --all')


def _git(cmd):
    local('git {0}'.format(cmd))


@grintify
def git_push():
    """
    Push the repository to remote
    """
    _git('push origin --all')


@grintify
def git_push_pro():
    """
    Push the repository to the production env
    """
    _git('push %(repo_prod)s master' % env)


@grintify
def git_push_stage():
    """
    Push the repository to the staging env
    """
    _git('push %(repo_stage)s master' % env)


@grintify
def git_pull():
    """
    Pull the changes from origin remote branch
    """
    _git("pull")


@grintify
def git_add_dot():
    """
    run "git add ."
    """
    _git("add .")


@grintify
@contextmanager
def venv():
    """
    Activate the virtualenv
    """
    with cd(env.venv_path):
        with prefix(env.activate):
            yield


@grintify
def manage_local(cmd):
    """
    Run manage.py on local.
    """
    local('python manage.py %s' % cmd)


@grintify
def manage_pro(cmd):
    """
    Run a manage.py command at production level.
    """
    heroku_run('python manage.py {0}'.format(cmd))


## Heroku
@grintify
def main_app():
    """
    Set env to production.
    """
    set_env("<MAIN_APP_ENV>")


@grintify
def staging_app():
    """
    Set env to staging.
    """
    set_env("<STAGING_APP_ENV>")


@grintify
def heroku(cmd):
    """
    Run a command with heroku toolbet
    """
    local("heroku {0} --app {1}".format(cmd, env.env_name))


@grintify
def heroku_run(cmd):
    """
    Run a command at heroku.
    """
    heroku("run {0}".format(cmd))


@grintify
def restart_app():
    """
    Restart the app webserver
    """
    heroku('ps:restart')


@grintify
def heroku_config_set():
    """
    Set a new key on heroku config env vars
    """
    config_set = {}

    while True:
        grint('Set: [{0}]'.format(len(config_set)))
        key = prompt('Config Key:').upper()
        value = prompt('Config Value:')

        if key in ['', None]:
            break

        config_set[key.upper()] = value

        grint('Added {0}={1}'.format(key, value))

    config_cmd_list = []
    for k in config_set:
        config_cmd_list.append('{0}={1}'.format(k, config_set[k]))

    heroku("config:set {0}".format(' '.join(config_cmd_list)))


@grintify
def compile_po():
    """
    Compile GetText *.po files.
    """
    for app in localization_dirs:
        heroku_run('"cd {0} && django-admin.py compilemessages"'.format(app))


## !Heroku



@grintify
def upgrade_dj(mode):
    """
    Upgrading Django.
    """
    if mode == 'prod':
        grint("Production mode has initialed.")
        with cd(env.project_path):
            grint("Removing django from top python path.")
            try:
                run("rm -rf %(top_python_path)s/{django,Django*.egg*}" % env)
            except:
                pass
            grint("Copying django from VirtualEnv to to python path.")
            run("cp -r %(venv_python_path)s/{django,Django*.egg*} %(top_python_path)s/" % env)
            run("ls %(top_python_path)s/" % env)

    elif mode == 'dev':
        grint("Development mode has initialed.")

        if os.path.exists("django-trunk"):
            grint("Updating django master repo.")
            with lcd("django-trunk"):
                local("git pull origin stable/1.5.x")
                # local("git checkout tags/1.5.x")
        else:
            grint("Cloning django git repo.")
            local("git clone git://github.com/django/django.git django-trunk")

        grint("Uninstall old django.")
        local("pip uninstall django")
        grint("Installing fresh ans shiny as fuck django version.")
        local("pip install -e django-trunk/")
    else:
        raise ValueError("env variable have UNKNOWN value: %s" % mode)


@grintify
def test_stage():
    """
    Run tests on stage environment.
    """
    manage_stage('test -v2 {0}'.format(' '.join(apps)))


@grintify
def validate():
    """
    Validate the local project
    """
    grint('Validating the local source code...')
    manage_local('validate')


@grintify
def run_tests():
    """
    Run Tests.
    """
    manage_local('test -v2 {0}'.format(' '.join(apps)))


@grintify
def clean_pyc():
    """
    Clean python compiled files (*.pyc)
    """
    local("find %(app_path)s/ -name '*.pyc' -delete" % env)


@grintify
def cs():
    """
    Collect static files
    """
    manage_pro('collectstatic --noinput')



@grintify
def deploy():
    """
    Deploy the project to production server
    """
    validate()
    git_push()
    git_push_pro()


@grintify
def stage():
    """
    Deploy the project staging server.
    """
    validate()
    git_push()
    git_push_stage()