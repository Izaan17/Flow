import datetime


class Note:
    def __init__(self, title: str, content: str, date_created: datetime.datetime | None = None,
                 date_modified: datetime.datetime | None = None):

        self.title = title
        self.content = content
        self.date_created = date_created if date_created else datetime.datetime.now()
        self.date_modified = date_modified if date_modified else self.date_created

    def to_dict(self):
        return {'title': self.title,
                'content': self.content,
                'date_created': self.date_created,
                'date_modified': self.date_modified}

    @staticmethod
    def from_dict(data):
        return Note(
            data["title"],
            data["content"],
            datetime.datetime.fromisoformat(data["date_created"]),
            datetime.datetime.fromisoformat(data["date_modified"])
        )


if __name__ == '__main__':
    note = Note("Title", "Content")
    print(note.title)
    print(note.content)
    print(note.date_created)
    print(note.date_modified)
