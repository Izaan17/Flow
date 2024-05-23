class CheckBoxData:
    def __init__(self, task_id, task_name, task_source, task_link, task_due_date, completion_status):
        self.task_id = task_id
        self.task_name = task_name
        self.task_source = task_source
        self.task_link = task_link
        self.task_due_date = task_due_date
        self.completion_status = completion_status

    def get_data(self):
        return {'task_id': self.task_id,
                'task_name': self.task_name,
                'task_source': self.task_source,
                'task_link': self.task_link,
                'task_due_date': self.task_due_date,
                'completion_status': self.completion_status}

    @staticmethod
    def from_checkbox(check_box):
        return CheckBoxData(check_box.task_id, check_box.cget("text"), check_box.source_text_var.get(),
                            check_box.link_text_var.get(), check_box.due_date, check_box.get())

    @staticmethod
    def from_dict(data):
        return CheckBoxData(data['task_id'], data['task_name'], data['task_source'], data['task_link'],
                            data['task_due_date'], data['completion_status'])

    def __eq__(self, other):
        if isinstance(other, CheckBoxData):
            return self.task_id == other.task_id
