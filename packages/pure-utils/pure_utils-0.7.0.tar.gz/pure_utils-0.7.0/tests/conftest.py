import pytest


@pytest.fixture(scope="function")
def fake_logger(mocker):
    return mocker.patch("logging.getLogger", return_value=mocker.MagicMock())


@pytest.fixture(scope="function")
def with_fake_profile_runcall(mocker):
    def runcall(func, *args, **kwargs):
        return func(*args, **kwargs)

    profile = mocker.patch("cProfile.Profile")
    profile.runcall = runcall
