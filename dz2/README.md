# Git Graph Visualizer #

## Общее описание ##
Это инструмент командной строки для визуализации зависимостей npm-пакетов, включая транзитивные зависимости. Программа анализирует файл package.json для указанного пакета, строит граф зависимостей в формате Mermaid и сохраняет его в виде PNG-файла.

## Особенности ##
- Использует стандартные библиотеки Python.
- Не требует установки дополнительных зависимостей.
- Генерирует граф зависимостей пакетов в формате Mermaid.
- Поддерживает конфигурацию через XML-файл.

## Функции ##
1. <code>parse_config</code>: Загружает конфигурацию из XML-файла, который указывает путь к инструменту визуализации, имя пакета, путь для сохранения PNG-файла, максимальную глубину анализа зависимостей и URL репозитория.
2. <code>fetch_dependencies</code>: Получает зависимости для указанного пакета из репозитория. Использует рекурсивный подход для получения транзитивных зависимостей.
3. <code>generate_mermaid_graph</code>: Генерирует граф зависимостей в формате Mermaid.
4. <code>save_graph_as_png</code>: Конвертирует граф в изображение с помощью mermaid-cli и сохраняет его в формате PNG.

## Настройки config.xml ##
```xml
<config>
    <path_to_graph_tool>C:\Users\user\AppData\Roaming\npm\mmdc.cmd</path_to_graph_tool> # путь к Mermaid CLI
    <package_name>config2</package_name> # имя пакета, для которого строится граф 
    <output_file>output.png</output_file> # файл, в который будет сохранён изображённый граф 
    <max_depth>3</max_depth> # максимальная глубина анализа зависимостей
    <repository_url>https://registry.npmjs.org/</repository_url> # путь к git репозиторию, из которого будут извлечены данные о зависимостях
</config>
``````
## Использование ##

1.Клонирование репозитория:
<pre><code>git clone https://github.com/sophialx22/confyprav.git
cd confyprav/dz2 </code></pre>
2.Настройка конфигурации:
Отредактируйте файл config.xml:
```xml
<config>
    <path_to_graph_tool>C:\Users\user\AppData\Roaming\npm\mmdc.cmd</path_to_graph_tool> 
    <package_name>config2</package_name> 
    <output_file>output.png</output_file>
    <max_depth>3</max_depth> 
    <repository_url>https://registry.npmjs.org/</repository_url>
</config>
``````
Запуск программы:
<pre><code>python GraphBuilder.py </code></pre>

## Пример вывода ##

### Пример вывода

```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
``````
Этот граф показывает:

- **Узлы** — коммиты с их сообщениями.
- **Стрелки** — связи между коммитами (родитель → потомок).
- **История изменений** отображается сверху вниз.

## Тестирование ##
- Парсинг XML конфигурации
- Получение зависимостей пакета
- Генерация графа зависимостей в формате Mermaid
- Сохранение графа как PNG изображение
- Полный процесс визуализации зависимостей

Запуск тестов:
<pre><code>python -m pytest Test_GraphBuilder.py -v</code></pre>

## Структура проекта ##
config2/
├── dependency_visualizer.py    # Основной модуль
├── test_dependency_visualizer.py # Тесты
├── config.xml                  # Конфигурационный файл
├── output.png                  # Сгенерированный граф
└── README.md                   # Документация
