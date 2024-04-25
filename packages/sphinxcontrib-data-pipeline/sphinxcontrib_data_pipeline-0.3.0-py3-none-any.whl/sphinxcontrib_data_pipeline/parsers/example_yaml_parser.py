from strictyaml import Map, MapPattern, Optional, Seq, Str, load

gio_field_schema = MapPattern(
    Str(), Map({"description": Str(), "type": Str(), "units": Str()})
)

data_product_schema = MapPattern(
    Str(),
    Map(
        {
            Optional("format"): Str(),
            Optional("file-extension"): Str(),
            Optional("description"): Str(),
            Optional("subcategory"): Str(),
            Optional("fields"): Seq(gio_field_schema),
        }
    ),
)

driver_schema = MapPattern(
    Str(),
    Map(
        {
            Optional("executable"): Str(),
            Optional("inputs"): Seq(Str()),
            Optional("outputs"): Seq(Str()),
            Optional("repository"): Str(),
            Optional("documentation"): Str(),
            Optional("contact"): Str(),
            Optional("usage"): Str(),
            Optional("notes"): Str(),
        }
    ),
)

file_schema = Map(
    {
        Optional("data_products"): Seq(data_product_schema),
        Optional("drivers"): Seq(driver_schema),
    }
)


def parse_dataproducts(rawdata: str):
    data = load(rawdata, file_schema)

    data_products = {k: v for dp in data["data_products"].data for k, v in dp.items()}
    for dp_name, dp in data_products.items():
        assert "format" in dp
        assert "description" in dp

        if "fields" in dp:
            data_fields = dp.pop("fields")
            dp["data_fields"] = {
                k: v for field in data_fields for k, v in field.items()
            }

    return data_products


def parse_drivers(rawdata: str):
    data = load(rawdata, file_schema)

    drivers = {k: v for d in data["drivers"].data for k, v in d.items()}
    return drivers
