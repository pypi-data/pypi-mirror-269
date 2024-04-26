from jira import JIRA

class JiraApi:

    def __init__(self, url, username, password):
        self.jira = JIRA(url, basic_auth=(username, password))

    def get_issue(self, issue_key):
        return self.jira.issue(issue_key)

    def get_open_issues(self, project_key, team=None):
        if team is None:
            return self.jira.search_issues(f'project = {project_key} and status in (open, reopened)')
        else:
            return self.jira.search_issues(f'project = {project_key} '
                                           f'and status in (open, reopened) and cf[10108] = "{team}"')

    def create_issue(self, project, title, description, team):
        return self.jira.create_issue(
            project=project,
            summary=title,
            description=description,
            customfield_10108={'value': team},
            issuetype={'name': 'Task'}
        )

    def add_comment(self, issue_key, comment):
        return self.jira.add_comment(issue_key, comment)

    def get_transitions(self, issue_key):
        return self.jira.transitions(issue_key)

    def update_state_of_issue(self, issue_key, state):
        return self.jira.transition_issue(issue=issue_key, transition=state)






