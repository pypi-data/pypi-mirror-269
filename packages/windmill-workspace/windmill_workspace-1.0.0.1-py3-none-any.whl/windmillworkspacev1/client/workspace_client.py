#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/4/25
# @Author  : yanxiaodong
# @File    : workspace_client.py
"""
from typing import Optional
from baidubce.http import http_methods
from baidubce.bce_client_configuration import BceClientConfiguration
from bceinternalsdk.client.bce_internal_client import BceInternalClient
from bceinternalsdk.client.paging import PagingRequest


class WorkspaceClient(BceInternalClient):
    """
    A client class for interacting with the Workspace service.
    """
    def __init__(self, config: Optional[BceClientConfiguration] = None, ak: Optional[str] = "",
                 sk: Optional[str] = "", endpoint: Optional[str] = ""):
        super(WorkspaceClient, self).__init__(config=config, ak=ak, sk=sk, endpoint=endpoint)

    def list_workspace(self, page_request: Optional[PagingRequest] = PagingRequest()):
        """
        list workspace.
        """
        params = {
            "pageNo": str(page_request.get_page_no()),
            "pageSize": str(page_request.get_page_size()),
            "order": page_request.order,
            "orderBy": page_request.orderby
        }

        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces",
                encoding="utf-8",
            ),
            params=params,
        )