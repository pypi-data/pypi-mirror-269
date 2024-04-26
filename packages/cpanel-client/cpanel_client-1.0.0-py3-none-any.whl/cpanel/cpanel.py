import requests
from .utils import generate_random_password, convert_domain_to_username


class ServerAPI(object):
    """
    This class interact with cPanel API
    """

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/50.0.2661.102 Safari/537.36'}

    def __init__(self, *args) -> None:
        self.username = args[0]
        self.password = args[1]
        self.url = args[2]
        self.port = str(args[3])

    def create_account(self, *args):
        email = args[0]
        domain = args[1]
        hosting_package = args[2]

        # create username from domain
        user_user = convert_domain_to_username(domain)
        pass_pass = generate_random_password()

        url = self.url + ':' + self.port + '/json-api/createacct'
        payload = {'username': user_user, 'password': pass_pass,
                   'domain': domain, 'plan': hosting_package,
                   'contactemail': email, 'api.version': '1'}

        try:
            r = requests.get(url, auth=(self.username, self.password), params=payload, headers=self.headers)
            success = 0
            if r.status_code == 200:
                json = r.json()
                # print json
                json_data = json['metadata']
                json_msg = json_data['reason']

                raw_html = None
                if json_data['result'] == 1:
                    json_output = json_data['output']
                    raw_html = json_output['raw']  # get html with account info
                    success = 1  # everything ok

            return dict({'success': success, 'username': user_user,
                         'message': json_msg, 'data': raw_html})
        except requests.exceptions.RequestException as e:
            return dict({'success': 0, 'message': str(e), 'data': None})

    def suspend_account(self, c_user):
        url = self.url + ':' + self.port + '/json-api/suspendacct'
        payload = {'user': str(c_user).lower(), 'reason': 'No Payment', 'api.version': '1'}

        try:
            r = requests.get(url, auth=(self.username, self.password),
                             params=payload, headers=self.headers)

            success = 0
            if r.status_code == 200:
                json = r.json()

                json_data = json['metadata']
                json_msg = json_data['reason']

                if json_data['result'] == 1:
                    success = 1  # everything ok

            return dict({'success': success, 'message': json_msg})
        except requests.exceptions.RequestException as e:
            return dict({'success': 0, 'message': str(e), 'data': None})

    def terminate_account(self, c_user):
        url = self.url + ':' + self.port + '/json-api/removeacct'
        payload = {'user': str(c_user).lower(), 'api.version': '1'}

        try:
            r = requests.get(url, auth=(self.username, self.password),
                             params=payload, headers=self.headers)

            success = 0
            if r.status_code == 200:
                json = r.json()

                json_data = json['metadata']
                json_msg = json_data['reason']

                if json_data['result'] == 1:
                    success = 1  # everything ok

            return dict({'success': success, 'message': json_msg})
        except requests.exceptions.RequestException as e:
            return dict({'success': 0, 'message': str(e), 'data': None})
