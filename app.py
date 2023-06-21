import PySimpleGUI as sg
import os
from utils import seq2vid

sg.theme("default 1")

# Define the layout for the first tab
tab1 = [
    [sg.Text("PNG Sequence folder")],
    [sg.Input(key="-SOURCE-", enable_events=True), sg.FolderBrowse()],
    [sg.Text("Video Output Path")],
    [sg.Input(key="-DEST-", enable_events=True), sg.FileSaveAs()],
    [sg.Text("FPS"), sg.Input(default_text=30, key="-FPS-", size=(5, 1))],
    [
        sg.Column(
            [
                [
                    sg.Button(
                        "Seq2Vid",
                        button_color=("white", "green"),
                        bind_return_key=True,
                        size=(10, 1),
                    )
                ]
            ],
            justification="right",
        )
    ],
]

# Define the layout for the second tab
tab2 = [
    [sg.Text("Video Input")],
    [sg.Input(key="-SOURCE_VIDEO-", enable_events=True), sg.FileBrowse()],
    [sg.Text("Sequence Output Folder")],
    [sg.Input(key="-SEQ_DEST-", enable_events=True), sg.FolderBrowse()],
    [sg.Text("FPS"), sg.Input(default_text=30, key="-FPS2-", size=(5, 1))],
    [
        sg.Column(
            [
                [
                    sg.Button(
                        "Vid2Seq",
                        button_color=("white", "green"),
                        bind_return_key=True,
                        size=(10, 1),
                    )
                ]
            ],
            justification="right",
        )
    ],
]

# Define the main layout
layout = [
    [
        sg.TabGroup(
            [
                [sg.Tab("Seq2Video", tab1), sg.Tab("Video2Seq", tab2)],
            ],
            selected_background_color="white",
        )
    ]
]

# Create the window
window = sg.Window("Cobanov Ultimate", layout, element_justification="center")

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "Seq2Vid":
        # Process the tab 1 form data
        source_folder = values["-SOURCE-"]
        dest_path = values["-DEST-"]
        fps = int(values["-FPS-"])

        if source_folder and dest_path:
            if os.path.isfile(dest_path):
                overwrite = sg.popup_yes_no(
                    "A file with the same name already exists at the destination. Do you want to overwrite it?",
                    title="Overwrite Confirmation",
                )
                if overwrite == "Yes":
                    seq2vid.seq_list_to_video(source_folder, dest_path, fps)
                    sg.popup("Conversion completed!", title="Seq2Vid")
            else:
                seq2vid.seq_list_to_video(source_folder, dest_path, fps)
                sg.popup("Conversion completed!", title="Seq2Vid")

    if event == "Vid2Seq":
        # Process the tab 2 form data
        video_input = values["-SOURCE_VIDEO-"]
        seq_output_folder = values["-SEQ_DEST-"]
        fps = int(values["-FPS2-"])

        if video_input and seq_output_folder:
            seq2vid.video_to_seq_list(video_input, seq_output_folder, fps)
            sg.popup("Conversion completed!", title="Vid2Seq")

window.close()
