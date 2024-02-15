import setuptools
import os
from datetime import datetime
from codecs import open

now = datetime.now()
date_time = now.strftime("%Y.%m.%d.%H.%M.%S")

with open("./README.md", "r", "utf-8") as handle:
    readme = handle.read()


setuptools.setup(
    name="sidefx_lic_exporter",
    version=os.getenv("CI_COMMIT_TAG", date_time),
    author="Arthur Desplanches",
    author_email="arthur.desplanches@forticheprod.com",
    description="Prometheus exporter for SideFX / Houdini licenses",
    long_description=readme,
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    license="LGPL v3",
    classifiers=[],
    install_requires=["prometheus_client", "pyyaml"],
    entry_points={
        "console_scripts": ["sidefx-lic-exporter=sidefx_lic_exporter.main:main"]
    },
)
