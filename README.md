# msgraph-email
Microsoft Graph Email API using Python

## Installation
msgraph-email is available on PyPI.
```python
    pip install msgraph-email
```

## Import modules

```python
from mail.msgraph import EmailService
from mail.models import EmailMessage,EmailAttachment
```

## Configure a Email_Service 
```python

emailService = EmailService(tenant_id, client_id, client_secret, email_address)

```
## Make a read email request
By default it will read unread emails of the **'Inbox'** mailfolder
```python
emailMessages:list(EmailMessage) = emailService.readEmails() 
```
## Make a send email request
```python
emailMessage = EmailMessage()
emailMessage.toEmails="test@mail.com"
emailMessage.message="Hello"
emailService.sendEmail(message)
```

## Make a read and unread email request
```python
emailMessages = emailService.readEmails()
for email in emailMessages:
    emailService.markEmailReadUnRead(email.messageId)
```
## Make a delete email request
```python
emailMessages = emailService.readEmails()
for email in emailMessages:
    emailService.deleteEmail(email.messageId)
```