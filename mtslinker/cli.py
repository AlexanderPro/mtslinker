import argparse
import logging
import re
from mtslinker.webinar import fetch_webinar_data

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='mtslinker - tool for downloading MTS Link webinars.'
    )
    parser.add_argument(
        'url',
        help=(
            'Webinar link in one of the following formats: '
            'https://my.mts-link.ru/12345678/987654321/record-new/123456789/record-file/1234567890 or '
            'https://my.mts-link.ru/12345678/987654321/record-new/123456789'
        )
    )
    parser.add_argument(
        '--session-id',
        help='[Optional] sessionId token for accessing private recordings.'
    )
    return parser.parse_args()

def extract_ids_from_url(url: str):
    url_pattern = (
        r'https://my\.mts-link\.ru/\d+/\d+/record-new/(\d+)(?:/record-file/(\d+))?'
    )
    match = re.match(url_pattern, url)

    if match:
        # If there's a second capturing group, it's for the recording ID
        event_sessions = match.group(1)
        record_id = match.group(2) if match.group(2) else None
        return event_sessions, record_id
    
    return None, None

def main():
    logging.basicConfig(level=logging.INFO)

    args = parse_arguments()

    ids = extract_ids_from_url(args.url)
    if not ids:
        logging.error('Invalid URL format. Please check the link.')
        return

    event_sessions, record_id = ids

    logging.info(f'Starting download: event_sessions={event_sessions}, record_id={record_id}')
    if fetch_webinar_data(
    event_sessions=event_sessions,
        record_id=record_id,
        session_id=args.session_id
    ):
        logging.info('Download completed.')

if __name__ == '__main__':
    main()
