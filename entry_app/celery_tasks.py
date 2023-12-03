import json

from celery import shared_task

from .models import Entry


@shared_task(ignore_result=False)
def backup_entries() -> None:
    entries_from_db = Entry.query.all()
    entries = [
        {
            'user-id': entry.user_id,
            'entry-text': entry.text
        } for entry in entries_from_db
    ]
    with open(f'entries.json', 'w', encoding='utf-8') as file_object:
        json.dump(entries, file_object, ensure_ascii=False, indent=4)
