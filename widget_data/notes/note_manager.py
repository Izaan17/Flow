import utils.string_utils
from utils.directory_manager import get_notes_dir

# Todo: Finish note manager operations.
#

import os
import json
import datetime
import utils.string_utils
from widget_data.notes.note import Note


class NoteManager:
    def __init__(self):
        self.parent_notes_directory = get_notes_dir()

    def create_notes_folder(self, folder_name: str):
        new_created_folder_path = self.parent_notes_directory / folder_name
        print(new_created_folder_path)
        os.makedirs(new_created_folder_path, exist_ok=True)

    def notes_folder_exists(self, folder_name: str):
        return (self.parent_notes_directory / folder_name).exists()

    def add_note(self, folder_name: str, title: str, content: str, date_created: datetime.datetime | None = None,
                 date_modified: datetime.datetime | None = None):
        self.__check_if_folder_exists__(folder_name)
        created_note = Note(title, content, date_created, date_modified)
        self.__write_note__(folder_name, created_note)
        print("Saved Note.")

    def delete_note(self, folder_name: str, note_file_name: str):
        self.__check_if_folder_exists__(folder_name)
        note_file_path = self.parent_notes_directory / folder_name / note_file_name
        os.remove(note_file_path)

    def delete_notes_folder(self, folder_name: str):
        self.__check_if_folder_exists__(folder_name)
        folder_path = self.parent_notes_directory / folder_name
        os.rmdir(folder_path)

    def __check_if_folder_exists__(self, folder_name):
        if not self.notes_folder_exists(folder_name):
            raise FileNotFoundError(f"'{folder_name}' does not exist.")

    def __write_note__(self, folder_name: str, note):
        generated_file_name = utils.string_utils.generate_random_string(8, use_special_chars=False)
        generated_file_name = generated_file_name + '.json'
        # Write new created note
        note_file_path = self.parent_notes_directory / folder_name / generated_file_name
        with open(note_file_path, 'w') as note_file:
            json.dump(note.to_dict(), note_file, default=str)


if __name__ == '__main__':
    n = NoteManager()
    n.create_notes_folder("Test Folder")
    n.add_note("Test Folder", "Note Title", "Content")
