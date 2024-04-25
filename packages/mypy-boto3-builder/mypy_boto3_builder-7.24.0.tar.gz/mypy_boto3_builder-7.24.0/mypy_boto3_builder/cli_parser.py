"""
CLI parser.
"""

import argparse
import logging
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from mypy_boto3_builder.constants import PROG_NAME
from mypy_boto3_builder.enums.product import Product
from mypy_boto3_builder.service_name import ServiceName
from mypy_boto3_builder.utils.version import get_builder_version


def get_absolute_path(path: str) -> Path:
    """
    Get absolute path from a string.

    Arguments:
        path -- String containing path.

    Returns:
        Absolute path.
    """
    return Path(path).absolute()


@dataclass(kw_only=True, slots=True)
class CLINamespace:
    """
    CLI arguments namespace.
    """

    log_level: int
    output_path: Path
    service_names: list[str]
    build_version: str
    installed: bool
    products: list[Product]
    list_services: bool
    partial_overload: bool
    skip_published: bool
    disable_smart_version: bool


def parse_args(args: Sequence[str]) -> CLINamespace:
    """
    Parse CLI arguments.

    Returns:
        Argument parser.
    """
    version = get_builder_version()

    parser = argparse.ArgumentParser(
        PROG_NAME, description="Builder for boto3-stubs and types-aiobotocore."
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Show debug messages")
    parser.add_argument(
        "-b",
        "--build-version",
        help="Set custom output version, otherwise smart versioning is used.",
    )
    parser.add_argument("-V", "--version", action="version", version=version)
    parser.add_argument(
        "--product",
        dest="products",
        type=Product,
        choices=list(Product),
        nargs="+",
        default=[Product.boto3, Product.boto3_services],
        help="Select package to create annotations for",
    )
    parser.add_argument(
        "--skip-published", action="store_true", help="Skip packages that are already on PyPI"
    )
    parser.add_argument(
        "--no-smart-version",
        action="store_true",
        help=(
            "Disable version bump based od last PyPI version. "
            "Set this flag to run packages build in offline mode. "
            "skip-published flag is ignored in this case."
        ),
    )
    parser.add_argument(
        "--panic",
        action="store_true",
        help="Raise exception on logger warning and above",
    )
    parser.add_argument(
        "output_path", metavar="OUTPUT_PATH", help="Output path", type=get_absolute_path
    )
    parser.add_argument(
        "-s",
        "--services",
        dest="service_names",
        nargs="*",
        metavar="NAME",
        help=(
            "List of AWS services, by default all services are used."
            " Use `updated` to build only services updated in the release."
            " Use `all` to build all services."
        ),
        default=[ServiceName.ALL],
    )
    parser.add_argument(
        "--partial-overload",
        action="store_true",
        help="Build boto3-stubs client/service overload only for selected services",
    )
    parser.add_argument(
        "--installed",
        action="store_true",
        help="Generate already installed packages for typings folder.",
    )
    parser.add_argument(
        "--list-services",
        action="store_true",
        help="List supported boto3 service names.",
    )
    result = parser.parse_args(args)

    return CLINamespace(
        log_level=logging.DEBUG if result.debug else logging.INFO,
        output_path=result.output_path,
        service_names=result.service_names,
        products=result.products,
        build_version=result.build_version,
        installed=result.installed,
        list_services=result.list_services,
        partial_overload=result.partial_overload,
        skip_published=result.skip_published,
        disable_smart_version=result.no_smart_version,
    )
