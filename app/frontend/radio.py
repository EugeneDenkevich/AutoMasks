import flet as ft


jobs_radio = ft.Radio(label="jobs", value="jobs")
tasks_radio = ft.Radio(label="tasks", value="tasks")

type_radio_group = ft.RadioGroup(
    value="jobs",
    content=ft.Row(
        [
            jobs_radio,
            tasks_radio,
        ]
    ),
)
