from cmder import __version__
import os.path as p


def test_version():
    ver = '2.0.0'

    assert __version__ == ver
    setup_file = p.join(p.dirname(p.dirname(__file__)), 'setup.py')
    with open(setup_file, 'r') as f:
        content = f.read()
        assert f"version='{ver}'" in content
