import asyncio
import base64
from typing import List
from msgraph_email.models.email_attachment import EmailAttachment
from msgraph_email.services.email_service import EmailService
from msgraph_email.models.email_message import EmailMessage
from msgraph_email.models.auth_credentials import AuthCredentials

import os
from dotenv import load_dotenv
load_dotenv()   

client_id = os.getenv("MSGRAPH_CLIENT_ID")
tenant_id = os.getenv("MSGRAPH_TENANT_ID")
client_secret = os.getenv("MSGRAPH_CLIENT_SECRET")
email_address = os.getenv("MSGRAPH_EMAIL_ADDRESS")
scopes = ["User.Read","Mail.ReadWrite","Mail.Send","MailboxSettings.ReadWrite"]

async def send_email(emailService: EmailService):
    
    emailMessage = EmailMessage()
    emailMessage.subject = "Test Email"
    emailMessage.message = "This is a test email"
    emailMessage.to_emails=["abhishek2185@gmail.com"]
    emailMessage.has_attachments = True
    emailAttachment = EmailAttachment()
    emailAttachment.name = "test.txt"
    emailAttachment.content_type = "text/plain"
    emailAttachment.content_bytes = bytearray(base64.b64encode("This is a test attachment".encode("utf-8")))
    emailMessage.attachments = [
        emailAttachment
    ]
    await emailService.send_email(emailMessage)
    
async def read_email(emailService: EmailService):
    emailMessages: List[EmailMessage] = await emailService.get_emails()
    for email in emailMessages:
        for attachment in email.attachments:
            print(f"Attachment Name: {attachment.name}")
            print(f"Attachment Size: {attachment.size} bytes")
            print(f"Attachment Content Type: {attachment.content_type}")
            
            # Save the attachment to a file
            with open(attachment.name, "wb") as f:
                f.write(attachment.content_bytes)
                
        #mark it read
        await emailService.mark_email_read_unread(email.message_id,is_read=True)
    
async def main():
    authCredentials = AuthCredentials(client_id,tenant_id,client_secret,email_address,scopes)
    emailService = EmailService(authCredentials)
    await emailService.authenticate()
    await send_email(emailService)
    #await read_email(emailService)

# Run the event loop
if __name__ == '__main__':
   asyncio.run(main())