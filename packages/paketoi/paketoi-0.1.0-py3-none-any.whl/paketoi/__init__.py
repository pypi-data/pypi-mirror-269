import importlib.resources
import itertools
import shutil
from argparse import ArgumentError, ArgumentTypeError
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator, Literal

import click
import pex.cli
import pex.result
from pex.cli.pex import Pex3
from pex.commands.command import GlobalConfigurationError
from repro_zipfile import ReproducibleZipFile


@dataclass
class ArchiveEntry:
    path: Path
    archive_name: Path


DEFAULT_EXCLUDES = [".git", ".jj", ".mypy_cache", ".ruff_cache"]


def pex3(args: list[str]) -> str | int:
    pex3 = Pex3(command_types=pex.cli.commands.all_commands())
    try:
        with pex3.parsed_command(args=args) as command:
            result: pex.result.Result = pex.result.catch(command.run)
            result.maybe_display()
            return result.exit_code  # type: ignore[no-any-return]
    except (ArgumentError, ArgumentTypeError, GlobalConfigurationError) as e:
        return str(e)


def is_excluded(path: Path, excludes: list[Path]) -> bool:
    return any(path.is_relative_to(exclude) for exclude in excludes)


def scan_tree(root: Path, excludes: list[Path] = []) -> Iterator[ArchiveEntry]:
    for base, dirs, files in root.walk():
        for file in files:
            file_path = base / file
            if not is_excluded(file_path, excludes):
                archive_name = file_path.relative_to(root)
                yield ArchiveEntry(path=file_path, archive_name=archive_name)

        for dir in dirs:
            if is_excluded(base / dir, excludes):
                dirs.remove(dir)


@click.command(help="Build AWS Lambda deployment packages (zip files) for Python projects.")
@click.option(
    "-s",
    "--source",
    default=".",
    help="The source root of the project.",
    type=click.Path(file_okay=False, path_type=Path),
)
@click.option(
    "-I",
    "--include",
    default=["."],
    help="Files to be included, relative to the source root.",
    multiple=True,
    type=click.Path(path_type=Path),
)
@click.option("-E", "--exclude", help="Files to be excluded, relative to the source root.", multiple=True)
@click.option("-r", "--requirement", help="Path to requirements.txt.", multiple=True)
@click.option(
    "--runtime",
    help="Python version to target.",
    type=click.Choice(["3.8", "3.9", "3.10", "3.11", "3.12"]),
    default="3.12",
)
@click.option("--platform", help="Architecture to target.", type=click.Choice(["x86_64", "arm64"]), default="x86_64")
@click.option(
    "--default-excludes/--no-default-excludes",
    help=f"Enable/disable the default exclusion list. ({', '.join(DEFAULT_EXCLUDES)})",
    default=True,
)
@click.argument("output", type=click.Path(writable=True, dir_okay=False))
def build(
    source: Path,
    output: Path,
    include: list[Path],
    exclude: list[str],
    requirement: str,
    default_excludes: bool,
    runtime: Literal["3.11", "3.12"],
    platform: Literal["x86_64", "arm64"],
) -> None:
    excludes = list(Path(x) for x in exclude) + [output]
    if default_excludes:
        excludes += [Path(x) for x in DEFAULT_EXCLUDES]

    with TemporaryDirectory() as tmpdir:
        venv_dir = Path(tmpdir, "lambda")
        output_file = Path(tmpdir, "lambda.zip")

        archive_entries: list[ArchiveEntry] = []

        complete_platform = (
            importlib.resources.files(__name__) / "resources" / f"cp-python{runtime}-{platform}.json"
        ).read_text()

        if requirement:
            pex3(
                [
                    "venv",
                    "create",
                    "--dest-dir",
                    str(venv_dir),
                    "--layout",
                    "flat",
                    "--complete-platform",
                    complete_platform,
                    *itertools.chain(*(["-r", r] for r in requirement)),
                ]
            )
            archive_entries.extend(scan_tree(venv_dir))

        for root in include:
            archive_entries.extend(scan_tree(source / root, excludes))

        with ReproducibleZipFile(output_file, "w") as zip:
            for entry in sorted(archive_entries, key=lambda x: x.archive_name):
                zip.write(entry.path, entry.archive_name)

        shutil.move(str(output_file), str(output))


if __name__ == "__main__":
    build()
