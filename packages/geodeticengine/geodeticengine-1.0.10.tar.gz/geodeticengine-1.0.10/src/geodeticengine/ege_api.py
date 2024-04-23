import json
import requests
import os
from functools import wraps
from typing import Literal
from .AuthBearerToken import AuthBearerToken
from dotenv import load_dotenv
load_dotenv(override=True)


class InputException(ValueError):
    pass

class AuthenticationError(ValueError):
    pass

class EndpointException(ValueError):
    pass




def trim_all_whitespace(string):
    return string.strip()

def strip_arguments(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        new_args = tuple(trim_all_whitespace(arg) if isinstance(arg, str) else arg for arg in args)
        new_kwargs = {k: trim_all_whitespace(v) if isinstance(v, str) else v for k, v in kwargs.items()}
        return func(*new_args, **new_kwargs)
    return wrapper




class EGE:
    """
    Singleton Class for communicating with the Geodetic Engine API
    """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EGE, cls).__new__(cls)
            cls.instance.initialize()
        return cls.instance

    def initialize(self):
        self.EGE_API_ENV = os.getenv('EGE_API_ENV', 'prod')  # set "prod" as default if not defined
        if self.EGE_API_ENV in ('test', 'dev'):
            self.GE_API = f"https://api-{self.EGE_API_ENV}.gateway.equinor.com/geodetic-engine/v1"
        else:
            self.GE_API = "https://api.gateway.equinor.com/geodetic-engine/v1"

        self.GE_ENDPOINT_TRANSFORMATION = f"{self.GE_API}/transform"
        self.GE_WKT_ENDPOINT = f'{self.GE_API}/crs/wkt'
        self.GE_VALIDATE_ENDPOINT = f'{self.GE_API}/validate'
        if self.EGE_API_ENV in ('test', 'dev'):
            self.GE_CRS_SEARCH_ENDPOINT = f'{self.GE_API}/crs/search'
            self.GE_CT_SEARCH_ENDPOINT = f'{self.GE_API}/ct/search'
        self.auth = AuthBearerToken()

    @strip_arguments
    def get_pipeline(self, crs_from, crs_to):
        """Request transformation pipeline"""
        input_params = {'crs_from': crs_from, 'crs_to': crs_to}
        response = self.call_endpoint(self.GE_ENDPOINT_TRANSFORMATION, 'post', input_params)
        return response

    @strip_arguments
    def transform_crs(self, points, crs_from, crs_to):
        """Transform points"""
        input_params = {'coordinates_from': points, 'crs_from': crs_from, 'crs_to': crs_to}
        response = self.call_endpoint(self.GE_ENDPOINT_TRANSFORMATION, 'post', input_params)
        return response

    @strip_arguments
    def crs_search(self, types, polygon_coords, target_crs):
        """Search CRSs"""
        input_params = {'types': types, 'polygon_coords': polygon_coords, 'target_crs': target_crs}
        response = self.call_endpoint(self.GE_CRS_SEARCH_ENDPOINT, 'post', input_params)
        return response

    @strip_arguments
    def ct_search(self, types, polygon_coords, source_crs, target_crs):
        """Query CTs"""
        input_params = {'types': types, 'polygon_coords': polygon_coords, 'source_crs': source_crs, 'target_crs': target_crs}
        response = self.call_endpoint(self.GE_CT_SEARCH_ENDPOINT, 'post', input_params)
        return response

    def validate_input(self, user_input):
        """
        Validate user input using
        the API validate endpoint
        """
        endpoint = f"{self.GE_VALIDATE_ENDPOINT}?input={user_input}"
        response = self.call_endpoint(endpoint, 'get')
        return response

    @strip_arguments
    def request_wkt_for_crs(self, crs:str, wkt_version: Literal["WKT1_ESRI", "WKT1_GDAL", "WKT2_2019"]):
        """Request WKT for a CRS"""
        url = f"{self.GE_WKT_ENDPOINT}?input={crs}&wkt_version={wkt_version}"
        return self.call_endpoint(url, 'get')

    def call_endpoint(self, endpoint,  http_method='get', input_params_dict=None):
        """Get endpoint together with valid bearer token"""
        try:
            if http_method.lower() == 'get':
                if input_params_dict:
                    response = requests.get(
                        endpoint, headers=self.auth.authorization_headers(self.EGE_API_ENV), params=input_params_dict, timeout=30
                    )
                else:
                    response = requests.get(
                        endpoint, headers=self.auth.authorization_headers(self.EGE_API_ENV), timeout=30
                    )
            elif http_method.lower() == 'post':
                if not input_params_dict:
                    raise InputException("Input parameters are empty")
                json_payload = json.dumps(input_params_dict).strip(' \t\n\r')
                response = requests.post(endpoint, headers=self.auth.authorization_headers(self.EGE_API_ENV), data=json_payload, timeout=30)
            else:
                raise InputException("Invalid HTTP method specified")

            result = response.json()
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise EndpointException("Request timed out")
        except requests.exceptions.RequestException as e:
            if response.status_code == 401:
                message = result['message']
            else:
                message = result.get('detail', {}).get('reason', '')
            raise EndpointException(f"{e}. {message}")
        except ValueError as e:
            raise EndpointException(f"JSON decoding failed: {e}")
        return result
