import json
import os
from typing import Optional

from CheckBoxData import CheckBoxData
from widgets.CheckBox import TaskCheckBox


class CheckBoxManager:
    id_file = "checkbox_ids.json"
    max_id = 1000000  # Define a maximum ID value, adjust as needed

    def __init__(self, filename: Optional[str] = None):
        self.filename = filename
        self.check_boxes_data: dict[int, CheckBoxData] = self.load_from_file() if self.load_from_file() else {}
        self.active_checkbox: Optional[TaskCheckBox] = None
        self.last_id = self.load_last_id()

    def load_last_id(self):
        if self.filename:
            return self.get_next_id()  # Load and use the next available ID
        else:
            return 0

    @staticmethod
    def get_next_id():
        if os.path.exists(CheckBoxManager.id_file):
            with open(CheckBoxManager.id_file, "r") as f:
                data = json.load(f)
                last_id = data.get("last_id", 0)
        else:
            last_id = 0

        # Increment the last used ID
        last_id = (last_id % CheckBoxManager.max_id) + 1

        # Save the next ID back to the file
        with open(CheckBoxManager.id_file, "w") as f:
            json.dump({"last_id": last_id}, f)

        return last_id

    def reset_ids(self):
        os.remove(self.id_file)

    def add_checkbox(self, check_box_data: CheckBoxData):
        self.check_boxes_data[check_box_data.id] = check_box_data
        self.save_to_file()

    def get_checkbox_data(self, uid: int) -> Optional[CheckBoxData]:
        return self.check_boxes_data.get(uid)

    def get_checkboxes(self) -> dict[int, CheckBoxData]:
        return self.check_boxes_data

    def remove_checkbox_data(self, uid: int):
        if uid in self.check_boxes_data:
            del self.check_boxes_data[uid]
            self.save_to_file()

    def get_active(self) -> Optional[CheckBoxData]:
        return self.active_checkbox

    def set_active(self, checkbox: CheckBoxData):
        self.active_checkbox = checkbox

    def remove_active(self):
        self.active_checkbox = None

    def save_to_file(self):
        data_to_save = {str(id): checkbox_data.get_data() for id, checkbox_data in self.check_boxes_data.items()}
        with open(self.filename, 'w') as file_handler:
            json.dump(data_to_save, file_handler, indent=4)

    def load_from_file(self) -> dict[int, CheckBoxData]:
        try:
            with open(self.filename, 'r') as file_handler:
                data = json.load(file_handler)
                return {int(id): CheckBoxData.from_dict(values) for id, values in data.items()}
        except FileNotFoundError:
            print("File not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON data.")
        return {}

    def remove_checkbox_by_id(self, uid: int):
        if uid in self.check_boxes_data:
            del self.check_boxes_data[uid]
