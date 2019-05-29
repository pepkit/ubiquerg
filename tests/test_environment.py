""" Tests for environment-related functionality """

import os
import pytest
from ubiquerg import TmpEnv


@pytest.mark.parametrize("envvars", [
    {"DUMMYTESTVAR": "arbitrary"},
    {"DUMMYTESTVAR": "random", "TOTALLY_RAD_VARIABLE": "ephemeral"}
])
def test_overwrite_prohibited(envvars):
    """ Prohibition of overwrite causes ValueError in case of collision. """
    check_unset(envvars)
    with TmpEnv(**envvars), pytest.raises(ValueError):
        TmpEnv(overwrite=False, **{k: v + "_EXTRA" for k, v in envvars.items()})
    check_unset(envvars)


@pytest.mark.parametrize("envvars", [
    {"DUMMYTESTVAR": "arbitrary"},
    {"DUMMYTESTVAR": "random", "TOTALLY_RAD_VARIABLE": "ephemeral"}
])
def test_overwrite_allowed(envvars):
    """ Verify that overwriting existing value with different one works if permitted. """
    check_unset(envvars)
    with TmpEnv(**envvars):
        modified = {k: v + "_EXTRA" for k, v in envvars.items()}
        with TmpEnv(overwrite=True, **modified):
            for k, v in modified.items():
                assert v == os.getenv(k)
    check_unset(envvars)


@pytest.mark.parametrize("overwrite", [False, True])
@pytest.mark.parametrize("envvars", [
    {"DUMMYTESTVAR": "arbitrary"},
    {"DUMMYTESTVAR": "random", "TOTALLY_RAD_VARIABLE": "ephemeral"}
])
def test_no_intersection(overwrite, envvars):
    """ Verify that overwrite permission is irrelevant if no variable name collision occurs. """
    check_unset(envvars)
    with TmpEnv(overwrite=overwrite, **envvars):
        for k, v in envvars.items():
            assert v == os.getenv(k)


def check_unset(envvars):
    """ Verify that each environment variable is not set. """
    fails = [v for v in envvars if os.getenv(v) or v in os.environ]
    assert not fails, "Vars set: {}".format(fails)
