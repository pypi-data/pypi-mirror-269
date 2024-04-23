"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import sys
import logging
import socket
import pathlib
import os
import io
import json
import getpass

from colorama import init, Fore
from requests import request

from data_studio.io_storages.s3.utils import synchronize_s3_import_storage


if sys.platform == 'win32':
    init(convert=True)

# on windows there will be problems with sqlite and json1 support, so fix it
from data_studio.core.utils.windows_sqlite_fix import windows_dll_fix

windows_dll_fix()

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from django.db import connections, DEFAULT_DB_ALIAS, IntegrityError
from django.db.backends.signals import connection_created
from django.db.migrations.executor import MigrationExecutor
from data_studio.core.argparser import parse_input_args
from data_studio.core.utils.params import get_env

logger = logging.getLogger(__name__)

LS_PATH = str(pathlib.Path(__file__).parent.absolute())
DEFAULT_USERNAME = 'default_user@localhost'



def _setup_env():
    sys.path.insert(0, LS_PATH)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_studio.core.settings.data_studio")
    application = get_wsgi_application()

from django.contrib.auth import authenticate


def _app_run(host, port):
    http_socket = '{}:{}'.format(host, port)
    call_command('runserver', '--noreload', http_socket)


def _set_sqlite_fix_pragma(sender, connection, **kwargs):
    """Enable integrity constraint with sqlite."""
    if connection.vendor == 'sqlite' and get_env('AZURE_MOUNT_FIX'):
        cursor = connection.cursor()
        cursor.execute('PRAGMA journal_mode=wal;')


def is_database_synchronized(database):
    connection = connections[database]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    return not executor.migration_plan(targets)


def connect_and_save_ml_backends(project_name, ml_backend_urls, ml_backend_names, is_interactive = 1):
    from django.contrib.auth.models import User
    from django.core.exceptions import ObjectDoesNotExist
    from projects.models import Project
    from ml.models import MLBackend

    try:
        project = Project.objects.get(title=project_name)
        if project.created_by != User and not User.is_superuser:
            print(f"User '{User.username}' is not authorized to modify project '{project_name}'.")
            sys.exit(1)
    except ObjectDoesNotExist:
        print(f"Project '{project_name}' not found.")
        sys.exit(1)

    for url, name in zip(ml_backend_urls, ml_backend_names + [''] * (len(ml_backend_urls) - len(ml_backend_names))):
        name = name or url
        if connect_to_ml_backend(url, is_interactive):
            ml_backend, created = MLBackend.objects.get_or_create(
                url=url,
                project=project,
                defaults={'title': name, 'is_interactive': is_interactive}
            )
            if not created:
                ml_backend.title = name
                ml_backend.is_interactive = is_interactive
                ml_backend.save()
            print(f"{'Connected to' if created else 'Updated'} ML backend '{name}' for project '{project_name}'.")

import requests

def connect_to_ml_backend(url, is_interactive):
    HEALTH_CHECK_ENDPOINT = "/health"
    try:
        response = requests.get(f"{url}{HEALTH_CHECK_ENDPOINT}")
        if response.status_code == 200:
            print(f"Successfully connected to ML backend at {url}. Interactive: {is_interactive}")
            return True
        else:
            print(f"Failed to connect to ML backend at {url}. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error connecting to the ML backend at {url}: {e}")
        return False

def _apply_database_migrations():
    connection_created.connect(_set_sqlite_fix_pragma)
    if not is_database_synchronized(DEFAULT_DB_ALIAS):
        print('Initializing database..')
        call_command('migrate', '--no-color', verbosity=0)


def _get_config(config_path):
    with io.open(os.path.abspath(config_path), encoding='utf-8') as c:
        config = json.load(c)
    return config




def _create_project(title, user, label_config=None, sampling=None, description=None, ml_backends=None):
    from projects.models import Project
    from organizations.models import Organization

    project = Project.objects.filter(title=title).first()
    if project is not None:
        print('Project with title "{}" already exists'.format(title))
    else:
        org = Organization.objects.first()
        org.add_user(user)
        project = Project.objects.create(title=title, created_by=user, organization=org)
        print('Project with title "{}" successfully created'.format(title))

    if label_config is not None:
        with open(os.path.abspath(label_config)) as c:
            project.label_config = c.read()

    if sampling is not None:
        project.sampling = sampling

    if description is not None:
        project.description = description

    if ml_backends is not None:
        from ml.models import MLBackend

        # e.g.: localhost:8080,localhost:8081;localhost:8082
        for url in ml_backends:
            logger.info('Adding new ML backend %s', url)
            MLBackend.objects.create(project=project, url=url)

    project.save()
    return project


def _get_user_info(username):
    from users.models import User
    from users.serializers import UserSerializer
    if not username:
        username = DEFAULT_USERNAME

    user = User.objects.filter(email=username)
    if not user.exists():
        print({'status': 'error', 'message': f"user {username} doesn't exist"})
        return

    user = user.first()
    user_data = UserSerializer(user).data
    user_data['token'] = user.auth_token.key
    user_data['status'] = 'ok'
    print('=> User info:')
    print(user_data)
    return user_data



def _create_user(input_args, config):
    from users.models import User
    from organizations.models import Organization

    username = input_args.username or config.get('username') or get_env('USERNAME')
    password = input_args.password or config.get('password') or get_env('PASSWORD')
    
    token = input_args.user_token or config.get('user_token') or get_env('USER_TOKEN')

    if not username:
        user = User.objects.filter(email=DEFAULT_USERNAME).first()
        if user is not None:
            if password and not user.check_password(password):
                user.set_password(password)
                user.save()
                print(f'User {DEFAULT_USERNAME} password changed')
            return user

        if input_args.quiet_mode:
            return None

        print(f'Please enter default user email, or press Enter to use {DEFAULT_USERNAME}')
        username = input('Email: ')
        if not username:
            username = DEFAULT_USERNAME

    if not password and not input_args.quiet_mode:
        password = getpass.getpass(f'User password for {username}: ')

    try:
        user = User.objects.create_user(email=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if token and len(token) > 5:
            from rest_framework.authtoken.models import Token
            Token.objects.filter(key=user.auth_token.key).update(key=token)
        elif token:
            print(f"Token {token} is not applied to user {DEFAULT_USERNAME} "
                  f"because it's empty or len(token) < 5")

    except IntegrityError:
        print('User {} already exists'.format(username))

    user = User.objects.get(email=username)
    org = Organization.objects.first()
    if not org:
        org = Organization.create_organization(created_by=user, title='Data Studio')
    else:
        org.add_user(user)
    user.active_organization = org
    user.save(update_fields=['active_organization'])

    return user


def _init(input_args, config):
    user = _create_user(input_args, config)

    if user and input_args.project_name and not _project_exists(input_args.project_name):
        from projects.models import Project
        sampling_map = {'sequential': Project.SEQUENCE, 'uniform': Project.UNIFORM,
                        'prediction-score-min': Project.UNCERTAINTY}
        _create_project(
            title=input_args.project_name,
            user=user,
            label_config=input_args.label_config,
            description=input_args.project_desc,
            sampling=sampling_map.get(input_args.sampling, 'sequential'),
            ml_backends=input_args.ml_backends
        )
    elif input_args.project_name:
        print('Project "{0}" already exists'.format(input_args.project_name))


def _reset_password(input_args):
    from users.models import User

    username = input_args.username
    if not username:
        username = input('Username: ')

    user = User.objects.filter(email=username).first()
    if user is None:
        print('User with username {} not found'.format(username))
        return

    password = input_args.password
    if not password:
        password = getpass.getpass('New password:')

    if not password:
        print('Can not set empty password')
        return

    if user.check_password(password):
        print('Entered password is the same as current')
        return

    user.set_password(password)
    user.save()
    print('Password successfully changed')


def check_port_in_use(host, port):
    logger.info('Checking if host & port is available :: ' + str(host) + ':' + str(port))
    host = host.replace('https://', '').replace('http://', '')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


def _get_free_port(port, debug):
    # check port is busy
    if not debug:
        original_port = port
        # try up to 1000 new ports
        while check_port_in_use('localhost', port):
            old_port = port
            port = int(port) + 1
            if port - original_port >= 1000:
                raise ConnectionError(
                    '\n*** WARNING! ***\n Could not find an available port\n'
                    + ' to launch Data Studio. \n Last tested port was '
                    + str(port)
                    + '\n****************\n'
                )
            print(
                '\n*** WARNING! ***\n* Port '
                + str(old_port)
                + ' is in use.\n'
                + '* Trying to start at '
                + str(port)
                + '\n****************\n'
            )
    return port


def _project_exists(project_name):
    from projects.models import Project

    return Project.objects.filter(title=project_name).exists()


def main():
    input_args = parse_input_args(sys.argv[1:])

    # setup logging level
    if input_args.log_level:
        os.environ.setdefault("LOG_LEVEL", input_args.log_level)

    if input_args.database:
        database_path = pathlib.Path(input_args.database)
        os.environ.setdefault("DATABASE_NAME", str(database_path.absolute()))

    if input_args.data_dir:
        data_dir_path = pathlib.Path(input_args.data_dir)
        os.environ.setdefault("LABEL_STUDIO_BASE_DATA_DIR", str(data_dir_path.absolute()))

    config = _get_config(input_args.config_path)

    # set host name
    host = input_args.host or config.get('host', '')
    if not get_env('HOST'):
        os.environ.setdefault('HOST', host)  # it will be passed to settings.HOSTNAME as env var

    _setup_env()
    _apply_database_migrations()

    from data_studio.core.utils.common import collect_versions
    versions = collect_versions()

    if input_args.command == 'reset_password':
        _reset_password(input_args)
        return

    if input_args.command == 'shell':
        call_command('shell_plus')
        return

    if input_args.command == 'calculate_stats_all_orgs':
        from tasks.functions import calculate_stats_all_orgs
        calculate_stats_all_orgs(input_args.from_scratch, redis=True)
        return
    # -------------------------------------------------------
    
    if input_args.command == 'ml-backend':
        from django.contrib.auth import authenticate
        from ml.models import MLBackend
        from projects.models import Project
        from django.core.exceptions import ObjectDoesNotExist
        from django.db.utils import IntegrityError

        user = authenticate(username=input_args.username, password=input_args.password)
        if not user:
            print('Authentication failed.')
            sys.exit(1)
            
        else:
            print('Authentication successful.')
            
        

        try:
            project = Project.objects.get(title=input_args.project_name)
        except ObjectDoesNotExist:
            print(f"Project '{input_args.project_name}' does not exist.")
            sys.exit(1)

        ml_backend_url = input_args.ml_backend_urls
        ml_backend_name = input_args.ml_backend_name if 'ml_backend_name' in input_args else ml_backend_url
        is_interactive = input_args.is_interactive if 'is_interactive' in input_args else False

        try:
            ml_backend, created = MLBackend.objects.update_or_create(
                project=project,
                url=ml_backend_url,
                defaults={
                    'title': ml_backend_name,
                    'is_interactive': is_interactive
                }
            )
        except IntegrityError as e:
            print(f'Failed to add or update ML backend due to error: {e}')
            sys.exit(1)

        action = "Added" if created else "Updated"
        print(f"{action} ML backend '{ml_backend_name}' with URL '{ml_backend_url}' to project '{project.title}'.")


    # if input_args.command == 'ml_backend':
    #     from django.core.management.base import CommandError
        
    #     user = authenticate(username=input_args.username, password=input_args.password)
    #     if not user:
    #         raise CommandError('Authentication failed.')

    #     # Get project
    #     from ml.models import MLBackend

    #     try:
    #         project = Project.objects.get(title=input_args.project_title)
    #     except Project.DoesNotExist:
    #         raise CommandError(f"Project titled '{input_args.project_title}' does not exist.")

    #     # Connect and save ML backend
    #     ml_backend, created = MLBackend.objects.update_or_create(
    #         project=project,
    #         url=input_args.ml_backend_url,
    #         defaults={'title': input_args.ml_backend_name or input_args.ml_backend_url, 'is_interactive': 1}
    #     )
    #     action = "Added" if created else "Updated"
    #     print(f"{action} ML backend '{input_args.ml_backend_name}' with URL '{input_args.ml_backend_url}' to project '{input_args.project_title}'.")
        
        # if created:
        #     connect_to_ml_backend(input_args.ml_backend_url, 1)
        # return
    
    # if input_args.command == 'connect_ml_backends':
    #     from django.core.management.base import CommandError
    #     user = authenticate(username=input_args.username, password=input_args.password)
    #     if not user:
    #         raise CommandError('Authentication failed.')
        
    #     connect_and_save_ml_backends(input_args.project_name, input_args.ml_backend_urls, input_args.ml_backend_names, 1)
    #     return
    
    
    
        
    # Handle login and project initialization
    # if input_args.command == 'login_init':
    #     from users.models import User
    #     # Authenticate the user
        
    #     if input_args.username:
    #         try:
    #             user = User.objects.get(email=input_args.username)
    #         except User.DoesNotExist:
    #             print("User with the provided email does not exist.")
    #             sys.exit(1)
    #     else:
    #         print("Email is required for login.")
    #         sys.exit(1)

    #     user = authenticate(username=input_args.username, password=input_args.password)
    #     if user is not None:
    #         from projects.models import Project
    #         print("Login successful.")
    #         sampling_map = {'sequential': Project.SEQUENCE, 'uniform': Project.UNIFORM, 'prediction-score-min': Project.UNCERTAINTY}
    #         # Initialize the project
    #         if input_args.project_name:
    #             project = _create_project(
    #                 title=input_args.project_name, 
    #                 user=user,
    #                 label_config=input_args.label_config,
    #                 description=input_args.project_desc,
    #                 sampling=sampling_map.get(input_args.sampling, 'sequential'),
    #                 ml_backends=input_args.ml_backends
    #             )
    #             print(f'Project "{input_args.project_name}" successfully created under the account {user.email}.')
    #             if project:
    #                 print(f'Project "{input_args.project_name}" successfully created.')
    #             else:
    #                 print(f'Project "{input_args.project_name}" already exists.')
    #     else:
    #         print("Login failed. Please check your credentials.")
    #         sys.exit(1)
    
    if input_args.command == 'login_init':
        # Existing user authentication logic
        from users.models import User
        from io_storages.s3.models import S3ImportStorage
        
        user = authenticate(username=input_args.username, password=input_args.password)
        if user is not None:
            print("Login successful.")
            from projects.models import Project
            sampling_map = {'sequential': Project.SEQUENCE, 'uniform': Project.UNIFORM, 'prediction-score-min': Project.UNCERTAINTY}
            
            # Project initialization logic
            project = _create_project(
                title=input_args.project_name,
                user=user,
                label_config=input_args.label_config,
                description=input_args.project_desc,
                sampling=sampling_map.get(input_args.sampling, 'sequential'),
                ml_backends=input_args.ml_backends
            )
            print(f'Project "{input_args.project_name}" successfully created or already exists under the account {user.email}.')
            
            if input_args.imported:
                # S3 Import Storage Configuration
                from io_storages.s3.models import S3ImportStorage

                s3_import_storage, created_import = S3ImportStorage.objects.get_or_create(
                    project=project,
                    bucket=input_args.s3_bucket,  # Assuming you want to use the same bucket for simplicity
                    defaults={
                    
                        'aws_access_key_id': input_args.s3_access_key,
                        'aws_secret_access_key': input_args.s3_secret_key,
                        'region_name': input_args.s3_region_name,
                        'prefix': input_args.s3_prefix,
                        's3_endpoint': input_args.s3_endpoint,
                        'use_blob_urls': input_args.use_blob_urls,
                        'presign': input_args.presign,
                        'presign_ttl': input_args.presign_ttl,
                        'aws_session_token': input_args.aws_session_token if input_args.aws_session_token else '',
                        'regex_filter': input_args.regex_filter,
                        'recursive_scan': input_args.recursive_scan,
                        'aws_sse_kms_key_id': input_args.aws_sse_kms_key_id,
                        'title': input_args.s3_titles,
                        'use_blob_urls': 1,
                        'presign': 1,
                        'recursive_scan': 1
                        
                    }
                )

                if created_import:
                    try:
                        # Assuming you have refactored your synchronization logic into this callable method
                        synchronize_s3_import_storage(s3_import_storage.id)
                        print(f"Synchronized S3 storage for bucket '{input_args.s3_bucket}'.")
                    except Exception as e:
                        print(f"Failed to synchronize S3 storage for bucket '{input_args.s3_bucket}': {e}")
                else:
                    print(f"S3 storage for bucket '{input_args.s3_bucket}' already exists and was not synchronized automatically.")
                    
            if input_args.export:
                from io_storages.s3.models import S3ExportStorage
                s3_export_storage, created_export = S3ExportStorage.objects.get_or_create(
                    project=project,
                    bucket=input_args.s3_bucket,  # Assuming same bucket for simplicity; adjust as necessary
                    defaults={
                        'aws_access_key_id': input_args.s3_access_key,
                        'aws_secret_access_key': input_args.s3_secret_key,
                        'region_name': input_args.s3_region_name,
                        'prefix': input_args.s3_prefix,
                        's3_endpoint': input_args.s3_endpoint,
                        'use_blob_urls': input_args.use_blob_urls,
                        'aws_session_token': input_args.aws_session_token if input_args.aws_session_token else '',
                        'regex_filter': input_args.regex_filter,
                        'aws_sse_kms_key_id': input_args.aws_sse_kms_key_id,
                        'title': input_args.s3_titles,
                    }
                )
                from io_storages.s3.utils import synchronize_s3_export_storage

                if created_export:
                    try:
                        # Synchronize the S3 export storage right after creation
                        synchronize_s3_export_storage(s3_export_storage.id)
                        print(f"Synchronized S3 export storage for bucket '{input_args.s3_bucket}'.")
                    except Exception as e:
                        print(f"Failed to synchronize S3 export storage for bucket '{input_args.s3_bucket}': {e}")
        else:
            print("Login failed. Please check your credentials.")
            sys.exit(1)
            
        # Handle project deletion
    if input_args.command == 'delete_project':
        from django.core.exceptions import ObjectDoesNotExist
        from projects.models import Project

        user = authenticate(username=input_args.username, password=input_args.password)
        if user is None:
            print("Login failed. Please check your credentials.")
            sys.exit(1)

        try:
            project = None
            identifier = "unknown"
            if hasattr(input_args, 'project_id') and input_args.project_id:
                project = Project.objects.get(id=input_args.project_id)
                identifier = f'ID: {input_args.project_id}'
            elif hasattr(input_args, 'project_name') and input_args.project_name:
                project = Project.objects.get(title=input_args.project_name)
                identifier = f'name: "{input_args.project_name}"'
            
            if project:
                confirm = input(f'Are you sure you want to delete the project with {identifier}? [y/N]: ').lower()
                if confirm in ['y', 'yes']:
                    project.delete()
                    print(f'Project with {identifier} has been successfully deleted.')
                else:
                    print("Project deletion cancelled.")
            else:
                print(f"No project found with {identifier}.")
        
        except ObjectDoesNotExist:
            print(f'Project with {identifier} does not exist.')
        except Exception as e:
            print(f'An error occurred: {e}')

    # -------------------------------------------------------

    if input_args.command == 'export':
        from tasks.functions import export_project

        try:
            filename = export_project(
                input_args.project_id, input_args.export_format, input_args.export_path,
                serializer_context=input_args.export_serializer_context
            )
        except Exception as e:
            logger.exception(f'Failed to export project: {e}')
        else:
            logger.info(f'Project exported successfully: {filename}')

        return

    # print version
    if input_args.command == 'version' or getattr(input_args, 'version', False):

    # if input_args.command == 'version' or input_args.version:
        from data_studio import __version__
        print('\nLabel Studio version:', __version__, '\n')
        print(json.dumps(versions, indent=4))

    # init
    elif input_args.command == 'user' or getattr(input_args, 'user', None):
        _get_user_info(input_args.username)
        return

    # init
    elif input_args.command == 'init' or getattr(input_args, 'init', None):
        _init(input_args, config)

        print('')
        print('Data Studio has been successfully initialized.')
        if input_args.command != 'start' and input_args.project_name:
            print('Start the server: data-studio start ' + input_args.project_name)
            return

    # start with migrations from old projects, '.' project_name means 'data-studio start' without project name
    elif input_args.command == 'start' and input_args.project_name != '.':
        from data_studio.core.old_ls_migration import migrate_existing_project
        from projects.models import Project
        sampling_map = {'sequential': Project.SEQUENCE, 'uniform': Project.UNIFORM,
                        'prediction-score-min': Project.UNCERTAINTY}

        if input_args.project_name and not _project_exists(input_args.project_name):
            migrated = False
            project_path = pathlib.Path(input_args.project_name)
            if project_path.exists():
                print('Project directory from previous version of data-studio found')
                print('Start migrating..')
                config_path = project_path / 'config.json'
                config = _get_config(config_path)
                user = _create_user(input_args, config)
                label_config_path = project_path / 'config.xml'
                project = _create_project(
                    title=input_args.project_name,
                    user=user,
                    label_config=label_config_path,
                    sampling=sampling_map.get(config.get('sampling', 'sequential'), Project.UNIFORM),
                    description=config.get('description', ''),
                )
                migrate_existing_project(project_path, project, config)
                migrated = True

                print(
                    Fore.LIGHTYELLOW_EX +
                    '\n*** WARNING! ***\n'
                    + f'Project {input_args.project_name} migrated to Data Studio Database\n'
                    + "YOU DON'T NEED THIS FOLDER ANYMORE"
                    + '\n****************\n' +
                    Fore.WHITE
                )
            if not migrated:
                print(
                    'Project "{project_name}" not found. '
                    'Did you miss create it first with `data-studio init {project_name}` ?'.format(
                        project_name=input_args.project_name
                    )
                )
                return


    if input_args.command == 'start' or input_args.command is None:
        from data_studio.core.utils.common import start_browser
        email = input_args.email
        password = input_args.password
        
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                print("Authentication successful. Starting the server.")
            else:
                print("Authentication failed. Please check your credentials.")
        elif get_env('USERNAME') and get_env('PASSWORD') or input_args.username:
            print("Creating a new user and starting the server.")
            _create_user(input_args, config)
        else:
            print("No authentication provided. Exiting.")
            sys.exit(1)
        
        cert_file = input_args.cert_file or config.get('cert')
        key_file = input_args.key_file or config.get('key')
        if cert_file or key_file:
            logger.error("Label Studio doesn't support SSL web server with cert and key.\n"
                        'Use nginx or other servers for it.')
            return

        # internal port and internal host for server start
        internal_host = input_args.internal_host or config.get('internal_host', '0.0.0.0')  # nosec
        internal_port = input_args.port or get_env('PORT') or config.get('port', 8080)
        try:
            internal_port = int(internal_port)
        except ValueError as e:
            logger.warning(f"Can't parse PORT '{internal_port}': {e}; default value 8080 will be used")
            internal_port = 8080

        internal_port = _get_free_port(internal_port, input_args.debug)

        # save selected port to global settings
        from django.conf import settings
        settings.INTERNAL_PORT = str(internal_port)

        # browser
        url = ('http://localhost:' + str(internal_port)) if not host else host
        start_browser(url, input_args.no_browser)

        _app_run(host=internal_host, port=internal_port)

if __name__ == "__main__":
    sys.exit(main())


