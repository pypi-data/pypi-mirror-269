from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import ViewList
from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective
from sphinx_toolbox.collapse import CollapseNode
from sphinxcontrib.mermaid import mermaid

from .utils import create_field_list, create_table


class data_product(nodes.Admonition, nodes.Element):
    pass


def visit_data_product_node(self, node):
    self.visit_admonition(node)


def depart_data_product_node(self, node):
    self.depart_admonition(node)


class DataProductDirective(SphinxDirective):
    # this enables content in the directive
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    option_spec = {
        "format": directives.unchanged,
        "file_extension": directives.unchanged,
        "description": directives.unchanged,
        "data_fields": directives.unchanged,
    }

    def run(self):
        dp_name = self.arguments[0]
        dp_category = self.env.docname.split("/")[-1]

        # targetid = "data-product-%d" % self.env.new_serialno("data-product")
        targetid = f"data-product-{dp_name}"
        targetnode = nodes.target("", "", ids=[targetid])

        data_product_node = data_product()
        data_product_node += nodes.title(_(dp_name), _(dp_name))

        field_list = []
        if "description" in self.options:
            field_list.append(("Description", self.options["description"]))
        if "format" in self.options:
            field_list.append(("Data Format", self.options["format"]))
        if "file_extension" in self.options:
            field_list.append(("File Extension", self.options["file_extension"]))
        fields = create_field_list(self, field_list)
        data_product_node += fields

        # Create an empty figure
        mermaid_node = mermaid()
        mermaid_node["code"] = ""
        mermaid_node["options"] = {}
        figure_node = nodes.figure("t", mermaid_node)
        figure_node["align"] = "center"
        caption = f"``{dp_name}`` producers and consumers"
        parsed = nodes.Element()
        self.state.nested_parse(
            ViewList([caption], source=""), self.content_offset, parsed
        )
        caption_node = nodes.caption(parsed[0].rawsource, "", *parsed[0].children)
        caption_node.source = parsed[0].source
        caption_node.line = parsed[0].line
        figure_node += caption_node
        data_product_node += figure_node

        # Create a table for data fields
        if "data_fields" in self.options:
            table_header = ["Field", "Type", "Units", "Description"]
            table_data = [table_header]
            for field_name, fields in self.options["data_fields"].items():
                table_data.append(
                    [
                        field_name,
                        fields.get("type", "N/A"),
                        fields.get("units", "N/A"),
                        fields.get("description", "N/A"),
                    ]
                )
            # table_container = nodes.container()
            table_container = CollapseNode(label="Data Fields")
            table_node = create_table(self, table_data, 1)
            table_node["classes"] += ["table-sm"]
            table_container += table_node
            data_product_node += table_container

        if not hasattr(self.env, "data_product_all_products"):
            self.env.data_product_all_products = []

        self.env.data_product_all_products.append(
            {
                "docname": self.env.docname,
                "lineno": self.lineno,
                "driver": data_product_node.deepcopy(),
                "target": targetnode,
                "data_product_name": dp_name,
                "data_product_category": dp_category,
            }
        )

        return [targetnode, data_product_node]


def purge_data_products(app, env, docname):
    if not hasattr(env, "data_product_all_products"):
        return

    env.data_product_all_products = [
        dp for dp in env.data_product_all_products if dp["docname"] != docname
    ]


def merge_data_products(app, env, docnames, other):
    if not hasattr(env, "data_product_all_products"):
        env.data_product_all_products = []

    if hasattr(other, "data_product_all_products"):
        env.data_product_all_products.extend(other.data_product_all_products)
        env.data_product_all_products.extend(other.data_product_all_products)
