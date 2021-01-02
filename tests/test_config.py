from gnrt import gnrt
import pytest

def test_load_config():
    config = gnrt.load_config()
    assert type(config) is dict
    assert 'defaults' in config
    assert 'lists' in config
