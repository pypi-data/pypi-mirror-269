from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import ViewList
from sphinx.directives.code import CodeBlock
from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective
from sphinxcontrib.mermaid import mermaid

from .utils import create_field_list, list_option


class driver(nodes.Admonition, nodes.Element):
    pass


def visit_driver_node(self, node):
    self.visit_admonition(node)


def depart_driver_node(self, node):
    self.depart_admonition(node)


class DriverDirective(SphinxDirective):
    # this enables content in the directive
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    option_spec = {
        "description": directives.unchanged,
        "executable": directives.unchanged,
        "inputs": list_option,
        "outputs": list_option,
        "repository": directives.unchanged,
        "documentation": directives.unchanged,
        "contact": directives.unchanged,
    }

    def run(self):
        driver_name = self.arguments[0]
        driver_category = self.env.docname.split("/")[1:-2]

        # targetid = "driver-%d" % self.env.new_serialno("driver")
        targetid = f"driver-{driver_name}"
        targetnode = nodes.target("", "", ids=[targetid])

        driver_node = driver()
        driver_node += nodes.title(_(driver_name), _(driver_name))

        field_list = []
        if "description" in self.options:
            field_list.append(("Description", self.options["description"]))
        if "executable" in self.options:
            field_list.append(("Executable", f"``{self.options['executable']}``"))
        if "repository" in self.options:
            field_list.append(("Repository", self.options["repository"]))
        if "documentation" in self.options:
            field_list.append(("Documentation", self.options["documentation"]))
        if "contact" in self.options:
            field_list.append(("Contact", self.options["contact"]))
        fields = create_field_list(self, field_list)
        driver_node += fields

        # Add a code-block!
        codeblock_directive = CodeBlock(
            name="",
            arguments=["bash"],
            options={"caption": f"{driver_name} command line arguments"},
            content=self.content,
            lineno=self.lineno,
            content_offset=self.content_offset,
            block_text="",
            state=self.state,
            state_machine=self.state_machine,
        )
        driver_node += codeblock_directive.run()[0]

        # Add an empty diagram (filled later)!
        mermaid_node = mermaid()
        mermaid_node["code"] = ""
        mermaid_node["options"] = {}
        figure_node = nodes.figure("t", mermaid_node)
        figure_node["align"] = "center"
        caption = f"``{driver_name}`` inputs/outputs"
        parsed = nodes.Element()
        self.state.nested_parse(
            ViewList([caption], source=""), self.content_offset, parsed
        )
        caption_node = nodes.caption(parsed[0].rawsource, "", *parsed[0].children)
        caption_node.source = parsed[0].source
        caption_node.line = parsed[0].line
        figure_node += caption_node
        driver_node += figure_node

        # self.state.nested_parse(self.content, self.content_offset, driver_node)

        if not hasattr(self.env, "driver_all_drivers"):
            self.env.driver_all_drivers = []

        self.env.driver_all_drivers.append(
            {
                "docname": self.env.docname,
                "lineno": self.lineno,
                "driver": driver_node.deepcopy(),
                "target": targetnode,
                "inputs": self.options["inputs"],
                "outputs": self.options["outputs"],
                "driver_name": driver_name,
                "driver_category": driver_category,
            }
        )

        return [targetnode, driver_node]


def purge_drivers(app, env, docname):
    if not hasattr(env, "driver_all_drivers"):
        return

    env.driver_all_drivers = [
        driver for driver in env.driver_all_drivers if driver["docname"] != docname
    ]


def merge_drivers(app, env, docnames, other):
    if not hasattr(env, "driver_all_drivers"):
        env.driver_all_drivers = []

    if hasattr(other, "driver_all_drivers"):
        env.driver_all_drivers.extend(other.driver_all_drivers)
