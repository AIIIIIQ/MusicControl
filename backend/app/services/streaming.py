import mimetypes
import os
from typing import Iterator

from fastapi import Request
from fastapi.responses import Response, StreamingResponse


CHUNK_SIZE = 1024 * 256


def file_iterator(path: str, start: int = 0, end: int | None = None) -> Iterator[bytes]:
    with open(path, 'rb') as f:
        f.seek(start)
        remaining = (end - start + 1) if end is not None else None
        while True:
            chunk_size = CHUNK_SIZE if remaining is None else min(CHUNK_SIZE, remaining)
            if chunk_size <= 0:
                break
            data = f.read(chunk_size)
            if not data:
                break
            if remaining is not None:
                remaining -= len(data)
            yield data


def range_response(path: str, request: Request, download: bool = False, filename: str | None = None):
    file_size = os.path.getsize(path)
    range_header = request.headers.get('range')
    mime = mimetypes.guess_type(path)[0] or 'application/octet-stream'

    headers = {'Accept-Ranges': 'bytes'}
    if download and filename:
        headers['Content-Disposition'] = f'attachment; filename="{filename}"'

    if not range_header:
        headers['Content-Length'] = str(file_size)
        return StreamingResponse(file_iterator(path), media_type=mime, headers=headers)

    _, range_value = range_header.split('=')
    start_str, end_str = range_value.split('-')
    start = int(start_str) if start_str else 0
    end = int(end_str) if end_str else file_size - 1
    end = min(end, file_size - 1)

    content_length = end - start + 1
    headers.update(
        {
            'Content-Range': f'bytes {start}-{end}/{file_size}',
            'Content-Length': str(content_length),
        }
    )
    return StreamingResponse(
        file_iterator(path, start, end),
        status_code=206,
        media_type=mime,
        headers=headers,
    )
