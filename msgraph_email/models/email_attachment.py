# ------------------------------------
# Copyright (c) Abhishek Joshi PixelByAJ.
# Licensed under the Apache License.
# ------------------------------------
from typing import Optional, Set

class EmailAttachment:
    """Email attachment model."""

    file_id: str
    name: str
    content_type: str
    content_base64: bytearray
    size: int
    is_inline: bool
    is_mime_type: bool
    mime_body: str



