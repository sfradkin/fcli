from fc.jira import tasks
from .task import Task
from datetime import datetime
from ..auth.auth import Auth
from . import tasks


class TriageTask(Task):

    def __init__(self, a_task: Task):
        self.title = a_task.title
        self.description = a_task.description
        self.id = a_task.id
        self.url = a_task.url
        self.type = a_task.type
        self.state = a_task.state
        self.auth = a_task.auth

    @classmethod
    def from_json(cls, json: dict, auth: Auth):
        return TriageTask(Task.from_json(json, auth))

    @classmethod
    def from_args(cls, title: str, description: str, in_progress: bool, no_assign: bool, importance: str,
                  level_of_effort: str, due_date: datetime, auth: Auth):
        new_task = TriageTask(Task.from_args(title, description, auth))

        new_task.in_progress = in_progress
        new_task.no_assign = no_assign
        new_task.importance = importance
        new_task.level_of_effort = level_of_effort
        new_task.due_date = due_date

        new_task._modify_description_for_parameters(new_task.importance, new_task.level_of_effort, new_task.due_date)

        return new_task

    def create(self):
        super(TriageTask, self).create()

        self._update_vfr()

        if self.in_progress:
            self._transition(self.transition_id_for_triage_ready)
            self._transition(self.transition_id_for_start_progress)

        return self.id, self.url

    def type_str(self) -> str:
        return 'Triage'

    def _extra_json_for_create(self, existing_json: dict):
        existing_json['fields']['issuetype'] = {
            'name': 'Triage Task'
        }

        if not self.no_assign:
            existing_json['fields']['assignee'] = {
                'name': self.auth.username()
            }

    def _modify_description_for_parameters(self, importance: str, level_of_importance: str, due_date: datetime):
        additional_description = 'Importance: {}\r\n\r\nLOE: {}\r\n\r\nDate needed: {}'\
            .format(importance, level_of_importance, due_date.strftime('%m/%d/%Y'))
        self.description = self.description + '\r\n\r\n' + additional_description + '\r\n\r\n'

    def _update_vfr(self):
        issue_json = tasks.get_issue(self.api_url, self.id, self.auth)
        tasks.score(issue_json, self.auth)
