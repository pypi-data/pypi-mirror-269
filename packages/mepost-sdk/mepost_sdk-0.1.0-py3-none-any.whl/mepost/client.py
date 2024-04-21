import requests

class MepostClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.mepost.io/v1'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        }

    def send_email(self, email_data):
        """Send an email using the Mepost API."""
        url = f"{self.base_url}/messages/send"
        response = requests.post(url, json=email_data, headers=self.headers)
        return response.json()

    def send_email_by_template(self, email_data, template_id):
        """Send an email using a template."""
        url = f"{self.base_url}/messages/send-by-template"
        data = {'message': email_data, 'templateId': template_id}
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    def get_info(self, schedule_id, email):
        """Retrieve information about a specific scheduled message."""
        url = f"{self.base_url}/messages/{schedule_id}/{email}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def cancel_scheduled_message(self, scheduled_message_id):
        """Cancel a scheduled message."""
        url = f"{self.base_url}/messages/cancel-scheduled"
        data = {'scheduledMessageId': scheduled_message_id}
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    def get_scheduled_message(self, schedule_id):
        """Retrieve a scheduled message."""
        url = f"{self.base_url}/messages/schedule/{schedule_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()
