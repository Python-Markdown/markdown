"""Generate the code reference pages and navigation."""

import textwrap
import yaml
from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

per_module_options = {
    "markdown": {"summary": {"attributes": True, "functions": True, "classes": True}}
}

base_path = Path(__file__).resolve().parent.parent

modules = [
    base_path.joinpath("markdown", "__init__.py"),
    base_path.joinpath("markdown", "preprocessors.py"),
    base_path.joinpath("markdown", "blockparser.py"),
    base_path.joinpath("markdown", "blockprocessors.py"),
    base_path.joinpath("markdown", "treeprocessors.py"),
    base_path.joinpath("markdown", "inlinepatterns.py"),
    base_path.joinpath("markdown", "postprocessors.py"),
    base_path.joinpath("markdown", "serializers.py"),
    base_path.joinpath("markdown", "util.py"),
    base_path.joinpath("markdown", "htmlparser.py"),
    base_path.joinpath("markdown", "test_tools.py"),
    *sorted(base_path.joinpath("markdown", "extensions").rglob("*.py")),
]

for src_path in modules:
    path = src_path.relative_to(base_path)
    module_path = path.with_suffix("")
    doc_path = path.with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1].startswith("_"):
        continue

    nav_parts = [f"<code>{part}</code>" for part in parts]
    nav[nav_parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}")
        if ident in per_module_options:
            yaml_options = yaml.dump({"options": per_module_options[ident]})
            fd.write(f"\n{textwrap.indent(yaml_options, prefix='    ')}")
        elif ident.startswith("markdown.extensions."):
            yaml_options = yaml.dump({"options": {"inherited_members": False}})
            fd.write(f"\n{textwrap.indent(yaml_options, prefix='    ')}")

    mkdocs_gen_files.set_edit_path(full_doc_path, ".." / path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
