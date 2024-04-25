import uuid

from docutils import nodes
from docutils.statemachine import ViewList
from sphinx.util import logging

# from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective
from sphinxcontrib.mermaid import mermaid

from .data_product import data_product
from .driver import driver
from .utils import create_tabs


class pipeline(nodes.Structural, nodes.Element):
    pass


def visit_pipeline_node(self, node):
    pass
    # self.visit_admonition(node)


def depart_pipeline_node(self, node):
    pass
    # self.depart_admonition(node)


class PipelineDirective(SphinxDirective):
    has_content = False
    required_arguments = 0
    optional_arguments = 0

    def run(self):
        inner_node = nodes.container(type="div")
        inner_node["classes"] = ["full-width"]
        pipeline_node = pipeline("Pipeline Diagrams")
        # pipeline_node += nodes.title(_("Pipeline Charts"), _("Pipeline Charts"))
        # pipeline_node["classes"] += ["full-width"]

        # TODO: add tabs for different categories
        tab_node, panels = create_tabs(self, ["Full Pipeline"])
        inner_node += tab_node

        mermaid_node = mermaid()
        mermaid_node["code"] = ""
        mermaid_node["options"] = {}
        mermaid_node["zoom"] = True
        mermaid_node["zoom_id"] = f"id-pipeline-{uuid.uuid4()}"
        figure_node = nodes.figure("t", mermaid_node)
        figure_node["align"] = "center"
        caption = "exaworkflows pipeline"
        parsed = nodes.Element()
        self.state.nested_parse(
            ViewList([caption], source=""), self.content_offset, parsed
        )
        caption_node = nodes.caption(parsed[0].rawsource, "", *parsed[0].children)
        caption_node.source = parsed[0].source
        caption_node.line = parsed[0].line
        figure_node += caption_node
        panels["Full Pipeline"] += figure_node

        pipeline_node += inner_node
        return [pipeline_node]


def process_pipeline(app, doctree, fromdocname):
    # Replace all todolist nodes with a list of the collected todos.
    # Augment each todo with a backlink to the original location.
    env = app.builder.env
    if not hasattr(env, "driver_all_drivers"):
        env.driver_all_drivers = []

    if not hasattr(env, "data_product_all_products"):
        env.data_product_all_products = []

    # # All sub-categories
    # categories = dict()
    # for dp in env.data_product_all_products:
    #     categories
    # TODO: diagram per category

    # Full pipeline diagrams
    for pipeline_node in doctree.findall(pipeline):
        all_dp = dict()
        all_driver = dict()
        for dp in env.data_product_all_products:
            dp_name = dp["data_product_name"]
            dp_url = app.builder.get_relative_uri(fromdocname, dp["docname"])
            refid = dp["target"].get("refid", None)
            if refid is None and "ids" in dp["target"]:
                refid = dp["target"]["ids"][0]
            if refid is not None:
                dp_url += f"#{refid}"
            all_dp[dp_name] = dp_url
        for driver_info in env.driver_all_drivers:
            driver_name = driver_info["driver_name"]
            driver_url = app.builder.get_relative_uri(
                fromdocname, driver_info["docname"]
            )
            refid = driver_info["target"].get("refid", None)
            if refid is None and "ids" in driver_info["target"]:
                refid = driver_info["target"]["ids"][0]
            if refid is not None:
                driver_url += f"#{refid}"
            all_driver[driver_name] = driver_url
            for dp in driver_info["inputs"] + driver_info["outputs"]:
                if dp not in all_dp:
                    all_dp[dp] = None

        mermaid_content = ["flowchart TD"]
        for dp_name, dp_url in all_dp.items():
            mermaid_content.append(f" {dp_name}([{dp_name}])")
            if dp_url is not None:
                mermaid_content.append(
                    f' click {dp_name} href "{dp_url}" "go to data product"'
                )
        for driver_name, driver_url in all_driver.items():
            mermaid_content.append(
                driver_name + "{{" + driver_name + "}}:::driverClass"
            )
            mermaid_content.append(
                f' click {driver_name} href "{driver_url}" "go to driver"'
            )

        for driver_info in env.driver_all_drivers:
            driver_name = driver_info["driver_name"]
            for dp in driver_info["inputs"]:
                mermaid_content.append(f" {dp} --> {driver_name}")
            for dp in driver_info["outputs"]:
                mermaid_content.append(f" {driver_name} --> {dp}")
        mermaid_content.append(
            " classDef driverClass fill:#f96,color:black,stroke:#854c30;"
        )

        mermaid_node = next(pipeline_node.findall(mermaid))
        mermaid_node["code"] = "\n".join(mermaid_content)

    # Drivers diagrams
    driver_node: driver
    for driver_node in doctree.findall(driver):
        title_node = driver_node.children[
            driver_node.first_child_matching_class(nodes.title)
        ]
        assert len(title_node.children) > 0
        driver_name = title_node.children[0].astext()
        driver_info = next(
            (di for di in env.driver_all_drivers if di["driver_name"] == driver_name),
            None,
        )
        assert driver_info is not None

        mermaid_content = ["flowchart LR"]
        # nodes
        mermaid_content.append(driver_name + "{{" + driver_name + "}}:::driverClass")
        for dp_name in driver_info["inputs"] + driver_info["outputs"]:
            mermaid_content.append(f" {dp_name}([{dp_name}])")
            if dp_info := next(
                (
                    dp
                    for dp in env.data_product_all_products
                    if dp["data_product_name"] == dp_name
                ),
                False,
            ):
                url = app.builder.get_relative_uri(fromdocname, dp_info["docname"])
                refid = dp_info["target"].get("refid", None)
                if refid is None and "ids" in dp_info["target"]:
                    refid = dp_info["target"]["ids"][0]
                if refid is not None:
                    url += f"#{refid}"
                mermaid_content.append(
                    f' click {dp_name} href "{url}" "go to data product"'
                )
            else:
                logger = logging.getLogger(__name__)
                logger.warning(
                    f"no documentation for data product {dp_name}, "
                    f"referenced in driver {driver_name}"
                )

        # connections
        for input in driver_info["inputs"]:
            mermaid_content.append(f" {input} --> {driver_name}")
        for output in driver_info["outputs"]:
            mermaid_content.append(f" {driver_name} --> {output}")
        mermaid_content.append(
            " classDef driverClass fill:#f96,color:black,stroke:#854c30;"
        )

        mermaid_node = next(driver_node.findall(mermaid))
        mermaid_node["code"] = "\n".join(mermaid_content)

    # Data Products diagrams
    dp_node: data_product
    for dp_node in doctree.findall(data_product):
        title_node = dp_node.children[dp_node.first_child_matching_class(nodes.title)]
        assert len(title_node.children) > 0
        dp_name = title_node.children[0].astext()

        producers = []
        consumers = []

        for driver_info in env.driver_all_drivers:
            refid = driver_info["target"].get("refid", None)
            if refid is None and "ids" in driver_info["target"]:
                refid = driver_info["target"]["ids"][0]
            if refid is None:
                refid = ""
            else:
                refid = "#" + refid

            if dp_name in driver_info["inputs"]:
                consumers.append(
                    (driver_info["driver_name"], driver_info["docname"], refid)
                )
            if dp_name in driver_info["outputs"]:
                producers.append(
                    (driver_info["driver_name"], driver_info["docname"], refid)
                )

        # Add a diagram!
        mermaid_content = ["flowchart LR"]
        # nodes
        mermaid_content.append(" " + dp_name + "([" + dp_name + "])")
        for driver_name, docname, refid in producers + consumers:
            mermaid_content.append(
                " " + driver_name + "{{" + driver_name + "}}:::driverClass"
            )
            url = app.builder.get_relative_uri(fromdocname, docname) + refid
            mermaid_content.append(f' click {driver_name} href "{url}" "go to driver"')
        # connections
        for driver_name, docname, refid in consumers:
            mermaid_content.append(f" {dp_name} --> {driver_name}")
        for driver_name, docname, refid in producers:
            mermaid_content.append(f" {driver_name} --> {dp_name}")
        mermaid_content.append(
            " classDef driverClass fill:#f96,color:black,stroke:#854c30;"
        )

        mermaid_node = next(dp_node.findall(mermaid))
        mermaid_node["code"] = "\n".join(mermaid_content)
        mermaid_node["code"] = "\n".join(mermaid_content)
        mermaid_node["code"] = "\n".join(mermaid_content)
        mermaid_node["code"] = "\n".join(mermaid_content)
