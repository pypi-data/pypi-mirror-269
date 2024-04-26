#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK

# git_smudge
#
# Copyright (C) 2022 Katie Rust (katie@ktpanda.org)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import os
import argparse
import argcomplete
import subprocess
import logging
import shlex
from io import StringIO
from pathlib import Path

from git_smudge import VERSION, LANG_MAP, add_common_args
from git_smudge.config import Config, run_git

from ktpanda.cli import Parser, arg

log = logging.getLogger(__name__)

arg_parser = Parser(description=f'git_smudge version {VERSION}')
command = arg_parser.command

@command('setup',
         help="Set up the repository / worktree to enable git-smudge and create an empty "
         "configuration if it doesn't exist")
@arg('-n', '--no-completion', action='store_true',
     help="Do not attempt to install bash-completion scripts")
def cmd_setup(parser, args):
    if not args.no_completion:
        created, path = setup_completion(True)
        if created:
            print(f'Created bash-completion script for git-smudge in {path}')

    cfg = load_config()
    cfg.setup()

@command('apply',
         help='Update the configuration from git-smudge.toml and apply changes to files')
@arg('-N', '--no-update-files',
     action='store_true',
     help="Apply the new configuration but do not update any files")
def cmd_apply(parser, args):
    cfg = load_config()
    cfg.apply(not args.no_update_files)

@command('clean',
         help='Undo any changes made to files, as if an empty configuration were applied')
def cmd_clean(parser, args):
    cfg = load_config()
    cfg.load_new({})
    cfg.apply()

@command('comment-styles',
         help='List all available values for `comment_style`')
def cmd_list_style(parser, args):
    for lang, (line, block, extensions) in LANG_MAP.items():
        extensions = ', '.join(extensions.split())
        print(f'{lang}, {extensions}:')
        if line:
            print(f'   {line[0]}LINE{line[1]}')
        if block:
            print(f'   {block[0]}BLOCK{block[1]}')
        print()

@command('comp', help='Reinstall the bash completion script')
def cmd_comp(parser, args):
    try:
        created, path = setup_completion(True)
        print(f'Set up completion in {path}')
    except OSError as e:
        print('Unable to install completion: {e}')

@command('edit', help='Edit the git-smudge configuration file')
@arg('-a', '--apply', action='store_true', help="Apply the new configuration after editing")
def cmd_edit(parser, args):
    cfg = load_config()
    editor = run_git(['var', 'GIT_EDITOR']).stdout.strip()
    subprocess.run(f'{editor} git-smudge.toml', shell=True, cwd=cfg.config_path.parent)
    if args.apply:
        cfg.apply()
    else:
        print('Run `git smudge apply` to apply the new configuration', file=sys.stderr)

@command('diff', help='Show what changes have been applied to files')
@arg('-c', '--current', action='store_true',
     help="Compare to current content instead of cleaned content")
@arg('-p', '--preview', action='store_true',
     help="Show what changes would be applied with new configuration")
@arg('diffargs', nargs='*', help="Extra arguments to `git diff` (use '--' to pass options)")
def cmd_diff(parser, args):
    cfg = load_config()
    cfg.diff(args.preview, args.current, args.diffargs)

def _getenv_path(var):
    if value := os.getenv(var):
        return Path(value)
    return None

def setup_completion(ignore_existing=False):
    if not (completion_user_dir := _getenv_path('BASH_COMPLETION_USER_DIR')):
        data_home = _getenv_path('XDG_DATA_HOME') or (Path.home() / '.local/share')
        completion_user_dir = data_home / 'bash-completion'

    completion_user_dir = completion_user_dir / 'completions'

    user_path = completion_user_dir / 'git-smudge'
    if not ignore_existing and user_path.exists():
        return False, user_path

    text = argcomplete.shellcode(['git-smudge'], True, 'bash', [], None)
    text += '\n\n_git_smudge() { _python_argcomplete "git-smudge"; }\n'

    # First, try to install it in global completion if we can
    data_dirs = os.getenv('XDG_DATA_DIRS') or '/usr/local/share:/usr/share'
    for dir in data_dirs.split(':'):
        if not dir:
            continue

        path = Path(dir) / '/bash-completion/completions/git-smudge'
        if not ignore_existing and path.exists():
            return False, path

        try:
            path.write_text(text)
            return True, path
        except OSError:
            pass

    completion_user_dir.mkdir(exist_ok=True, parents=True)

    try:
        user_path.write_text(text)
        return True, user_path
    except OSError as ex:
        if ignore_existing:
            raise
        return False, None

def load_config():
    cfg = Config.from_git()
    cfg.load()
    return cfg

def add_arguments_for_main(p):
    p.set_defaults(debug=False)
    add_common_args(p)

def setup_logging(debug):
    if os.getenv('GIT_SMUDGE_DEBUG') not in {None, '', '0'}:
        debug = True

    root = logging.getLogger()
    root.setLevel(logging.DEBUG if debug else logging.INFO)

    console_formatter = logging.Formatter('git-smudge: %(levelname)s: [%(name)s] %(message)s')
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(console_formatter)
    root.addHandler(console_handler)

def fix_comp_line():
    comp_line = os.getenv('COMP_LINE')
    comp_point = os.getenv('COMP_POINT') or ''
    if comp_line is not None:
        try:
            comp_point = int(comp_point)
        except ValueError:
            comp_point = len(comp_line)

        io = StringIO(comp_line)
        lex = shlex.shlex(io, posix=True)
        while True:
            split_pos = io.tell()
            tok = lex.read_token()
            if tok is None:
                return

            if tok == 'smudge':
                # If we found the word "smudge", then process the rest of the line past
                # the current token.
                split_pos = io.tell()
                break
            elif (tok,) in arg_parser.commands:
                # If we found a supported command, process the rest of the line including
                # the current token.
                break

        new_prefix = 'git-smudge '
        comp_point += len(new_prefix) - split_pos
        os.environ['COMP_LINE'] = new_prefix + comp_line[split_pos:]
        os.environ['COMP_POINT'] = str(comp_point)

def main(prog='git-smudge'):
    p = arg_parser.root_parser

    add_arguments_for_main(p)

    fix_comp_line()
    argcomplete.autocomplete(p)

    args = p.parse_args()

    setup_logging(args.debug)

    arg_parser.dispatch(args)

if __name__ == '__main__':
    main('python3 -m git_smudge')
