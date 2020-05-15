""" Tests for rendering CLI options and arguments """

from collections import OrderedDict
import pytest
from ubiquerg import build_cli_extra, powerset, VersionInHelpParser, convert_value
import argparse


def pytest_generate_tests(metafunc):
    """ Test case generation and parameterization for this module """
    if "ordwrap" in metafunc.fixturenames:
        metafunc.parametrize("ordwrap", [tuple, OrderedDict])


def build_parser():
    """
    Example argument parser, needed solely for testing purposes.
    This example parser was copied from looper/__init__.py

    :return argparse.ArgumentParser
    """

    banner = "%(prog)s - Loop through samples and submit pipelines."
    additional_description = "For subcommand-specific options, " \
                             "type: '%(prog)s <subcommand> -h'"
    additional_description += "\nhttps://github.com/pepkit/looper"

    parser = VersionInHelpParser(prog="looper", description=banner,
        epilog=additional_description, version=0.1)

    # Logging control
    parser.add_argument("--logfile", dest="logfile",
        help="Optional output file for looper logs (default: %(default)s)")
    parser.add_argument("--verbosity", dest="verbosity", type=int,
        choices=range(4),
        help="Choose level of verbosity (default: %(default)s)")
    parser.add_argument("--logging-level", dest="logging_level",
        help=argparse.SUPPRESS)
    parser.add_argument("--dbg", dest="dbg", action="store_true",
        help="Turn on debug mode (default: %(default)s)")
    parser.add_argument("--env", dest="env", default=None,
        help="Environment variable that points to the DIVCFG file. "
             "(default: DIVCFG)")
    parser.add_argument("--dotfile-template", action="store_true",
                        help="Print out a looper dotfile template and exit")

    # Individual subcommands
    msg_by_cmd = {"run": "Main Looper function: Submit jobs for samples.",
        "rerun": "Resubmit jobs with failed flags.",
        "runp": "Submit jobs for a project.",
        "summarize": "Summarize statistics of project samples.",
        "destroy": "Remove all files of the project.",
        "check": "Checks flag status of current runs.",
        "clean": "Runs clean scripts to remove intermediate "
                 "files of already processed jobs."}

    subparsers = parser.add_subparsers(dest="command")

    def add_subparser(cmd):
        message = msg_by_cmd[cmd]
        return subparsers.add_parser(cmd, description=message, help=message)

    # Run and rerun command
    run_subparser = add_subparser("run")
    rerun_subparser = add_subparser("rerun")
    collate_subparser = add_subparser("runp")
    for subparser in [run_subparser, rerun_subparser, collate_subparser]:
        subparser.add_argument("--ignore-flags", dest="ignore_flags",
            default=False, action="store_true",
            help="Ignore run status flags? Default: False. "
                 "By default, pipelines will not be submitted if a pypiper "
                 "flag file exists marking the run (e.g. as "
                 "'running' or 'failed'). Set this option to ignore flags "
                 "and submit the runs anyway. Default=False")
        subparser.add_argument("-t", "--time-delay", dest="time_delay",
            type=int, default=0,
            help="Time delay in seconds between job submissions.")
        subparser.add_argument("-p", "--package",
            help="Name of computing resource package to use")
        subparser.add_argument("--compute",
            help="Specification of individual computing resource settings; "
                 "separate setting name/key from value with equals sign, "
                 "and separate key-value pairs from each other by comma")
        subparser.add_argument("--limit", dest="limit", default=None,
            type=int, help="Limit to n samples.")
        subparser.add_argument("-a", "--pipeline-args",
            dest="pipeline_args", default="",
            help="arguments to pass to a pipline")
        subparser.add_argument("-s", "--settings", dest="settings",
            default="",
            help="path to a YAML-formatted settings file used to populate "
                 "the command template")
    for subparser in [run_subparser, rerun_subparser]:
        # Note that defaults for otherwise numeric lump parameters are
        # set to
        # null by default so that the logic that parses their values may
        # distinguish between explicit 0 and lack of specification.
        subparser.add_argument("--lump", default=None,
            type=float,
            help="Maximum total input file size for a lump/batch of "
                 "commands in a single job (in GB)")
        subparser.add_argument("--lumpn", default=None,
            type=int,
            help="Number of individual scripts grouped into "
                 "single submission")

    # Other commands
    summarize_subparser = add_subparser("summarize")
    destroy_subparser = add_subparser("destroy")
    check_subparser = add_subparser("check")
    clean_subparser = add_subparser("clean")

    check_subparser.add_argument("-A", "--all-folders",
        action="store_true", default=False,
        help="Check status for all project's output folders, not just "
             "those for samples specified in the config file used. "
             "Default=False")

    for subparser in [destroy_subparser, clean_subparser]:
        subparser.add_argument("--force-yes", action="store_true",
            default=False,
            help="Provide upfront confirmation of destruction intent, "
                 "to skip console query.  Default=False")

    # Common arguments
    for subparser in [run_subparser, rerun_subparser, summarize_subparser,
                      destroy_subparser, check_subparser, clean_subparser,
                      collate_subparser]:
        subparser.add_argument("config_file", nargs="?",
                               help="Project configuration file (YAML).")
        # subparser.add_argument(
        #         "-c", "--config", required=False, default=None,
        #         dest="looper_config", help="Looper configuration file (
        #         YAML).")
        subparser.add_argument("--pipeline-interfaces", dest="pifaces",
            nargs="+", action='append',
            help="Path to a pipeline interface file")
        subparser.add_argument("--file-checks", dest="file_checks",
            action="store_true",
            help="Perform input file checks. Default=True.")
        subparser.add_argument("-d", "--dry-run", dest="dry_run",
            action="store_true",
            help="Don't actually submit the jobs.  Default=False")

        fetch_samples_group = subparser.add_argument_group("select samples",
            "This group of arguments lets you specify samples to use by "
            "exclusion OR inclusion of the samples attribute values.")
        fetch_samples_group.add_argument("--selector-attribute",
            dest="selector_attribute", default="toggle",
            help="Specify the attribute for samples exclusion OR inclusion")
        protocols = fetch_samples_group.add_mutually_exclusive_group()
        protocols.add_argument("--selector-exclude", nargs='*',
            dest="selector_exclude",
            help="Operate only on samples that either lack this attribute "
                 "value or for which this value is not in this collection.")
        protocols.add_argument("--selector-include", nargs='*',
            dest="selector_include",
            help="Operate only on samples associated with these attribute "
                 "values; if not provided, all samples are used.")
        subparser.add_argument("--amendments", dest="amendments", nargs="+",
            help="Name of amendment(s) to use, as designated in the "
                 "project's configuration file")

    return parser, msg_by_cmd


@pytest.mark.parametrize(["optargs", "expected"], [
    ([("-X", None), ("--revert", 1), ("-O", "outfile"),
      ("--execute-locally", None), ("-I", ["file1", "file2"])],
     "-X --revert 1 -O outfile --execute-locally -I file1 file2")
])
def test_build_cli_extra(optargs, expected, ordwrap):
    """ Check that CLI optargs are rendered as expected. """
    observed = build_cli_extra(ordwrap(optargs))
    print("expected: {}".format(expected))
    print("observed: {}".format(observed))
    assert expected == observed


@pytest.mark.parametrize(
    "optargs", powerset([(None, "a"), (1, "one")], nonempty=True))
def test_illegal_cli_extra_input_is_exceptional(optargs, ordwrap):
    """ Non-string keys are illegal and cause a TypeError. """
    with pytest.raises(TypeError):
        build_cli_extra(ordwrap(optargs))


def test_dests_by_subparser_return_type():
    """ Check if the return type is dict of lists keyed by subcommand name """
    parser, msgs_by_cmd = build_parser()
    assert isinstance(parser.dests_by_subparser(), dict)
    assert all([isinstance(v, list)
                for k, v in parser.dests_by_subparser().items()])
    assert all([k in parser.dests_by_subparser()
                for k in list(msgs_by_cmd.keys())])

@pytest.mark.parametrize("subcmd",
                         list(build_parser()[0].dests_by_subparser().keys()))
def test_dests_by_subparser_specific_subcmd(subcmd):
    """
    Should return only specified section of the
    return if subparser specified
    """
    parser, _ = build_parser()
    assert isinstance(parser.dests_by_subparser(subcmd), dict)
    assert subcmd in parser.dests_by_subparser(subcmd).keys()
    assert isinstance(parser.dests_by_subparser(subcmd)[subcmd], list)


def test_dests_by_subparser_toplevel_actions():
    """
    Should return only top level dests, which is a list
    """
    parser, _ = build_parser()
    tld = parser.dests_by_subparser(top_level=True)
    assert isinstance(tld, list)
    assert len(tld) == 6


def test_arg_defaults_return_type():
    """ Check if the return type is dict of dicts keyed by subcommand name """
    parser, msgs_by_cmd = build_parser()
    assert isinstance(parser.arg_defaults(), dict)
    assert all([isinstance(v, dict)
                for k, v in parser.arg_defaults().items()])
    assert all([k in parser.arg_defaults()
                for k in list(msgs_by_cmd.keys())])


@pytest.mark.parametrize("subcmd",
                         list(build_parser()[0].dests_by_subparser().keys()))
def test_arg_defaults_specific_subcmd(subcmd):
    """
    Should return only specified section of the
    return if subparser specified
    """
    parser, _ = build_parser()
    assert isinstance(parser.arg_defaults(subcmd), dict)
    assert subcmd in parser.arg_defaults(subcmd).keys()
    assert isinstance(parser.arg_defaults(subcmd)[subcmd], dict)


def test_arg_defaults_toplevel_actions():
    """
    Should return only top level defaults, which is a dict
    """
    parser, _ = build_parser()
    tld = parser.arg_defaults(top_level=True)
    assert isinstance(tld, dict)
    assert len(tld) == 6


def test_arg_defaults_unqiue():
    """
    Should return only dict of unique kv pairs, not keyed by subcommands
    """
    parser, _ = build_parser()
    tld = parser.arg_defaults(unique=True)
    assert isinstance(tld, dict)
    assert len(tld) == 17
    assert len(set(tld.keys())) == len(tld.keys())


@pytest.mark.parametrize(["input", "output"],
                         [(None, None), ("None", None), ("1", 1), ("0.1", 0.1),
                          ("True", True), ("False", False)])
def test_value_conversion(input, output):
    assert convert_value(input) == output
