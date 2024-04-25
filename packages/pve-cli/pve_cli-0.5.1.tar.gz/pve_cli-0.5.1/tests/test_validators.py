import pytest
from typer import BadParameter, Context

from pve_cli.util.exceptions import InvalidConfigError
from pve_cli.util.validators import validate_cluster, validate_config


class TestValidateConfig:
    def test_valid_config(self):
        config = {
            'defaults': {'cluster': 'examplecluster'},
            'clusters': {
                'examplecluster': {
                    'host': 'examplehost',
                    'user': 'root',
                    'realm': 'foo',
                    'token_name': 'test',
                    'token_secret': 'PSSST!'
                }
            }
        }
        try:
            validate_config(config)
        except Exception as exc:
            pytest.fail(f'validate_config raised exception {exc}')

    def test_invalid_default_cluster(self):
        config = {
            'defaults': {'cluster': 'invalid'},
            'clusters': {
                'examplecluster': {
                    'host': 'examplehost',
                    'user': 'root',
                    'realm': 'foo',
                    'token_name': 'test',
                    'token_secret': 'PSSST!'
                }
            }
        }
        with pytest.raises(InvalidConfigError):
            validate_config(config)

    def test_missing_cluster_key(self):
        config = {
            'defaults': {'cluster': 'examplecluster'},
            'clusters': {
                'examplecluster': {
                    'host': 'examplehost',
                    'user': 'root',
                    'token_name': 'test',
                    'token_secret': 'PSSST!'
                },
                'second_cluster': {
                    'host': 'host2',
                    'token_name': 'test',
                    'token_secret': 'PSSST!'
                }
            }
        }

        with pytest.raises(InvalidConfigError) as exc:
            validate_config(config)

        assert 'examplecluster: realm' in str(exc.value)
        assert 'second_cluster: user, realm' in str(exc.value)


class TestValidateCluster:
    def test_valid_cluster(self, test_ctx_with_config: Context):
        try:
            validate_cluster(test_ctx_with_config, 'examplecluster')
        except Exception as exc:
            pytest.fail(f'validate_cluster raised exception {exc}')

    def test_invalid_cluster(self, test_ctx_with_config: Context):
        with pytest.raises(BadParameter):
            validate_cluster(test_ctx_with_config, 'invalidcluster')
