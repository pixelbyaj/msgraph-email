# ------------------------------------
# Copyright (c) PixelByAJ.
# Licensed under the MIT License.
# ------------------------------------
from msgraph.core import GraphClient
from azure.identity import ClientSecretCredential
from typing import List
import requests
from requests.sessions import Session
import json
import base64
from models import EmailAttachment, EmailMessage
"""Email Service to be used for reading/sending emails against Microsoft Graph

    :keyword credential: TokenCredential used to acquire an access token for the Microsoft
        Graph API. Created through one of the credential classes from `azure.identity`
    :keyword list middleware: Custom middleware(HTTPAdapter) list that will be used to create
        a middleware pipeline. The middleware should be arranged in the order in which they will
        modify the request.
    :keyword enum api_version: The Microsoft Graph API version to be used, for example
        `APIVersion.v1` (default). This value is used in setting the base url for all requests for
        that session.
        :class:`~msgraphcore.enums.APIVersion` defines valid API versions.
    :keyword enum cloud: a supported Microsoft Graph cloud endpoint.
        Defaults to `NationalClouds.Global`
        :class:`~msgraphcore.enums.NationalClouds` defines supported sovereign clouds.
    :keyword tuple timeout: Default connection and read timeout values for all session requests.
        Specify a tuple in the form of Tuple(connect_timeout, read_timeout) if you would like to set
        the values separately. If you specify a single value for the timeout, the timeout value will
        be applied to both the connect and the read timeouts.
    :keyword obj session: A custom Session instance from the python requests library
    """
class EmailService:
    def __init__(self,tenant_id,client_id,client_secret,email_address:str,**kwargs):
        if not client_id:
            raise ValueError("client_id should be the id of an Azure Active Directory application")
        if not tenant_id:
            raise ValueError("tenant_id should be the an Azure Active Directory tenant's id (also called its 'directory id')")
        if not client_secret:
            raise ValueError("secret should be the an Azure Active Directory application's client secret")
        if not email_address:
            raise ValueError("email_address should be the an Azure Active Directory application's email address")
        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        self.__emailAddress= email_address            
        self.__graph_session = GraphClient(credential=credential,**kwargs)
           
    def __get(self,url):
        url = "/users/"+self.__emailAddress+"/"+url
        resonse = self.__graph_session.get(url)
        json_response=json.loads(response.text)
        return response

    def __post(self,url,headers,data):
        url = "/users/"+self.__emailAddress+"/"+url
        resonse = self.__graph_session.post(url,data=data,headers=headers)        
        return response
    
    def __patch(self,url,headers,data):
        url = "/users/"+self.__emailAddress+"/"+url
        resonse = self.__graph_session.patch(url,data=data,headers=headers)        
        return response

    def __delete(self,url):
        url = "/users/"+self.__emailAddress+"/"+url
        resonse = self.__graph_session.delete(url)        
        return response

    def __getEmailAddressess(self,emailAddressess:list(str)):
        __emailAddresess=[]
        for email in emailAddressess:
            __emailAddresess.append({
                'emailAddress':{
                    'address':email
                }
            })

    def __getAttachments(self,emailMessage:EmailMessage):
        __attachments=[]        
        for file in emailMessage.attachments:
            __attachments.append({
                "@odata.type":"#microsoft.graph.fileAttachment",
                "name":file.name,
                "contentType":file.contentType,
                "contentBytes":file.contentBase64
            })
        
        return __attachments

    def __getEmail(self,emailMessage:EmailMessage):
        __emailMessage = {
            'message':{
                'subject':emailMessage.subject,
                'toRecipients':[],
                'ccRecipients':[],
                'bccRecipients':[],
                'body':{
                    'contentType':'HTML',
                    'content':"<html><body>"+emailMessage.message+"<html></body>"
                }
            }
        }                
        
        if emailMessage.toEmails == None:
             raise ValueError("toRecipients should be email address")

        __emailMessage['message']['toRecipients']=__getEmailAddressess(emailMessage.toEmails)        
        
        if emailMessage.ccEmails != None:
            __emailMessage['message']['ccRecipients']=__getEmailAddressess(emailMessage.ccEmails)
        
        if emailMessage.bccEmails != None:
            __emailMessage['message']['bccRecipients']=__getEmailAddressess(emailMessage.bccEmails)
        
        if emailMessage.hasAttachments:
            __emailMessage['message']['attachments']=self.__getAttachments(emailMessage)

        return __emailMessage

    def __getMimeBody(self,messageId,attachmentId):
        try:
            url="/users/"+self.__emailAddress+"/messages/"+messageId+"/attachments/"+attachmentId+"/$value"
            response = self.__graph_session.get(url)
            return response.text
        except requests.exceptions.HTTPError as err:
            return (err)

    def readEmails(self,mailFolder:str="Inbox",unRead:bool=True,filter:str=None) -> List[EmailMessage]:
        try:
            url = "mailFolders/"+mailFolder+"/messages"
            if unRead:
                url += "?$filter=isRead ne true&$count=true"
            if filter:
                url += "&"+filter
            response = self.__get(url)
            __emailMessages=[]
            for message in response["value"]:
                __msg = EmailMessage()
                __msg.messageId = message["id"]
                __msg.receivedDateTime = message["receivedDateTime"]
                __msg.sendDataTime = message["sendDataTime"]
                __msg.messagePreview = message["bodyPreview"]
                __msg.message = message["body"]["content"]
                __msg.fromEmail = message["from"]["emailAddress"]["address"]
                __msg.hasAttachments = message["hasAttachments"]
                
                if __msg.hasAttachments:
                    __msg.attachments=self.readAttachments(__msg.messageId)
                
                __emailMessages.append(__msg)
                
                return __emailMessages

        except requests.exceptions.HTTPError as err:
            return (err)

    def readAttachments(self,messageId:str,encodeType:str='utf-8') -> List[EmailAttachment]:
        try:
            if not messageId:
                raise ValueError("messageId should be the id of an Email Message")
            
            url = "/messages/"+messageId+"/attachments"
            response = self.__get(url)
            __attachments=[]
            for file in response["value"]:
                __file = EmailAttachment()
                __file.fileId = file["id"]    
                __file.name = file["name"]    
                __file.size = file["size"]    
                __file.contentType = file["contentType"]    
                
                if __file.contentType != "message/rfc822":
                    __data=file["contentBytes"]
                    __dataStr= json.dumps(__data)
                    __file.contentBase64 = base64.b64encode(__dataStr.encode(encodeType))
                else:
                    __file.isMimeType=True
                    __file.mimeBody = self.__getMimeBody(messageId, __file.fileId)
                
                __attachments.append(__file)

            return __attachments
        except requests.exceptions.HTTPError as err:
            return (err)

    def sendEmail(self,message:EmailMessage):
        try:
            __message=self.__getEmail(emailMessage=message)
            __url = "sendEmail"
            response = self.__post(url, {'Content-Type':'application/json'}, json.dumps(__message))
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            return (err)

    def markEmailReadUnRead(self,messageId:str,mailFolder:str="Inbox",isRead:bool=True):
        try:
            __message={'IsRead':isRead}
            __url = "mailFolders/"+mailFolder+"/messages/"+messageId
            response = self.__patch(url, {'Content-Type':'application/json'}, json.dumps(__message))
            reponse.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            return (err)

    def deleteEmail(self,messageId:str,mailFolder:str="Inbox",isRead:bool=True):
        try:
            __url = "mailFolders/"+mailFolder+"/messages/"+messageId
            response = self.__delete(url)
            reponse.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            return (err)