import argparse
import datetime
import logging
from kestrel_datasource_stixshifter.diagnosis import Diagnosis
from kestrel_datasource_stixshifter.connector import setup_connector_module
from firepit.timestamp import timefmt


def default_patterns(use_now_as_stop_time: bool):
    start_time = "START t'2000-01-01T00:00:00.000Z'"
    stop_time = (
        f"STOP t'{timefmt(datetime.datetime.utcnow())}'"
        if use_now_as_stop_time
        else "STOP t'3000-01-01T00:00:00.000Z'"
    )
    patterns = [
        "[ipv4-addr:value != '255.255.255.255']",
        "[process:pid > 0]",
        "[email-addr:value != 'null@xyz.com']",
    ]
    return [" ".join([p, start_time, stop_time]) for p in patterns]


def stix_shifter_diag():
    parser = argparse.ArgumentParser(
        description="Kestrel stix-shifter data source interface diagnosis"
    )
    parser.add_argument(
        "datasource", help="data source name specified in stixshifter.yaml"
    )
    parser.add_argument(
        "--ignore-cert",
        help="ignore certificate (PKI) verification in connector verification",
        action="store_false",
    )
    parser.add_argument(
        "-p",
        "--stix-pattern",
        help="STIX pattern in double quotes",
    )
    parser.add_argument(
        "-f",
        "--pattern-file",
        help="write your STIX pattern in a file and put the file path here to use for diagnosis",
    )
    parser.add_argument(
        "--stop-at-now",
        help="use the current timestamp as the STOP time instead of default year 3000 for default patterns",
        action="store_true",
    )
    parser.add_argument(
        "-t",
        "--translate-only",
        help="Only translate pattern; don't transmit",
        action="store_true",
    )
    parser.add_argument(
        "-d", "--debug", help="Enable DEBUG logging", action="store_true"
    )
    args = parser.parse_args()

    if args.debug:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if args.stix_pattern:
        patterns = [args.stix_pattern]
    elif args.pattern_file:
        with open(args.pattern_file) as pf:
            patterns = [pf.read()]
    else:
        patterns = default_patterns(args.stop_at_now)

    diag = Diagnosis(args.datasource)

    # 1. check config manually
    diag.diagnose_config()

    # 2. setup connector and ping
    setup_connector_module(
        diag.connector_name, diag.allow_dev_connector, args.ignore_cert
    )

    # 3. query translation test
    diag.diagnose_translate_query(patterns[0])

    if not args.translate_only:
        # 4. transmit ping test
        diag.diagnose_ping()

        # 5. single-batch query execution test
        diag.diagnose_run_query_and_retrieval_result(patterns, 1)

        # 6. multi-batch query execution test
        diag.diagnose_run_query_and_retrieval_result(patterns, 5)
