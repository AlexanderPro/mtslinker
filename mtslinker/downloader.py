import os
from typing import Dict, Union

import httpx
import tqdm

TIMEOUT_SETTINGS = httpx.Timeout(18.0, connect=9.0)


def construct_json_data_url(event_session_id: str, recording_id: str) -> str:
    if not recording_id:
        raise ValueError('Missing webinar recording ID.')
    if not event_session_id:
        raise ValueError('Missing webinar event session ID.')
    return f'https://my.mts-link.ru/api/event-sessions/{event_session_id}/record-files/{recording_id}/flow?withoutCuts=false'


def fetch_json_data(url: str, session_id: Union[str, None]) -> Dict:
    cookies = {}
    if session_id:
        cookies['sessionId'] = session_id

    with httpx.Client(timeout=TIMEOUT_SETTINGS) as client:
        response = client.get(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            },
            cookies=cookies
        )
    response.raise_for_status()
    return response.json()


def download_video_chunk(video_url: str, save_directory: str) -> str:
    filename = os.path.basename(video_url)
    file_path = os.path.join(save_directory, filename)

    if not os.path.exists(file_path):
        with open(file_path, 'wb') as file:
            with httpx.Client(timeout=TIMEOUT_SETTINGS) as client:
                with client.stream('GET', video_url) as response:
                    response.raise_for_status()
                    total_size = int(response.headers.get('content-length', 0))
                    with tqdm.tqdm(total=total_size, unit='B', unit_scale=True,
                                   desc=f'Downloading {filename}') as progress:
                        for chunk in response.iter_bytes(chunk_size=8192):
                            file.write(chunk)
                            progress.update(len(chunk))
    return file_path
