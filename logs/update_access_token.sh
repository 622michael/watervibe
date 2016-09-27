[START CRONTAB]
Unknown command: 'update_access_tokens'
Type 'manage.py help' for usage.
[END CRONTAB]
[START CRONTAB]
Traceback (most recent call last):
  File "manage.py", line 22, in <module>
    execute_from_command_line(sys.argv)
  File "/usr/local/lib/python2.7/dist-packages/django/core/management/__init__.py", line 367, in execute_from_command_line
    utility.execute()
  File "/usr/local/lib/python2.7/dist-packages/django/core/management/__init__.py", line 359, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/usr/local/lib/python2.7/dist-packages/django/core/management/__init__.py", line 208, in fetch_command
    klass = load_command_class(app_name, subcommand)
  File "/usr/local/lib/python2.7/dist-packages/django/core/management/__init__.py", line 40, in load_command_class
    module = import_module('%s.management.commands.%s' % (app_name, name))
  File "/usr/lib/python2.7/importlib/__init__.py", line 37, in import_module
    __import__(name)
ImportError: No module named management.commands.update_access_tokens
[END CRONTAB]
[START CRONTAB]
Traceback (most recent call last):
  File "manage.py", line 22, in <module>
    execute_from_command_line(sys.argv)
  File "/usr/local/lib/python2.7/dist-packages/django/core/management/__init__.py", line 367, in execute_from_command_line
    utility.execute()
  File "/usr/local/lib/python2.7/dist-packages/django/core/management/__init__.py", line 359, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/usr/local/lib/python2.7/dist-packages/django/core/management/__init__.py", line 208, in fetch_command
    klass = load_command_class(app_name, subcommand)
  File "/usr/local/lib/python2.7/dist-packages/django/core/management/__init__.py", line 40, in load_command_class
    module = import_module('%s.management.commands.%s' % (app_name, name))
  File "/usr/lib/python2.7/importlib/__init__.py", line 37, in import_module
    __import__(name)
  File "/home/watervibe/fitbit/management/commands/update_access_tokens.py", line 4, in <module>
    class Command(BaseCommand):
NameError: name 'BaseCommand' is not defined
[END CRONTAB]
[START CRONTAB]
[{u'message': u'Refresh token invalid: 17d3740e900662b237352a120d72726fe3262402b289df8f89e7595218d512e2. Visit https://dev.fitbit.com/docs/oauth2 for more information on the Fitbit Web API authorization process.', u'errorType': u'invalid_grant'}]
[END CRONTAB]
[START CRONTAB]
[{u'message': u'Refresh token invalid: 4844489ff0ee1706adc5785b4f09320c60ebbf4eac2ba1a027684f5d56f19343. Visit https://dev.fitbit.com/docs/oauth2 for more information on the Fitbit Web API authorization process.', u'errorType': u'invalid_grant'}]
[{u'message': u'Refresh token invalid: 17d3740e900662b237352a120d72726fe3262402b289df8f89e7595218d512e2. Visit https://dev.fitbit.com/docs/oauth2 for more information on the Fitbit Web API authorization process.', u'errorType': u'invalid_grant'}]
[END CRONTAB]
[START CRONTAB]
[{u'message': u'Refresh token invalid: 4844489ff0ee1706adc5785b4f09320c60ebbf4eac2ba1a027684f5d56f19343. Visit https://dev.fitbit.com/docs/oauth2 for more information on the Fitbit Web API authorization process.', u'errorType': u'invalid_grant'}]
[{u'message': u'Refresh token invalid: 17d3740e900662b237352a120d72726fe3262402b289df8f89e7595218d512e2. Visit https://dev.fitbit.com/docs/oauth2 for more information on the Fitbit Web API authorization process.', u'errorType': u'invalid_grant'}]
[END CRONTAB]
[START CRONTAB]
Traceback (most recent call last):
  File "manage.py", line 22, in <module>
    execute_from_command_line(sys.argv)
  File "/usr/local/lib/python2.7/dist-packages/django/core/management/__init__.py", line 367, in execute_from_command_line
    utility.execute()
  File "/usr/local/lib/python2.7/dist-packages/django/core/management/__init__.py", line 359, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/usr/local/lib/python2.7/dist-packages/django/core/management/base.py", line 294, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/usr/local/lib/python2.7/dist-packages/django/core/management/base.py", line 345, in execute
    output = self.handle(*args, **options)
  File "/home/watervibe/fitbit/management/commands/update_access_tokens.py", line 8, in handle
    authorization.refresh_access_for_user(user)
  File "/home/watervibe/fitbit/authorization.py", line 92, in refresh_access_for_user
    print json_response
NameError: global name 'json_response' is not defined
[END CRONTAB]
[START CRONTAB]
{u'user_id': u'4TP97K', u'access_token': u'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0VFA5N0siLCJhdWQiOiIyMjdSUjkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3c2xlIHd3ZWkgd2FjdCB3c2V0IHdsb2MiLCJleHAiOjE0NzQ5MTkxNjgsImlhdCI6MTQ3NDg5MDM2OH0.Erj2bFSo-aC3kqE6_AwJDv-ad-7eSJPuwX4YoiYO9Ig', u'expires_in': 28800, u'token_type': u'Bearer', u'scope': u'profile activity settings sleep weight location heartrate', u'refresh_token': u'6b0517b3df073dfbb51d2346319d26e574ae6921f60ad85062dfa7ce69218ca8'}
None
[{u'message': u'Refresh token invalid: 17d3740e900662b237352a120d72726fe3262402b289df8f89e7595218d512e2. Visit https://dev.fitbit.com/docs/oauth2 for more information on the Fitbit Web API authorization process.', u'errorType': u'invalid_grant'}]
[END CRONTAB]
[START CRONTAB]
{u'user_id': u'4TP97K', u'access_token': u'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0VFA5N0siLCJhdWQiOiIyMjdSUjkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3c2xlIHd3ZWkgd2FjdCB3c2V0IHdsb2MiLCJleHAiOjE0NzQ5MTkxNjgsImlhdCI6MTQ3NDg5MDM2OH0.Erj2bFSo-aC3kqE6_AwJDv-ad-7eSJPuwX4YoiYO9Ig', u'expires_in': 28800, u'token_type': u'Bearer', u'scope': u'profile activity settings sleep weight location heartrate', u'refresh_token': u'6b0517b3df073dfbb51d2346319d26e574ae6921f60ad85062dfa7ce69218ca8'}
None
[{u'message': u'Refresh token invalid: 17d3740e900662b237352a120d72726fe3262402b289df8f89e7595218d512e2. Visit https://dev.fitbit.com/docs/oauth2 for more information on the Fitbit Web API authorization process.', u'errorType': u'invalid_grant'}]
[END CRONTAB]
[START CRONTAB]
{u'user_id': u'4TP97K', u'access_token': u'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0VFA5N0siLCJhdWQiOiIyMjdSUjkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3c2xlIHd3ZWkgd2FjdCB3c2V0IHdsb2MiLCJleHAiOjE0NzQ5MTkxNjgsImlhdCI6MTQ3NDg5MDM2OH0.Erj2bFSo-aC3kqE6_AwJDv-ad-7eSJPuwX4YoiYO9Ig', u'expires_in': 28800, u'token_type': u'Bearer', u'scope': u'profile activity settings sleep weight location heartrate', u'refresh_token': u'6b0517b3df073dfbb51d2346319d26e574ae6921f60ad85062dfa7ce69218ca8'}
None
[{u'message': u'Refresh token invalid: 17d3740e900662b237352a120d72726fe3262402b289df8f89e7595218d512e2. Visit https://dev.fitbit.com/docs/oauth2 for more information on the Fitbit Web API authorization process.', u'errorType': u'invalid_grant'}]
[END CRONTAB]
[START CRONTAB]
{u'user_id': u'4TP97K', u'access_token': u'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0VFA5N0siLCJhdWQiOiIyMjdSUjkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3c2xlIHd3ZWkgd2FjdCB3c2V0IHdsb2MiLCJleHAiOjE0NzQ5MTkxNjgsImlhdCI6MTQ3NDg5MDM2OH0.Erj2bFSo-aC3kqE6_AwJDv-ad-7eSJPuwX4YoiYO9Ig', u'expires_in': 28800, u'token_type': u'Bearer', u'scope': u'profile activity settings sleep weight location heartrate', u'refresh_token': u'6b0517b3df073dfbb51d2346319d26e574ae6921f60ad85062dfa7ce69218ca8'}
None
[{u'message': u'Refresh token invalid: 17d3740e900662b237352a120d72726fe3262402b289df8f89e7595218d512e2. Visit https://dev.fitbit.com/docs/oauth2 for more information on the Fitbit Web API authorization process.', u'errorType': u'invalid_grant'}]
[END CRONTAB]
[START CRONTAB]
{u'user_id': u'4TP97K', u'access_token': u'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0VFA5N0siLCJhdWQiOiIyMjdSUjkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3c2xlIHd3ZWkgd2FjdCB3c2V0IHdsb2MiLCJleHAiOjE0NzQ5MTkxNjgsImlhdCI6MTQ3NDg5MDM2OH0.Erj2bFSo-aC3kqE6_AwJDv-ad-7eSJPuwX4YoiYO9Ig', u'expires_in': 28800, u'token_type': u'Bearer', u'scope': u'profile activity settings sleep weight location heartrate', u'refresh_token': u'6b0517b3df073dfbb51d2346319d26e574ae6921f60ad85062dfa7ce69218ca8'}
None
[{u'message': u'Refresh token invalid: 17d3740e900662b237352a120d72726fe3262402b289df8f89e7595218d512e2. Visit https://dev.fitbit.com/docs/oauth2 for more information on the Fitbit Web API authorization process.', u'errorType': u'invalid_grant'}]
[END CRONTAB]
[START CRONTAB]
{u'user_id': u'4TP97K', u'access_token': u'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0VFA5N0siLCJhdWQiOiIyMjdSUjkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3c2xlIHd3ZWkgd2FjdCB3c2V0IHdsb2MiLCJleHAiOjE0NzQ5MTkxNjgsImlhdCI6MTQ3NDg5MDM2OH0.Erj2bFSo-aC3kqE6_AwJDv-ad-7eSJPuwX4YoiYO9Ig', u'expires_in': 28800, u'token_type': u'Bearer', u'scope': u'profile activity settings sleep weight location heartrate', u'refresh_token': u'6b0517b3df073dfbb51d2346319d26e574ae6921f60ad85062dfa7ce69218ca8'}
None
[{u'message': u'Refresh token invalid: 17d3740e900662b237352a120d72726fe3262402b289df8f89e7595218d512e2. Visit https://dev.fitbit.com/docs/oauth2 for more information on the Fitbit Web API authorization process.', u'errorType': u'invalid_grant'}]
[END CRONTAB]
