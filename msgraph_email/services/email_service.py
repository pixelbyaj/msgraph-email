# ------------------------------------
# Copyright (c) Abhishek Joshi - PixelByAJ.
# Licensed under the  Apache License.
# ------------------------------------
import base64
from requests import Response
import requests

from msgraph.generated.users.item.messages.messages_request_builder import MessagesRequestBuilder
from msgraph.generated.users.item.send_mail.send_mail_post_request_body import SendMailPostRequestBody
from msgraph.generated.models.message_collection_response import MessageCollectionResponse
from msgraph.generated.models.attachment import Attachment
from msgraph.generated.models.message import Message
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.email_address import EmailAddress
from typing import Any, Optional, Union, List

from ..models.email_message import EmailMessage
from ..models.email_attachment import EmailAttachment
from ..models.auth_credentials import AuthCredentials
from ..auth.auth_service import AuthService

class EmailService:
    """
    Service class to interact with Microsoft Graph API for email operations.
    """
    def __init__(self, auth_credentials: AuthCredentials):
        """
        Initializes the EmailService with ClientSecretCredential.
        
        :param tenant_id: Azure Active Directory tenant ID.
        :param client_id: Azure Active Directory application ID.
        :param client_secret: Azure Active Directory application client secret.
        :param email_address: Email address of the Azure Active Directory application.
        :param scopes: List of scopes for the Graph API.
        """
        self.__auth_service = AuthService(auth_credentials)
        self.__client = None

    async def authenticate(self, **kwargs: Any):
        self.__client = await self.__auth_service.get_authenticate(**kwargs)    

    def __get_user(self):
        return self.__client.users.by_user_id(self.__get_email_address())
   
    def __get_email_address(self):
        return self.__auth_service.get_email_address()

    def __get_user_messages(self, message_id:str=None):
        if message_id is None:
            return self.__client.users.by_user_id(self.__get_email_address()).messages
        else:
            return self.__client.users.by_user_id(self.__get_email_address()).messages.by_message_id(message_id)

    def __get_email_addressess(self,emailAddressess):
        """
        Converts a list of email addresses into a list of dictionaries with the format required by the email service.

        Args:
            emailAddressess (list): A list of email addresses as strings.

        Returns:
            list: A list of dictionaries, each containing an email address in the required format.
        """
        _emailAddresess=[]
        for email in emailAddressess:
            recepient = Recipient(
                email_address = EmailAddress (
                    address=email
                )
            )
            _emailAddresess.append(recepient)
                
        return _emailAddresess

    def __get_attachments(self,emailMessage:EmailMessage):
        """
        Extracts and formats the attachments from an EmailMessage object.
        Args:
            emailMessage (EmailMessage): The email message containing attachments.
        Returns:
            list: A list of dictionaries, each representing an attachment with the following keys:
            - "@odata.type": The type of the attachment, always "#microsoft.graph.fileAttachment".
            - "name": The name of the attachment file.
            - "content_type": The MIME type of the attachment.
            - "content_bytes": The base64-encoded content of the attachment.
        """

        __attachments=[]
        for file in emailMessage.attachments:
            __attachments.append({
                "name":file.name,
                "content_type":file.contentType,
                "content_bytes":file.contentBase64
            })

        return __attachments

    def __get_email(self,emailMessage:EmailMessage):
        """
        Constructs an email message object from the provided EmailMessage instance.
        Args:
            emailMessage (EmailMessage): The email message instance containing the details for the email.
        Raises:
            ValueError: If 'toEmails' in emailMessage is None.
        Returns:
            Message: A Message object representing the constructed email.
        """
        if emailMessage.to_emails is None:
             raise ValueError("toRecipients should be email address")
        
        sender_recepient = Recipient()
        sender_recepient.email_address = EmailAddress(address=self.__get_email_address())
        to_recepient = self.__get_email_addressess(emailMessage.to_emails)
        if len(emailMessage.cc_emails) > 0:
            cc_recepient = self.__get_email_addressess(emailMessage.cc_emails) 
        if len(emailMessage.bcc_emails) > 0:
            bcc_recepient = self.__get_email_addressess(emailMessage.bcc_bccEmails)

        _emailMessage = Message()
        _emailMessage.sender = sender_recepient
        _emailMessage.subject = emailMessage.subject
        _emailMessage.to_recipients =  to_recepient

        if len(emailMessage.cc_emails) > 0:
            _emailMessage.cc_recipients = cc_recepient
        if len(emailMessage.bcc_emails) > 0:            
            _emailMessage.bcc_recipients = bcc_recepient

        
        itemBody = ItemBody()        
        
        ItemBody.content = emailMessage.message
        ItemBody.content_type = BodyType.Html

        _emailMessage.body = itemBody
        
        if emailMessage.has_attachments:
            _emailMessage.attachments = self.__get_attachments(emailMessage)

        return _emailMessage

    async def __getMimeBody(self,message_id,attachment_id):
        """
        Asynchronously retrieves and decodes the MIME body of an email attachment.
        Args:
            message_id (str): The ID of the email message.
            attachment_id (str): The ID of the attachment.
        Returns:
            bytes: The decoded MIME body of the attachment.
            If an HTTP error occurs, returns the error.
        Raises:
            requests.exceptions.HTTPError: If an HTTP error occurs during the request.
        """

        try:
            attachment: Attachment  = await self.__get_user_messages(message_id).attachments.by_id(attachment_id).get()
            return base64.b64decode(attachment.content_bytes)
        except requests.exceptions.HTTPError as err:
            return (err)

    async def get_emails(self,is_read:bool=False,filter:str=None, orderby: str =None, top: int=50, skip: int=None) -> List[EmailMessage]:
        
        try:
            _filter = None
            if not is_read:
                _filter = "IsRead eq false"
            
            if filter:
                if _filter:
                    _filter += " and " + filter
                else:
                    _filter = filter
            
            query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
                skip = skip, top=top,orderby=orderby,filter=_filter 
            )
            
            request_config =  MessagesRequestBuilder.MessagesRequestBuilderGetRequestConfiguration(
                query_parameters=query_params
            )
            
            messages: MessageCollectionResponse = await self.__get_user_messages().get(request_configuration=request_config)

            _emailMessages:List[EmailMessage] = []
            if messages.value:
                for message in messages.value:
                    _msg = EmailMessage()
                    _msg.message_id = message.id
                    _msg.subject = message.subject
                    _msg.received_date_time = message.received_date_time
                    _msg.send_date_time = message.sent_date_time
                    _msg.message = message.body.content
                    _msg.sender_email = message.sender.email_address.address
                    _msg.has_attachments = message.has_attachments
                    _msg.message_preview = message.body_preview                    
                    _msg.message = message.body.content
                    _msg.is_read = message.is_read
                    if _msg.has_attachments:
                        _msg.attachments = self.readAttachments(_msg.message_id)

                    _emailMessages.append(_msg)

            return _emailMessages

        except requests.exceptions.HTTPError as err:
            return (err)

    async def get_email_attachments(self,message_id:str,encodeType:str='utf-8') -> Union[List[EmailAttachment], Exception]:
        """
        Reads the attachments of an email message by its message ID.
        Args:
            message_id (str): The ID of the email message.
            encodeType (str, optional): The encoding type to use for decoding the attachment content. Defaults to 'utf-8'.
        Returns:
            List[EmailAttachment]: A list of EmailAttachment objects containing the details of each attachment.
        Raises:
            ValueError: If the message_id is not provided.
            requests.exceptions.HTTPError: If there is an HTTP error during the request.
        """
        try:
            if not message_id:
                raise ValueError("messageId should be the id of an Email Message")

            response = await self.__get_user_messages(message_id).attachments.get()
            _attachments=[]
            for file in response.value:
                _file = EmailAttachment()
                _file.file_id = file.id
                _file.name = file.name
                _file.size = file.size
                _file.content_type = file.content_type
                
                if _file.content_type != "message/rfc822":                            
                    _file.content_base64 = base64.b64encode(file.content_bytes).decode(encodeType)
                else:
                    _file.is_mime_type=True
                    _file.mime_body = await self.__getMimeBody(message_id, _file.fileId).decode(encodeType)

                _attachments.append(_file)

            return _attachments
        except requests.exceptions.HTTPError as err:
            return (err)

    async def send_email(self,emailMessage:EmailMessage) -> Union[Response, Exception]:
        """
        Sends an email using the provided EmailMessage object.
        Args:
            emailMessage (EmailMessage): The email message to be sent.
        Returns:
            response: The response from the email sending operation.
            If an HTTP error occurs, the error is returned instead.
        Raises:
            requests.exceptions.HTTPError: If an HTTP error occurs during the email sending process.
        """
        try:
            _message = self.__get_email(emailMessage=emailMessage)        
            response = await self.__get_user().send_mail.post(SendMailPostRequestBody(message=_message))
            return response
        except requests.exceptions.HTTPError as err:
            return (err)

    async def mark_email_read_unread(self,message_id:str,is_read:bool=True):
        """
        Marks an email as read or unread.
        Args:
            message_id (str): The ID of the email message to be marked.
            isRead (bool, optional): Flag indicating whether the email should be marked as read (True) or unread (False). Defaults to True.
        Returns:
            response: The response object from the patch request if successful.
            err: The HTTPError exception if the request fails.
        """
        try:
            message_patch = Message(is_read=is_read)
            response = await self.__get_user_messages(message_id).patch(message_patch)
            return response
        except requests.exceptions.HTTPError as err:
            return (err)

    async def delete_email(self, message_id: str) -> Union[Response, Exception] :
        """
        Deletes an email message with the given message ID.
        Args:
            message_id (str): The ID of the email message to be deleted.
        Returns:
            Union[Response, Exception]: Returns the response object if the deletion is successful,
                                        otherwise returns the exception raised during the process.
        """
        try:
            response = await self.__get_user_messages(message_id).delete()
            return response
        except requests.exceptions.HTTPError as err:
            return err
