import PySimpleGUI as sg
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
                    sg.Cancel(),
                    sg.Button(
                        "Seq2Vid", button_color=("white", "green"), bind_return_key=True
                    ),
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
    [sg.Text(" Sequence Output Folder")],
    [sg.Input(key="-SEQ_DEST-", enable_events=True), sg.FolderBrowse()],
    [sg.Text("FPS"), sg.Input(default_text=30, key="-FPS-", size=(5, 1))],
    [
        sg.Column(
            [
                [
                    sg.Cancel(),
                    sg.Button(
                        "Vid2Seq", button_color=("white", "green"), bind_return_key=True
                    ),
                ]
            ],
            justification="right",
        )
    ],
]

# Define the layout for the second tab
tab3 = [
    [sg.Text("Video Input")],
    [sg.Input(key="-SOURCE_VIDEO-", enable_events=True), sg.FileBrowse()],
    [sg.Text(" Sequence Output Folder")],
    [sg.Input(key="-SEQ_DEST-", enable_events=True), sg.FolderBrowse()],
    [sg.Text("Select an option:")],
    [sg.Radio("Depth", "radio_group", default=True, key="-DEPTH-")],
    [sg.Radio("MLSD", "radio_group", key="-MLSD-")],
    [sg.Radio("HED", "radio_group", key="-HED-")],
    [sg.Radio("Normal", "radio_group", key="-NORMAL-")],
    [
        sg.Column(
            [
                [
                    sg.Cancel(),
                    sg.Button(
                        "Vid2Seq", button_color=("white", "green"), bind_return_key=True
                    ),
                ]
            ],
            justification="right",
        ),
    ],
]


# Define the main layout
layout = [
    [
        sg.TabGroup(
            [
                [
                    sg.Tab("Seq2Video", tab1),
                    sg.Tab("Video2Seq", tab2),
                    sg.Tab("Depth", tab3),
                ]
            ],
        )
    ]
]


# Create the window
window = sg.Window("Cobanov Ultimate", layout)


while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Cancel":
        break

    if event == "Seq2Vid":
        # Determine the active tab and process the form data accordingly

        if values["-SOURCE-"] and values["-DEST-"]:
            source_folder = values["-SOURCE-"]
            dest_path = values["-DEST-"]
            fps = int(values["-FPS-"])
            seq2vid.seq_list_to_video(source_folder, dest_path, fps)

    if event == "Vid2Seq":
        # Process the tab 2 form data
        if values["-SOURCE_VIDEO-"] and values["-SEQ_DEST-"]:
            video_input = values["-SOURCE_VIDEO-"]
            seq_output_folder = values["-SEQ_DEST-"]
            fps = int(values["-FPS-"])

            seq2vid.video_to_seq_list(video_input, seq_output_folder, fps)

window.close()
