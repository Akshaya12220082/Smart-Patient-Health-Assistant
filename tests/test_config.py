"""
Unit tests for configuration utilities
"""
import pytest
import sys
import os
import tempfile
import yaml

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.config import load_config, _replace_env_vars, get_project_root, ensure_dir


def test_get_project_root():
    """Test getting project root"""
    root = get_project_root()
    assert os.path.isabs(root)
    assert os.path.exists(root)


def test_ensure_dir():
    """Test directory creation"""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_path = os.path.join(tmpdir, 'test_dir', 'nested')
        ensure_dir(test_path)
        assert os.path.exists(test_path)


def test_replace_env_vars_string():
    """Test environment variable replacement in strings"""
    os.environ['TEST_VAR'] = 'test_value'
    result = _replace_env_vars('${TEST_VAR}')
    assert result == 'test_value'
    del os.environ['TEST_VAR']


def test_replace_env_vars_dict():
    """Test environment variable replacement in dictionaries"""
    os.environ['TEST_KEY'] = 'secret_key'
    config = {
        'api': {
            'key': '${TEST_KEY}',
            'other': 'value'
        }
    }
    result = _replace_env_vars(config)
    assert result['api']['key'] == 'secret_key'
    assert result['api']['other'] == 'value'
    del os.environ['TEST_KEY']


def test_replace_env_vars_list():
    """Test environment variable replacement in lists"""
    os.environ['TEST_ITEM'] = 'item_value'
    config = ['normal', '${TEST_ITEM}', 'another']
    result = _replace_env_vars(config)
    assert result[1] == 'item_value'
    del os.environ['TEST_ITEM']


def test_replace_env_vars_missing():
    """Test handling of missing environment variables"""
    result = _replace_env_vars('${NONEXISTENT_VAR}')
    assert result == '${NONEXISTENT_VAR}'  # Should return original if not found


def test_load_config_template():
    """Test loading config from template"""
    # This test assumes config.yaml.template exists
    try:
        config = load_config()
        assert 'project' in config
        assert 'ml_models' in config
    except RuntimeError:
        pytest.skip("Config file not available")
