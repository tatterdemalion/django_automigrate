#!/usr/bin/env python
import sys
import os
import subprocess
import re
from collections import defaultdict

"""
A script for running migrations on branch switch.
Usage:
automigrate.py develop

This will get the differences between your branch and `develop` and run them.
You can switch back to your branch and run the migrations again:

automigrate.py <your_branch>
"""

target_branch = sys.argv[1]

migration_file_pattern = re.compile(r'^(.*)\/migrations\/((\d+).*\.py)$')

prefix = 'docker-compose run --rm django'

location = os.environ.get('AUTOMIGRATE_LOCATION', '')
if location == 'local':
    prefix = ''


def execute(command):
    return subprocess.check_output(command, shell=True).decode('utf-8')


def get_migration_files(branch_name):
    branch_output = execute(f'git ls-tree -r {branch_name}')
    migration_files = defaultdict(list)
    for output in branch_output.split('\n'):
        if output:
            _, filepath = output.split(' ')[2].split('\t')
            match = migration_file_pattern.match(filepath)
            if match:
                app, _file, order = match.groups()
                migration_files[app].append((order, _file))
    return migration_files


current_branch = execute('git rev-parse --abbrev-ref HEAD')
current_migration_files = get_migration_files(current_branch)
target_migration_files = get_migration_files(target_branch)

for app in current_migration_files:
    current_diff = sorted(
        [i for i in set(current_migration_files[app]) - set(target_migration_files[app])],
        key=lambda x: x[0]
    )
    if current_diff:
        last = current_migration_files[app][:-len(current_diff)][-1][1][:-3]
        print(execute(f'{prefix} python manage.py migrate {app} {last}'))

print(execute(f'git checkout {target_branch}'))
print(execute(f'{prefix} python manage.py migrate'))
