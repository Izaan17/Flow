import sqlite3
from typing import List

from models import Task


class TaskManager:
    def __init__(self, db_name: str = 'tasks.db'):
        self.db_name = db_name
        self.init_db()

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def init_db(self) -> None:
        """
        Initialize the database schema by creating the necessary tables.
        """
        with self as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                source TEXT,
                task_link TEXT,
                due_date TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                is_complete BOOLEAN DEFAULT 0
            )
            ''')
            conn.commit()

    def add_task(self, task: Task) -> int:
        """
        Add a new task to the database.

        Args:
            task (Task): The task to be added.

        Returns:
            task_id (int): Returns the newly created tasks id.
        """
        with self as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO tasks (task_name, source, task_link, due_date, is_complete)
            VALUES (?, ?, ?, ?, ?);
            ''', (task.name, task.source, task.link, task.due_date, task.is_complete))
            conn.commit()
            return cursor.lastrowid

    def add_bulk_tasks(self, tasks: List[Task]) -> None:
        """
        Add multiple tasks at once using a single database transaction.

        Args:
            tasks (List[Task]): A list of tasks to add.
        """
        if not tasks:
            return

        with self as conn:
            cursor = conn.cursor()

            # Prepare the SQL statement with placeholders for bulk insertion
            sql = '''INSERT INTO tasks (task_name, source, task_link, due_date, is_complete) VALUES (?, ?, ?, ?, ?)'''

            # Create a list of tuples containing the task data
            task_data = [(task.name, task.source, task.link, task.due_date, task.is_complete) for task in tasks]

            # Execute the bulk insert
            cursor.executemany(sql, task_data)
            conn.commit()

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from the database.

        Returns:
            List[Task]: A list of all tasks.
        """
        with self as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks')
            rows = cursor.fetchall()
            return [Task(_id=row[0], name=row[1], source=row[2], link=row[3], due_date=row[4], is_complete=row[5]) for row in rows]

    def get_task_count(self) -> int:
        with self as conn:
            cursor = conn.cursor()
            # Execute the SQL query to count the number of rows
            cursor.execute('SELECT COUNT(*) FROM tasks')
            # Fetch the result
            row_count = cursor.fetchone()[0]

            return int(row_count)

    def update_task(self, task: Task) -> None:
        """
        Update a task from the database.

        Args:
            task (Task): The task to be updated.
        """
        with self as conn:
            cursor = conn.cursor()
            print(task.id)
            cursor.execute('''
            UPDATE tasks 
            SET task_name = ?, source = ?, task_link = ?, due_date = ?, is_complete = ?
            WHERE id = ?
            ''', (task.name, task.source, task.link, task.due_date, task.is_complete, task.id))
            conn.commit()

    def delete_task(self, task: Task) -> None:
        """
        Delete a task from the database.

        Args:
            task (Task): The id of the task to delete.
        """
        with self as conn:
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM tasks WHERE id = ?;''', (task.id,))
            conn.commit()

    def set_task_status(self, task: Task, status: int):
        with self as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET is_complete = ? WHERE id = ?', (status, task.id))
            conn.commit()

    def toggle_task_status(self, task: Task):
        new_status = 0 if task.is_complete == 1 else 1
        self.set_task_status(task, new_status)

    def clear_table(self) -> None:
        """
        Drop the tasks table from the database.
        """
        with self as conn:
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM tasks''')
            # Reset IDS to 1
            cursor.execute(f"UPDATE sqlite_sequence SET seq = 0 WHERE name = 'tasks'")
            conn.commit()