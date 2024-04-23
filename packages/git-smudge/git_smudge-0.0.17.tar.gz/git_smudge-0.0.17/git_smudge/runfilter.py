from git_smudge import ConfigDispatchFilter
from git_smudge.config import Config
from git_smudge.__main__ import setup_logging

def main():
    setup_logging(False)
    cfg = Config.from_git()
    cfg.load()
    cfg.warn_config_newer()
    filter = ConfigDispatchFilter(cfg)
    try:
        filter.run_process()
    except EOFError:
        pass

if __name__ == '__main__':
    main()
