import pytest
from unittest.mock import patch, mock_open

from GraphBuilder import (
    parse_config,
    fetch_dependencies,
    generate_mermaid_graph,
    save_graph_as_png
)

@pytest.fixture
def sample_config():
    return {
        'visualizer_path': '/usr/local/bin/mmdc',
        'package_name': 'example-package',
        'output_file': 'output.png',
        'max_depth': 2,
        'repository_url': 'https://registry.npmjs.org/'
    }

def test_parse_config():
    config_data = """<config>
        <path_to_graph_tool>C:\\Users\\user\\AppData\\Roaming\\npm\\mmdc.cmd</path_to_graph_tool>
        <package_name>example-package</package_name>
        <output_file>output.png</output_file>
        <max_depth>2</max_depth>
        <repository_url>https://registry.npmjs.org/</repository_url>
    </config>"""

    with patch('builtins.open', mock_open(read_data=config_data)):
        config = parse_config('config.xml')
        assert config['path_to_graph_tool'] == 'C:\\Users\\user\\AppData\\Roaming\\npm\\mmdc.cmd'
        assert config['package_name'] == 'example-package'
        assert config['output_file'] == 'output.png'
        assert config['max_depth'] == 2
        assert config['repository_url'] == 'https://registry.npmjs.org/'

def test_fetch_dependencies():
    mock_response = '{"dependencies": {"dep1": {}, "dep2": {}}}'.encode()

    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value.read.return_value = mock_response
        result = fetch_dependencies('example-package', 0, 2, 'https://registry.npmjs.org/')

        assert 'example-package' in result
        assert 'dep1' in result['example-package']
        assert 'dep2' in result['example-package']


def test_generate_mermaid_graph():
    dependencies = {
        'example-package': ['dep1', 'dep2'],
        'dep1': ['dep3'],
        'dep2': []
    }
    graph = generate_mermaid_graph(dependencies)

    assert 'example-package-->dep1;' in graph
    assert 'example-package-->dep2;' in graph
    assert 'dep1-->dep3;' in graph
    assert 'dep2' in graph


def test_save_graph_as_png(sample_config):
    with patch('os.path.exists', return_value=True), patch('subprocess.run') as mock_run:
        mock_run.return_value = None
        try:
            save_graph_as_png('graph TD;\n  A-->B;', sample_config['output_file'], sample_config['visualizer_path'])
        except FileNotFoundError:
            pytest.fail("FileNotFoundError raised unexpectedly!")
