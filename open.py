#!/usr/bin/env python3

import argparse
import subprocess

browser = 'firefox'
github_username = 'IdpugantiSanjay'


def browser_open(p_args: list[str]):
    subprocess.Popen([browser] + p_args, stdout=subprocess.DEVNULL)


def github(args: argparse.Namespace):
    match args.options:
        case ['repos']:
            gh_process = subprocess.run(["gh repo list --json  'name' -q '.[].name'"], stdout=subprocess.PIPE,
                                        check=True,
                                        shell=True)
            repos = gh_process.stdout.decode('utf-8').strip().split('\n')
            repo = choose(repos)
            args.options += [repo]
            github(args)
        case ['repos', _]:
            section = choose(['open', 'issues', 'pulls', 'actions'])
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("what", choices=('gh', 'todos'))
    parser.add_argument("options", nargs=argparse.REMAINDER, default='repos')
    args = parser.parse_args()

    match args.what:
        case 'gh' | 'github':
            github(args)
        case 'todos':
            todos(args)


def choose(choices: list[str]) -> str:
    """
    Gum choose any of the given choices interactively
    :param choices: Feed, Read Later, Latest
    :return: executed process
    """
    process = subprocess.run(["gum", "choose"] + list(choices), stdout=subprocess.PIPE)
    return process.stdout.decode("utf-8").strip()


if __name__ == "open" or 'open.py':
    main()
