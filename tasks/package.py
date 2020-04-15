# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# ISC License <https://opensource.org/licenses/isc>

import re
import shutil

import invoke
import parver

from .utils import report, get_previous_version


@invoke.task
def test(ctx, verbose=False):
    """ Run package tests.
    """

    test_command = "pytest"
    report.info(ctx, "package.test", "running package tests")
    if verbose:
        test_command += " --verbose"
    ctx.run(test_command)


@invoke.task
def clean(ctx):
    """ Clean previously built package artifacts.
    """

    clean_command = "python setup.py clean"
    report.info(ctx, "package.clean", "cleaning up built package artifacts")
    ctx.run(clean_command)

    egg_name = f"{ctx.metadata['package_name']}.egg-info"
    report.info(ctx, "pacakge.clean", "removing build directories")
    for artifact in ("dist", "build", egg_name, f"src/{egg_name}"):
        artifact_dir = ctx.directory / artifact
        if artifact_dir.is_dir():
            report.debug(ctx, "package.clean", f"removing directory {artifact_dir!s}")
            ctx.run(f"rm -rf {artifact_dir!s}")


@invoke.task
def format(ctx):
    """ Auto format package source files.
    """

    isort_command = f"isort -rc {ctx.package.directory!s}"
    black_command = f"black {ctx.package.directory.parent!s}"

    report.info(ctx, "package.format", "sorting imports")
    ctx.run(isort_command)
    report.info(ctx, "package.format", "formatting code")
    ctx.run(black_command)


@invoke.task()
def requirements(ctx):
    """ Generate requirements.txt from Pipfile.lock.
    """

    report.info(
        ctx, "package.requirements", "generating requirements.txt from Pipfile.lock"
    )
    ctx.run("pipenv lock --requirements > requirements.txt")


@invoke.task(pre=[clean, format])
def build(ctx):
    """ Build pacakge source files.
    """

    build_command = "python setup.py sdist bdist_wheel"
    report.info(ctx, "package.build", "building package")
    ctx.run(build_command)


@invoke.task(pre=[build])
def check(ctx):
    """ Check built package is valid.
    """

    check_command = f"twine check {ctx.directory!s}/dist/*"
    report.info(ctx, "package.check", "checking package")
    ctx.run(check_command)


@invoke.task
def licenses(
    ctx,
    summary=False,
    from_classifier=False,
    with_system=False,
    with_authors=False,
    with_urls=False,
):
    """ List dependency licenses.
    """

    licenses_command = "pip-licenses --order=license"
    report.info(ctx, "package.licenses", "listing licenses of package dependencies")
    if summary:
        report.debug(ctx, "package.licenses", "summarizing licenses")
        licenses_command += " --summary"
    if from_classifier:
        report.debug(ctx, "package.licenses", "reporting from classifiers")
        licenses_command += " --from-classifier"
    if with_system:
        report.debug(ctx, "package.licenses", "including system packages")
        licenses_command += " --with-system"
    if with_authors:
        report.debug(ctx, "package.licenses", "including package authors")
        licenses_command += " --with-authors"
    if with_urls:
        report.debug(ctx, "package.licenses", "including package urls")
        licenses_command += " --with-urls"
    ctx.run(licenses_command)


@invoke.task
def version(ctx, identifier="patch", version=None, force=False):
    """ Specify a new version for the package.

    .. important:: The identifier property can be one of the following strings:

        - major
        - minor
        - patch

        Which will subsequently bump the indicated semver version index. If no version
        is specified, this task will bump the patch number from the most recent git tag.

    :param str identifier: The semver identifier to bump the new version with
    :param str version: The new version of the package.
    :param bool force: If True, skips version check
    """

    valid_semver_identifiers = ["major", "minor", "patch"]
    semver_identifier = (
        identifier.strip().lower()
        if isinstance(identifier, str)
        else valid_semver_identifiers[-1]
    )

    # define replacement strategies for files where the version needs to be in sync
    updates = {
        ctx.directory.joinpath("setup.cfg"): [
            (r"^(version\s?=\s?)(.*)", "\\g<1>{version}")
        ],
        ctx.package.directory.joinpath("__version__.py"): [
            (r"(__version__\s?=\s?)(.*)", '\\g<1>"{version}"')
        ],
    }

    previous_version = get_previous_version(ctx)
    if isinstance(version, str):
        version = parver.Version.parse(version)
        if not force and version <= previous_version:
            error_message = (
                f"version {version!s} is <= to previous version {previous_version!s}"
            )
            report.error(ctx, "package.version", error_message)
            raise ValueError(error_message)
    else:
        release_index = len(previous_version.release) - 1
        if semver_identifier in valid_semver_identifiers:
            release_index = valid_semver_identifiers.index(semver_identifier)
        version = previous_version.bump_release(index=release_index)

    report.info(
        ctx,
        "package.version",
        f"updating version from {previous_version!s} to {version!s}",
    )
    for (path, replacements) in updates.items():
        if path.is_file():
            content = path.read_text()
            for (pattern, sub) in replacements:
                report.debug(
                    ctx,
                    "package.version",
                    f"applying replacement ({pattern!r}, {sub!r}) to {path!s}",
                )
                content = re.sub(
                    pattern, sub.format(version=version), content, flags=re.M
                )
            path.write_text(content)


@invoke.task
def stub(ctx):
    """ Generate typing stubs for the package.
    """

    report.info(ctx, "package.stub", f"generating typing stubs for package")
    ctx.run(
        f"stubgen --include-private --no-import "
        f"--output {ctx.directory.joinpath('stubs')!s} "
        f"--search-path {ctx.directory.joinpath('src')!s} "
        f"--package {ctx.metadata['package_name']}"
    )


@invoke.task(pre=[stub])
def typecheck(ctx):
    """ Run type checking with generated package stubs.
    """

    report.info(ctx, "package.typecheck", f"typechecking package")
    ctx.run(f"mypy {ctx.package.directory!s}")
