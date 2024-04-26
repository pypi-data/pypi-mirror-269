import sys
import subprocess
from git_smudge import ConfigDispatchFilter
from git_smudge.config import Config
from git_smudge.__main__ import setup_logging

def main():
    # HACK: On windows, git runs our filter process through 'sh.exe'. However since
    # 'sh.exe' can't just exec us, it has to stick around and wait for us to exit.
    # This is a problem, because it also holds a handle to the console, causing windows
    # to try to send all user input to 'sh' instead of 'git'. This means that running
    # 'git add -p' can hang while the filter is running.
    #
    # To work around this, we launch a separate process with a flag to actually run the
    # filter, then immediately exit so that 'sh.exe' exits. Git doesn't care if the
    # process that it launched exits as long as the pipe is still open.

    args = sys.argv[1:]
    if args and args[0] == '--run':
        del args[0]
    elif sys.platform == 'win32':
        subprocess.Popen(
            [sys.executable, '-m', 'git_smudge.runfilter', '--run'] + args)
        return

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
