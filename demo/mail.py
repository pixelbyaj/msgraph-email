from mail.msgraph import EmailService
from mail.models import EmailMessage,EmailAttachment
from dotenv import load_dotenv
import os

client_id = os.getenv("MSGRAPH_CLIENT_ID")
tenant_id = os.getenv("MSGRAPH_TENANT_ID")
client_secret = os.getenv("MSGRAPH_CLIENT_SECRET")
email_address = os.getenv("MSGRAPH_EMAIL_ADDRESS")

emailService = EmailService(tenant_id, client_id, client_secret, email_address)

def readEmails():
    emailMessages = emailService.readEmails()
    for email in emailMessages:
        print(email.subject)
        print(email.body)
        print(email.sender)
        print(email.to)
        print(email.cc)
        print(email.bcc)
        print(email.attachments.count())
        #mark it read
        emailService.markEmailReadUnRead(email.messageId,isRead=True)

def sendEmail():
    emailMessage = EmailMessage()
    emailMessage.subject = "Test Email"
    emailMessage.body = "This is a test email"
    emailMessage.toEmails="test@mail.com"
    emailService.sendEmail(emailMessage)
