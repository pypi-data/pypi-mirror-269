[Version 0.0.17 (2024-04-22)](https://pypi.org/project/git_smudge/0.0.17/)
=============================

* Windows: Run git with CREATE_NO_WINDOW flag ([a4ae838](https://gitlab.com/ktpanda/git_smudge/-/commit/a4ae838475c365e45d02e37c733ff78a5ceb2783))


[Version 0.0.16 (2024-04-12)](https://pypi.org/project/git_smudge/0.0.16/)
=============================

* Use roundtrip_encoding from ktpanda-modules ([9d6820c](https://gitlab.com/ktpanda/git_smudge/-/commit/9d6820c5b832dddf5fee6db5b09ec459a40dab1f))


[Version 0.0.15 (2024-03-29)](https://pypi.org/project/git_smudge/0.0.15/)
=============================

* Add `skip` and `count` parameters to InsertLineFilter ([67c8205](https://gitlab.com/ktpanda/git_smudge/-/commit/67c820579f882a4fedc90c20ecf5fc9e9dc32b31))


[Version 0.0.14 (2022-11-15)](https://pypi.org/project/git_smudge/0.0.14/)
=============================

* Add `--current` option to `git smudge diff` ([2f5f335](https://gitlab.com/ktpanda/git_smudge/-/commit/2f5f33535d7a9dbfb4f2ecc48552a63432a4e508))


[Version 0.0.13 (2022-11-15)](https://pypi.org/project/git_smudge/0.0.13/)
=============================

* Add 'before' option to InsertLineFilter ([7da88db](https://gitlab.com/ktpanda/git_smudge/-/commit/7da88dbcc205610876c79d17734b05f80813fa4f))


[Version 0.0.12 (2022-11-15)](https://pypi.org/project/git_smudge/0.0.12/)
=============================

* Add a bunch of comment styles ([5f00805](https://gitlab.com/ktpanda/git_smudge/-/commit/5f00805af45af6d204d267ee27255a4cf78bb019))


[Version 0.0.11 (2022-11-14)](https://pypi.org/project/git_smudge/0.0.11/)
=============================

* Update documentation ([619c633](https://gitlab.com/ktpanda/git_smudge/-/commit/619c63374372d9ec483107b4809b55b53ebfdee5))
* Add `git smudge diff` command ([cc162fd](https://gitlab.com/ktpanda/git_smudge/-/commit/cc162fde3baed858a80e5a9c8aabd692d8b3a1da))


[Version 0.0.10 (2022-11-14)](https://pypi.org/project/git_smudge/0.0.10/)
=============================

* Add [options] section to configuration ([b68f3ee](https://gitlab.com/ktpanda/git_smudge/-/commit/b68f3eec1618a3df82995e2164c72b8d8887b686))
* Warn when inconsistent line endings are seen ([f240983](https://gitlab.com/ktpanda/git_smudge/-/commit/f240983c690b528f20ae42ee9c36a1fdd75fc55d))


[Version 0.0.9 (2022-11-14)](https://pypi.org/project/git_smudge/0.0.9/)
============================

* Add integration test which creates actual repository ([ece41c7](https://gitlab.com/ktpanda/git_smudge/-/commit/ece41c723be9a7c8fa76fdadf82fe1c4f633e326))
* Add filter name and index to marker text ([7141f06](https://gitlab.com/ktpanda/git_smudge/-/commit/7141f06ff679d2d57d3743e5b8e85c64620202cb))
* Do more preprocessing when loading TOML config ([8e3dabd](https://gitlab.com/ktpanda/git_smudge/-/commit/8e3dabd2eea62f94155cc07b49834151a12f0b0e))
* Run `git update-index` on changed files after running `git smudge clean` or `git smudge apply` ([0ab492c](https://gitlab.com/ktpanda/git_smudge/-/commit/0ab492c91bab730f11f9f1c9c9e3c3beda2983d6))
* Don't warn of changed config unless config file is at least 2 seconds newer than the working config ([ec13858](https://gitlab.com/ktpanda/git_smudge/-/commit/ec13858b0e0c5c04c46a9369d6cd1d5d8d207b8d))
  * This mitigates the issue where it would warn right after doing `git smudge setup`
* Restore behavior of running `clean` on idempotent filters ([308a06a](https://gitlab.com/ktpanda/git_smudge/-/commit/308a06a4132ee7c183cf5740e4ee80caac8f0a2c))


[Version 0.0.8 (2022-11-13)](https://pypi.org/project/git_smudge/0.0.8/)
============================

* Add auto-installation of bash completion scripts ([1fa8b20](https://gitlab.com/ktpanda/git_smudge/-/commit/1fa8b20174a75710f77311e89859403d422cfc38))
* Fix bug with clean and apply not using new checked methods ([8e5c39a](https://gitlab.com/ktpanda/git_smudge/-/commit/8e5c39a198d2eeab9641e205fde3fa9034116a5d))


[Version 0.0.7 (2022-11-13)](https://pypi.org/project/git_smudge/0.0.7/)
============================

* Add check and warning when applying a filter results in text that cannot be restored ([bf204c6](https://gitlab.com/ktpanda/git_smudge/-/commit/bf204c66a62af9a5d97c89a07bab1026069dcf63))
* Move filters to a separate module ([07369ce](https://gitlab.com/ktpanda/git_smudge/-/commit/07369cecbe582a0f645b0c72d05dce49fb346812))


[Version 0.0.6 (2022-11-13)](https://pypi.org/project/git_smudge/0.0.6/)
============================

* New CLI interface and configuration management ([e4e9d5a](https://gitlab.com/ktpanda/git_smudge/-/commit/e4e9d5ab938a6fdfa8f59e397accd574777c54b9))
  * * Keeps a copy of the configuration that is currently applied to the working tree
  * * `git smudge apply` will apply configuration changes to files by undoing
  *   current filters, then applying new ones
  * * `git smudge edit` will open the configuration in the default editor and
  *   will optionally apply the new configuration afterward
  * * Setup command is now `git smudge setup`


[Version 0.0.5 (2022-11-12)](https://pypi.org/project/git_smudge/0.0.5/)
============================

* Add Slime and Jinja comment styles ([1ccc371](https://gitlab.com/ktpanda/git_smudge/-/commit/1ccc371745113f68d746b0cce8df09eb7c1b7b7d))
* Fix bug where configuration was not applied ([329f85b](https://gitlab.com/ktpanda/git_smudge/-/commit/329f85b92e0c3bbdd7a3f8df0fc2962315eb2b21))


[Version 0.0.4 (2022-11-12)](https://pypi.org/project/git_smudge/0.0.4/)
============================

* Add plugins and remove obsolete command-line arguments ([acc72ed](https://gitlab.com/ktpanda/git_smudge/-/commit/acc72eda907b543cd2ff0357f0246bac04ae2f18))
* Switch configuration to TOML and simplify it ([75751f9](https://gitlab.com/ktpanda/git_smudge/-/commit/75751f9a9e8907af14877daf70f157500ad80080))
* Add ability to process files from configuration ([4b68a60](https://gitlab.com/ktpanda/git_smudge/-/commit/4b68a60cbea2373722bb137f53baddd6ccad349a))
* Add `config` module and associated tests ([e97dc1c](https://gitlab.com/ktpanda/git_smudge/-/commit/e97dc1c84c1937e8a25a56a5c49e400e45e1043e))
* Add configuration dict to filters ([be05e17](https://gitlab.com/ktpanda/git_smudge/-/commit/be05e17255ca6987eaca6311b9dc5f09fcc067a5))


[Version 0.0.3 (2022-11-11)](https://pypi.org/project/git_smudge/0.0.3/)
============================

* Add `FileContent` class to manage content and simplify filtering ([e8e329b](https://gitlab.com/ktpanda/git_smudge/-/commit/e8e329b8bd124b3fe011cb309ab350469c960979))


[Version 0.0.2 (2022-11-11)](https://pypi.org/project/git_smudge/0.0.2/)
============================

* Add a bit more documentation and tweak documentation styles ([d4c38aa](https://gitlab.com/ktpanda/git_smudge/-/commit/d4c38aa3b441ef3514eb40a8503fd65acec1c6f2))
* Refactor command line arguments so that --block, --line, and --count apply to last filter ([86eadf7](https://gitlab.com/ktpanda/git_smudge/-/commit/86eadf7b449127740de91020ce1a12472b892986))
* Add a lot more automatic extensions ([0610b83](https://gitlab.com/ktpanda/git_smudge/-/commit/0610b833ecaae7ccdd95f70fde59b67204945d9a))


[Version 0.0.1 (2022-11-11)](https://pypi.org/project/git_smudge/0.0.1/)
============================

* Initial version of code ([9a9a8ba](https://gitlab.com/ktpanda/git_smudge/-/commit/9a9a8ba7038ae10eaf7bc8e77ef5c267400ae050))
