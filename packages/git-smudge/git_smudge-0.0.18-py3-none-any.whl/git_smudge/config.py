# git_smudge.config
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
import fnmatch
import subprocess
import logging
import tempfile

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib

from pathlib import Path

try:
    from subprocess import CREATE_NO_WINDOW
except ImportError:
    CREATE_NO_WINDOW = 0

from ktpanda.fileutils import load_json, save_json

from git_smudge import GitFilter, FileContent
from git_smudge.filters import SimpleFilter, InsertLineFilter, CommentOutFilter

log = logging.getLogger('config')

MAX_FILTER_LIST = 5000

CONFIG_TEMPLATE = r'''
## Example configuration.
## See https://toml.io/en/v1.0.0 for TOML syntax

[options]
warn-inconsistent-line-endings = true

## List of plugins to load. The plugin can create one or more subclasses of `GitFilter`.
## Each class can be referenced by name, without `Filter` on the end.
# plugins = [
#     "plugin1.py",
#     "plugin2.py",
# ]

## Define a simple filter that applies to all .c files except foo.c
# [filters.filter1]
# type = "simple"
# search = "filter1"
# replace = "qwer"
# files = [ "*.c", "!foo.c" ]

## Define an insert filter that applies to all files in 'subdir/' except .txt files
# [filters.filter2]
# type = "InsertLine"
# after = 'filter2'
# insert = [ "test1", "test2" ]
# files = [ "subdir/*", "!*.txt" ]

## Define a multi-part filter that applies to all .js files in the project root
# [filters.filter3]
# files = "/*.js"
#
# [[filters.filter3.filters]]
# type = "InsertLine"
# after = 'old_call\(123, (.*)\)'
# insert = [ 'new_call(456, $1);']
#
# [[filters.filter3.filters]]
# type = "CommentOut"
# match = 'old_call\(123, (.*)\)'

# Add an extra match patterns
# [[rule]]
# filters = [ "filter1", "filter2" ]
# files = "!special.c"
#
# [[rule]]
# filters = "filter3"
# files  = "special.c"
'''

class CacheDict(dict):
    '''Works like `defaultdict`, except it passes the key to the factory function'''
    def __init__(self, factory):
        super().__init__()
        self.factory = factory

    def __missing__(self, key):
        r = self[key] = self.factory(key)
        return r

def run_cmd(cmd, check=True, **kw):
    if CREATE_NO_WINDOW:
        kw['creationflags'] = CREATE_NO_WINDOW

    return subprocess.run(cmd, check=check, **kw)

def run_git(cmd, check=True, **kw):
    return run_cmd(
        ['git'] + cmd, stdout=subprocess.PIPE, check=check,
        encoding='utf8', errors='surrogateescape', **kw)

def git_path(relpath) -> Path:
    '''Return a `Path` object pointing to a file within the .git directory'''
    return Path(run_git(['rev-parse', '--git-path', relpath]).stdout.rstrip('\n'))

def item_or_list(val):
    return val if isinstance(val, list) else [val]

def _build_filter_list(filter_list, obj):
    if isinstance(obj, dict):
        sub_filters = obj.get('filters')
        if sub_filters:
            _build_filter_list(filter_list, sub_filters)

        if obj.get('type'):
            filter_list.append(obj)

    elif isinstance(obj, list):
        for part in obj:
            _build_filter_list(filter_list, part)

    elif isinstance(obj, str):
        filter_list.append(obj)
    else:
        raise TypeError(f'Invalid value in filter list: {obj!r}')

def _resolve_references(named_filters, input_list, output_list):
    for val in input_list:
        if isinstance(val, str):
            sub_list = named_filters[val]
            if sub_list is None:
                raise ValueError(f'Reference loop detected in filters: {val}')

            # Temporarily remove the referenced list to detect loops
            named_filters[val] = None
            _resolve_references(named_filters, sub_list, output_list)
            named_filters[val] = sub_list
        else:
            output_list.append(val)

class Pattern:
    def __init__(self, pat):
        self.dir_pattern, self.file_pattern = pat
        self.include_rules = []
        self.exclude_rules = []

class FilterConfig:
    def __init__(self, root):
        self.root = root
        self.filter_classes = {}
        self.named_filters = {}
        self.patterns = []

    @classmethod
    def from_toml(cls, tomlobj, worktree, gitdir):
        plugin_content = []
        patterns = CacheDict(lambda k: [[], []])
        filters = {}

        new_root = {
            'plugins': plugin_content,
            'filters': filters,
            'patterns': patterns
        }

        for obj in tomlobj.get('plugins', ()):
            # support both `plugins = [ ... ]` and [[plugins]] path = ...
            if isinstance(obj, str):
                obj = { 'path': obj }
            path = obj['path']

            # If path starts with '~/', make it relative to the user's home directory. If
            # it starts with '.git/' exactly, then it's relative to the common Git directory,
            # even if it's not in the usual place.
            if path.startswith('.git/'):
                script_path = gitdir / path[5:]
            elif path.startswith('~/'):
                script_path = Path.home() / path[2:]
            else:
                script_path = worktree / path

            log.debug('Loading plugin %s', script_path)
            content = FileContent(script_path, script_path.read_bytes())
            plugin_content.append({'path': str(script_path), 'content': content.get_text().split('\n')})

        filter_rules = CacheDict(lambda k: [])
        for rule in tomlobj.get('rule', ()):
            files = item_or_list(rule.get('files', []))
            for filter in item_or_list(rule.get('filters', [])):
                filter_rules[filter].extend(files)

        for name, obj in tomlobj.get('filters', {}).items():
            filter_list = []
            _build_filter_list(filter_list, obj)
            filters[name] = filter_list


            files = item_or_list(obj.get('files', []))
            files.extend(filter_rules[name])

            for pattern in files:
                if exclude := pattern.startswith('!'):
                    pattern = pattern[1:]

                # If there is no '/' in the rule, then it applies to the filename only
                dirpart, sep, filepart = pattern.rpartition('/')
                if sep:
                    dirpart = dirpart.lstrip('/')
                else:
                    dirpart = '*'

                key = dirpart + '/' + filepart
                if exclude:
                    patterns[key][1].append(name)
                else:
                    patterns[key][0].append(name)

        for name, obj in filters.items():
            filters[name] = None
            output_list = []
            _resolve_references(filters, obj, output_list)
            filters[name] = output_list

        return cls(new_root)

    @classmethod
    def load_json(cls, jsonpath):
        root = load_json(jsonpath)
        if root is None:
            return cls({})

        return cls(root)

    def load(self):
        for cls in (SimpleFilter, InsertLineFilter, CommentOutFilter):
            self.add_filter_class(cls)

        for obj in self.root.get('plugins', ()):
            try:
                block = compile(
                    '\n'.join(obj['content']), obj['path'],
                    mode='exec', dont_inherit=True)

                namespace = { 'GitFilter': GitFilter }
                exec(block, namespace)

                for value in namespace.values():
                    if (isinstance(value, type)
                        and issubclass(value, GitFilter)
                        and value is not GitFilter):
                        log.debug('Adding filter class %s', value)
                        self.add_filter_class(value)
            except Exception as ex:
                raise ValueError(f'Failed to load plugin {obj["path"]} (see attached exception)') from ex

        self.named_filters = filters = {}
        for name, filter_list in self.root.get('filters', {}).items():
            filters[name] = new_filter_list = []
            for index, obj in enumerate(filter_list):
                filter_type = obj['type']
                cls = self.filter_classes[filter_type.lower()]
                filter = cls(obj, name, index)
                filter.update_config()
                new_filter_list.append(filter)

        patterns = self.patterns = []
        for key, (include, exclude) in self.root.get('patterns', {}).items():
            dirpart, _, filepart = key.rpartition('/')
            patterns.append((dirpart, filepart, include, exclude))

    def add_filter_class(self, cls):
        name = cls.__name__
        if name.endswith('Filter'):
            name = name[:-6]
        #log.debug('Adding filter class %s as %s', cls, name.lower())
        self.filter_classes[name.lower()] = cls

    def get_filters_for_path(self, path):
        dirpart, _, filepart = path.rpartition('/')

        include_filters = set()
        exclude_filters = set()
        for dir_pattern, file_pattern, include, exclude in self.patterns:
            if (fnmatch.fnmatch(dirpart, dir_pattern) and
                fnmatch.fnmatch(filepart, file_pattern)):

                log.debug('%s: matches %s/%s', path, dir_pattern, file_pattern)
                include_filters.update(include)
                exclude_filters.update(exclude)

        include_filters -= exclude_filters
        if not include_filters:
            log.debug('%s: no filters matched', path)
            return []

        rtnlist = []
        for name, filter_list in self.named_filters.items():
            if name in include_filters:
                rtnlist.extend(filter_list)

        log.debug('Filters for %s: %r', path, rtnlist)
        return rtnlist

class Config:
    def __init__(self, worktree, git_dir, git_common_dir=None, config_path=None):
        self.worktree = worktree
        self.git_dir = git_dir
        self.git_common_dir = git_common_dir or git_dir

        self.config = {}
        self.options = {}

        self.new_config = None
        self.working_config = None

        if config_path is None:
            config_path = git_dir / f'git-smudge.toml'
        self.config_path = config_path
        self.working_config_path = config_path.with_name(f'worktree-git-smudge.json')

    @classmethod
    def from_git(cls):
        paths = run_git([
            'rev-parse', '--show-toplevel', '--git-dir',
            '--git-common-dir', '--git-path', 'git-smudge.toml'
        ]).stdout.replace('\r\n', '\n').rstrip('\n').split('\n')

        worktree, gitdir, gitcommon, configpath = paths

        return cls(Path(worktree), Path(gitdir), Path(gitcommon), Path(configpath))

    def check_config_newer(self):
        '''Check if the user configuration has been changed since the last time
        `git smudge apply` was run'''
        try:
            wt_mtime = self.working_config_path.stat().st_mtime
        except FileNotFoundError:
            wt_mtime = 0

        try:
            config_mtime = self.config_path.stat().st_mtime
            if (config_mtime - wt_mtime) > 2:
                return True
        except FileNotFoundError:
            pass

        return False

    def warn_config_newer(self):
        if self.check_config_newer():
            log.warning(
                'Configuration %s has changed, please run `git smudge apply`',
                self.config_path)

    def load(self):
        try:
            with self.config_path.open('rb') as fp:
                self.config = tomllib.load(fp)
        except FileNotFoundError:
            self.config = {}

        self.options = self.config.get('options', {})
        FileContent.warn_inconsistent_line_endings = self.options.get('warn-inconsistent-line-endings', True)

        self.working_config = FilterConfig.load_json(self.working_config_path)
        self.working_config.load()

    def load_new(self, root=None):
        if root is None:
            root = self.config

        self.new_config = FilterConfig.from_toml(
            root, self.worktree, self.git_common_dir)
        self.new_config.load()

    def save_json(self, root):
        new_root = {
            'note': [
                "DO NOT EDIT THIS FILE. EDIT git-smudge.toml, THEN RUN",
                "`git smudge apply` TO APPLY CONFIGURATION CHANGES"
            ],
            'plugins': root.get('plugins', []),
            'filters': root.get('filters', {}),
            'patterns': root.get('patterns', {})
        }
        save_json(self.working_config_path, new_root)

    def walk_files(self, old_config, new_config):
        # Get a list of all files tracked in the repository. `git ls-files -z` will spit
        # out a NUL-separated list.
        repo_files = run_git(['ls-files', '--stage', '-z']).stdout.split('\0')

        # If there are no files, or there was a terminating NUL, there will be a blank
        # item at the end
        if repo_files[-1] == '':
            repo_files.pop()

        for entry in repo_files:
            path = entry.split('\t', 1)[-1]

            # Run the file through the `clean` method of the old filters, then the
            # `smudge` method of the new filters.
            old_filters = old_config.get_filters_for_path(path)
            new_filters = new_config.get_filters_for_path(path)
            if old_filters or new_filters:
                fpath = self.worktree / path

                orig_data = fpath.read_bytes()
                content = FileContent(fpath, orig_data, True)
                orig_content = content.copy()

                content.clean(old_filters)
                clean_content = content.copy()
                content.is_smudged = False
                content.smudge(new_filters)

                yield fpath, path, entry, orig_content, clean_content, content

    def apply(self, update_files=True):
        if not self.new_config:
            self.load_new()

        if not update_files:
            self.save_json(self.new_config.root)
            return

        update_index_data = []

        change_count = 0
        written_files = []
        try:
            itr = self.walk_files(self.working_config, self.new_config)
            for fpath, path, entry, orig_content, clean_content, new_content in itr:
                if not new_content.changed:
                    continue

                new_data = new_content.get_binary()
                if new_data == orig_content.get_binary():
                    continue

                change_count += 1
                log.info('apply: Content of %s has changed', path)
                update_index_data.append(entry + '\0')
                tf = tempfile.NamedTemporaryFile(
                    dir=str(fpath.parent), prefix=fpath.name,
                    suffix='.smudge-apply-temp', delete=False, mode='wb')
                written_files.append((fpath, tf.name))
                with tf:
                    tf.write(new_data)

                try:
                    os.chmod(tf.name, fpath.stat().st_mode)
                except OSError as e:
                    # Don't get too worked up about a chmod failure
                    log.debug('Failed to chmod %s: %s', tf.name, e)

            # Save the new config.
            self.save_json(self.new_config.root)

            self.working_config = self.new_config

            # Now we're ready to commit all the files. There's no going back now.
            to_replace = written_files

            # Clear this out - if we fail to replace the files with the temporaries, just
            # leave the temporaries for the user to sort out.
            written_files = []

            for path, temppath in to_replace:
                try:
                    os.replace(temppath, path)
                except OSError as e:
                    log.error('Could not apply new content to %s: %s', path, e)
                    log.error('Keeping temporary file %s.', temppath)

            # Have git stat() all the files we've changed so it doesn't automatically
            # assume they have been "modified" just because th
            if update_index_data:
                run_git(['update-index', '-z', '--index-info'], input=''.join(update_index_data))

            log.info('git-smudge configuration updated for %s, %d files changed',
                     self.worktree, change_count)

        finally:
            for path, temppath in written_files:
                try:
                    os.unlink(temppath)
                except FileNotFoundError:
                    pass
                except OSError as e:
                    log.warn('Failed to remove temporary path %s: %s', temppath, e)

    def diff(self, preview=False, current=False, extra_diff_args=()):
        if preview:
            if not self.new_config:
                self.load_new()
            new_config = self.new_config
        else:
            new_config = self.working_config

        with tempfile.TemporaryDirectory(prefix='git_smudge_diff_') as td:
            td = Path(td)
            dir_a = td / 'a'
            dir_b = td / 'b'
            dir_a.mkdir()
            dir_b.mkdir()

            itr = self.walk_files(self.working_config, new_config)
            for fpath, path, entry, orig_content, clean_content, new_content in itr:
                source_content = orig_content if current else clean_content
                if source_content != new_content:
                    for dir, content in [(dir_a, source_content), (dir_b, new_content)]:
                        npath = dir / path
                        npath.parent.mkdir(parents=True, exist_ok=True)
                        npath.write_bytes(content.get_binary())

            diff_args = ['git', 'diff', '--no-index', '--no-prefix']
            diff_args.extend(extra_diff_args)
            diff_args.extend(['--', 'a', 'b'])
            subprocess.run(diff_args, cwd=td)

    def setup(self):
        '''Prepare a git repository. Set up `git config` to define our filter, add an
        entry to `.git/info/attributes, and create an empty '''
        if not self.config_path.exists():
            self.config_path.write_text(CONFIG_TEMPLATE, encoding='ascii')
            print(f'Created template configuration in {self.config_path.absolute()}')
        else:
            print(f'Configuration {self.config_path.absolute()} already exists')

        if not self.working_config_path.exists():
            self.save_json({})

        exe_esc = sys.executable.replace("'", r"'\''")
        cmd = f"'{exe_esc}' -m git_smudge.runfilter"
        run_git(['config', 'filter.git-smudge.process', cmd])

        attributes = git_path('info/attributes')
        try:
            attribute_data = attributes.read_bytes()
        except FileNotFoundError:
            attribute_data = b''

        content = FileContent(attributes, attribute_data)
        text = content.get_text()

        insert = '* filter=git-smudge'
        if insert not in text:
            if text and not text.endswith('\n'):
                text += '\n'

            text += (
                f'# Added by `git-smudge setup`\n'
                f'{insert}\n'
            )
            content.set_text(text)
            attributes.write_bytes(content.get_binary())
            print(f'Inserted {insert!r} into {attributes}')
        print(f'Repository {self.worktree.absolute()} set up for git-smudge')
