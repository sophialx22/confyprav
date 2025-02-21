import json
import urllib.request
import xml.etree.ElementTree as ET
import subprocess
import os

def parse_config(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return {
        'path_to_graph_tool': root.find('path_to_graph_tool').text,
        'package_name': root.find('package_name').text,
        'output_file': root.find('output_file').text,
        'max_depth': int(root.find('max_depth').text),
        'repository_url': root.find('repository_url').text
    }

def fetch_dependencies(package_name, depth, max_depth, repository_url, visited=None):
    if visited is None:
        visited = set()
    if depth > max_depth or package_name in visited:
        return {}

    visited.add(package_name)
    url = f'{repository_url}{package_name}/'
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
    except urllib.error.URLError:
        return {}

    dependencies = data.get('dependencies', {})
    result = {package_name: list(dependencies.keys())}

    for dep in dependencies:
        result.update(fetch_dependencies(dep, depth + 1, max_depth, repository_url, visited))

    return result

def generate_mermaid_graph(dependencies):
    graph = 'graph TD;\n'
    for package, deps in dependencies.items():
        for dep in deps:
            graph += f'  {package}-->{dep};\n'
    return graph

def save_graph_as_png(graph, output_file, mmdc_path):
    if not os.path.exists(mmdc_path):
        raise FileNotFoundError(f"Утилита {mmdc_path} не найдена.")
    temp_file = 'draph.mmd'
    with open(temp_file, 'w') as f:
        f.write(graph)
    try:
        subprocess.run([mmdc_path, '-i', temp_file, '-o', output_file], capture_output=True, check=True)
        print(f"Граф зависимостей сохранён в {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при генерации графа: {e}")

def main(config_file):
    config = parse_config(config_file)
    dependencies = fetch_dependencies(config['package_name'], 0, config['max_depth'], config['repository_url'])
    graph = generate_mermaid_graph(dependencies)
    save_graph_as_png(graph, config['output_file'], config['path_to_graph_tool'])

if __name__ == '__main__':
    main('config.xml')
