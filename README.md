# About

# Running the script

```
 % python Things_json-to-Todoist_csv.py --help
usage: Things_json-to-Todoist_csv.py [-h] [-a [AREA_NAME]] [-i] input_json [output_dir]

Convert Things 3 JSON export to CSV files. By default (without -a or -i options), the script processes all projects under all areas, creating separate CSV files for each project, and also processes top-level items into an 'inbox' file.

To obtain the JSON file from Things 3:
1. Install things-cli: https://github.com/thingsapi/things-cli
2. Run the following command to generate the JSON file:
   things-cli -j --recursive all > things-all-output.json
   (Replace 'things-all-output.json' with your desired filename)

To import into Todoist, drag and drop one of the generated csv files into a Todoist project.
Also see: 
   https://todoist.com/help/articles/introduction-to-backups
   https://todoist.com/help/articles/import-or-export-todoist-project-templates

positional arguments:
  input_json            Path to the input JSON file exported from Things 3 using things-cli
  output_dir            Output directory for CSV files (default: current directory)

options:
  -h, --help            show this help message and exit
  -a [AREA_NAME], --area [AREA_NAME]
						Process a specific area or all areas individually. If AREA_NAME is provided, only that area is processed. If -a is used without AREA_NAME, all areas
						are processed individually, creating separate files for each area.
  -i, --inbox           Process only top-level items (Inbox, Today, Upcoming, Anytime, Someday) into a single 'inbox' file.

Examples:
  python Things_json-to-Todoist_csv.py things-all-output.json
	(Process all projects under all areas and create an inbox file)
  python Things_json-to-Todoist_csv.py things-all-output.json output_directory
	(Same as above, but output to specified directory)
  python Things_json-to-Todoist_csv.py things-all-output.json -a 'Area Name'
	(Process only the specified area)
  python Things_json-to-Todoist_csv.py things-all-output.json -a
	(Process each area individually, creating separate files for each)
  python Things_json-to-Todoist_csv.py things-all-output.json -i
	(Process only top-level items into an inbox file)

```

# things-cli 

[Github source](https://github.com/thingsapi/things-cli)


```shell

things-cli -j --recursive all > things-all-output.json

```

## Examples

```

```

# Todoist spec

[Todoist CSV format Specification](https://todoist.com/help/articles/format-a-csv-file-to-import-into-todoist)

