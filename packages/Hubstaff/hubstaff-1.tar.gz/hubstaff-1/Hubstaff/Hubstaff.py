import requests
import sys

class Connect:
    def __init__(self , personal_access_tokens):
        url = "https://account.hubstaff.com/access_tokens"
        headers = {}
        data = {
            "grant_type": "refresh_token" ,
            "refresh_token": personal_access_tokens
        }
        response = requests.post(url , headers=headers , data=data)

        if response.status_code == 200:
            self.access_token = response.json().get("access_token")
            url = f'https://api.hubstaff.com/v2/organizations'
            headers = {'Authorization': f'Bearer {self.access_token}'}
            response = requests.get(url , headers=headers)
            if response.status_code == 200:
                organization_info = response.json()
                for i in organization_info['organizations']:
                    self.organization_id = i["id"]
            else:
                print('Error while authenticating')
                sys.exit()

    def get_projects_data(self):
        url = f'https://api.hubstaff.com/v2/organizations/' + str(self.organization_id) + '/projects'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.get(url , headers=headers)

        if response.status_code == 200:
            project_info = response.json()
            project_data = []
            for i in project_info['projects']:
                id = i['id']
                name = i['name']
                project = dict(id=id , name=name)
                project_data.append(project)
            return project_data



