#!/usr/bin/env python3

import argparse
import itertools
import os
import subprocess
import sys
from collections.abc import Iterator, Iterable
from enum import Enum
from typing import List

from pyfzf.pyfzf import FzfPrompt

fzf = FzfPrompt().prompt

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
    Tmux = 'tmux'
    Mail = 'mail'
    News = 'news'
    ChatGPT = "chat-gpt"
    GoogleCalendar = "google-calendar"
    Rss = "rss"
    Courses = "courses"
    Kibana = "kibana"
    Azure = "azure"
    FastMail = "fastmail"
    Bard = "bard"
    CloudflareSpeedTest = "cloudflare-speed-test"
    GitLab = "gl"
    Rider = "rider"


rider_projects = {"tasks": "/home/sanjay/Work/RiderProjects/Tasks/Tasks.sln"}

graph = {
    Programs.GitHub: ['home', 'profile', 'repos'],
    Programs.Todos: ['myday', 'important', 'planned', 'flagged', 'inbox'],
    Programs.Calendar: ['month', 'week', 'workweek', 'day'],
    Programs.GoogleCalendar: ['agenda', 'day', 'week', 'month', 'year'],
    Programs.Tmux: ['sessions'],
    Programs.Rider: rider_projects.keys()
}

GitHubRepoActions = ('code', 'issues', 'pulls', 'actions')
GitLabOptions = ('projects', 'profile', 'todos', 'issues')
SubCommands = {x.value for x in Programs.__members__.values()}


# firefox 'ext+container:name=ChatGPT&url=https://chat.openai.com/'
def firefox_container(url: str, container: str):
    subprocess.Popen(['firefox', 
                      f'ext+container:name={container}&url={url}'], 
                      stdout=subprocess.PIPE)


def browser_open(p_args: list[str]):
    subprocess.Popen([browser] + p_args, stdout=subprocess.DEVNULL)


def write_to_history(cmd: str) -> None:
    with open(history_file_location, 'a') as history:
        history.write(cmd + '\n')


def rider(solution_path: str) -> None:
    rider_path = '/home/sanjay/.local/share/JetBrains/Toolbox/apps/rider/bin/rider.sh'
    subprocess.Popen([rider_path, solution_path], 
                     stdout=subprocess.DEVNULL, 
                     stderr=subprocess.DEVNULL)


def open_rider_projects(args: argparse.Namespace):
    match args.options:
        case []:
            option = choose(rider_projects.keys())
            if not option:
                sys.exit(os.EX_NOINPUT)
            args.options.append(option)
            open_rider_projects(args)
        case [project]:
            if project in rider_projects.keys():
                rider(rider_projects[project])


def github(args: argparse.Namespace):
    match args.options:
        case []:
            option = choose(['repos', 'profile', 'home'])
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
            section = choose(GitHubRepoActions)
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

def gitlab(args: argparse.Namespace):
    gitlab_username = 'leosanchez'
    match args.options:
        case []:
            option = choose(GitLabOptions)
            if not option:
                sys.exit(os.EX_NOINPUT)
            args.options.append(option)
            gitlab(args)
        case ['profile']:
            browser_open([f'gitlab.com/{gitlab_username}'])
        case ['todos']:
            browser_open(['gitlab.com/dashboard/todos'])
        case ['issues']:
            browser_open(['gitlab.com/dashboard/issues?sort=created_date&state=opened&assignee_username%5B%5D=leosanchez'])
        case ['projects']:
            projects = spin_execute("glab repo list | tail -n +3 | awk '{print $1}'", 
                                    title='Fetching gitlab projects...').split('\n')
            project = choose(projects)
            if not project:
                sys.exit(os.EX_NOINPUT)
            browser_open(['/'.join(['gitlab.com', project])])


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
    match args.options:
        case []:
            view = choose(['month', 'week', 'workweek', 'day'])
            if not view:
                sys.exit(os.EX_NOINPUT)
            args.options += [view]
            calendar(args)
        case [view]:
            browser_open([f'outlook.live.com/calendar/0/view/{view}'])
            write_to_history(f"open {Programs.Calendar.value} {view}")


def google_calendar(args: argparse.Namespace):
    match args.options:
        case []:
            view = choose(['agenda', 'day', 'week', 'month', 'year'])
            if not view:
                sys.exit(os.EX_NOINPUT)
            args.options += [view]
            google_calendar(args)
        case [view]:
            browser_open([f'https://calendar.google.com/calendar/u/0/r/{view}'])
            write_to_history(f"open {Programs.GoogleCalendar.value} {view}")


def mail(_: argparse.Namespace):
    browser_open(['https://outlook.live.com/mail/0/'])


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


def tmux(args: argparse.Namespace):
    def is_not_colon(c: str) -> bool:
        return c != ':'

    match args.options:
        case []:
            options = ('sessions', 'new-session')

            selected = choose(options)
            if not selected:
                sys.exit(os.EX_NOINPUT)

            match selected:
                case 'new-session':
                    session_name = gum_input('Session name?')
                    if not session_name:
                        sys.exit(os.EX_NOINPUT)
                    run(['tmux', 'new-session', '-s', session_name, '-d'])
                case 'sessions':
                    args.options.append('sessions')
                    tmux(args)

        case ['sessions']:
            sessions = run(['tmux', 'list-sessions'])
            if sessions:
                sessions = sessions.split('\n')
            normalized_sessions = [
                ''.join(itertools.takewhile(is_not_colon, session)) 
                for session in sorted(sessions)
            ]
            session = choose(normalized_sessions)
            if not session:
                sys.exit(os.EX_NOINPUT)
            args.options.append(session)
            tmux(args)
        case ['sessions', _]:
            session_actions = ("attach", "rename", "kill")
            action = choose(session_actions)
            if not action:
                sys.exit(os.EX_NOINPUT)
            args.options.append(action)
            tmux(args)
        case ['sessions', session, action]:
            match action:
                case 'kill':
                    run(['tmux', 'kill-session', '-t', session])
                case 'attach':
                    run(['tmux', 'switch-client', '-t', session])
                case 'rename':
                    new_name = gum_input(f'New Session name for {session}')
                    if not new_name:
                        sys.exit(os.EX_NOINPUT)
                    run(['tmux', 'rename-session', '-t', session, new_name])


def generate_options(comp_words: List[str]) -> Iterator[str]:
    if len(comp_words) == 1:
        program: Programs = comp_words[0] in SubCommands and Programs(comp_words[0])
        if program:
            if program not in graph:
                return
            for option in graph[program]:
                yield option
            return

    if len(comp_words) == 2:
        program = (comp_words[0] in SubCommands and Programs(comp_words[0]))
        if program and program in graph:
            if comp_words[1] not in graph[program]:
                for option in graph[program]:
                    if option.startswith(comp_words[1]):
                        yield option
            return

    if len(comp_words) > 0 and comp_words[0] == Programs.GitHub.value:
        if len(comp_words) == 3:
            for option in GitHubRepoActions:
                yield option
        elif len(comp_words) == 4 and comp_words[-1] not in GitHubRepoActions:
            for option in GitHubRepoActions:
                if option.startswith(comp_words[3]):
                    yield option
        return

    if len(comp_words) > 2:
        return

    for x in Programs:
        value = x.value
        if len(comp_words) > 0:
            if comp_words[0] in value:
                yield value
        else:
            yield value
        if x in graph:
            for sub_program in graph[x]:
                value = f"{x.value} {sub_program}"
                if len(comp_words) > 0:
                    if comp_words[0] in value:
                        yield value
                else:
                    yield value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", action='store_true')
    parser.add_argument("-p", "--prefix")
    parser.add_argument("options", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if args.list:
        comp_words = [x for x in filter(bool, args.options)]
        print("\n".join(sorted(generate_options(comp_words))))
        return

    open_what(args)


def open_what(args: argparse.Namespace):
    match args.options:
        case []:
            to_open = [
                x.value for x in Programs
            ]
            what = choose([x for x in to_open])
            if not what:
                sys.exit(os.EX_NOINPUT)
            args.options = [what]
            open_what(args)
        case [what, *options]:
            args.options = options
            if what not in programs():
                print(f"{what} is not a valid option", file=sys.stderr)
                sys.exit(1)
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
                case Programs.Tmux:
                    tmux(args)
                case Programs.Mail:
                    mail(args)
                case Programs.News:
                    browser_open(["news.ycombinator.com"])
                case Programs.ChatGPT:
                    firefox_container('https://chat.openai.com', 'ChatGPT')
                case Programs.GoogleCalendar:
                    google_calendar(args)
                case Programs.Courses:
                    browser_open(["http://192.168.29.157:5010"])
                case Programs.Rss:
                    browser_open(["http://192.168.29.157:5011/feeds"])
                case Programs.Kibana:
                    browser_open(["http://192.168.29.157:5601"])
                case Programs.Azure:
                    firefox_container('portal.azure.com', 'Azure')
                case Programs.FastMail:
                    browser_open(["app.fastmail.com/mail/Inbox/?u=b601406a"])
                case Programs.Bard:
                    browser_open(["bard.google.com"])
                case Programs.CloudflareSpeedTest:
                    browser_open(["speed.cloudflare.com/"])
                case Programs.GitLab:
                    gitlab(args)
                case Programs.Rider:
                    open_rider_projects(args)


def programs():
    return [x.value for x in Programs.__members__.values()]


def choose(choices: Iterable[str]) -> str:
    """
    fzf choose any of the given choices interactively
    :param choices: list of strings for the user to choose from
    :return: selected choice or None if ^C is pressed
    """
    choice = fzf(choices)
    if choice and len(choice):
        return choice[0]


def gum_input(placeholder: str) -> str:
    """
    :param placeholder: Gum input placeholder text
    :return: executed process output
    """
    process = subprocess.run(["gum", "input"] + ['--placeholder', placeholder], 
                             stdout=subprocess.PIPE)
    return process.stdout.decode("utf-8").strip()


def run(cmds: list[str]) -> str:
    process = subprocess.run(list(cmds), stdout=subprocess.PIPE)
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


if __name__ == 'open' or 'open.py':
    if "pytest" not in sys.modules:
        main()
