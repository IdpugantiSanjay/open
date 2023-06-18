#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

from enum import Enum

browser = 'firefox'
github_username = 'IdpugantiSanjay'
history_file_location = "/home/sanjay/.bash_history"


class Programs(Enum):
    GitHub = 'gh'
    Todos = 'todos'
    AzureDevOps = 'ado'
    Calendar = 'calendar'
    Youtube = 'youtube'
    Search = 'search'


def browser_open(p_args: list[str]):
    subprocess.Popen([browser] + p_args, stdout=subprocess.DEVNULL)


def write_to_history(cmd: str) -> None:
    with open(history_file_location, 'a') as history:
        history.write(cmd + '\n')


def github(args: argparse.Namespace):
    match args.options:
        case []:
            option = choose(['home', 'profile', 'repos'])
            if not option:
                sys.exit(os.EX_NOINPUT)
            args.options.append(option)
            github(args)
        case ['home']:
            browser_open(['github.com'])
            write_to_history('open gh home')
        case ['profile']:
            write_to_history('open gh profile')
            browser_open(['/'.join(['github.com', github_username])])
        case ['repos']:
            repos = spin_execute("gh repo list --json  'name' -q '.[].name'",
                                 title='Fetching github repos...').split(
                '\n')
            repo = choose(repos)
            if not repo:
                sys.exit(os.EX_NOINPUT)
            args.options += [repo]
            github(args)
        case ['repos', _]:
            section = choose(['code', 'issues', 'pulls', 'actions'])
            if not section:
                sys.exit(os.EX_NOINPUT)
            args.options += [section]
            github(args)
        case ['repos', repo, section]:
            write_to_history(f'open gh repos {repo} {section}')
            browser_open([
                '/'.join([
                    'github.com',
                    github_username,
                    repo,
                    '' if section == 'code' else section
                ])
            ])


def todos(args: argparse.Namespace):
    match args.options:
        case []:
            which_tasks = choose(['myday', 'important', 'planned', 'flagged', 'inbox'])
            if not which_tasks:
                sys.exit(os.EX_NOINPUT)
            args.options += [which_tasks]
            todos(args)
        case [which_tasks]:
            write_to_history(f'open todos {which_tasks}')
            browser_open(['/'.join(['to-do.live.com/tasks', which_tasks])])


def azure_dev_ops(args: argparse.Namespace):
    match args.options:
        case []:
            org = choose([
                'sanjay-idpuganti',
                '10XD',
                'sanjay-collections',
                'sanjayidpuganti0904'
            ])
            if not org:
                sys.exit(os.EX_NOINPUT)
            args.options.append(org)
            azure_dev_ops(args)
        case [org]:
            project: str = ''
            match org:
                case 'sanjay-idpuganti':
                    project = choose(['courses'])
                case '10XD':
                    project = choose(['10X'])
                case 'sanjay-collections':
                    project = choose(['collections'])
                case 'sanjayidpuganti0904':
                    project = choose([
                        'plutus-web',
                        'plutus_mvc',
                        '10X',
                        'odin',
                        'odin-api',
                        'odin-web',
                        'plutus',
                        'plutus backend'
                    ])
            if project:
                args.options.append(project)
                azure_dev_ops(args)
        case [org, project]:
            write_to_history(f'open ado {org} {project}')
            browser_open(['/'.join(['dev.azure.com', org, project])])


def calendar(args: argparse.Namespace):
    browser_open(['calendar.google.com/calendar/u/0/r/agenda'])


def youtube(args: argparse.Namespace):
    match args.options:
        case ['subs']:
            write_to_history('open youtube subs')
            browser_open(['youtube.com/feed/subscriptions'])
        case ['watch-later']:
            write_to_history('open youtube watch-later')
            browser_open(['youtube.com/playlist?list=WL'])
        case []:
            section = choose(['subs', 'watch-later'])
            if not section:
                sys.exit(os.EX_NOINPUT)
            args.options.append(section)
            youtube(args)


def search(args: argparse.Namespace):
    match args.options:
        case []:
            write_to_history('open search')
            browser_open(['google.com'])
        case [*query]:
            query = ' '.join(query)
            write_to_history(f'open search {query}')
            browser_open(['/'.join(['google.com', f'search?q={query}'])])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("options", nargs=argparse.REMAINDER, default='repos')
    args = parser.parse_args()
    open_what(args)


def open_what(args: argparse.Namespace):
    match args.options:
        case []:
            to_open = [
                Programs.GitHub,
                Programs.Todos,
                Programs.AzureDevOps,
                Programs.Calendar,
                Programs.Youtube,
                Programs.Search
            ]
            what = choose([x.value for x in to_open])
            args.options = [what]
            open_what(args)
        case [what, *options]:
            args.options = options
            match Programs(what):
                case Programs.GitHub:
                    github(args)
                case Programs.Todos:
                    todos(args)
                case Programs.AzureDevOps:
                    azure_dev_ops(args)
                case Programs.Calendar:
                    calendar(args)
                case Programs.Youtube:
                    youtube(args)
                case Programs.Search:
                    search(args)


def choose(choices: list[str]) -> str:
    """
    Gum choose any of the given choices interactively
    :param choices: Feed, Read Later, Latest
    :return: executed process
    """
    process = subprocess.run(["gum", "choose"] + list(choices), stdout=subprocess.PIPE)
    return process.stdout.decode("utf-8").strip()


def spin_execute(command: str, title: str) -> str:
    """
    Run gum spinner until an arbitrary command completed execution
    :param command: {rss} read-later ls
    :param title: The title user seen when the spinner spins
    :return: executed process
    """
    process = subprocess.run([
        f"gum spin --spinner minidot --title '{title}'  --show-output -- {command}"
    ], stdout=subprocess.PIPE, check=True, shell=True)
    return process.stdout.decode("utf-8").strip()


if __name__ == "open" or 'open.py':
    main()
