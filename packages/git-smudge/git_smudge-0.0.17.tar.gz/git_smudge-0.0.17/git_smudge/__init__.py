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

'''
git_smudge
==========

A filter driver for Git which cam make local changes to a repository.
'''

import sys
import re
import time
import os
import argparse
import subprocess
import traceback
import struct
import logging
from io import BytesIO
from pathlib import Path

import argcomplete

from ktpanda.roundtrip_encoding import TextContent

proc_log = logging.getLogger('git-process')
filt_log = logging.getLogger('filters')

VERSION = "0.0.17"

MAX_PACKET_CONTENT_SIZE = 65516
BOM = '\ufeff'
DEBUG = False

# Line comments
COMMENT_HASH = '# ', ''
COMMENT_SLASH = '/ ', ''
COMMENT_DSLASH = '// ', ''
COMMENT_SEMI = '; ', ''
COMMENT_DDASH = '-- ', ''
COMMENT_EXCL = '! ', ''
COMMENT_PCT = '% ', ''
COMMENT_REM = 'REM ', ''
COMMENT_QUOT = "' ", ''

# Block comments
COMMENT_C = '/* ', ' */'
COMMENT_PS = '<* ', ' *>'
COMMENT_SGML = '<!-- ', ' -->'
COMMENT_PASCAL = '(* ', ' *)'
COMMENT_HASKELL = '{- ', ' -}'
COMMENT_LUA = '--[=[ ', ' ]=]'
COMMENT_JINJA = '{# ', ' #}'
COMMENT_MUSTACHE = '{{!  ', ' }}'

EXT_MAP = {}
LANG_MAP = {}

# This is by no means a comprehensive list. I went through this page:
# https://en.wikipedia.org/wiki/Comparison_of_programming_languages_(syntax)#Comments
# and just added a bunch of them
LANG_MAP = {
    # Shell-like
    'Python':     (COMMENT_HASH,   None,            'py'),
    'Shell':      (COMMENT_HASH,   None,            'sh bash'),
    'Ruby':       (COMMENT_HASH,   None,            'rb'),
    'Perl':       (COMMENT_HASH,   None,            'pl pm'),
    'Raku':       (COMMENT_HASH,   None,            'raku rakumod rakudoc rakutest t'),
    'Elixir':     (COMMENT_HASH,   None,            'ex exs'),
    'Julia':      (COMMENT_HASH,   None,            'jl'),
    'Config':     (COMMENT_HASH,   None,            'conf ini'),
    'Nim':        (COMMENT_HASH,   None,            'nim nims nimble'),

    # C-like
    'C':          (COMMENT_DSLASH, COMMENT_C,       'c h'),
    'C++':        (COMMENT_DSLASH, COMMENT_C,       'cpp hpp c++ h++ cc hh'),
    'C#':         (COMMENT_DSLASH, COMMENT_C,       'cs'),
    'D':          (COMMENT_DSLASH, COMMENT_C,       'd'),
    'F#':         (COMMENT_DSLASH, None,            'fs fsi fsx fsscript'),
    'Go':         (COMMENT_DSLASH, COMMENT_C,       'go'),
    'Kotlin':     (COMMENT_DSLASH, COMMENT_C,       'kt kts ktm'),
    'ObjC':       (COMMENT_DSLASH, COMMENT_C,       'm mm'),
    'Rust':       (COMMENT_DSLASH, COMMENT_C,       'rs rlib'),
    'Scala':      (COMMENT_DSLASH, COMMENT_C,       'sc scala'),
    'CSS':        (None,           COMMENT_C,       'css'),
    'SASS':       (COMMENT_DSLASH, COMMENT_C,       'sass scss'),
    'Java':       (COMMENT_DSLASH, COMMENT_C,       'java'),
    'Javascript': (COMMENT_DSLASH, COMMENT_C,       'js ts'),
    'Swift':      (COMMENT_DSLASH, COMMENT_C,       'swift'),
    'PHP':        (COMMENT_DSLASH, COMMENT_C,       'php'),

    # SGML
    'HTML':       (None,           COMMENT_SGML,    'html'),
    'XML':        (None,           COMMENT_SGML,    'xml'),
    'SGML':       (None,           COMMENT_SGML,    'html xml sgml'),

    # ';'
    'Lisp':       (COMMENT_SEMI,   None,            'el scm lisp lsp l cl fasl'),
    'Scheme':     (COMMENT_SEMI,   None,            'scm ss'),
    'Clojure':    (COMMENT_SEMI,   None,            'clj cljs cljc edn'),
    'Rebol':      (COMMENT_SEMI,   None,            'r reb'),
    'Red':        (COMMENT_SEMI,   None,            'red reds'),
    'Assembler':  (COMMENT_SEMI,   None,            'asm s'),
    'Autohotkey': (COMMENT_SEMI,   COMMENT_C,       'ahk'),

    # '--'
    # Some SQL variants support /* */, but not all
    'SQL':        (COMMENT_DDASH,  None,            'sql'),
    'Lua':        (COMMENT_DDASH,  COMMENT_LUA,     'lua'),
    'Ada':        (COMMENT_DDASH,  None,            'ada'),
    'Haskell':    (COMMENT_DDASH,  COMMENT_HASKELL, 'hs lhs'),
    'Eiffel':     (COMMENT_DDASH,  None,            'e'),

    # '%'
    'MATLAB':     (COMMENT_PCT,    None,            'm p mex mat fig mlx mlapp'),
    'Erlang':     (COMMENT_PCT,    None,            'erl hrl'),
    'TeX':        (COMMENT_PCT,    None,            'tex'),
    'Postscript': (COMMENT_PCT,    None,            'ps'),

    # Templating systems
    'Jinja':      (None,           COMMENT_JINJA,   'jinja'),
    'Slime':      (COMMENT_SLASH,  None,            'slime'),
    'Mustache':   (None,           COMMENT_MUSTACHE,'mustache'),

    # Weirdos
    'Fortran 90': (COMMENT_EXCL,   None,            'f for f90'),
    'Pascal':     (None,           COMMENT_PASCAL,  'pas'),
    'Batch':      (COMMENT_REM,    None,            'bat'),
    'Visual Basic':(COMMENT_QUOT,  None,            'vb vba vbs bas'),
}

def _fill_comment_map():
    for item in LANG_MAP.items():
        EXT_MAP[item[0].lower()] = item
        for extn in item[1][2].split():
            EXT_MAP[extn] = item

def get_comment_style(ext, path=None, prefer_block=False):
    if not EXT_MAP:
        _fill_comment_map()

    if ext == 'auto' and path:
        ext = path.suffix.strip('.')

    ext = ext.lower()

    defn = EXT_MAP.get(ext)
    if defn is None:
        defn = 'Unknown', (COMMENT_HASH, None, ext)

    line_comment, block_comment, _ = defn[1]
    if line_comment is None:
        return block_comment

    if block_comment is None:
        return line_comment

    return block_comment if prefer_block else line_comment

def add_single_run_args(p):
    '''Add the common arguments to an `argparse.ArgumentParser`'''
    p.add_argument(
        '-s', '--smudge',
        dest='clean', action='store_false', default=None,
        help='Filter data from STDIN and apply working tree changes')

    p.add_argument(
        '-c', '--clean',
        dest='clean', action='store_true',
        help='Filter data from STDIN and undo working tree changes')

    p.add_argument(
        '-p', '--path', type=Path,
        help='Path to the file being processed')

    p.add_argument(
        '-P', '--process', action='store_true',
        help='Run the filter in "process" mode, filtering multiple files')

def add_common_args(p):
    '''Add common arguments to an `argparse.ArgumentParser`'''
    p.add_argument(
        '-D', '--debug', action='store_true',
        help='Show debugging output. Always set true if environment variable '
        'GIT_SMUDGE_DEBUG is set to "1"')

class FileContent(TextContent):
    '''Represents the contents of a file being processed. Contains information on how to
    re-encode the contents back to binary.'''

    warn_inconsistent_line_endings = True

    def __init__(self, path, data, is_smudged=False):
        super().__init__(data)
        self.path = path
        self.is_smudged = is_smudged
        self.warned_line_endings = False

    @property
    def is_dos(self):
        return self.line_endings == 'dos'

    @classmethod
    def load(cls, path, is_smudged=False):
        return cls(path, path.read_bytes(), is_smudged)

    def copy(self):
        new = type(self)(self.path, None)
        new.set_from(self)
        return new

    def get_text(self):
        '''Retrieves the current text, converting it from binary if necessary'''
        text = super().get_text()

        if (self.line_endings == 'mixed'
            and self.warn_inconsistent_line_endings):
            filt_log.warning('%s has inconsistent line endings!', self.path)
            self.warn_inconsistent_line_endings = False

        return text

    def _smudge_check(self, filter):
        '''Run `smudge`, checking that `clean` properly restores the content'''
        if not filter.config.get('smudge_check_clean', True):
            filter.smudge(self)
            return

        new_content = self.copy()
        filter.smudge(new_content)

        check_content = new_content.copy()
        check_content.is_smudged = True
        filter.clean(check_content)
        #filt_log.debug('orig:  %r', self.text_data)
        #filt_log.debug('new:   %r', new_content.text_data)
        #filt_log.debug('clean: %r', check_content.text_data)
        if check_content == self:
            self.set_from(new_content)
            self.changed |= new_content.changed
        else:
            filt_log.warning(
                '%s: applying filter %r results in text that '
                'does not restore properly',
                self.path, filter)

    def smudge(self, filters):
        # Reverse any idempotent filters
        self.is_smudged = False

        for filter in reversed(filters):
            filter.clean(self)

        for filter in filters:
            self._smudge_check(filter)

        self.is_smudged = True

    def clean(self, filters):
        self.is_smudged = True

        for filter in reversed(filters):
            filter.clean(self)

        self.is_smudged = False

class GitFilter:
    args = None

    def __init__(self, config=None, name='', index=0, **kw):
        self.name = name
        self.index = index
        if config is None:
            config = {}
        self.config = config
        if kw:
            config.update(kw)

    def _set_from_config(self, **kw):
        pass

    def update_config(self):
        self._set_from_config(**self.config)

    def read_packet(self):
        length_data = sys.stdin.buffer.read(4)
        if not length_data:
            raise EOFError()


        proc_log.debug('length = %r', length_data)

        ln = int(length_data.decode('ascii'), 16)
        if ln == 0:
            pkt = None
        else:
            pkt = sys.stdin.buffer.read(ln - 4)

        proc_log.debug('read packet %d %r', ln, pkt)

        return pkt

    def read_packet_text(self):
        data = self.read_packet()
        return None if data is None else data.decode('utf8').rstrip('\n')

    def write_packet(self, val):
        if isinstance(val, str):
            val = (val + '\n').encode('utf8')
        length_data = f'{len(val) + 4:04X}'.encode('ascii')

        proc_log.debug('write packet %r %r', length_data, val)
        sys.stdout.buffer.write(length_data)
        sys.stdout.buffer.write(val)

    def flush(self):
        proc_log.debug('flush')

        sys.stdout.buffer.write(b'0000')
        sys.stdout.buffer.flush()

    def expect_packet(self, expect):
        pkt = self.read_packet_text()
        if pkt != expect:
            raise ValueError(f'Expected {expect!r}, got {pkt!r}')

    def get_filters(self, path):
        return (self,)

    def clean(self, content):
        pass

    def smudge(self, content):
        pass

    def read_key_val(self):
        rtn = {}
        while True:
            pkt = self.read_packet_text()
            if pkt is None:
                return rtn
            key, _, val = pkt.partition('=')
            if key in rtn:
                rtn[key] = rtn[key] + '\n' + val
            else:
                rtn[key] = val

    def run_process(self):
        try:
            # Make sure stdout is in binary mode on Windows. Use `getattr` so pylint
            # doesn't complain about the attribute being missing.
            import msvcrt
            msvcrt.setmode(sys.stdin.fileno(), getattr(os, 'O_BINARY'))
        except (ImportError, AttributeError):
            pass

        ident = self.read_packet_text()
        if ident != 'git-filter-client':
            raise ValueError(f'Invalid ident {ident!r}')

        header = self.read_key_val()
        if header.get('version') != '2':
            raise ValueError(f'Invalid version {header.get("version")}')

        self.write_packet('git-filter-server')
        self.write_packet('version=2')
        self.flush()

        caps = self.read_key_val()

        self.write_packet('capability=clean')
        self.write_packet('capability=smudge')
        self.flush()

        while True:
            header = self.read_key_val()
            cmd = header['command']
            path = header['pathname']

            if not path:
                raise ValueError('Empty path')

            filters = self.get_filters(path)
            if not filters:
                proc_log.debug('No filters for %s, bailing early', path)
                # Read the data and discard it
                while self.read_packet() is not None:
                    pass
                self.write_packet('status=error')
                self.flush()
                continue

            fp = BytesIO()
            while True:
                pkt = self.read_packet()
                if not pkt:
                    break
                fp.write(pkt)

            data = fp.getvalue()
            if cmd in {'clean', 'smudge'}:
                content = FileContent(Path(path), data, cmd == 'clean')

                try:
                    if cmd == 'smudge':
                        content.smudge(filters)
                    else:
                        content.clean(filters)

                except Exception:
                    proc_log.exception('Failed to %s %s', cmd, path)
                    self.write_packet('status=error')
                    self.flush()
                    continue
            else:
                raise ValueError('Invalid command: {command!r}')

            if not content.changed:
                proc_log.debug('Filters for %s did not change content', path)
                self.write_packet('status=error')
                self.flush()
                continue

            self.write_packet('status=success')
            self.flush()

            fp = BytesIO(content.get_binary())
            while True:
                pkt = fp.read(MAX_PACKET_CONTENT_SIZE)
                if not pkt:
                    break
                self.write_packet(pkt)
            self.flush()
            self.flush()

    def filter_one(self, path, clean):
        data = sys.stdin.buffer.read()
        content = FileContent(path, data, clean)
        try:
            self.clean(content)
            if not clean:
                self.smudge(content)
        except Exception:
            sys.stdout.buffer.write(data)
            traceback.print_exc()
        else:
            sys.stdout.buffer.write(content.get_binary())

    def add_extra_arguments(self, p):
        pass

    def run_main_other(self):
        print('Must specify --smudge, --clean, or --process')

    def run_main(self):
        '''Run this filter in standalone mode'''
        self.update_config()

        p = argparse.ArgumentParser(description='')
        add_common_args(p)
        add_single_run_args(p)
        self.add_extra_arguments(p)
        argcomplete.autocomplete(p)
        args = p.parse_args()

        self.args = args
        if args.process:
            try:
                self.run_process()
            except EOFError:
                pass
        elif args.clean is not None:
            self.filter_one(args.path, args.clean)
        else:
            self.run_main_other()

    def __repr__(self):
        params = ", ".join(f'{k}={v!r}' for k, v in self.config.items())
        return f'{type(self).__name__}({params})'

class ConfigDispatchFilter(GitFilter):
    def __init__(self, config):
        super().__init__()
        self.cfg = config

    def get_filters(self, path):
        return self.cfg.working_config.get_filters_for_path(path)
