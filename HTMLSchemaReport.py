# MySQL Workbench Python script
# Script to Generate an HTML Schema Report from Mysql Model
# Original Author: Tito Sanchez (tmsanchez@gmail.com)
# Current Author: Ivan Miloslavov (github.com/vanyamil)
# Written in MySQL Workbench 8.0.24

from wb import *
import grt
import mforms

title = "Database schema report in HTML format"
ModuleInfo = DefineModule(
    name="DBHTMLReport", 
    author="Ivan Miloslavov", 
    version="3.0.1", 
    description=title
)

@ModuleInfo.plugin("vanyamil.htmlReportSchema", 
    caption=title, 
    description=title, 
    input=[wbinputs.currentCatalog()], 
    pluginMenu="Catalog"
)

@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)
def htmlDataDictionary(catalog):
    # Select filename for the HTML file
    htmlOut = ""
    filechooser = mforms.FileChooser(mforms.SaveFile)
    filechooser.set_extensions("HTML File (*.html)|*.html","html");
    if filechooser.run_modal():
        htmlOut = filechooser.get_path()
    print(f"HTML File: {htmlOut}")
    if len(htmlOut) <= 1:
        return 1
    
    # open up file
    with open(htmlOut, "w") as htmlFile:
        # iterate through columns from schema
        schema = catalog.schemata[0]
        htmlFile = open(htmlOut, "w")
        print("<html><head>", file=htmlFile)
        print(f"<title>Schema Report for database: {schema.name}</title>", file=htmlFile)
        print("""<style>
            td,th {
            text-align:left;
            vertical-align:middle;
            }
            table {
            border-collapse: collapse;
            border: 1px solid;
            }
            caption, th, td {
            padding: .2em .8em;
            border: 1px solid #000000;
            }
            caption {
            background: #D3D3D3;
            font-weight: bold;
            font-size: 1.1em;
            }
            th {
            font-weight: bold;
            background: #000000;
            color: white;
            }
            td {
            background: #FFFFFF;
            }
            </style>
          </head>
         <body>""", file=htmlFile)
        print(f"<h1>Schema Report for database: {schema.name}</h1>", file=htmlFile)
        print("<a id=\"home\">Table List </a><br /><ul>", file=htmlFile)
        for table in schema.tables:
            print(f"<li><a href=\"#{table.name}\">{table.name} </a></li>", file=htmlFile)
        print("</ul>", file=htmlFile)
        for table in schema.tables:
            print(f"<a id=\"{table.name}\"></a><table style=\"width:100%%\"><caption>Table: {table.name} </caption>", file=htmlFile)
            print(f"<tr><td>Table Comments</td><td colspan=\"6\">{table.comment}</td></tr>", file=htmlFile)
            print("""<tr><td colspan=\"7\">Columns</td></tr>
            <tr>
            <th>Name</th>
            <th>Data Type</th>
            <th>Nullable</th>
            <th>PK</th>
            <th>FK</th>
            <th>Default</th>
            <th>Comment</th>
            </tr>""", file=htmlFile)
            for column in table.columns:
                pk = ('No', 'Yes')[bool(table.isPrimaryKeyColumn(column))]
                fk = ('No', 'Yes')[bool(table.isForeignKeyColumn(column))]
                nn = ('Yes', 'No')[bool(column.isNotNull)]
                print(f"<tr><td>{column.name}</td><td>{column.formattedType}</td><td>{nn}</td><td>{pk}</td><td>{fk}</td><td>{column.defaultValue}</td><td>{column.comment}</td></tr>", file=htmlFile)
            print("</table><a href=\"#home\">Table List </a></br>", file=htmlFile)
        print("</body></html>", file=htmlFile)

    mforms.Utilities.show_message("Report generated", "HTML Report format from current model generated", "OK","","")
    return 0