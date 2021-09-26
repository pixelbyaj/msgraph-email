# ------------------------------------
# Copyright (c) PixelByAJ.
# Licensed under the MIT License.
# ------------------------------------
class EmailAttachment:
    def __init__(self):
        self.fileId: str
        self.name: str
        self.contentType: str
        self.contentBase64: bytearray
        self.size: int
        self.isInline: bool
        self.isMimeType: bool
        self.mimeBody: str


class EmailMessage:
    def __init__(self):
        self.messageId: str = None
        self.receivedDateTime: str = None
        self.sendDataTime: str = None
        self.fromEmail: str = None
        self.toEmails: list(str) = None
        self.ccEmails: list(str) = None
        self.bccEmails: list(str) = None
        self.subject: str = None
        self.message: str = None
        self.messagePreview: str = None
        self.hasAttachments: bool
        self.attachments: list(EmailAttachment) = None
