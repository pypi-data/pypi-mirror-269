import curses
import json

from jira import JIRA

from lint4jira.selector import Selector
from lint4jira import bcolors

class JIRAI:
    def __init__(self, config: dict, config_path):
        self.config = config
        self.config_path = config_path
        if config['JIRA_API_KEY']:
            self.jira = JIRA(server=config['JIRA_API_URL'], basic_auth=(config['JIRA_API_USER'], config['JIRA_API_KEY']))
        else:
            self.jira = JIRA(server=config['JIRA_API_URL'], basic_auth=(config['JIRA_API_USER'], config['JIRA_API_PASSWORD']))
        self.sprints = {}
        self.current_sprint = None
        if 'JIRA_STORY_POINT_FIELD' not in config:
            self.set_story_point_field()
        self.story_point_field = config['JIRA_STORY_POINT_FIELD']


    def calculate_task_health(self, task):
        print(f"Calculating Task Health for {task.key}")
        total_health = 100
        total_start_health = total_health
        is_failed = False
        if task.fields.assignee is None:
            bcolors.print_warning(f"{task.key} task has no assignee")
            total_health -= 5
            is_failed = True
        else:
            bcolors.print_success(f"{task.key} task has assignee")
        if getattr(task.fields, self.story_point_field, 0) == 0:
            bcolors.print_warning(f"{task.key} task has no story point")
            total_health -= 5
            is_failed = True
        else:
            bcolors.print_success(f"{task.key} task has story point")
        if task.fields.description is None or len(task.fields.description) < 280:
            bcolors.print_warning(f"{task.key} task has no description")
            total_health -= 5
            is_failed = True
        else:
            bcolors.print_success(f"{task.key} task has description")
            if "Definition of Ready" not in task.fields.description:
                bcolors.print_warning(f"{task.key} task has no definition of ready")
                total_health -= 2.5
                is_failed = True
            else:
                bcolors.print_success(f"{task.key} task has acceptance criteria")
            ### Definition of Done is exist on the description
            if "Definition of Done" not in task.fields.description:
                bcolors.print_warning(f"{task.key} task has no definition of done")
                total_health -= 2.5
                is_failed = True
            else:
                bcolors.print_success(f"{task.key} task has definition of done")
        return total_health

    def get_sprints(self):
        sprints = self.jira.sprints(self.config['JIRA_BOARD'])
        for sprint in sprints:
            self.sprints[sprint.name] = sprint
        return self.sprints

    def get_sprints_without_closed(self):
        sprints = self.jira.sprints(self.config['JIRA_BOARD'], state='active,future')
        for sprint in sprints:
            self.sprints[sprint.name] = sprint
        return self.sprints


    def get_sprint(self, sprint_name):
        issues = self.jira.search_issues(f'project={self.config["JIRA_PROJECT"]} AND sprint="{sprint_name}"')
        return issues

    def get_tasks_in_sprint(self, sprint):
        issues = self.jira.search_issues(f'project={self.config["JIRA_PROJECT"]} AND sprint={sprint.id}')
        return issues

    def get_tasks_backlog(self, sprint):
        issues = self.jira.search_issues(f'project={self.config["JIRA_PROJECT"]} AND sprint!={sprint.id}')
        return issues

    def get_unique_people_in_sprint(self, issues):
        people = set()
        for issue in issues:
            if issue.fields.assignee:
                people.add(issue.fields.assignee.displayName)
        return people

    def calculate_sprint_health(self, issues, options: dict, rules:dict):
        total_issues = 0

        people = self.get_unique_people_in_sprint(issues)
        map_people = {}
        map_people_task_count = {}
        total_story_points = 0
        for person in people:
            try:
                if person is None:
                    continue
                map_people[person] = 0
                map_people_task_count[person] = 0
            except:
                bcolors.print_error(f"{person} has no display name")
        total_health = len(issues) * options['health_rate']
        total_start_health = total_health

        bcolors.print_header(f"Details of Sprint")
        for issue in issues:
            if rules['is_detailed']:
                bcolors.dot_line()
                bcolors.print_bold(f"{issue.key} - {issue.fields.summary}")
                bcolors.print_info(f"Assignee: {issue.fields.assignee.displayName}")
                bcolors.dot_line()
            is_failed = False
            if issue.fields.assignee is None:
                bcolors.print_warning(f"{issue.key} task has no assignee")
                total_health -= options['penalty_rate']
                is_failed = True
                total_issues += 1
            elif rules['is_success_show']:
                bcolors.print_success(f"{issue.key} task has assignee")

            sp = getattr(issue.fields, self.story_point_field, 0)
            if sp == 0 or sp is None:
                bcolors.print_warning(f"{issue.key} task has no story point")
                total_health -= options['penalty_rate']
                is_failed = True
                total_issues += 1
            else:
                if issue.fields.assignee:
                    map_people[issue.fields.assignee.displayName] += float(sp)
                    map_people_task_count[issue.fields.assignee.displayName] += 1
                total_story_points += float(sp)
                if rules['is_success_show']:
                    bcolors.print_success(f"{issue.key} task has story point")

            if issue.fields.description is None or len(issue.fields.description) < 280:
                bcolors.print_warning(f"{issue.key} task has no description")
                total_health -= options['penalty_rate']
                is_failed = True
                total_issues += 1
            elif rules['is_success_show']:
                    bcolors.print_success(f"{issue.key} task has description")

            if issue.fields.description is None or "Definition of Ready" not in issue.fields.description:
                bcolors.print_warning(f"{issue.key} task has no definition of ready")
                total_health -= 2.5
                is_failed = True
                total_issues += 1
            elif rules['is_success_show']:
                bcolors.print_success(f"{issue.key} task has definition of ready")

            if issue.fields.description is None or "Definition of Done" not in issue.fields.description:
                bcolors.print_warning(f"{issue.key} task has no definition of done")
                total_health -= options['penalty_rate']/2
                is_failed = True
                total_issues += 1
            elif rules['is_success_show']:
                bcolors.print_success(f"{issue.key} task has definition of done")

            if is_failed or rules['is_success_show']:
               bcolors.dot_line()

        if total_issues == 0:
            bcolors.print_success(f"Sprint has no issue")

        if rules['is_show_people_story_point']:
            bcolors.space(1)
            bcolors.print_header("People Story Points")
            ### sort people by story points
            people = sorted(people, key=lambda x: map_people[x], reverse=True)
            for person in people:
                bcolors.print_info(f"{person} has {map_people[person]} story points")
            count_people = len(people)
            if count_people != 0:
                people_story_check = True
                bcolors.space(1)
                bcolors.print_header("People Story Check Result")
                avg_story_point = total_story_points / len(people)
                for person in map_people:
                    is_failed = self.enough_story_point(map_people[person], avg_story_point, options['max_people_story_point_rate'], options['min_people_story_point_rate'])
                    is_failed = self.enough_story_count(map_people_task_count[person], total_issues, count_people)
                    people_story_check = is_failed and not people_story_check
                    if not is_failed and rules['is_success_show']:
                        bcolors.print_success(f"{person} has enough story points", )

                if people_story_check:
                    bcolors.print_success("People Story Check is OK")


        return total_health * 100 / total_start_health

    def get_projects(self):
        projects = self.jira.projects()
        project_map = {}
        for project in projects:
            project_map[project.key] = project.id
        return project_map

    def get_fields(self):
        return self.jira.fields()

    def set_story_point_field(self):
        fields = self.get_fields()
        field_map = {}
        for field in fields:
            field_map[field['name']] = field['id']
        story_point_field_key = curses.wrapper(Selector.select_field, field_map)
        self.config['JIRA_STORY_POINT_FIELD'] = field_map[story_point_field_key]
        ### write to config file
        with open(self.config_path, 'w') as config_file:
            json.dump(self.config, config_file)
        return

    def choose_sprint(self):
        sprints = self.get_sprints_without_closed()
        sprint_key = curses.wrapper(Selector.select_field, self.sprints)
        self.current_sprint = self.sprints[sprint_key]
        pass

    def choose_project_and_set(self):
        projects = self.get_projects()
        project_key = curses.wrapper(Selector.select_field, projects)
        print(f"Project Key: {project_key}")
        print(f"Project: {projects[project_key]}")
        self.config['JIRA_PROJECT'] = projects[project_key]
        boards = self.jira.boards(projectKeyOrID=project_key)
        board_map = {}
        for board in boards:
            board_map[board.name] = board.id
        board_key = curses.wrapper(Selector.select_field, board_map)
        print(f"Board Key: {board_key}")
        print(f"Board: {board_map[board_key]}")
        self.config['JIRA_BOARD'] = board_map[board_key]
        with open(self.config_path, 'w') as config_file:
            json.dump(self.config, config_file)

    def enough_story_point(self, person, avg_story_point, min_story, max_story, min_rate=0.5, max_rate=1.5):
        is_failed = False
        if person < avg_story_point * min_rate or person < min_story:
            bcolors.print_warning(f"{person} has too few story points")
            is_failed = True
        elif person > avg_story_point * max_rate and person > max_story:
            bcolors.print_warning(f"{person} has too many story points")
            is_failed = True

        return is_failed

    def enough_story_count(self, person, total_issues, count_people, bufffer_rate=0.2):
        is_failed = False
        avg_story_count = total_issues / count_people
        if person < avg_story_count * (1 - bufffer_rate):
            bcolors.print_warning(f"{person} has too few story count")
            is_failed = True
        elif person > avg_story_count * (1 + bufffer_rate):
            bcolors.print_warning(f"{person} has too many story count")
            is_failed = True
        return is_failed
        pass

    def get_boards(self):
        boards = self.jira.boards(projectKeyOrID=self.config['JIRA_PROJECT'])
        board_map = {}
        for board in boards:
            bcolors.print_cross_color(f"{board.name} - {board.id}", True)
            board_map[board.name] = board.id

        return board_map

    def get_board_tasks(self):
        issues = self.jira.search_issues(f'project={self.config["JIRA_PROJECT"]} AND statusCategory != Done')
        return issues
