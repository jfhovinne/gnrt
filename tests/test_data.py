from gnrt import gnrt
import pytest

def test_load_dataset():
    config = gnrt.load_config()
    dataset = gnrt.load_dataset(config)
    assert type(dataset) is dict
