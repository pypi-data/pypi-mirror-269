from docutils import nodes
from docutils.statemachine import ViewList
from sphinx_tabs.tabs import (
    SphinxTabsPanel,
    SphinxTabsTab,
    SphinxTabsTablist,
    get_compatible_builders,
)


def list_option(argument):
    if argument is None:
        return []
    if isinstance(argument, list):
        return argument
    arguments = argument.replace("[", "").replace("]", "").split(",")
    arguments = [a.strip() for a in arguments]
    return arguments


def create_field_list(directive, field_kv_pairs):
    fields = nodes.field_list()
    for key, value in field_kv_pairs:
        field = nodes.field()
        field_name = nodes.field_name()
        field_name += nodes.Text(key)
        field += field_name

        field_value = nodes.field_body()
        field_par = nodes.paragraph()
        field_txt = ViewList()
        field_txt.append(value, directive.env.docname, 0)
        directive.state.nested_parse(field_txt, 0, field_par)
        field_value += field_par
        field += field_value
        fields += field
    return fields


def create_table(directive, data, header_rows=1):
    num_cols = len(data[0])
    col_widths = [0] * num_cols
    for row in data:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    table = nodes.table()
    table["classes"] += ["colwidths-auto"]

    tgroup = nodes.tgroup(cols=num_cols)
    table += tgroup

    for col_width in col_widths:
        colspec = nodes.colspec()
        if col_width is not None:
            colspec.attributes["colwidth"] = col_width
        tgroup += colspec
    rows = []
    for row in data:
        row_node = nodes.row()
        for cell in row:
            entry = nodes.entry()
            entry_par = nodes.container()
            _txt = ViewList()
            _txt.append(cell, directive.env.docname, 0)
            directive.state.nested_parse(_txt, 0, entry_par)
            entry += entry_par
            row_node += entry
        rows.append(row_node)
    if header_rows:
        thead = nodes.thead()
        thead.extend(rows[:header_rows])
        tgroup += thead
    tbody = nodes.tbody()
    tbody.extend(rows[header_rows:])
    tgroup += tbody
    return table


def create_tabs(directive, tab_titles):
    node = nodes.container(type="tab-element")
    node["classes"].append("sphinx-tabs")

    if directive.env.app.builder.name in get_compatible_builders(directive.env.app):
        tablist = SphinxTabsTablist()
        tablist["role"] = "tablist"
        tablist["aria-label"] = "Tabbed content"
        if not directive.env.config["sphinx_tabs_disable_tab_closing"]:
            tablist["classes"].append("closeable")

        for idx, title in enumerate(tab_titles):
            titletxt = ViewList()
            titletxt.append(title, directive.env.docname, 0)
            tab_name = SphinxTabsTab()
            directive.state.nested_parse(titletxt, 0, tab_name)
            tab_name.children[0].replace_self(tab_name.children[0].children)
            tab_name["classes"].append("sphinx-tabs-tab")

            tab_name.attributes["role"] = "tab"
            tab_name["ids"] = [f"tab-{idx}"]
            tab_name["name"] = title
            tab_name["tabindex"] = "0" if idx == 0 else "-1"
            tab_name["aria-selected"] = "true" if idx == 0 else "false"
            tab_name["aria-controls"] = tab_name["ids"][0].replace("tab-", "panel-")

            tablist += tab_name
        node.insert(0, tablist)

    panels = {}
    for idx, title in enumerate(tab_titles):
        panel = SphinxTabsPanel()
        panel["role"] = "tabpanel"
        panel["ids"] = [f"panel-{idx}"]
        panel["name"] = str(idx)
        panel["tabindex"] = 0
        panel["aria-labelledby"] = panel["ids"][0].replace("panel-", "tab-")
        panel["classes"].append("sphinx-tabs-panel")
        if idx > 0:
            panel["hidden"] = True

        if directive.env.app.builder.name not in get_compatible_builders(
            directive.env.app
        ):
            # Use base docutils classes
            outer_node = nodes.container()
            tab = nodes.container()
            tab_name = nodes.container()
            panel = nodes.container()

            tab += tab_name
            outer_node += tab
            outer_node += panel

            panels[title] = outer_node
        else:
            panels[title] = panel

    for title, panel in panels.items():
        node += panel
    return node, panels
