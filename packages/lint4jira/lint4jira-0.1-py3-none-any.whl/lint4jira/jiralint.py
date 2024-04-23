import argparse
import json
import os
from lint4jira.jirapi import JIRAI
from lint4jira.bcolors import BCOLORS
import curses

class JiraCLI:
    def __init__(self):
        self.config_path = os.path.expanduser("~/.lint4jira/config.json")
        self.rules_path = os.path.expanduser("~/.lint4jira/rules.json")
        self.config = self.load_config()
        self.rules = self.load_rules()
        self.jiraai = JIRAI(self.config, self.config_path)

    def load_config(self):
        try:
            if not os.path.exists(self.config_path):
                return self.initial_setup()
            with open(self.config_path, 'r') as config_file:
                return json.load(config_file)
        except Exception as e:
            print(f"Error loading configuration: {e}")
            default_config = {
                'JIRA_API_URL': '',
                'JIRA_API_USER': '',
            'JIRA_API_KEY': '',
            'JIRA_PROJECT': '',
            'JIRA_BOARD': '',
            'JIRA_STORY_POINT_FIELD': ''
            }
            with open(self.config_path, 'w') as config_file:
                json.dump(default_config, config_file)
            self.initial_setup()
            return default_config

    def clean_config(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
            BCOLORS.print_fail("Configuration cleaned.")

    def initial_setup(self):
        BCOLORS.print_header("Initial Setup")
        if input("Do you want to use email and password? (y/n): [Default: n] ").lower() == 'y':
            config = {
                'JIRA_API_URL': input('Enter JIRA API URL: '),
                'JIRA_API_USER': input('Enter JIRA username: '),
                'JIRA_API_PASSWORD': input('Enter JIRA password: '),
                'JIRA_PROJECT': input('Enter JIRA project key: '),
                'JIRA_BOARD': input('Enter JIRA board ID: ')
            }
        else:
            config = {
                'JIRA_API_URL': input('Enter JIRA API URL: '),
                'JIRA_API_USER': input('Enter JIRA username: '),
                'JIRA_API_KEY': input('Enter JIRA API key: '),
                'JIRA_PROJECT': input('Enter JIRA project key: '),
                'JIRA_BOARD': input('Enter JIRA board ID: ')
            }

        if not os.path.exists(os.path.dirname(self.config_path)):
            os.makedirs(os.path.dirname(self.config_path))
        with open(self.config_path, 'w') as config_file:
            json.dump(config, config_file)
        BCOLORS.print_success("Configuration saved.")
        return config

    def run(self):
        parser = argparse.ArgumentParser(description='JiraCLI Tool')
        parser.add_argument('--sprint', help='Name of the sprint to analyze')
        parser.add_argument('--set-project', action='store_true', help='Set project and board')
        parser.add_argument('--set-story-point', help='Set story point field')
        ### sub argument for sprint to list people story points
        parser.add_argument('--people', action='store_true', help='List people story points in a sprint')
        parser.add_argument('-s', action='store_true', help='Show success messages')
        parser.add_argument('-d', action='store_true', help='total day count for sprint')
        parser.add_argument('--sprints', action='store_true', help='List sprints')
        ### tasks with sprint name
        parser.add_argument('--tasks', help='List tasks in a sprint')
        parser.add_argument('--clean', action='store_true', help='Clean configuration')
        parser.add_argument('--setup', action='store_true', help='Initial setup')
        parser.add_argument('--version', action='version', version='%(prog)s 1.0')
        parser.add_argument('--task', help='Task key to analyze')
        parser.add_argument('--verbose', action='store_true', help='Show detailed information')
        args = parser.parse_args()
        if not any(vars(args).values()):
            parser.print_help()
            return
        if args.clean:
            self.clean_config()
            return
        if args.setup:
            self.initial_setup()
            return
        if args.set_project:
            self.set_project_args(args)
            return
        if args.set_story_point:
            self.set_story_point_args(args)
            return
        if args.sprints:
            try:
                self.sprints_args(args)
            except Exception as e:
                ### kanbna
                self.kanban_args(args)
            return
        if args.tasks:
            self.tasks_args(args)
            return
        if args.task:
            self.task_args(args)

        if args.sprint:
            self.sprint_args(args)

    def choose_project_and_set(self):
        return self.jiraai.choose_project_and_set()

    def choose_sprint_and_set(self):
        sprints = self.jiraai.choose_sprint()

    def status_print(self, result):
        BCOLORS.dot_line()
        BCOLORS.space(2)
        BCOLORS.print_header("Task Health")
        BCOLORS.print_success(f"Task Health: {result:.2f}%", result > 70)
        BCOLORS.print_warning(f"Task Health: {result:.2f}%", 50 < result <= 70)
        BCOLORS.print_fail(f"Task Health: {result:.2f}%", result <= 50)

    def task_args(self, args):
        task = self.jiraai.jira.issue(args.task)
        if task is None:
            BCOLORS.print_fail("Task not found.")
            return
        result = self.jiraai.calculate_task_health(task)
        self.status_print(result)

    def tasks_args(self, args):
        sprint = self.jiraai.get_sprint(args.tasks)
        tasks = self.jiraai.get_tasks_in_sprint(sprint)
        BCOLORS.print_header("Tasks")
        count = 0
        for task in tasks:
            count += 1
            sp = getattr(task.fields, self.config['JIRA_STORY_POINT_FIELD'], 0)
            BCOLORS.print_cross_color(f"{task.key} - {task.fields.summary} - {sp}", count % 2 == 0)
        BCOLORS.dot_line()

    def sprints_args(self, args):
        sprints = self.jiraai.get_sprints_without_closed()
        BCOLORS.print_header("Sprints")
        for sprint in sprints:
            print(f"* {sprint}")
        BCOLORS.dot_line()

    def set_story_point_args(self, args):
        self.jiraai.set_story_point_field()

    def set_project_args(self, args):
        self.choose_project_and_set()
        self.jiraai = JIRAI(self.config, self.config_path)
        BCOLORS.print_success("Project and board set.")

    def sprint_args(self, args):
        self.rules['is_detailed'] = False
        self.rules['is_story_point_show'] = False
        if args.people is True:
            self.rules['is_detailed'] = True
            self.rules['is_story_point_show'] = True
        self.rules['is_success_show'] = False
        if args.s:
            self.rules['is_success_show'] = True
        if args.verbose:
            self.rules['is_detailed'] = True
            self.rules['is_story_point_show'] = True
            self.rules['is_success_show'] = True

        total_day_count = 5
        if args.d:
            total_day_count = args.d
        try:
            issues = self.jiraai.get_sprint(args.sprint)
        except Exception as e:
            ### if kanban we cant see sprint
            issues = self.jiraai.get_board_tasks()
        if issues is None:
            BCOLORS.print_fail("Sprint not found.")
            return
        result = self.jiraai.calculate_sprint_health(issues,
                                                     options={'health_rate': 12, 'penalty_rate': 5,
                                                              'max_people_story_point_rate': 1.5,
                                                              'min_people_story_point_rate': 0.5,
                                                              'total_day_count': total_day_count},
                                                     rules=self.rules)
        BCOLORS.dot_line()
        BCOLORS.space(1)
        BCOLORS.print_header("Sprint Health")
        if result > 70:
            BCOLORS.print_success(f"Sprint Health: {result:.2f}%")
        elif result > 50:
            BCOLORS.print_warning(f"Sprint Health: {result:.2f}%")
        else:
            BCOLORS.print_fail(f"Sprint Health: {result:.2f}%")

    def load_rules(self):
        default_rules = {
            'is_detailed': True,
            'is_success_show': True,
            'is_show_people_story_point': True,
            'description_field': True,
            'story_point_field': True,
            'assignee_field': True,
            'status_field': True,
            'priority_field': True,
            'created_field': True,
            'updated_field': True,
            'too_big_story_point': True,
        }
        try:
            if not os.path.exists(self.rules_path):
                with open(self.rules_path, 'w') as rules_file:
                    json.dump(default_rules, rules_file)
            with open(self.rules_path, 'r') as rules_file:
                return json.load(rules_file)
        except Exception as e:
            print(f"Error loading rules: {e}")
            with open(self.rules_path, 'w') as rules_file:
                json.dump(default_rules, rules_file)
            self.load_rules()
            return default_rules

    def kanban_args(self, args):
        BCOLORS.dot_line()
        BCOLORS.print_header("Kanban Board")
        board = self.jiraai.get_boards()



def main():
    cli = JiraCLI()
    cli.run()
