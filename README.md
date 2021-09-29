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

## Configure an Email Service 
```python

emailService = EmailService(tenant_id, client_id, client_secret, email_address)

```
## Process  to read an email request
By default it will read unread emails of the **'Inbox'** mailfolder
```python
emailMessages= emailService.readEmails() 
```
## Process to send an email request
```python
emailMessage = EmailMessage()
emailMessage.toEmails="test@mail.com"
emailMessage.message="Hello"
emailService.sendEmail(message)
```

## Process to read and unread an email request
```python
emailMessages = emailService.readEmails()
for email in emailMessages:
    #mark it read
    emailService.markEmailReadUnRead(email.messageId,isRead=True)
    #mark it unread
    #emailService.markEmailReadUnRead(email.messageId,isRead=False)

```
## Make a delete email request
```python
emailMessages = emailService.readEmails()
for email in emailMessages:
    emailService.deleteEmail(email.messageId)
```