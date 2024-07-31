import json
import csv
import sys
import os
import re
import argparse

def sanitize_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename.replace(' ', '_')
    return filename

class CSVWriter:
    def __init__(self, base_filename, output_dir):
        self.base_filename = base_filename
        self.output_dir = output_dir
        self.file_counter = 1
        self.task_count = 0
        self.section_count = 0
        self.current_writer = None
        self.current_file = None
        self.create_new_file()

    def create_new_file(self):
        if self.current_file:
            self.current_file.close()
        filename = f"{self.base_filename}_{self.file_counter}.csv"
        filepath = os.path.join(self.output_dir, filename)
        self.current_file = open(filepath, 'w', newline='', encoding='utf-8')
        self.current_writer = csv.writer(self.current_file)
        self.current_writer.writerow([
            'TYPE', 'CONTENT', 'DESCRIPTION', 'PRIORITY', 'INDENT', 'AUTHOR',
            'RESPONSIBLE', 'DATE', 'DATE_LANG', 'TIMEZONE', 'DURATION', 'DURATION_UNIT'
        ])
        self.task_count = 0
        self.section_count = 0
        self.file_counter += 1
        print(f"Created file: {filepath}")

    def write_row(self, row_type, *args):
        if (row_type == 'task' and self.task_count >= 280) or \
           (row_type == 'section' and self.section_count >= 20):
            self.create_new_file()
        
        self.current_writer.writerow(args)
        
        if row_type == 'task':
            self.task_count += 1
        elif row_type == 'section':
            self.section_count += 1

    def close(self):
        if self.current_file:
            self.current_file.close()

def write_section(writer, title):
    writer.write_row('section', '', '', '', '', '', '', '', '', '', '', '', '')  # Insert empty row before section
    writer.write_row('section', 'section', title.strip(), '', '', '', '', '', '', '', '', '')

def process_item(csv_writer, item, parent_indent, is_specific_area=False):
    item_type = item['type']
    indent = parent_indent + 1

    if item_type == 'heading' and not is_specific_area:
        write_section(csv_writer, item['title'])
        for sub_item in item.get('items', []):
            process_item(csv_writer, sub_item, 0, is_specific_area)
    elif item_type == 'project' and is_specific_area:
        write_section(csv_writer, item['title'])
        for sub_item in item.get('items', []):
            process_item(csv_writer, sub_item, 0, is_specific_area)
    elif item_type in ['to-do', 'project', 'heading']:
        content = item['title'].strip()
        if item_type == 'heading' and is_specific_area:
            content = f"***{content}*** @Section"
        if 'tags' in item and item['tags']:
            content += ' ' + ' '.join(f'@{tag}' for tag in item['tags'])
        description = item.get('notes', '').strip()
        priority = str(map_priority(item.get('priority', 'low')))
        author = ''  # Default author
        date = item.get('start_date', '')
        
        csv_writer.write_row('task', 'task', content, description, priority, str(indent), author, '',
                             date, 'en', 'Europe/Zurich', '', '')

        checklist = item.get('checklist', [])
        for checklist_item in checklist:
            process_checklist_item(csv_writer, checklist_item, indent)

        for sub_item in item.get('items', []):
            process_item(csv_writer, sub_item, indent, is_specific_area)

def process_checklist_item(csv_writer, checklist_item, parent_indent):
    indent = parent_indent + 1
    content = checklist_item.get('title', '').strip()
    status = checklist_item.get('status')
    
    if status == 'completed':
        content += ' @✔️\ completed'
    
    csv_writer.write_row('task', 'task', content, '', '4', str(indent), '', '', '', '', '', '')

def map_priority(priority):
    priority_map = {
        'low': 4,
        'medium': 3,
        'high': 2,
        'urgent': 1
    }
    return priority_map.get(priority.lower(), 4)

def find_areas(data):
    """Recursively find all items of type 'area' in the data."""
    areas = []
    if isinstance(data, dict):
        if data.get('type') == 'area':
            areas.append(data)
        for value in data.values():
            areas.extend(find_areas(value))
    elif isinstance(data, list):
        for item in data:
            areas.extend(find_areas(item))
    return areas

def process_top_level_items(data, csv_writer):
    top_level_categories = ["Inbox", "Upcoming", "Anytime", "Someday"]
    # all "Today" items are also in "Anytime".

    for item in data:
        if isinstance(item, dict) and item.get('title') in top_level_categories:
            for sub_item in item.get('items', []):
                if 'project' not in sub_item and 'heading' not in sub_item and 'area' not in sub_item:
                    # Add '🗄️ Someday' tag for items in the Someday category
                    if item['title'] == "Someday":
                        sub_item['title'] += ' @🗄️\ Someday'
                    process_item(csv_writer, sub_item, 0)

def convert_json_to_csv(json_file, output_dir, specific_area=None, inbox_only=False, process_all_areas=False):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    os.makedirs(output_dir, exist_ok=True)
    
    if inbox_only:
        # Process only top-level items
        inbox_writer = CSVWriter('inbox', output_dir)
        process_top_level_items(data, inbox_writer)
        inbox_writer.close()
    else:
        areas = find_areas(data)
    
        if not areas:
            print("No areas found in the JSON file.")
            return
    
        if process_all_areas:
            for area in areas:
                area_title = area['title'].strip()
                base_filename = sanitize_filename(area_title)
                csv_writer = CSVWriter(base_filename, output_dir)
                for item in area.get('items', []):
                    process_item(csv_writer, item, 0, is_specific_area=True)
                csv_writer.close()
                print(f"Processed area: {area_title}")
        elif specific_area:
            area = next((a for a in areas if a['title'].strip() == specific_area.strip()), None)
            if not area:
                print(f"No area found with the title '{specific_area}'.")
                return
            
            base_filename = sanitize_filename(specific_area.strip())
            csv_writer = CSVWriter(base_filename, output_dir)
            for item in area.get('items', []):
                process_item(csv_writer, item, 0, is_specific_area=True)
            csv_writer.close()
        else:
            # Process all areas and their projects
            for area in areas:
                area_title = area['title'].strip()
                for item in area.get('items', []):
                    if item['type'] == 'project':
                        project_title = item['title'].strip()
                        base_filename = sanitize_filename(f"{area_title}-_-{project_title}")
                        csv_writer = CSVWriter(base_filename, output_dir)
                        for sub_item in item.get('items', []):
                            process_item(csv_writer, sub_item, 0)
                        csv_writer.close()
            
            # Process top-level items
            inbox_writer = CSVWriter('inbox', output_dir)
            process_top_level_items(data, inbox_writer)
            inbox_writer.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Things 3 JSON export to CSV files. "
                    "By default (without -a or -i options), the script processes all projects "
                    "under all areas, creating separate CSV files for each project, "
                    "and also processes top-level items into an 'inbox' file.\n\n"
                    "To obtain the JSON file from Things 3:\n"
                    "1. Install things-cli: https://github.com/thingsapi/things-cli\n"
                    "2. Run the following command to generate the JSON file:\n"
                    "   things-cli -j --recursive all > things-all-output.json\n"
                    "   (Replace 'things-all-output.json' with your desired filename)\n\n"
                    "To import into Todoist, drag and drop one of the generated csv files into a Todoist project.\n"
                    "Also see: \n"
                    "   https://todoist.com/help/articles/introduction-to-backups\n"
                    "   https://todoist.com/help/articles/import-or-export-todoist-project-templates\n",
        epilog="Examples:\n"
               "  python Things_json-to-Todoist_csv.py things-all-output.json\n"
               "    (Process all projects under all areas and create an inbox file)\n"
               "  python Things_json-to-Todoist_csv.py things-all-output.json output_directory\n"
               "    (Same as above, but output to specified directory)\n"
               "  python Things_json-to-Todoist_csv.py things-all-output.json -a 'Area Name'\n"
               "    (Process only the specified area)\n"
               "  python Things_json-to-Todoist_csv.py things-all-output.json -a\n"
               "    (Process each area individually, creating separate files for each)\n"
               "  python Things_json-to-Todoist_csv.py things-all-output.json -i\n"
               "    (Process only top-level items into an inbox file)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("input_json", 
                        help="Path to the input JSON file exported from Things 3 using things-cli")
    
    parser.add_argument("output_dir", 
                        nargs='?', 
                        default=os.getcwd(), 
                        help="Output directory for CSV files (default: current directory)")
    
    parser.add_argument("-a", "--area", 
                        nargs='?', 
                        const=True, 
                        metavar="AREA_NAME",
                        help="Process a specific area or all areas individually. "
                             "If AREA_NAME is provided, only that area is processed. "
                             "If -a is used without AREA_NAME, all areas are processed individually, "
                             "creating separate files for each area.")
    
    parser.add_argument("-i", "--inbox", 
                        action="store_true", 
                        help="Process only top-level items (Inbox, Today, Upcoming, Anytime, Someday) "
                             "into a single 'inbox' file.")
    
    args = parser.parse_args()
    
    # Ensure the output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    process_all_areas = args.area is True
    specific_area = args.area if isinstance(args.area, str) else None
    
    convert_json_to_csv(args.input_json, args.output_dir, specific_area, args.inbox, process_all_areas)
    print(f"Conversion complete. Output files are in: {args.output_dir}")