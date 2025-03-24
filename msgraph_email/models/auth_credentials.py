# ------------------------------------
# Copyright (c) Abhishek Joshi - PixelByAJ.
# Licensed under the  Apache License.
# ------------------------------------

from typing import List


class AuthCredentials:
    
    def __init__(self, client_id: str, tenant_id: str, client_secret: str, email_address: str, scopes: List[str]):
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.client_secret = client_secret
        self.email_address = email_address
        self.scopes = scopes

    client_id: str = None
    tenant_id: str = None
    client_id: str = None
    client_secret: str = None
    email_address: str = None
    scopes: List[str] = "https://graph.microsoft.com/.default"