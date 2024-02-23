# sidefx-lic-exporter

Export license usage for SideFX license server to Prometheus.

## Requirements

To run this exporter, you need to provide the binaries `hserver` and `sesictrl`.
They are part of the houdini install on Linux, and you can retrieve them from
their respective destination paths after installing houdini :

- `/opt/hfs<version>/bin/hserver`
- `/opt/hfs<version>/houdini/sbin/sesictrl`

The version of houdini (which translates 1:1 with the version of these binaries)
should be above the version of your license server. At the time of writing, the
exporter has been tested with versions 19.5 and 20.

## Usage

### Quick start from source

Here is a quick way to test the application from source, it requires a docker
engine with the docker compose plugin, and gnu make :

- Retrieve the `hserver` and `sesictrl` binaries from a Houdini install on
    Linux, and store them both in a directory named `./hfs-bin`.
- Copy the `./example/config.yml` file to the root of the repository and adjust
    the `license_server_hostname` entry to match your license server.
- Start a dev build with the command `make run`.
- The exporter should be running on your host, on the port `9102`.

### Command line parameters

```
usage: sidefx-lic-exporter [-h] [--config CONFIG] [-l LOG_LEVEL] [-p PORT]

options:
  -h, --help            show this help message and exit
  --config CONFIG       path to config file
                        Default : /etc/sidefx-lic-exporter/config.yml
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                        Default : INFO
  -p PORT, --port PORT  port to run the exporter on
                        Default : 9102
```

### Configuration file

A YAML configuration file is expected, with the following parameters :

```yaml
---
# The interval at which the license data will be scrapped from the license
# server
scrape_interval: 15
# The path to the two required binaries
hserver_path: "/usr/local/bin/hserver"
sesictrl_path: "/usr/local/bin/sesictrl"
# The hostname, or IP address of your sidefx license server you want to scrape
# license data from
license_server_hostname: "sidefx-licserv.example.com"
```
