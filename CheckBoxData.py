from widgets.CheckBox import TaskCheckBox


class CheckBoxData:
    def __init__(self, uid, task_name, task_source, task_link, task_due_date, completion_status):
        self.id = uid
        self.task_name = task_name
        self.task_source = task_source
        self.task_link = task_link
        self.task_due_date = task_due_date
        self.completion_status = completion_status

    def get_data(self):
        return {'id': self.id,
                'task_name': self.task_name,
                'task_source': self.task_source,
                'task_link': self.task_link,
                'task_due_date': self.task_due_date,
                'completion_status': self.completion_status}

    @staticmethod
    def from_checkbox(check_box: TaskCheckBox, uid):
        return CheckBoxData(uid,
                            check_box.cget("text"),
                            check_box.source_text_var.get(),
                            check_box.link_text_var.get(),
                            check_box.due_date,
                            check_box.get())

    @staticmethod
    def from_dict(data):
        return CheckBoxData(data['id'], data['task_name'], data['task_source'], data['task_link'],
                            data['task_due_date'], data['completion_status'])
