from jinja2 import Environment, PackageLoader, select_autoescape

from constants import INPUT_FILE_PATH


env = Environment(
    loader=PackageLoader("helpers", "templates"),
    autoescape=select_autoescape(["html"]),
)


def populate_template(template_name, data):
    template = env.get_template(template_name)
    populated_template = template.render(**data)
    return populated_template


def write_file(path, contents):
    with open(path, "w") as file_:
        file_.write(contents)


def read_input():
    with open(INPUT_FILE_PATH) as file_:
        raw_lines = file_.read().splitlines()
        sorted_lines = sorted(raw_lines, reverse=True)
        return sorted_lines
