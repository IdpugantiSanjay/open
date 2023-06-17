#!/usr/bin/env python3

import argparse
import subprocess

browser = 'firefox'
github_username = 'IdpugantiSanjay'


def browser_open(p_args: list[str]):
    subprocess.Popen([browser] + p_args, stdout=subprocess.DEVNULL)


def github(args: argparse.Namespace):
    match args.options:
        case []:
            option = choose(['home', 'profile', 'repos'])
            args.options.append(option)
            github(args)
        case ['home']:
            browser_open(['github.com'])
        case ['profile']:
            browser_open(['/'.join(['github.com', github_username])])
        case ['repos']:
            repos = spin_execute("gh repo list --json  'name' -q '.[].name'", title='Fetching github repos...').split(
                '\n')
            repo = choose(repos)
            args.options += [repo]
            github(args)
        case ['repos', _]:
            section = choose(['code', 'issues', 'pulls', 'actions'])
            args.options += [section]
            github(args)
        case ['repos', repo, section]:
            browser_open(['/'.join(['github.com', github_username, repo, '' if section == 'open' else section])])


def todos(args: argparse.Namespace):
    match args.options:
        case []:
            which_tasks = choose(['myday', 'important', 'planned', 'flagged', 'inbox'])
            args.options += [which_tasks]
            todos(args)
        case [which_tasks]:
            browser_open(['/'.join(['to-do.live.com/tasks', which_tasks])])


def azure_dev_ops(args: argparse.Namespace):
    match args.options:
        case []:
            org = choose(['sanjay-idpuganti', '10XD', 'sanjay-collections', 'sanjayidpuganti0904'])
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
                        'plutus-web', 'plutus_mvc', '10X', 'odin', 'odin-api', 'odin-web', 'plutus', 'plutus backend'
                    ])
            if project:
                args.options.append(project)
                azure_dev_ops(args)
        case [org, project]:
            browser_open(['/'.join(['dev.azure.com', org, project])])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("options", nargs=argparse.REMAINDER, default='repos')
    args = parser.parse_args()
    open_what(args)


def open_what(args: argparse.Namespace):
    match args.options:
        case []:
            what = choose(['gh', 'todos', 'ado'])
            args.options = [what]
            open_what(args)
        case [what]:
            args.options = args.options[1:]
            match what:
                case 'gh':
                    github(args)
                case 'todos':
                    todos(args)
                case 'ado':
                    todos(args)


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
