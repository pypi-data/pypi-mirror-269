"""
a module to provide an interface with the AtonixOI APIs
written by: Kolton Stimpert
date: 10/15/2021
"""
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
import atonix.assets as assets
import atonix.models as models
import atonix.processdata as processdata
import atonix.actions as actions
import atonix.issues as issues


class Api:
    def __init__(self, api_key: str, private_key: RSAPrivateKey):
        self.base_url = "https://api.oi.atonix.com"

        self.api_key = api_key.replace("-", "").lower()
        self.private_key = private_key

        self.Assets = assets.Assets(base_url=self.base_url, user_key=self.api_key, key=self.private_key)
        self.Models = models.Models(base_url=self.base_url, user_key=self.api_key, key=self.private_key)
        self.Actions = actions.Actions(base_url=self.base_url, user_key=self.api_key, key=self.private_key)
        self.ProcessData = processdata.ProcessData(base_url=self.base_url, user_key=self.api_key, key=self.private_key)
        self.Issues = issues.Issues(base_url=self.base_url, user_key=self.api_key, key=self.private_key)
