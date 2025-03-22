from azure.identity import ClientSecretCredential, InteractiveBrowserCredential
from msgraph import GraphServiceClient

from ..models.auth_credentials import AuthCredentials

class AuthService:
    def __init__(self, auth_credentials: AuthCredentials):
        self.__auth_credentials = auth_credentials
        self.__client = None
        self.__display_name = None
        self.__email_address = auth_credentials.email_address

    def __get_client_secret_credentials(self, **kwargs):
        if not self.__auth_credentials.client_id:
            raise ValueError("client_id should be the id of an Azure Active Directory application")
        if not self.__auth_credentials.tenant_id:
            raise ValueError("tenant_id should be the ID of an Azure Active Directory tenant (also called its 'directory ID')")
        if not self.__auth_credentials.client_secret:
            raise ValueError("client_secret should be the client secret of an Azure Active Directory application")
        
        return ClientSecretCredential(self.__auth_credentials.tenant_id, self.__auth_credentials.client_id, self.__auth_credentials.client_secret, **kwargs)
        
    def __get_interactive_credentials(self, **kwargs):
        if not self.__auth_credentials.client_id:
            raise ValueError("client_id should be the id of an Azure Active Directory application")
        if not self.__auth_credentials.tenant_id:
            self.__auth_credentials.tenant_id = "consumers"
        if self.__auth_credentials.scopes is None:
            self.__auth_credentials.scopes = ["User.Read","Mail.ReadWrite","Mail.Send"]

        return InteractiveBrowserCredential(client_id=self.__auth_credentials.client_id,tenant_id=self.__auth_credentials.tenant_id, **kwargs)

    async def get_authenticate(self, **kwargs):
        credentials = None
        if self.__auth_credentials.email_address:
            self.__email_address = self.__auth_credentials.email_address
            credentials = self.__get_client_secret_credentials(self)
            self.__client = GraphServiceClient(credential=credentials, scopes=self.__auth_credentials.scopes, **kwargs)
            self.__display_name = await self.__client.users.by_user_id(self._emailAddress).get().user_principal_name
        else:
            credentials = self.__get_interactive_credentials(**kwargs)
            self.__client = GraphServiceClient(credentials=credentials, scopes=self.__auth_credentials.scopes, **kwargs)
            user = await self.__client.me.get()
            self.__email_address = user.mail or user.user_principal_name
            self.__display_name = user.user_principal_name
    
        return self.__client
    
    def get_client(self):
        return self.__client
    
    def get_email_address(self):
        return self.__email_address

    def get_display_name(self):
        return self.__display_name
   

        