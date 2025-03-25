# Automate your Emails with msgraph-email
**msgraph-email** allows you to automate email operation using the Microsoft Graph API. It provides a simple interface to interact with Microsoft Graph Email API.

[![License](https://img.shields.io/badge/License-apache-blue.svg)](https://img.shields.io/badge/)
[![Downloads](https://static.pepy.tech/badge/msgraph-email)](https://pepy.tech/project/msgraph-email)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/msgraph-email?style=plastic)](https://pypi.org/project/msgraph-email)
[![PayPal Donate](https://img.shields.io/badge/donate-PayPal.me-ff69b4.svg)](https://www.paypal.me/pixelbyaj)


## Features

- Send emails
- Read emails
- Manage email attachments
- Mark emails as read/unread
- Delete emails

## Installation

You can install the package using pip:

```sh
pip install msgraph-email
```

## Usage

### Authentication

To use the package, you need to authenticate with Microsoft Graph. You can do this by providing your Azure Active Directory credentials.

```python
from msgraph_email.services.email_service import EmailService
from msgraph_email.models.auth_credentials import AuthCredentials
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("MSGRAPH_CLIENT_ID")
tenant_id = os.getenv("MSGRAPH_TENANT_ID")
client_secret = os.getenv("MSGRAPH_CLIENT_SECRET")
email_address = os.getenv("MSGRAPH_EMAIL_ADDRESS")
scopes = ["User.Read", "Mail.ReadWrite", "Mail.Send", "MailboxSettings.ReadWrite"]

auth_credentials = AuthCredentials(client_id, tenant_id, client_secret, email_address, scopes)
email_service = EmailService(auth_credentials)

async def authenticate():
    await email_service.authenticate()

# Run the authentication
import asyncio
asyncio.run(authenticate())
```

### Sending an Email

```python
from msgraph_email.models.email_message import EmailMessage

async def send_email():
    email_message = EmailMessage()
    email_message.subject = "Test Email"
    email_message.message = "This is a test email"
    email_message.to_emails = ["recipient@example.com"]
    await email_service.send_email(email_message)

# Send the email
asyncio.run(send_email())
```

### Reading Emails

```python
async def read_emails():
    email_messages = await email_service.get_emails()
    for email in email_messages:
        print(f"Subject: {email.subject}, From: {email.sender_email}")

# Read the emails
asyncio.run(read_emails())
```

### Marking an Email as Read/Unread

```python
async def mark_email_as_read(message_id):
    await email_service.mark_email_read_unread(message_id, is_read=True)

# Mark an email as read
message_id = "your-message-id"
asyncio.run(mark_email_as_read(message_id))
```

### Deleting an Email

```python
async def delete_email(message_id):
    await email_service.delete_email(message_id)

# Delete an email
message_id = "your-message-id"
asyncio.run(delete_email(message_id))
```

---

### Build & Publish to PyPI
Ensure you have `twine` installed:

```sh
pip install build twine
python -m build
twine upload dist/*
```
Enter your PyPI credentials when prompted.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
