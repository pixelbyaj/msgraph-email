# ------------------------------------
# Copyright (c) Abhishek Joshi - PixelByAJ.
# Licensed under the Apache License.
# ------------------------------------
from typing import Optional, Set

from .email_attachment import EmailAttachment

class EmailMessage:
    """Email message model."""

    message_id: Optional[str] = None
    received_date_time: Optional[str] = None
    sent_date_time: Optional[str] = None
    sender_email: Optional[str] = None
    to_emails: set[str] = set()
    cc_emails: set[str] = set()
    bcc_emails: set[str] = set()
    subject: Optional[str] = None
    message: Optional[str] = None
    message_preview: Optional[str] = None
    has_attachments: bool = False
    attachments: Set[EmailAttachment] = set()
    is_read: bool = False