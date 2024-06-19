from typing import Any

from widgets.popups.validation.widget_data_validator import NumericValidator
from widgets.UtilitySection import UtilitySection
from widgets.Entry import DefaultEntry
from widgets.Buttons import DefaultButton
from widgets.Page import Page
import customtkinter


class UtilitiesPage(Page):
    def __init__(self, master: Any, *args, **kwargs):
        super().__init__(master, *args, **kwargs, page_title="Utilities Page", subheading="Useful tools.")

        self.main_frame = customtkinter.CTkFrame(self, fg_color='transparent')

        self.final_grade_simulator_section = UtilitySection(self.main_frame, section_title="Final Grade Simulator",
                                                            section_subtitle="Use this tool to find the grade "
                                                                             "needed on the final exam to "
                                                                             "get a desired grade in a course.",
                                                            fg_color='transparent')
        self.final_grade_simulator_section.pack(side='right', expand=True, fill='both')

        self.entries_grid = customtkinter.CTkFrame(self.final_grade_simulator_section, fg_color='transparent')
        self.entries_grid.pack(pady=25)
        entry_size = 115

        self.current_grade_entry = DefaultEntry(self.entries_grid, placeholder_text="Current Grade",
                                                validators=[NumericValidator(0, 100)],
                                                width=entry_size)
        self.current_grade_entry.pack(side='left', padx=25, pady=5)

        self.desired_grade_entry = DefaultEntry(self.entries_grid, placeholder_text="Desired Grade",
                                                validators=[NumericValidator(0, 100)],
                                                width=entry_size)
        self.desired_grade_entry.pack(side='left', padx=25, pady=5)

        self.final_exam_weight_entry = DefaultEntry(self.entries_grid, placeholder_text="Final Weight",
                                                    validators=[NumericValidator(0, 100)],
                                                    width=entry_size)
        self.final_exam_weight_entry.pack(side='left', padx=25, pady=5)

        self.simulate_button = DefaultButton(self.final_grade_simulator_section, text="Simulate",
                                             command=self.simulate_grade)
        self.simulate_button.pack(pady=10)

        self.simulation_result = customtkinter.CTkLabel(self.final_grade_simulator_section, text="",
                                                        font=('Roboto', 16))

        self.main_frame.pack(expand=True, fill='both', padx=5, pady=5)

    def simulate_grade(self):
        current_grade = int(self.current_grade_entry.validated_get())
        desired_grade = int(self.desired_grade_entry.validated_get())
        final_exam_weight = int(self.final_exam_weight_entry.validated_get())
        if current_grade and desired_grade and final_exam_weight:
            # Convert final grade to decimal
            final_exam_weight /= 100.0

            # Calculate the grade needed on the final exam
            needed_final_exam_grade = (desired_grade - current_grade * (1 - final_exam_weight)) / final_exam_weight
            self.simulation_result.pack()
            self.simulation_result.configure(text=f"You need to get a grade of {needed_final_exam_grade:.2f} or "
                                                  f"higher on your final.")
        else:
            self.simulation_result.pack_forget()


if __name__ == "__main__":
    app = customtkinter.CTk()

    page = UtilitiesPage(app)
    page.pack(expand=True, fill='both')

    app.mainloop()
