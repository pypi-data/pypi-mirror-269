git-smudge
==========

A powerful filter driver for Git which can automatically apply local changes to the
working tree of a repository.

## Installing

Run

```
$ pip3 install git-smudge
```

If you're using `bash`, run:

```
$ git smudge comp
```

This will set up tab completion for `git smudge`

## Setting up a filter

The first step is to run:

```
$ git smudge setup
```

This will do three things:

* It will create `.git/git-smudge.toml`, and pre-populate it with comments explaining how
  to define filters. For more information on the TOML format, see [the TOML site](https://toml.io/en/v1.0.0).

* It will run `git config filter.git-smudge 'python3 -m git_smudge.runfilter'`. This tells
  `git` how to run our filters.

* It will add `* filter=git-smudge` to `.git/info/attributes` which tells `git` to have
  `git-smudge` handle filtering for all files. Only files which match filters in
  `git-smudge.toml` are actually updated, however.

You can run `git smudge edit` to edit the configuration file, or you can just open it in
your normal editor.

Once you have your configuration set up, run:

```
$ git smudge apply
```

This will read `git-smudge.toml` and apply any filters defined there to the files in your
working tree. If you had already defined filters previously, it will reverse those changes
(using a saved copy of the old configuration). If there are any errors, `git smudge apply`
will try to undo any changes and get back to the previous working state.

If you want to undo all changes, as if a blank configuration were applied, run:

```
$ git smudge clean
```

To see what changes have been applied to files, run:

```
$ git smudge diff
```

If you change the configuration and you want to preview what changes will be applied, run:

```
$ git smudge diff --preview
```


## Plugins

`git smudge` supports defining custom filters by specifying a path to a Python
script. This script should subclass `GitFilter` (which is pre-defined when executing the
script). A class which is named `XYZFilter` would define a filter named `XYZ` or `xyz`
(filter names are case-insensitive).

The filter class has two methods, `clean` and `smudge`. Both methods take a single
parameter, `content`, which is used to manage the content of the file. This object has an
attribute `path`, which is an instance of `pathlib.Path`, and methods `get_text()`,
`set_text()`, `get_binary()`, and `set_binary()`. Most filters will be working with text,
but the data can be converted to and from binary as needed.

When running `git smudge apply`, the contents of the plugin script is saved to the working
configuration so that the exact code can be run to reverse those changes even if the code
changes.
