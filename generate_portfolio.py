import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, Template

def load_json(file_path: str) -> Dict[str, Any]:
    """Loads JSON data from a file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        Dict[str, Any]: The parsed JSON data.
    """
    with Path(file_path).open(encoding="utf-8") as f:
        return json.load(f)

def setup_jinja_env(template_dir: str) -> Environment:
    """Sets up the Jinja2 environment.

    Args:
        template_dir (str): The directory containing the templates.

    Returns:
        Environment: The Jinja2 environment.
    """
    return Environment(loader=FileSystemLoader(template_dir), autoescape=True)

def load_template(env: Environment, template_name: str) -> Template:
    """Loads a Jinja2 template.

    Args:
        env (Environment): The Jinja2 environment.
        template_name (str): The name of the template file.

    Returns:
        Template: The loaded template.
    """
    return env.get_template(template_name)

def render_template(template: Template, context: Dict[str, Any]) -> str:
    """Renders a Jinja2 template with the given context.

    Args:
        template (Template): The Jinja2 template to render.
        context (Dict[str, Any]): The context data for rendering.

    Returns:
        str: The rendered template output.
    """
    return template.render(**context)

def write_to_file(file_path: str, content: str) -> None:
    """Writes content to a file.

    Args:
        file_path (str): The path to the output file.
        content (str): The content to write.
    """
    with Path(file_path).open("w", encoding="utf-8") as f:
        f.write(content)

def main() -> None:
    """Main function that loads data, processes templates, and writes output files."""
    data: Dict[str, Any] = load_json(file_path="portfolio.json")
    data["current_year"] = datetime.now(tz=UTC).year

    if "social_links" in data:
        for link in data["social_links"]:
            if isinstance(link, dict) and "svg_path" in link:
                svg_path: str = link["svg_path"]
                with Path(svg_path).open(encoding="utf-8") as svg_file:
                    link["svg_data"] = svg_file.read()

    env: Environment = setup_jinja_env(template_dir=".")
    index_template: Template = load_template(env=env, template_name="index_template.html")
    resume_template: Template = load_template(env=env, template_name="resume_template.html")

    html_output: str = render_template(template=index_template, context=data)
    resume_output: str = render_template(template=resume_template, context=data)

    write_to_file(file_path="index.html", content=html_output)
    write_to_file(file_path="resume.html", content=resume_output)

    print("HTML files generated successfully!")

if __name__ == "__main__":
    main()
