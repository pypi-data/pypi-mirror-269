import requests
import os
import json
import xml.etree.ElementTree as ET
from icecream import ic
from dotenv import load_dotenv

# Load environment variables from .env file just once
load_dotenv()

class DataAccess:
    def __init__(self, access_token, school_id, base_url, queries_root_path, xml_file_name, max_retries=3):
        self.access_token = access_token
        self.school_id = school_id
        self.base_url = base_url
        self.queries_root_path = queries_root_path
        self.xml_file_name = xml_file_name
        self.max_retries = max_retries
        self.queries = {}  # Initialize to an empty dictionary
        self.load_queries()

    def load_queries(self):
        queries_path = os.path.join(self.queries_root_path, self.xml_file_name)
        try:
            tree = ET.parse(queries_path)
            root = tree.getroot()
            for query in root.findall('query'):
                full_name = query.get('name')
                if full_name:
                    self.queries[full_name] = f"{self.base_url}/ws/schema/query/{full_name}"
            # Log loaded queries to debug
            ic(f"Loaded queries: {list(self.queries.keys())}")
        except FileNotFoundError:
            ic(f"File not found: {queries_path}")
        except ET.ParseError as e:
            ic(f"Error parsing XML: {e}")


    def fetch_data(self, last_part_query_name, json_body=None, method='GET'):
        endpoint = self.queries.get(last_part_query_name)
        if not endpoint:
            ic(f"Query not found: {last_part_query_name}. Available queries: {self.queries.keys()}")
            raise ValueError(f"No matching endpoint found for query part: {last_part_query_name}.")

        retries = 0
        while retries < self.max_retries:
            try:
                response = self.make_api_request(endpoint, json_body, method)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                ic(f"Error occurred: {str(e)}")
                retries += 1
        return None

    def make_api_request(self, endpoint, json_body, method):
        headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
        }

        if method.upper() == 'POST':
            response = requests.post(endpoint, headers=headers, json=json_body)  # Use json parameter directly
        else:
            # For GET, assuming json_body should actually be URL parameters
            response = requests.get(endpoint, headers=headers, params=json_body)  # Use params for GET requests

        return response

class StandardAccess:
    def __init__(self, access_token, base_url, max_retries=3):
        self.access_token = access_token
        self.base_url = base_url
        self.max_retries = max_retries

    def fetch_data(self, endpoint, params=None, method='GET', headers=None):
        retries = 0
        while retries < self.max_retries:
            try:
                response = self.make_api_request(endpoint, params, method, headers)
                response.raise_for_status()
                return response.json() if response.content else None
            except Exception as e:
                print(f"Error occurred: {str(e)}")
                retries += 1
        return None

    def make_api_request(self, endpoint, params, method, additional_headers):
        headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
        }

        if additional_headers:
            headers.update(additional_headers)

        full_url = f"{self.base_url}/{endpoint}"

        if method.upper() == 'POST':
            response = requests.post(full_url, headers=headers, data=json.dumps(params))
        elif method.upper() == 'PUT':
            response = requests.put(full_url, headers=headers, data=json.dumps(params))
        else:  # Default to GET
            response = requests.get(full_url, headers=headers, params=params)

        return response
