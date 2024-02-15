#!/usr/bin/env python3

import sys
import time
import json
import yaml
import signal
import logging
import datetime
import argparse
import subprocess
import prometheus_client


logger = logging.getLogger(__name__)


def signal_handler(sig, frame):
    logger.info("Received signal {}. Cleaning up...".format(sig))
    sys.exit(0)


def register_lic_server(hserver_path: str, license_server_hostname: str) -> bool:
    """
    Register a license server with hserver
    """
    command = [hserver_path, "-h", license_server_hostname]
    logger.debug("Running command: {}".format(command))
    process = subprocess.run(command, capture_output=True)
    if process.returncode != 0:
        raise Exception("Failed to register license server with hserver")
    return True


def get_licenses(sesictrl_path: str, license_server_hostname: str) -> dict:
    """
    Get licenses from license server using sesictrl
    The returned dict is in the following format:
    {
        "server_list":"http://server:port",
        "licenses":[
            {
                "id":"12345678", # hex
                "platform":"Generic",
                "product":"Houdini-Master",
                "display":"Houdini FX",
                "version":"20.0",
                "available":0,
                "total_tokens":1,
                "disabled":false,
                "expiry":"dd-mmm-yyyy", # month in 3 letter format (%b)
                "ip_mask":"+.+.*.*,192.168.*.*,10.*.*.*,172.*.*.*",
                "servers":"hostname",
                "resolved_server":"fqdn",
                "license_access_mode":"",
                "start_time":"",
                "users":[
                    {
                        "id":61415,
                        "machine":"username@workstation-fqdn",
                        "time":"YYYY/MM/DD HH:MM:SS"
                    }
                ]
            },
            ...
        ]
    }
    """
    command = [
        sesictrl_path,
        "print-license",
        "--format",
        "json",
        "-h",
        license_server_hostname,
    ]
    logger.debug("Running command: {}".format(command))
    process = subprocess.run(command, capture_output=True)
    if process.returncode != 0:
        raise Exception("Failed to get licenses from sesictrl")
    # We need to strip the first line of the output
    # which is not valid json
    output = process.stdout.decode("utf-8").split("\n")[1:]
    return json.loads("\n".join(output))


def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        help="path to config file",
        default="/etc/sidefx-lic-exporter/config.yml",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        help="the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
        default="INFO",
    )
    parser.add_argument(
        "-p",
        "--port",
        help="port to run the exporter on",
        default=9102,
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    with open(args.config, "r") as fd:
        config = yaml.safe_load(fd)
    logger.debug("Config: {}".format(config))

    logger.info("Registering license server with hserver")
    register_lic_server(config["hserver_path"], config["license_server_hostname"])

    metric_prefix = config.get("metric_prefix", "sidefx")
    metric_tags = [
        "license_id",
        "product",
        "version",
    ]

    metric_licenses_total = prometheus_client.Gauge(
        f"{metric_prefix}_licenses_total",
        "Total license tokens for a particular license id",
        metric_tags,
    )

    metric_licenses_used = prometheus_client.Gauge(
        f"{metric_prefix}_licenses_used",
        "Used license tokens for a particular license id",
        metric_tags,
    )

    metric_licenses_expiry_date = prometheus_client.Gauge(
        f"{metric_prefix}_licenses_expiry_date",
        "Expiry date for a particular license id",
        metric_tags + ["count"],
    )

    prometheus_client.start_http_server(args.port)
    scrape_interval = int(config.get("scrape_interval", 15))
    while True:
        licenses_data = get_licenses(
            config["sesictrl_path"], config["license_server_hostname"]
        )
        for license in licenses_data["licenses"]:
            logger.debug(license)
            metric_licenses_total.labels(
                license_id=license["id"],
                product=license["product"],
                version=license["version"],
            ).set(license["total_tokens"])

            used_licenses = license["total_tokens"] - license["available"]
            metric_licenses_used.labels(
                license_id=license["id"],
                product=license["product"],
                version=license["version"],
            ).set(used_licenses)

            expiry_date = datetime.datetime.strptime(license["expiry"], "%d-%b-%Y")
            metric_licenses_expiry_date.labels(
                license_id=license["id"],
                product=license["product"],
                version=license["version"],
                count=license["total_tokens"],
            ).set(expiry_date.timestamp())
        time.sleep(scrape_interval)


if __name__ == "__main__":
    main()
