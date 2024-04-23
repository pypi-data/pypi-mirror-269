#!/usr/bin/python3
import sys
import re
import os
import argparse
import unittest
import tempfile
import shutil
import subprocess
import logging
from pathlib import Path

import git_smudge
import git_smudge.__main__
from git_smudge import config, filters

log = logging.getLogger(__name__)

def build_clean_text(pre_text, indent, match_part, post_text, **kw):
    return pre_text + indent + match_part + post_text

def build_insert_test_smudge_block_before(pre_text, indent, match_part, post_text, lines, comment, **kw):
    return (
        f'{pre_text}'
        f'{indent}{comment[0]}BEGIN SMUDGE InsertLineFilter.test[0]{comment[1]}\n'
        + ''.join(f'{indent}{line}\n' for line in lines) +
        f'{indent}{comment[0]}END SMUDGE InsertLineFilter.test[0]{comment[1]}\n'
        f'{indent}{match_part}{post_text}'
    )
def build_insert_test_smudge_line_before(pre_text, indent, match_part, post_text, lines, comment, **kw):
    return (
        f'{pre_text}'
        + ''.join(f'{indent}{line} {comment[0]}LINE SMUDGE InsertLineFilter.test[0]{comment[1]}\n' for line in lines) +
        f'{indent}{match_part}{post_text}'
    )

def build_insert_test_smudge_block_after(pre_text, indent, match_part, post_text, lines, comment, **kw):
    return (
        f'{pre_text}{indent}{match_part}'
        f'\n{indent}{comment[0]}BEGIN SMUDGE InsertLineFilter.test[0]{comment[1]}'
        + ''.join(f'\n{indent}{line}' for line in lines) +
        f'\n{indent}{comment[0]}END SMUDGE InsertLineFilter.test[0]{comment[1]}'
        f'{post_text}'
    )
def build_insert_test_smudge_line_after(pre_text, indent, match_part, post_text, lines, comment, **kw):
    return (
        f'{pre_text}{indent}{match_part}'
        + ''.join(f'\n{indent}{line} {comment[0]}LINE SMUDGE InsertLineFilter.test[0]{comment[1]}' for line in lines) +
        f'{post_text}'
    )

def build_comment_out_text(pre_text, indent, match_part, post_text, comment, **kw):
    text = []
    for line in (indent + match_part).split('\n'):
        split_pos = len(indent) if line.startswith(indent) else 0
        text.append(f'{line[:split_pos]}{comment[0]}SMUDGE CommentOutFilter.test[0] [{line[split_pos:]}]{comment[1]}')
    return pre_text + '\n'.join(text) + post_text


TEST_LINES = [
    'insert test line 1',
    '    insert test with leading space',
    'insert test with trailing space ',
]

INSERT_TESTS = []

MATCH_PARTS = [
    ('im_start im_end'),
    ('pre im_start im_end'),
    ('im_start im_end post'),
    ('pre im_start im_end post'),
    ('ml im_start(\n\ttest\n  )im_end post'),
]

for pre_text in ('', 'pre_text\n'):
    for post_text in ('', '\n', '\nextra_text'):
        for indent in ('', '   ', '\t', '\t '):
            for match_part in MATCH_PARTS:
                INSERT_TESTS.append({
                    'pre_text': pre_text,
                    'indent': indent,
                    'match_part': match_part,
                    'post_text': post_text,
                })

TEST_CONTENT_C = '''
void test() {
\tfilter1();

\tprintf("filter2\\n");

\ttest("filter3");
}
'''

TEST_CONTENT_PY = r'''
def root():
    filter1()

    print("filter2")

    test_comment("filter3")
'''

TEST_CONTENT_TXT = r'''
test filter1

test filter2

test filter3
'''

SMUDGE_CONTENT_C_1 = '''
void test() {
\tfilter1();
\t// BEGIN SMUDGE InsertLineFilter.filter1[0]
\txfilt1_1
\txfilt1_2
\t// END SMUDGE InsertLineFilter.filter1[0]

\tprintf("filter2\\n");

\ttest("filter3");
}
'''

SMUDGE_CONTENT_C_2 = '''\
test smudge

void test() {
\tfilter1();

\tprintf("filter2\\n");

\ttest("filter3");
}
'''

SMUDGE_CONTENT_C_3 = '''
void test() {
\tfilter1();
\t// SMUDGE CommentOutFilter.filter2[2] [// BEGIN SMUDGE InsertLineFilter.filter2[1]]
\txfilt1_1
\txfilt1_2
\t// SMUDGE CommentOutFilter.filter2[2] [// END SMUDGE InsertLineFilter.filter2[1]]
\t// BEGIN SMUDGE InsertLineFilter.filter1[0]
\txfilt1_1
\txfilt1_2
\t// END SMUDGE InsertLineFilter.filter1[0]

\t// SMUDGE CommentOutFilter.filter2[2] [printf("filter2\\n");]

\ttest("xfilt3");
}
'''

SMUDGE_CONTENT_C_4 = '''\
test smudge

void test() {
\tfilter1();
\t// SMUDGE CommentOutFilter.filter2[2] [// BEGIN SMUDGE InsertLineFilter.filter2[1]]
\txfilt1_1
\txfilt1_2
\t// SMUDGE CommentOutFilter.filter2[2] [// END SMUDGE InsertLineFilter.filter2[1]]

\t// SMUDGE CommentOutFilter.filter2[2] [printf("filter2\\n");]

\ttest("xfilt3");
}
'''

SMUDGE_CONTENT_C_5 = '''
void test() {
\tfilter1();
\t// BEGIN SMUDGE InsertLineFilter.filter3[1]
\txfilt1_1
\txfilt1_2
\t// END SMUDGE InsertLineFilter.filter3[1]

\tprintf("filter2\\n");

\ttest("xfilt3");
}
'''

SMUDGE_CONTENT_PY_1 = '''
def root():
    filter1()

    print("filter2")

    # BEGIN SMUDGE InsertLineFilter.rootpy[0]
    if True:
        do_stuff()
    # END SMUDGE InsertLineFilter.rootpy[0]
    test_comment("filter3")
'''

SMUDGE_CONTENT_PY_2 = '''
def root():
    filter1()
    # SMUDGE CommentOutFilter.filter2[2] [# BEGIN SMUDGE InsertLineFilter.filter2[1]]
    xfilt1_1
    xfilt1_2
    # SMUDGE CommentOutFilter.filter2[2] [# END SMUDGE InsertLineFilter.filter2[1]]

    # SMUDGE CommentOutFilter.filter2[2] [print("filter2")]

    test_comment("xfilt3")
'''

CONFIG_TEST_PATHS = [
    ('root.txt', TEST_CONTENT_TXT, TEST_CONTENT_TXT, []),
    ('root.c', TEST_CONTENT_C, SMUDGE_CONTENT_C_1, [
        ('InsertLineFilter', 'after', 'filter1'),
    ]),
    ('foo.c', TEST_CONTENT_C, SMUDGE_CONTENT_C_2, [
        ('TestFilter', 'test', '1234')
    ]),
    ('root.py', TEST_CONTENT_PY, SMUDGE_CONTENT_PY_1, [
        ('InsertLineFilter', 'before', 'test_com')
    ]),
    ('subdir/test.c', TEST_CONTENT_C, SMUDGE_CONTENT_C_3, [
        ('InsertLineFilter', 'after', 'filter1'),
        ('SimpleFilter', 'search', 'filter3'),
        ('InsertLineFilter', 'after', 'filter1'),
        ('CommentOutFilter', 'after', 'filter2'),
    ]),
    ('subdir/foo.c', TEST_CONTENT_C, SMUDGE_CONTENT_C_4, [
        ('SimpleFilter', 'search', 'filter3'),
        ('InsertLineFilter', 'after', 'filter1'),
        ('CommentOutFilter', 'after', 'filter2'),
        ('TestFilter', 'test', '1234')
    ]),
    ('subdir/foo.txt', TEST_CONTENT_TXT, TEST_CONTENT_TXT, []),
    ('subdir/notroot.py', TEST_CONTENT_PY, SMUDGE_CONTENT_PY_2, [
        ('SimpleFilter', 'search', 'filter3'),
        ('InsertLineFilter', 'after', 'filter1'),
        ('CommentOutFilter', 'after', 'filter2'),
    ]),
    ('subdir/special.c', TEST_CONTENT_C, SMUDGE_CONTENT_C_5, [
        ('SimpleFilter', 'search', 'filter3'),
        ('InsertLineFilter', 'after', 'filter1'),
    ]),
    ('subdir2/special.c', TEST_CONTENT_C, SMUDGE_CONTENT_C_5, [
        ('SimpleFilter', 'search', 'filter3'),
        ('InsertLineFilter', 'after', 'filter1'),
    ]),
]

CONFIG_TOML = r'''
plugins = [
    ".git/plugin-test.py"
]

[filters.filter1]
type = "InsertLine"
after = "filter1"
insert = ['xfilt1_1', 'xfilt1_2']
files = ["*.c", "!foo.c" ]

[filters.filter2]
filters = "filter3"
type = "CommentOut"
match = 'filter2'
files = [ "subdir/*", "!*.txt" ]

[filters.filter3]
filters = [
   { type = 'simple', search = 'filter3', replace = 'xfilt3' },
   "filter1"
]

[[rule]]
filters = [ "filter1", "filter2" ]
files = "!special.c"

[[rule]]
filters = "filter3"
files  = "special.c"

[filters.foo]
type = "test"
test = "1234"
files = "foo.c"

[filters.rootpy]
type = "InsertLine"
before = 'test_com'
insert = ['if True:', '    do_stuff()']
files = "/*.py"
'''

PLUGIN_TEST = r'''
import sys
class TestFilter(GitFilter):
    def smudge(self, content):
        content.set_text('test smudge\n' + content.get_text())

    def clean(self, content):
        text = content.get_text()
        needclean = text.startswith('test smudge\n')
        if needclean:
            content.set_text(text[12:])
'''

class BasicTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def do_test_filter(self, filter, kw, path, expect):
        content = git_smudge.FileContent(path, None, False)
        clean = build_clean_text(**kw)
        content.set_text(clean)

        with self.subTest(t=clean, s=expect, p=path, **kw):
            content.smudge([filter])
            self.assertEqual(content.get_text(), expect)

            content.clean([filter])

            # First make sure that it actually changed the text
            self.assertNotEqual(content.get_text(), expect)
            self.assertEqual(content.get_text(), clean)

    def do_test_inserts(self, comment_style, path, comments, block, after):
        kw = {
            'smudge_check_clean': False,
            'insert': '\n'.join(TEST_LINES),
            'comment_style': comment_style,
            'block': block
        }
        kw['after' if after else 'before'] = r'(?s)im_start.*im_end'

        filter = filters.InsertLineFilter(kw, 'test', 0)
        filter.update_config()
        if after:
            f = build_insert_test_smudge_block_after if block else build_insert_test_smudge_line_after
        else:
            f = build_insert_test_smudge_block_before if block else build_insert_test_smudge_line_before
        for kw in INSERT_TESTS:
            smudge_expect = f(**kw, lines=TEST_LINES, comment=comments)
            self.do_test_filter(filter, kw, path, smudge_expect)

    def test_insert_block_c(self):
        self.do_test_inserts('css', Path('test.xxx'), git_smudge.COMMENT_C, True, True)

    def test_insert_block_sql(self):
        self.do_test_inserts('auto', Path('test.sql'), git_smudge.COMMENT_DDASH, True, True)

    def test_insert_line_xml(self):
        self.do_test_inserts('auto', Path('test.xml'), git_smudge.COMMENT_SGML, False, True)

    def test_insert_line_cpp(self):
        self.do_test_inserts('auto', Path('test.cpp'), git_smudge.COMMENT_DSLASH, False, True)

    def test_insert_block_c_before(self):
        self.do_test_inserts('css', Path('test.xxx'), git_smudge.COMMENT_C, True, False)

    def test_insert_line_sql_before(self):
        self.do_test_inserts('sql', Path('test.sql'), git_smudge.COMMENT_DDASH, False, False)

    def test_comment_out(self):
        filter = filters.CommentOutFilter({
            'match': '(?s)im_start.*im_end'
        }, 'test', 0)
        filter.update_config()
        comment_styles = [
            ('test.py', git_smudge.COMMENT_HASH),
            ('test.xml', git_smudge.COMMENT_SGML),
            ('test.css', git_smudge.COMMENT_C),
        ]
        for i, kw in enumerate(INSERT_TESTS):
            fname, comments = comment_styles[i % len(comment_styles)]
            commented = build_comment_out_text(comment=comments, **kw)
            self.do_test_filter(filter, kw, Path(fname), commented)

    def test_check(self):
        filter = filters.SimpleFilter({'search': 'search_text', 'replace': 'replace_text'})
        filter.update_config()

        content = git_smudge.FileContent(Path('test.txt'), None, False)

        content.set_text('some x_text data')
        log.debug('check filter: %r', content.text_data)
        content.changed = False
        content.smudge([filter])
        filter.smudge(content)
        self.assertEqual(content.get_text(), 'some x_text data')
        self.assertEqual(content.changed, False)

        content.set_text('some search_text data')
        log.debug('check filter: %r', content.text_data)
        content.changed = False
        content.smudge([filter])
        self.assertEqual(content.get_text(), 'some replace_text data')
        self.assertEqual(content.changed, True)

        expect_error = re.compile(
            r"test\.txt: applying filter .* results in text that does not restore properly")

        content.set_text('some replace_text data')
        log.debug('check filter: %r', content.text_data)
        content.changed = False
        with self.assertLogs('filters', 'WARN') as cm:
            content.smudge([filter])
        self.assertRegex(cm.output[0], expect_error)

        self.assertEqual(content.get_text(), 'some replace_text data')
        self.assertEqual(content.changed, False)


        content.set_text('some replace_text data search_text')
        log.debug('check filter: %r', content.text_data)
        content.changed = False
        with self.assertLogs('filters', 'WARN') as cm:
            content.smudge([filter])
        self.assertRegex(cm.output[0], expect_error)

        self.assertEqual(content.get_text(), 'some replace_text data search_text')
        self.assertEqual(content.changed, False)


    def get_filters_for_args(self, argv):
        p = argparse.ArgumentParser(description='')
        git_smudge.__main__.add_arguments_for_main(p)
        args = p.parse_args(argv)
        for filter in args.filters:
            filter.update_config()

        return args.filters

class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = Path(tempfile.mkdtemp(prefix='git_smudge_unittest'))
        self.gitdir = self.tempdir / 'gitdir'
        self.gitdir.mkdir()

        self.config_path = self.gitdir / 'git-smudge.toml'
        self.config_path.write_text(CONFIG_TOML, encoding='ascii')

        (self.gitdir / 'plugin-test.py').write_text(PLUGIN_TEST)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_config_1(self):
        cfg = config.Config(self.tempdir, self.gitdir)
        self.assertEqual(self.config_path, cfg.config_path)

        cfg.load()
        cfg.load_new()
        filter_conf = cfg.new_config

        self.assertSetEqual(set(filter_conf.filter_classes), {
            'test', 'simple', 'insertline', 'commentout'
        })

        nf = filter_conf.named_filters
        self.assertSetEqual(set(nf), {'filter1', 'filter2', 'filter3', 'foo', 'rootpy'})

        filter_list = nf['filter1']
        self.assertEqual(len(filter_list), 1)
        self.assertIsInstance(filter_list[0], filters.InsertLineFilter)

        filter_list = nf['filter2']
        self.assertEqual(len(filter_list), 3)
        self.assertIsInstance(filter_list[0], filters.SimpleFilter)
        self.assertIsInstance(filter_list[1], filters.InsertLineFilter)
        self.assertIsInstance(filter_list[2], filters.CommentOutFilter)

        filter_list = nf['filter3']
        self.assertEqual(len(filter_list), 2)
        self.assertIsInstance(filter_list[0], filters.SimpleFilter)
        self.assertIsInstance(filter_list[1], filters.InsertLineFilter)

        pats = filter_conf.patterns
        self.assertSetEqual(set(pat[:2] for pat in pats), {
            ('*', '*.c'), ('*', 'foo.c'), ('subdir', '*'), ('*', '*.txt'),
            ('*', 'special.c'), ('', '*.py')
        })

        for path, clean_content, smudge_content, expect_filters in CONFIG_TEST_PATHS:
            with self.subTest(path=path):
                filter_list = filter_conf.get_filters_for_path(path)
                self.assertEqual([type(f).__name__ for f in filter_list], [f[0] for f in expect_filters])

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = Path(tempfile.mkdtemp(prefix='git_smudge_unittest'))
        self.gitdir = self.tempdir / '.git'

        # Make sure that running python -m git_smudge is actually testing the code where
        # we are located.
        self.env = dict(os.environ)
        self.env['PYTHONPATH'] = str(Path(__file__).absolute().parent.parent)
        #self.env['GIT_SMUDGE_DEBUG'] = '1'

        # This will exit with 0 if importing git_smudge.tests imports this file
        p = subprocess.run([
            sys.executable, '-c',
            'import sys;'
            'from git_smudge import tests;'
            'sys.exit(0 if tests.__file__ == sys.argv[1] else 1)',
            __file__
        ], env=self.env, cwd=self.tempdir, check=False)
        if p.returncode != 0:
            self.skipTest(
                "Importing git_smudge.tests from temporary directory "
                "imports a different module")

        try:
            self.run_git(['init'])
        except (OSError, subprocess.CalledProcessError):
            # If we can't run `git`, skip this test
            self.skipTest("Cannot run `git`")

        self.config_path = self.gitdir / 'git-smudge.toml'

        (self.gitdir / 'plugin-test.py').write_text(PLUGIN_TEST)
        for path, clean_content, smudge_content, expect_filters in CONFIG_TEST_PATHS:
            fpath = self.tempdir / path
            fpath.parent.mkdir(parents=True, exist_ok=True)
            fpath.write_text(clean_content)

        self.run_git(['add', '.'])
        self.run_git(['commit', '-m', 'Initial commit'])

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def run_smudge(self, args, **kw):
        cmd = [sys.executable, '-m', 'git_smudge'] + args
        return subprocess.run(
            cmd, env=self.env, cwd=self.tempdir,
            encoding='utf8',
            stdout=subprocess.PIPE, **kw)

    def run_git(self, args, **kw):
        return config.run_git(args, cwd=self.tempdir, env=self.env)

    def run_apply(self, cmd, expect_changed):
        p = self.run_smudge([cmd], stderr=subprocess.PIPE)
        self.assertRegex(p.stderr, f'{expect_changed} files changed')
        self.assertNotRegex(p.stderr, 'text that does not restore properly')

        p = self.run_git(['status', '--porcelain', '-uall'])
        self.assertEqual(p.stdout, '', "git status should indicate no changed files")

        p = self.run_git(['diff'])
        self.assertEqual(p.stdout, '', "git diff should indicate no changed files")

        for path, clean_content, smudge_content, expect_filters in CONFIG_TEST_PATHS:
            with self.subTest(cmd=cmd, path=path):
                fpath = self.tempdir / path
                content = fpath.read_text(encoding='utf8')
                if cmd == 'clean':
                    self.assertEqual(
                        content, clean_content,
                        "content should match clean content")
                else:
                    self.assertEqual(
                        content, smudge_content,
                        "content should match smudged content")


    def test_git(self):
        p = self.run_smudge(['setup'])
        self.assertRegex(p.stdout, 'set up for git-smudge')

        self.config_path.write_text(CONFIG_TOML, encoding='ascii')

        p = self.run_git(['status', '--porcelain', '-uall'])
        self.assertEqual(p.stdout, '', "git status should indicate no changed files")

        p = self.run_smudge(['diff'])
        self.assertEqual(p.stdout, '', "git smudge diff should show no differences")

        p = self.run_smudge(['diff', '--preview'])
        self.assertNotEqual(p.stdout, '', "git smudge diff --preview should show differences")

        self.run_apply('apply', 8)

        p = self.run_smudge(['diff'])
        self.assertNotEqual(p.stdout, '', "git smudge diff should show differences")

        # Make sure that running `apply` again doesn't change files
        self.run_apply('apply', 0)

        self.run_apply('clean', 8)

        self.run_apply('clean', 0)

if __name__ == '__main__':
    git_smudge.__main__.setup_logging(False)
    unittest.main()
