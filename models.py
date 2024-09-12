class Task:
    def __init__(self, _id: int, name: str, source: str = None, link: str = None, due_date: str = None,
                 is_complete: int = 0):
        self.id = _id
        self.name = name
        self.source = source
        self.link = link
        self.due_date = due_date
        self.is_complete = is_complete

    def __repr__(self):
        return (f'Task(id={self.id},'
                f' name={self.name},'
                f' source={self.source},'
                f' link={self.link},'
                f' due_date={self.due_date},'
                f' is_complete={self.is_complete})')