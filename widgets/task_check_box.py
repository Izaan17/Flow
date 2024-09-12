import datetime
from typing import Any
import customtkinter
from models import Task
from utils.date import parse_days_difference, get_time_suffix_string
from utils.string_utils import shorten_text
from widgets.hyper_link import HyperLink


class TaskCheckBox(customtkinter.CTkFrame):
    """A Frame containing a CheckBox and details of a task."""

    def __init__(self, master: Any, task: Task, **kwargs: Any):
        super().__init__(master, **kwargs)
        self.task = task

        # Style the outer frame
        self.configure(
            fg_color='transparent',  # Light background color
            corner_radius=8,
        )

        # Initialize StringVars and other variables
        self.task_name_var = customtkinter.StringVar(value=task.name)
        self.task_source_var = customtkinter.StringVar(value=task.source)
        self.task_link_var = customtkinter.StringVar(value=task.link)
        self.task_status_var = customtkinter.IntVar(value=task.is_complete)
        self.task_due_date = task.due_date  # Store the due date string

        # Create and pack widgets
        self.create_widgets()

        # Initial update of the due date label
        self._update_due_date_label()

    def create_widgets(self) -> None:
        """Create and place widgets within the frame."""
        self._create_checkbox()
        self._create_source_label()
        self._create_link_hyperlink()
        self._create_due_date_label()

    def _create_checkbox(self) -> None:
        """Create and pack the checkbox widget."""
        self.checkbox = customtkinter.CTkCheckBox(
            self,
            fg_color='#52bf90',  # Primary color
            hover_color='#398564',  # Darker shade on hover
            border_color='#49ab81',  # Light border color
            border_width=2,
            corner_radius=12,
            font=('Arial', 14, 'bold'),  # Modern font
            textvariable=self.task_name_var,
            text_color='black',
            variable=self.task_status_var,
            onvalue=1,
            offvalue=0
        )
        self.checkbox.pack(
            padx=5,
            pady=6,
            expand=True,
            fill='x'
        )

    def _create_source_label(self) -> None:
        """Create and pack the source label widget."""
        self.source_label = customtkinter.CTkLabel(
            self,
            textvariable=self.task_source_var,
            font=('Arial', 12),  # Font size for readability
            text_color='#8ca19e'  # Dark grey for text
        )
        self.source_label.pack(side='left', padx=(44, 10))

    def _create_link_hyperlink(self) -> None:
        """Create and pack the hyperlink widget."""
        self.link_hyperlink = HyperLink(
            self,
            text=shorten_text(self.task_link_var.get(), 30),
            url=self.task.link,
        )
        self.link_hyperlink.pack(side='left', padx=8)

    def _create_due_date_label(self) -> None:
        """Create and pack the due date label widget."""
        self.due_date_label = customtkinter.CTkLabel(
            self,
            font=('Arial', 12),  # Font size for readability
            text_color='#FF6F61'  # Accent color for dates
        )
        self.due_date_label.pack(side='right', padx=(8, 20))

    def _update_due_date_label(self) -> None:
        """Update the color and text of the due date label."""
        now = datetime.datetime.now()
        due_date_obj = datetime.datetime.strptime(self.task_due_date, '%m-%d-%Y-%H-%M')

        time_difference = due_date_obj - now
        difference_from_now = (due_date_obj.date() - now.date()).days
        seconds_difference = time_difference.total_seconds()

        if seconds_difference < 0:
            if difference_from_now == 0:
                # Due earlier today
                text_color = '#D64045'  # Deep coral
                label_text = f"Today at {due_date_obj.strftime('%I:%M %p')} (Overdue)"
            elif difference_from_now == -1:
                # Due yesterday
                text_color = '#D64045'  # Deep coral
                label_text = f"Yesterday at {due_date_obj.strftime('%I:%M %p')} (Overdue)"
            else:
                # Due on a previous day
                text_color = '#D64045'  # Deep coral
                label_text = f"{parse_days_difference(difference_from_now)}, {get_time_suffix_string(due_date_obj)} (Overdue)"
        elif difference_from_now == 0:
            # Due later today
            text_color = '#17A2B8'  # Vibrant teal
            label_text = f"Today at {due_date_obj.strftime('%I:%M %p')}"
        elif difference_from_now == 1:
            text_color = '#FFA300'  # Warm amber
            label_text = f"Tomorrow at {due_date_obj.strftime('%I:%M %p')}"
        elif 1 < difference_from_now <= 3:
            text_color = '#FFA300'  # Warm amber
            label_text = f"{parse_days_difference(difference_from_now)}, {get_time_suffix_string(due_date_obj)}"
        else:
            text_color = '#3C4048'  # Dark slate gray
            label_text = f"{parse_days_difference(difference_from_now)}, {get_time_suffix_string(due_date_obj)}"

        # Update the due date label
        self.due_date_label.configure(text=label_text, text_color=text_color)

        # Schedule the update every 60 seconds (adjust as needed)
        self.after(60000, self._update_due_date_label)

    def get_checkbox(self) -> customtkinter.CTkCheckBox:
        """Return the checkbox widget."""
        return self.checkbox


if __name__ == '__main__':
    root = customtkinter.CTk()
    task = Task(0, 'Task Name', 'Source Label', 'www.google.com', '09-25-2024-10-20')
    t = TaskCheckBox(root, task)
    t.pack(expand=True, fill='x', padx=10)
    root.mainloop()