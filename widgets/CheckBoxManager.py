from widgets.CheckBox import TaskCheckBox


class CheckBoxManager:
    def __init__(self):
        self.check_boxes: list[TaskCheckBox] = []

    def add_checkbox(self, check_box: TaskCheckBox):
        self.check_boxes.append(check_box)

    def get_checkbox(self, index: int) -> TaskCheckBox:
        return self.check_boxes[index]

    def get_checkboxes(self) -> list[TaskCheckBox]:
        return self.check_boxes

    def remove_checkbox(self, check_box):
        self.check_boxes.remove(check_box)

    def remove_checkbox_by_index(self, index: int):
        try:
            del self.check_boxes[index]
        except Exception as error:
            print(error)
