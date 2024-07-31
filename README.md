# things-cli 

[Github source](https://github.com/thingsapi/things-cli)

Start venv:

```shell
hschot@Hms1 Things-cli % source activate-things-venv.sh 
(.venv) hschot@Hms1 Things-cli %

things-cli --csv --recursive all > things-all-20240715.csv

things-cli -j --recursive all > things-all-20240717.json 

```

## Examples

```json

% things-cli inbox
 -  To-Do in Inbox with Checklist Items  ( Inbox )
 -  To-Do in Inbox  ( Inbox )

% things-cli --recursive areas
- Area 3 ()
  - Todo in Area 3 (Area 3)
- Area 2 ()
- Area 1 ()
  - Project in Area 1 (Area 1)
	- Todo in Area 1 (Project in Area 1)
	- Heading (Project in Area 1)
	  - To-Do in Heading (Heading)
  - To-Do in Area 1 (Area 1)

% things-cli --json today|jq
[
  {
	"uuid": "5pUx6PESj3ctFYbgth1PXY",
	"type": "to-do",
	"title": "To-Do in Today",
	"status": "incomplete",
	"notes": "With\nNotes",
	"start": "Anytime",
	"start_date": "2021-03-28",
	"deadline": null,
	"stop_date": null,
	"created": "2021-03-28 21:11:22",
	"modified": "2021-03-28 21:11:30"
  }
]

% things-cli --csv --recursive all > all.csv && open all.csv

% things-cli --opml --recursive all > all.opml && open all.opml

% things-cli --gantt --recursive all > all.mmd && mmdc -i all.mmd -o all.png && open all.png

% things-cli -h
usage: cli.py [-h] [-p FILTER_PROJECT] [-a FILTER_AREA] [-t FILTER_TAG] [-e] [-o] [-j] [-c] [-g] [-r] [-d DATABASE] [--version] command ...

Simple read-only Thing 3 CLI.

positional arguments:
  command
	inbox               Shows inbox tasks
	today               Shows todays tasks
	upcoming            Shows upcoming tasks
	anytime             Shows anytime tasks
	completed           Shows completed tasks
	someday             Shows someday tasks
	canceled            Shows canceled tasks
	trash               Shows trashed tasks
	todos               Shows all todos
	all                 Shows all tasks
	areas               Shows all areas
	projects            Shows all projects
	logbook             Shows completed tasks
	logtoday            Shows tasks completed today
	tags                Shows all tags ordered by their usage
	deadlines           Shows tasks with due dates
	feedback            Give feedback
	search              Searches for a specific task

optional arguments:
  -h, --help            show this help message and exit
  -p FILTER_PROJECT, --filter-project FILTER_PROJECT
						filter by project
  -a FILTER_AREA, --filter-area FILTER_AREA
						filter by area
  -t FILTER_TAG, --filtertag FILTER_TAG
						filter by tag
  -e, --only-projects   export only projects
  -o, --opml            output as OPML
  -j, --json            output as JSON
  -c, --csv             output as CSV
  -g, --gantt           output as mermaid-js GANTT
  -r, --recursive       in-depth output
  -d DATABASE, --database DATABASE
						set path to database
  --version, -v         show program's version number and exit

```

# Todoist spec

| COLUMN        | CONTENT                                                                                                    | DESCRIPTION                                                                                                                                                                                                                                                                                                            |
|---------------|------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TYPE          | task, section, or note (these are case-sensitive and should be written in lowercase)                       | Use task to add a task. Use section to add a section. Use note if you’re adding a comment to the task in the row above.                                                                                                                                                                                                 |
| CONTENT       | name of the task, name of the section, or content of the note                                              | Type the name of the task if you’re adding a task. (When creating a task, you can add labels by typing the @labelname as an addition to the name of the task.) Type the name of the section if you’re adding a section. Type the content of the note if you’re adding a comment.                                         |
| DESCRIPTION   | content of the task description                                                                            | Type the content of the task description if you'd like to add a description.                                                                                                                                                                                                                                            |
| PRIORITY      | 1, 2, 3, or 4                                                                                              | Type 1 to add p1 to the task (highest priority). Type 2 to add p2 to the task. Type 3 to add p3 to the task. Type 4 to add p4 to the task (lowest priority). Leaving this cell empty will automatically add p1 to the task.                                                                                             |
| INDENT        | 1, 2, 3 or 4                                                                                               | Use 1 and the task will not be indented (meaning the task is a parent task). Use 2 to indent the task to be a sub-task. Use 3 to indent the task to be a sub-sub-task. And so on. Leaving this cell empty will set the task to not be indented.                                                                          |
| AUTHOR        | username (ID)                                                                                              | Add the username + user ID in brackets of the person that created the task. For example, Evan (14781400). Leaving this cell empty will automatically add your name and ID.                                                                                                                                             |
| RESPONSIBLE   | username (ID)                                                                                              | Add the username + user ID in brackets of the person that you’d like to assign this task to. For example, Evan (14781400). Leaving this cell empty will not add an assignee to the task.                                                                                                                               |
| DATE          | due date and time or recurring due date and time                                                           | Add a due date and time if you want to schedule the task. You can also set a recurring due date. If you leave this cell empty, no due date will be assigned to the task.                                                                                                                                               |
| DATE_LANG     | Language code                                                                                              | Add the language code for the language of your Todoist app to set the due date (if any). These are the official Todoist language codes: cs for Czech. da for Danish. de for German. en for English. es for Spanish. fi for Finnish. fr for French. it for Italian. ja for Japanese. ko for Korean. nb for Norwegian. nl for Dutch. pl for Polish. pt_BR for Brazilian Portuguese. ru for Russian. sv for Swedish. zh_CN for Simplified Chinese. zh_TW for Traditional Chinese. |
| TIMEZONE      | Time zone                                                                                                  | Add the time zone that’s set for your Todoist account. (You can find your time zone under Settings > General.) For example, US/Eastern. Leaving this cell empty will have Todoist automatically detect your time zone.                                                                                                 |
| DURATION      | Number that represents the duration of a task                                                              | Add the estimated number of minutes it takes to work on a task. Leave this cell empty to not add a task duration.                                                                                                                                                                                                       |
| DURATION UNIT | minute or None                                                                                             | Specify the unit of measurement for the task duration. If there's no task duration, None will appear in this cell.                                                                                                                                                                                                      |
| meta          | view_style=board                                                                                           | Import the template in board layout.                                                                                                                                                                                                                                                                                    |