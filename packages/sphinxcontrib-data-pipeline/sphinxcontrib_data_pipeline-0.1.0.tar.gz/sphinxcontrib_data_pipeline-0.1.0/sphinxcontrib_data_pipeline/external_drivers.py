from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import ViewList
from docutils.transforms import Transform
from sphinx.util.docutils import SphinxDirective

from .driver import DriverDirective
from .workflow_parser import get_driver_parser
from .remote_files import fetch_file_from_repo


class external_drivers(nodes.Element):
    pass


def visit_external_drivers(self, node):
    pass


def depart_external_drivers(self, node):
    pass


class ExternalDriversTransform(Transform):
    # this transform will remove the external_drivers node and replace it with
    # the contents of the external_drivers node
    default_priority = 0

    def apply(self):
        for node in self.document.findall(external_drivers):
            index = node.parent.index(node)
            children = node.children
            node.parent.remove(node)
            for child in children:
                node.parent.insert(index, child)
                index += 1


class ExternalDriversDirective(SphinxDirective):
    # this enables content in the directive
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    option_spec = {
        "type": lambda t: directives.choice(t, ("path", "url", "git")),
        "git-branch": directives.unchanged_required,
        "git-url": directives.unchanged_required,
    }

    def run(self):
        patharg = self.arguments[0]
        pathtype = "path"
        if "type" in self.options:
            pathtype = self.options["type"]
        driver_parser = get_driver_parser(self.env.app)

        if pathtype == "path":
            this_path = Path(self.env.doc2path(self.env.docname))
            path = this_path.parent / patharg
            with open(path, "r") as f:
                data = driver_parser(f.read())
        elif pathtype == "git":
            assert "git-url" in self.options
            assert "git-branch" in self.options
            data_raw = fetch_file_from_repo(
                self.options["git-url"], patharg, self.options["git-branch"]
            )
            data = driver_parser(data_raw)
        else:
            raise NotImplementedError(f"pathtype {pathtype} not implemented")

        targetid = f"external-drivers-{patharg}"
        targetnode = nodes.target("", "", ids=[targetid])

        drivers_node = external_drivers()
        for driver_name, driver in data.items():
            driver_section = nodes.section(driver_name)
            driver_section["ids"].append(f"driver-{driver_name}-heading")
            driver_section += nodes.title(driver_name, driver_name)
            options = {
                "inputs": driver.get("inputs", []),
                "outputs": driver.get("outputs", []),
                "executable": driver.get("executable", driver_name),
            }
            if "repository" in driver:
                options["repository"] = driver["repository"]
            if "documentation" in driver:
                options["documentation"] = driver["documentation"]
            if "contact" in driver:
                options["contact"] = driver["contact"]
            content = driver.get("usage", "")
            notes = driver.get("notes", None)

            driver_directive = DriverDirective(
                name=driver_name,
                content=[content],
                arguments=[driver_name],
                options=options,
                lineno=self.lineno,
                content_offset=self.content_offset,
                block_text="",
                state=self.state,
                state_machine=self.state_machine,
            )
            driver_section += driver_directive.run()

            if notes is not None:
                notes_node = nodes.admonition()
                notes_node += nodes.title("Notes", "Notes")
                notestxt = ViewList(notes.split("\n"))
                _node = nodes.paragraph()
                self.state.nested_parse(notestxt, 0, _node)
                notes_node += _node
                driver_section += notes_node

            drivers_node += driver_section

        return [targetnode, drivers_node]
