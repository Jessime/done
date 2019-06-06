import argparse
import os

from pathlib import Path
from datetime import date, timedelta
from calendar import month_name
from subprocess import run

import pyperclip
import pendulum
import gitlab


GITLAB_DONE = os.environ['GITLAB_DONE']
DIR = Path('~/Documents/done/').expanduser()


def commit_file(path):
    filename = str(path.name)
    current_str = path.read_text()
    backend = gitlab.Gitlab('https://gitlab.com/', private_token=GITLAB_DONE)
    project = backend.projects.get('jessime.kirk/done')
    try:
        remote_version = project.files.get(filename, ref='master')
        previous_str = remote_version.decode().decode('utf-8')
        if previous_str != current_str:
            data = {'branch': 'master',
                    'commit_message': f'Updating {filename}.',
                    'actions': [{'action': 'update',
                                 'file_path': filename,
                                 'content': current_str}]
                    }
            project.commits.create(data)
    except gitlab.GitlabGetError:
        project.files.create({'file_path': filename,
                              'branch': 'master',
                              'content': current_str,
                              'commit_message': f'Create {filename}.'})


def run_year():
    """Aggregate notes for the year."""
    pass


def run_month():
    """Aggregate notes for the previous month.

    Notes
    -----
    To aggregate notes for January, run anytime during February.
    """
    today = date.today()
    agg = '\n\n' + '---' + '\n\n'
    for i in range(1, 6):
        # TODO Need some modulo or something for January and "today.month - 1"
        path = DIR / Path(f'{today.year}-{today.month - 1}-WEEK{i}.md')
        if path.is_file():
            week_text = f'### WEEK{i}\n' + path.read_text().split('---')[0]
            new_text = f'\n{week_text}'
            agg += new_text
    name = month_name[today.month - 1]
    month_path = DIR / Path(f'{today.year}-{name}.md')
    if not month_path.is_file(): # TODO this should come before all the aggregation as an early exit.
        month_path.write_text(agg)
    run(f'open -e {month_path}'.split(), check=True)
    return month_path


def run_week():
    """Aggregate notes for the last week.

    Notes
    -----
    Must be run by Sunday to work properly.
    """
    today = date.today()
    agg = '\n\n' + '---' + '\n\n'
    for i in range(today.weekday()+1):
        day = str(today - timedelta(days=i))
        path = DIR / Path(f'{day}.md')
        if path.is_file():
            new_text = f'\n### {day}\n\n{path.read_text()}\n\n'
            agg += new_text
    week_of_month = pendulum.datetime(today.year, today.month, today.day).week_of_month
    week_path = DIR / Path(f'{today.year}-{today.month}-WEEK{week_of_month}.md')
    if not week_path.is_file(): # TODO this should come before all the aggregation as an early exit.
        week_path.write_text(agg)
    run(f'open -e {week_path}'.split(), check=True)
    return week_path


def run_day(day_spec):
    """Open notes for today."""
    # TODO Provide option to edit note for another day besides today.
    day_to_edit = date.today()
    if day_spec is not None:
        day_to_edit = day_to_edit - timedelta(days=day_spec)
    path = DIR/Path(f'{day_to_edit}.md')
    if not path.is_file():
        run(f'touch {path}'.split(), check=True)
    run(f'open -e {path}'.split(), check=True)
    return path


def validate_day_parameter(day_spec):
    err_msg = 'Values passed to the `--day` flag must be a positive integer.'
    if day_spec is not None:
        try:
            day_spec = int(day_spec)
        except ValueError as e:
            raise e(err_msg)
        assert day_spec > 0, err_msg
    return day_spec


def run_done(args):
    if args.save:
        commit_file(Path(args.save))
        return                          # Early exit
    if args.week:
        path = run_week()
    elif args.month:
        path = run_month()
    elif args.year:
        path = run_year()
    else:
        day_spec = validate_day_parameter(args.day)
        path = run_day(day_spec)
    cmd = f'done -s {path}'
    pyperclip.copy(cmd)
    print(f'The command to save your work:\n{cmd}\nis now on the clipboard.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--day', '-d', help=('Specify a day other than today. '
                                             'Use negative integers to specify how many days ago to edit. '))
    parser.add_argument('--week', '-w', action='store_true', help='Set to aggregate week.')
    parser.add_argument('--month', '-m', action='store_true', help='Set to aggregate month.')
    parser.add_argument('--year', '-y', action='store_true', help='Set to aggregate year.')
    parser.add_argument('--save', '-s', help='Save file to Gitlab.')
    args = parser.parse_args()
    run_done(args)