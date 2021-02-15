# api.py
# Wrapper around the anonfiles.com API

from os.path import isfile
import requests

class Anonfiles:
    """Base API Class
    """
    def __init__(self, api_key: str=None):
        if api_key:
            # add api key to endpoint if provided
            self._endpoint_upload = f"https://api.anonfile.com/upload?token={api_key}"
        else:
            self._endpoint_upload = "https://api.anonfile.com/upload"
        
        self._endpoint_info = "https://api.anonfile.com/v2/file/{id}/info"

    def upload(self, path:str, proxies: dict=None):
        """Upload given File to anonfiles.com

        Args:
            path (str): Path to file
            proxies (dict, optional): Dictionary of proxies. Defaults to None.
        """
        if isfile(path):
            with open(path, "rb") as f:
                if proxies:
                    response = requests.post(self._endpoint_upload, files={"file": f}, proxies=proxies)
                else:
                    response = requests.post(self._endpoint_upload, files={"file": f})
            return AnonfilesResponse(response)
        else:
            raise AnonfilesError("-1")

    def info(self, id: str, proxies: dict=None):
        """Get info about files

        Args:
            id (str): file id

        Returns:
            AnonfilesResponse: Response object
        """
        response = requests.get(self._endpoint_info.format(id=id), proxies=proxies)
        return AnonfilesResponse(response)

    def download(self, path):
        pass

class AnonfilesResponse:
    """Response of an Anonfile Request
    """
    def __init__(self, response):
        self._response = response

    def __getattr__(self, attr):
        if attr in self._response.json():
            return self._response.json()[attr]
        else:
            return None

    def __repr__(self):
        return f"AnonfileResponse: Success: {self._response.json()['status']}"
    
    def json(self):
        return self._response.json()

class AnonfilesError(Exception):
    def __init__(self, code):
        self._code = code
        self._errors = {
            "10": "ERROR_FILE_NOT_PROVIDED",
            "11": "ERROR_FILE_EMPTY",
            "12": "ERROR_FILE_INVALID",
            "20": "ERROR_USER_MAX_FILES_PER_HOUR_REACHED",
            "21": "ERROR_USER_MAX_FILES_PER_DAY_REACHED",
            "22": "ERROR_USER_MAX_BYTES_PER_HOUR_REACHED",
            "23": "ERROR_USER_MAX_BYTES_PER_DAY_REACHED",
            "30": "ERROR_FILE_DISALLOWED_TYPE",
            "31": "ERROR_FILE_SIZE_EXCEEDED",
            "32": "ERROR_FILE_BANNED",
            "40": "STATUS_ERROR_SYSTEM_FAILURE",
            "-1": "ERROR_FILE_NOT_FOUND"
        }

    def __str__(self):
        return f"{self._code}: {self._errors[str(self._code)]}"
