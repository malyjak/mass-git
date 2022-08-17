"""
Script for performing commands over multiple git repositories

Usage: python mass_git.py
"""

import argparse
import json
import subprocess
import shlex

from pathlib import Path
from typing import Union

script_dir_path = Path(__file__).parent


def select_json() -> str:
    """
    Prompts user with available json files and returns the selection.

    :return: Json filename.
    """

    jsons_folder = script_dir_path / '.jsons'
    if not jsons_folder.is_dir():
        raise NotADirectoryError(errno.ENOTDIR, os.strerror(errno.ENOTDIR),
                                 jsons_folder)
    else:
        jsons = list(
            [json for json in jsons_folder.iterdir() if json.is_file()])
        print("Found json files:")
        n = 0
        for json in jsons:
            print(f"({n}) {json.name}")
            n += 1
        print("You can select the desired one by specifying its number")
        bad_number = True
        while bad_number:
            inpt = input("\nYour selection: ")
            try:
                sel = int(inpt)
                if sel < 0 or sel >= n:
                    print("Invalid number! Try again")
                else:
                    bad_number = False
            except ValueError:
                print("Not a number! Try again")

        return jsons[sel].name


def run_cmd(cmd: str, run_in: Path = script_dir_path, capture: bool = False) -> \
        Union[None, str]:
    """
    Runs command in specified directory.

    :param cmd: Command to run.
    :param run_in: Path to a directory where the command will be run.
    :param capture: Whether to capture output.

    :returns: Command output IF capture is true, otherwise nothing.
    """

    if capture:
        proc = subprocess.Popen(shlex.split(cmd),
                                cwd=run_in,
                                stdout=subprocess.PIPE)
        return proc.communicate()[0].decode('utf-8').rstrip()

    print(f"Running: '{cmd}' in {run_in}")
    proc = subprocess.Popen(shlex.split(cmd),
                            cwd=run_in)
    proc.communicate()


def get_current_branch(repo_dir: str = '') -> str:
    """
    Gets current branch for a given repository.

    :param repo_dir: Directory name of the repository.

    :returns: Current branch name.
    """

    return run_cmd("git rev-parse --abbrev-ref HEAD",
                   script_dir_path / repo_dir,
                   True)


class MassGit:
    """
    Class for mass git actions.
    """

    def __init__(self):
        self.json_path = None
        self.repos = None

    def load_memory(self, change_json: bool = False) -> None:
        """
        Tries to load json from memory file if present.
        Writes a newly selected json to the memory file otherwise.

        :param change_json: Whether a different json should be used.
        """

        mem_file_path = script_dir_path / '.memory'
        if not mem_file_path.is_file() or change_json:
            # Select json.
            json_file = select_json()

            # Write json to memory.
            with mem_file_path.open("w", encoding="utf-8") as mem_file:
                mem_file.write(json_file)
        else:
            # Read json from memory.
            with mem_file_path.open("r", encoding="utf-8") as mem_file:
                json_file = mem_file.read()

        # Save
        self.json_path = script_dir_path / '.jsons' / json_file

    def parse_json(self) -> None:
        """
        Parses data about repositories from json.
        """

        with open(self.json_path) as json_file:
            self.repos = json.load(json_file)['git']

    def download(self) -> None:
        """
        Downloads repositories listed in json if needed.
        """

        for repo in self.repos:
            keys = repo.keys()
            if not 'url' in keys:
                print("Invalid json (missing url entry)! Please add it")
                raise KeyError
            if 'dir' in keys:
                repo_path = script_dir_path / repo['dir']
            else:
                # Get repository name from url.
                repo_name = repo['url'].rsplit('/', 1)[1][:-4]
                repo_path = script_dir_path / repo_name
                repo['dir'] = repo_name
            if 'branch' in keys:
                branch = f"-b {repo['branch']}"
            else:
                repo['branch'] = ''
                branch = repo['branch']

            if not repo_path.is_dir():
                run_cmd(f"git clone {branch} {repo['url']} {repo['dir']}")

            if repo['branch'] == '':
                repo['branch'] = get_current_branch(repo['dir'])

    def help(self) -> None:
        """
        Displays help.
        """

        print("List of supported commands:")
        print(f"{'h help':<20}Displays this help")
        print(f"{'s show':<20}Shows current branches for all repositories")
        print(f"{'r refresh':<20}Refreshes branches to json defaults")
        print(f"{'p pull':<20}Performs pull in all repositories")
        print(f"{'q quit':<20}Quits program")

    def show(self) -> None:
        """
        Shows current branch for all repositories.
        """

        for repo in self.repos:
            print(f"{repo['dir']:<20}{get_current_branch(repo['dir'])}")

    def refresh(self) -> None:
        """
        Refresh branches of all repositories to default json value.
        """

        for repo in self.repos:
            run_cmd(f"git checkout {repo['branch']}",
                    script_dir_path / repo['dir'])

    def pull(self) -> None:
        """
        Performs a pull in all repositories.
        """

        for repo in self.repos:
            run_cmd(f"git pull",
                    script_dir_path / repo['dir'])

    def loop(self) -> None:
        """
        Main loop which awaits for commands.
        """

        print(
            "MassGit initialized! You can now enter commands (for help use `h` or `help`)")
        loop = True
        while loop:
            inpt = input("\nYour command: ")
            try:
                cmd = str(inpt)
                if cmd == 'h' or cmd == 'help':
                    self.help()
                elif cmd == 's' or cmd == 'show':
                    self.show()
                elif cmd == 'r' or cmd == 'refresh':
                    self.refresh()
                elif cmd == 'p' or cmd == 'pull':
                    self.pull()
                elif cmd == 'q' or cmd == 'quit':
                    loop = False
                else:
                    print("Invalid command! Try again")
            except ValueError:
                print("Invalid command! Try again")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--change',
                        help='Whether a different json should be used.',
                        action='store_true')
    args = parser.parse_args()
    mg = MassGit()
    mg.load_memory(args.change)
    mg.parse_json()
    mg.download()
    mg.loop()
