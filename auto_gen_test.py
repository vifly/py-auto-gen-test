import typer
import os
from parse_fastapi import get_info_list
from jinja2 import Environment, FileSystemLoader


def main(
    domain: str = typer.Option(..., help="Your backend domain"),
    define_path_code: str = typer.Option(
        ..., help="The path of your project code which define backend path"
    ),
    template_file_path: str = typer.Option(
        ..., help="Will generate test code according to this template"
    ),
    output_path: str = typer.Option(
        "./test.py", help="Generate test code's storage path"
    ),
):
    template_dir, template_file_name = os.path.split(
        os.path.expanduser(template_file_path)
    )
    file_loader = FileSystemLoader(template_dir)

    env = Environment(loader=file_loader)
    template = env.get_template(template_file_name)
    info_list = get_info_list(define_path_code)
    configs = []
    for i in info_list:
        configs.append(
            {
                "name": i.name,
                "url": domain + i.path,
                "method": i.method,
                "arg_num": i.arg_num,
                "arg_names": i.arg_names,
                "arg_types": i.arg_types,
            }
        )

    render_content = template.render(configs=configs)
    with open(output_path, "w") as f:
        f.write(render_content)


if __name__ == "__main__":
    typer.run(main)
