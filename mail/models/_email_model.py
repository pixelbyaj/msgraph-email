# ------------------------------------
# Copyright (c) PixelByAJ.
# Licensed under the MIT License.
# ------------------------------------
from typing import Optional


class EmailAttachment:
    """Email attachment model."""

    fileId: str
    name: str
    contentType: str
    contentBase64: bytearray
    size: int
    isInline: bool
    isMimeType: bool
    mimeBody: str


class EmailMessage:
    """Email message model."""

    messageId: Optional[str] = None
    receivedDateTime: Optional[str] = None
    sendDateTime: Optional[str] = None
    fromEmail: Optional[str] = None
    toEmails: list[str] = []
    ccEmails: list[str] = []
    bccEmails: list[str] = []
    subject: Optional[str] = None
    message: Optional[str] = None
    messagePreview: Optional[str] = None
    hasAttachments: bool = False
    attachments: list[EmailAttachment] = []
