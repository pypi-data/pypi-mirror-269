from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.transforms import Transform
from sphinx.util.docutils import SphinxDirective

from .data_product import DataProductDirective
from .workflow_parser import get_data_product_parser
from .remote_files import fetch_file_from_repo


class external_data_products(nodes.Element):
    pass


def visit_external_data_products_node(self, node):
    pass


def depart_external_data_products_node(self, node):
    pass


class ExternalDataProductsTransform(Transform):
    # this transform will remove the external_data_products node and replace it with
    # the contents of the external_data_products node
    default_priority = 0

    def apply(self):
        for node in self.document.findall(external_data_products):
            index = node.parent.index(node)
            children = node.children
            node.parent.remove(node)
            for child in children:
                node.parent.insert(index, child)
                index += 1


class ExternalDataProductsDirective(SphinxDirective):
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
        dataproduct_parser = get_data_product_parser(self.env.app)

        if pathtype == "path":
            this_path = Path(self.env.doc2path(self.env.docname))
            path = this_path.parent / patharg
            with open(path, "r") as f:
                data = dataproduct_parser(f.read())
        elif pathtype == "git":
            assert "git-url" in self.options
            assert "git-branch" in self.options
            data_raw = fetch_file_from_repo(
                self.options["git-url"], patharg, self.options["git-branch"]
            )
            data = dataproduct_parser(data_raw)
        else:
            raise NotImplementedError(f"pathtype {pathtype} not implemented")

        targetid = f"external-data-products-{patharg}"
        targetnode = nodes.target("", "", ids=[targetid])

        # # subsections
        # all_subsections = set(
        #     dp_data["subsection"]
        #     for dp_data in data.values()
        #     if "subsection" in dp_data
        # )

        products_node = external_data_products()
        for dp, dp_data in data.items():
            options = {
                "format": dp_data["format"],
                "file_extension": rf'``{dp_data["file-extension"]}``',
                "description": dp_data["description"],
            }
            if "data_fields" in dp_data:
                options["data_fields"] = dp_data["data_fields"]
            dp_directive = DataProductDirective(
                name=dp,
                content=self.content,
                arguments=[dp],
                options=options,
                lineno=self.lineno,
                content_offset=self.content_offset,
                block_text="",
                state=self.state,
                state_machine=self.state_machine,
            )
            products_node += dp_directive.run()

        return [targetnode, products_node]
