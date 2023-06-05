import dearpygui.dearpygui as dpg
from utils import seq2vid

dpg.create_context()
dpg.create_viewport(title='Cobanov Ultimate', width=600, height=500, resizable=False)

def _help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(?)", color=[0, 255, 0])
    with dpg.tooltip(t):
        dpg.add_text(message)

def file_folder(is_folder=False, input_text_id=0):
    """
    Open file/folder dialog
    """
    with dpg.file_dialog(
        directory_selector=is_folder, callback=lambda x,y: dpg.set_value(input_text_id, y["file_path_name"]), width=400 ,height=400):
        if not is_folder:
            dpg.add_file_extension(".*")
            
def procces(sender, data):
    """
    Starts Process button callback
    """
    active = dpg.get_item_alias(dpg.get_value("tab_bar"))
    if active == "Seq2Vid":
        source_folder = dpg.get_value("png_source")
        dest_path = dpg.get_value("video_output")
        fps = dpg.get_value("fps1")
        seq2vid.seq_list_to_video(source_folder, dest_path, fps)
    elif active == "Vid2Seq":
        video_input = dpg.get_value("video_input")
        seq_output_folder = dpg.get_value("output_folder")
        fps = dpg.get_value("fps2")
        seq2vid.video_to_seq_list(video_input, seq_output_folder, fps)
        

with dpg.window(label="Cobanov", width=dpg.get_viewport_width(), height=dpg.get_viewport_height(), tag="main"):
    with dpg.tab_bar(tag="tab_bar"):
        with dpg.tab(label="Seq2Video", tag="Seq2Vid"):
            dpg.add_text("PNG Sequence Folder")
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="png_source")
                dpg.add_button(label="Folder Select", callback=lambda: file_folder(is_folder=True, input_text_id="png_source"))
            
            dpg.add_text("Video Output Path")
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="video_output")
                dpg.add_button(label="Save As", callback=lambda: file_folder(is_folder=False, input_text_id="video_output"))
            
            dpg.add_text("FPS")
            _help("CTRL+click to enter value.")
            dpg.add_slider_int(min_value=1, max_value=120, tag="fps1")
            
        with dpg.tab(label="Video2Seq", tag="Vid2Seq"):
            dpg.add_text("Video Input")
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="video_input")
                dpg.add_button(label="Folder Select", callback=lambda: file_folder(is_folder=False, input_text_id="video_input"))
            
            dpg.add_text("Sequence Output Folder")
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="output_folder")
                dpg.add_button(label="Save As", callback=lambda: file_folder(is_folder=True, input_text_id="output_folder"))
            
            dpg.add_text("FPS")
            _help("CTRL+click to enter value.")
            dpg.add_slider_int(min_value=1, max_value=120, tag="fps2")
            
        with dpg.tab(label="Depth"):
            dpg.add_text("Empty For Now", color=(255, 0, 0))
    
    
    # start process theme (color red)
    with dpg.theme(tag="theme_red"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (135, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (255, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (195, 0, 0))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3, 3)
            
    dpg.add_spacer(height=25)
    dpg.add_button(label="Start Process", callback=procces)
    dpg.bind_item_theme(dpg.last_item(), "theme_red")

dpg.set_primary_window("main", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()