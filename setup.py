from setuptools import setup

setup(
    # The package metadata is specified in setup.cfg but GitHub's downstream dependency graph
    # does not work unless we put the name this here too.
    name="pyobis",
    version = "1.3.0",
    # use_scm_version={
    #     "write_to": "pyobis/_version.py",
    #     "write_to_template": '__version__ = "1.3.0"',
    #     "tag_regex": r"^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$",
    # },
)
