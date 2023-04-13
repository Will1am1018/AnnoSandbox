#!/usr/bin/env python
# coding=utf-8



import argparse
import logging
import os
import sys
import traceback

try:
    from lib.anno sandbox.common.constants import anno sandbox_VERSION, anno sandbox_ROOT
    from lib.anno sandbox.common.exceptions import anno sandboxCriticalError
    from lib.anno sandbox.common.exceptions import anno sandboxDependencyError
    from lib.anno sandbox.common.logo import logo
    from lib.anno sandbox.common.utils import exception_message
    from lib.anno sandbox.core.resultserver import ResultServer
    from lib.anno sandbox.core.scheduler import Scheduler
    from lib.anno sandbox.core.startup import check_working_directory, check_configs
    from lib.anno sandbox.core.startup import check_version, create_structure
    from lib.anno sandbox.core.startup import anno sandbox_clean, drop_privileges
    from lib.anno sandbox.core.startup import init_logging, init_modules
    from lib.anno sandbox.core.startup import init_tasks, init_yara, init_binaries
    from lib.anno sandbox.core.startup import init_rooter, init_routing
    from modules.processing.anno sandboxml import init_anno sandboxml

    import bson

    bson  # Pretend like it's actually being used (for static checkers.)
except (anno sandboxDependencyError, ImportError) as e:
    sys.exit("ERROR: Missing dependency: {0}".format(e))

log = logging.getLogger()

def anno sandbox_init(quiet=False, debug=False, artwork=False, test=False, ml=False):
    """anno sandbox initialization workflow.

    :param quiet: if set enable silent mode, it doesn't print anything except warnings
    :param debug: if set enable debug mode, it print all debug messages
    :param artwork: if set it will print only artworks, forever
    :param test: enable integration test mode, used only for testing
    :param ml: do anno sandboxML analysis of locally stored samples
    """
    cur_path = os.getcwd()
    os.chdir(anno sandbox_ROOT)

    logo()
    check_working_directory()
    check_configs()
    check_version()
    create_structure()

    if artwork:
        import time
        try:
            while True:
                time.sleep(1)
                logo()
        except KeyboardInterrupt:
            return

    init_logging()

    if quiet:
        log.setLevel(logging.WARN)
    elif debug:
        log.setLevel(logging.DEBUG)

    if ml:
        init_anno sandboxml()
        return
    # Todo: init_detection()
    init_modules()
    init_tasks()
    init_yara()
    init_binaries()
    init_rooter()
    init_routing()

    # TODO: This is just a temporary hack, we need an actual test suite to
    # integrate with Travis-CI.
    if test:
        return
    # 启动结果监听器
    ResultServer()

    os.chdir(cur_path)

def anno sandbox_main(max_analysis_count=0):
    """anno sandbox main loop.

    :param max_analysis_count: kill anno sandbox after this number of analyses
    """
    cur_path = os.getcwd()
    os.chdir(anno sandbox_ROOT)

    try:
        sched = Scheduler(max_analysis_count)
        sched.start()
    except KeyboardInterrupt:
        sched.stop()

    os.chdir(cur_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--quiet", help="Display only error messages", action="store_true", required=False)
    parser.add_argument("-d", "--debug", help="Display debug messages", action="store_true", required=False)
    parser.add_argument("-v", "--version", action="version", version="You are running anno sandbox Sandbox {0}".format(anno sandbox_VERSION))
    parser.add_argument("-a", "--artwork", help="Show artwork", action="store_true", required=False)
    parser.add_argument("-t", "--test", help="Test startup", action="store_true", required=False)
    parser.add_argument("-m", "--max-analysis-count", help="Maximum number of analyses", type=int, required=False)
    parser.add_argument("-u", "--user", type=str, help="Drop user privileges to this user")
    parser.add_argument("--ml", help="anno sandboxML: cluster reports and compare new samples", action="store_true", required=False)
    parser.add_argument("--clean", help="Remove all tasks and samples and their associated data", action='store_true', required=False)
    args = parser.parse_args()

    if args.user:
        drop_privileges(args.user)

    if args.clean:
        anno sandbox_clean()
        sys.exit(0)

    try:
        anno sandbox_init(quiet=args.quiet, debug=args.debug, artwork=args.artwork,
                    test=args.test, ml=args.ml)
        if not args.artwork and not args.test:
            anno sandbox_main(max_analysis_count=args.max_analysis_count)
    except anno sandboxCriticalError as e:
        message = "{0}: {1}".format(e.__class__.__name__, e)
        if len(log.handlers):
            log.critical(message)
        else:
            sys.stderr.write("{0}\n".format(message))
        sys.exit(1)
    except:
        # Deal with an unhandled exception.
        message = exception_message()
        traceback = traceback.format_exc()
        print message, traceback
