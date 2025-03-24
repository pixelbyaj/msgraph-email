import asyncio
from typing import List
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
    await emailService.send_email(emailMessage)

async def main():
    authCredentials = AuthCredentials(client_id,tenant_id,client_secret,email_address,scopes)
    emailService = EmailService(authCredentials)
    await emailService.authenticate()
    await send_email(emailService)
    emailMessages: List[EmailMessage] = await emailService.get_emails()
    for email in emailMessages:
        #mark it read
        await emailService.mark_email_read_unread(email.message_id,is_read=True)

# Run the event loop
if __name__ == '__main__':
   asyncio.run(main())