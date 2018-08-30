import re

import pandas as pd
from jira import JIRA

# Fill those manually
JIRA_SERVER=''
JIRA_BASIC_AUTH=('', '')  # user | password / token
CSV_FILE='sample_report.csv'  # Extracted Toggl csv report
XLSX_FILE='final_report.xlsx'


jira = JIRA(server=JIRA_SERVER, basic_auth=JIRA_BASIC_AUTH)

def extract_issue_number(row):
    number = "n/a"
    m = re.search(r"(\D+)-(\d+)", row['Description'])

    if len(m.groups()) > 0:
        number = m.group(0)

    return number

def extract_jira_data(row):
    issue = jira.issue(row['Issue'])

    component = ""
    estimation = 0.0

    if len(issue.fields.components) > 0:
        component = issue.fields.components[0]

    if issue.fields.timeoriginalestimate:
        estimation = issue.fields.timeoriginalestimate / 60.0 / 60.0

    return [component, estimation]

if __name__ == '__main__':
    df = pd.read_csv(CSV_FILE)

    df['Issue'] = df.apply(extract_issue_number, axis=1)
    df[['Component', 'Estimation (MH)']] = df.apply(extract_jira_data, axis=1, result_type='expand')

    df.to_excel(XLSX_FILE)