from .data_product import (
    DataProductDirective,
    data_product,
    depart_data_product_node,
    merge_data_products,
    purge_data_products,
    visit_data_product_node,
)
from .driver import (
    DriverDirective,
    depart_driver_node,
    driver,
    merge_drivers,
    purge_drivers,
    visit_driver_node,
)
from .external_data_products import (
    ExternalDataProductsDirective,
    ExternalDataProductsTransform,
    depart_external_data_products_node,
    external_data_products,
    visit_external_data_products_node,
)
from .external_drivers import (
    ExternalDriversDirective,
    ExternalDriversTransform,
    depart_external_drivers,
    external_drivers,
    visit_external_drivers,
)
from .pipeline import (
    PipelineDirective,
    depart_pipeline_node,
    pipeline,
    process_pipeline,
    visit_pipeline_node,
)
from .remote_files import ExternalLiteralFileDirective


def setup(app):
    app.setup_extension("sphinxcontrib.mermaid")
    app.add_node(
        external_data_products,
        html=(visit_external_data_products_node, depart_external_data_products_node),
        latex=(visit_external_data_products_node, depart_external_data_products_node),
        text=(visit_external_data_products_node, depart_external_data_products_node),
    )
    app.add_node(
        external_drivers,
        html=(visit_external_drivers, depart_external_drivers),
        latex=(visit_external_drivers, depart_external_drivers),
        text=(visit_external_drivers, depart_external_drivers),
    )
    app.add_node(
        pipeline,
        html=(visit_pipeline_node, depart_pipeline_node),
        latex=(visit_pipeline_node, depart_pipeline_node),
        text=(visit_pipeline_node, depart_pipeline_node),
    )
    app.add_node(
        driver,
        html=(visit_driver_node, depart_driver_node),
        latex=(visit_driver_node, depart_driver_node),
        text=(visit_driver_node, depart_driver_node),
    )
    app.add_node(
        data_product,
        html=(visit_data_product_node, depart_data_product_node),
        latex=(visit_data_product_node, depart_data_product_node),
        text=(visit_data_product_node, depart_data_product_node),
    )
    app.add_directive("driver", DriverDirective)
    app.add_directive("pipeline", PipelineDirective)
    app.add_directive("data_product", DataProductDirective)
    app.add_directive("external_data_products", ExternalDataProductsDirective)
    app.add_directive("external_drivers", ExternalDriversDirective)
    app.add_directive("external_literal_file", ExternalLiteralFileDirective)
    app.add_transform(ExternalDriversTransform)
    app.add_transform(ExternalDataProductsTransform)
    app.connect("doctree-resolved", process_pipeline)
    app.connect("env-purge-doc", purge_drivers)
    app.connect("env-purge-doc", purge_data_products)
    app.connect("env-merge-info", merge_drivers)
    app.connect("env-merge-info", merge_data_products)

    app.add_config_value("data_product_parser", None, "env")
    app.add_config_value("driver_parser", None, "env")

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


__version__ = "0.1.0"
