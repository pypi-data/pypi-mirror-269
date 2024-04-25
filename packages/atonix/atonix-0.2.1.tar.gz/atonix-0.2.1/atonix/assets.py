import json
import time
import datetime
from atonix.auth_helper import handle_atx_request


class Assets:
    def __init__(self, base_url: str, user_key: str, key, asset_id: str = None):
        self.base_url = base_url
        self.user_key = user_key
        self.private_key = key

    def get_top(self):
        """
        Retrieve top level of available assets

        Returns
        -------
        list of dictionaries containing asset data

        """
        asset_list = []
        resource = "/v1/assets"
        http_method = "get"  # get, post, put, patch, or delete
        skip = 0
        request_body = None
        headers = None
        while True:
            query_params = {"skip": skip, "take": 50}
            if skip != 0:
                time.sleep(0.21)
            response = handle_atx_request(
                self.base_url,
                self.user_key,
                self.private_key,
                resource,
                http_method,
                query_params,
                request_body,
                headers
            )
            response_json = json.loads(response.content)
            if response.status_code == 200:
                # Results element will be a list of dictionaries
                asset_list.extend(response_json["Results"])
            if response_json["Count"] >= 50:
                skip += response_json["Count"]
            else:
                break
        return asset_list

    def get_asset_details(self, asset_id: str = None):
        """
        Get the details for a single asset

        Parameters
        ----------
        asset_id

        Returns
        -------
        list containing the asset name
        """
        resource = f'/v1/assets/{asset_id}'
        http_method = "get"  # get, post, put, patch, or delete
        query_params = None
        request_body = None
        headers = None

        response = handle_atx_request(
            self.base_url,
            self.user_key,
            self.private_key,
            resource,
            http_method,
            query_params,
            request_body,
            headers)

        response_json = json.loads(response.content)

        if response.status_code == 200:
            # Results element will be a list of dictionaries
            return response_json["Results"]
        else:
            raise Exception(f'Request Unsuccessful. Status code: {response.status_code}')

    def get_children(self,
                     asset_id: str,
                     includeDescendants: bool = False,
                     changedAfter: datetime = None,
                     changedBefore: datetime = None,
                     includeSelf: bool=False):
        """
        get the children assets of a given node

        :param includeSelf: optional, default False
        :param changedBefore: optional, default None
        :param changedAfter: optional, default None
        :param includeDescendants: optional, default, False
        :param str asset_id: top level asset_id

        Returns
        -------
        list of dictionaries containing asset data

        """
        child_list = []
        resource = f'/v1/assets/{asset_id}/assets'
        http_method = "get"  # get, post, put, patch, or delete
        skip = 0
        take = 500
        request_body = None
        headers = None

        while True:
            query_params = {
                "skip": skip,
                "take": take,
                "includeDescendants": includeDescendants,
                "changedAfter": changedAfter,
                "changedBefore": changedBefore,
                "includeSelf": includeSelf
            }
            query_params = {k: v for k, v in query_params.items() if v is not None}
            if skip != 0:
                time.sleep(0.21)
            response = handle_atx_request(
                self.base_url,
                self.user_key,
                self.private_key,
                resource,
                http_method,
                query_params,
                request_body,
                headers
            )

            response_json = json.loads(response.content)

            if response.status_code == 200:
                # Results element will be a list of dictionaries
                child_list.extend(response_json["Results"])
            else:
                raise Exception(f'Request Unsuccessful. Status code: {response.status_code}')

            if response_json["Count"] >= take:
                skip += response_json["Count"]
            else:
                break
        return child_list
