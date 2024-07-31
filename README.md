# Things to Todoist Converter

This Python script converts data exported from the 'Things' todo app into CSV files compatible with 'Todoist'. It allows you to export tasks from 'Things' using the `things-cli` tool and then transform them into a format that can be imported into 'Todoist' projects.

## Prerequisites

1. **Install `things-cli`:**  
   To export your data from the 'Things' app in JSON format, you first need to install the `things-cli` tool. You can find the installation instructions and source code on the [GitHub page](https://github.com/thingsapi/things-cli).

2. **Export Data from Things:**  
   Use the following command to export all your tasks and projects from 'Things' into a JSON file:

   ```shell
   things-cli -j --recursive all > things-all-output.json
   ```

   Replace `things-all-output.json` with your desired filename.

## Getting Started

To use the script, simply download it from the repository:

### **Download the Script:**  
   Download the file `Things_json-to-Todoist_csv.py` directly from the repository [here](https://github.com/hschot/Things_json-to-Todoist_csv/blob/main/Things_json-to-Todoist_csv.py) (or clone this repository).

### **Run the Script:**
   - Open your terminal or command prompt.
   - Navigate to the directory where you saved the script.

### Usage

```
Things_json-to-Todoist_csv.py [-h] [-a [AREA_NAME]] [-i] input_json [output_dir]
```

Convert Things 3 JSON export to CSV files. By default (without `-a` or `-i` options), the script processes all projects under all areas, creating separate CSV files for each project, and also processes top-level items into an 'inbox' file.

#### To obtain the JSON file from Things 3:

1. Install `things-cli`: [GitHub source](https://github.com/thingsapi/things-cli)
2. Run the following command to generate the JSON file:

   ```shell
   things-cli -j --recursive all > things-all-output.json
   ```

   (Replace `'things-all-output.json'` with your desired filename)

#### To import into Todoist:

Drag and drop one of the generated CSV files into a Todoist project.  
Also see: 
- [Introduction to Backups](https://todoist.com/help/articles/introduction-to-backups)
- [Import or Export Todoist Project Templates](https://todoist.com/help/articles/import-or-export-todoist-project-templates)

### Positional Arguments

- `input_json`: Path to the input JSON file exported from Things 3 using `things-cli`.
- `output_dir`: Output directory for CSV files (default: current directory).

### Options

- `-h, --help`: Show this help message and exit.
- `-a [AREA_NAME], --area [AREA_NAME]`:  
  Process a specific area or all areas individually. If `AREA_NAME` is provided, only that area is processed. If `-a` is used without `AREA_NAME`, all areas are processed individually, creating separate files for each area.
- `-i, --inbox`: Process only top-level items (Inbox, Today, Upcoming, Anytime, Someday) into a single 'inbox' file.

### Examples

1. **Process all projects under all areas and create an inbox file:**
   ```shell
   python Things_json-to-Todoist_csv.py things-all-output.json
   ```

2. **Process all projects and output to a specified directory:**
   ```shell
   python Things_json-to-Todoist_csv.py things-all-output.json output_directory
   ```

3. **Process only the specified area:**
   ```shell
   python Things_json-to-Todoist_csv.py things-all-output.json -a 'Area Name'
   ```

4. **Process each area individually, creating separate files for each:**
   ```shell
   python Things_json-to-Todoist_csv.py things-all-output.json -a
   ```

5. **Process only top-level items into an inbox file:**
   ```shell
   python Things_json-to-Todoist_csv.py things-all-output.json -i
```

### Todoist CSV Format Specification

For more information on formatting CSV files for Todoist, refer to the [Todoist CSV format specification](https://todoist.com/help/articles/format-a-csv-file-to-import-into-todoist).

