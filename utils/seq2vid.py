import glob
import os
import ffmpeg
import shutil


def read_images_from_directory(image_directory: str, sort=False) -> list:
    """
    This function takes a directory as input and returns a list of all the images in that directory.

    :param image_directory: The directory where the images are stored
    :type image_directory: str
    :return: A list of image file paths
    """

    extensions = ["*.gif", "*.png", "*.jpg", "*.jpeg"]
    list_of_images = []
    for ext in extensions:
        pattern = os.path.join(image_directory, ext)
        list_of_images.extend(glob.glob(pattern))
    if sort:
        list_of_images = sorted(list_of_images)

    print(f"Images found: {len(list_of_images)}")

    return list_of_images


def seq_list_to_video(source_folder, dest_path, fps):
    """
    Convert a list of image sequences to an MP4 video file with adjustable FPS.

    :param paths: A list of paths to directories containing the image sequences
    :param dest_path: The output MP4 video file name
    :param fps: The frame rate of the video
    """

    paths = read_images_from_directory(source_folder)
    # Create temp directory
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Move files to temp directory and rename sequentially
        for i, file_name in enumerate(paths):
            dst = os.path.join(temp_dir, f"frame_{i:06d}.png")
            shutil.copy(file_name, dst)

        # Add extension if not
        if not dest_path.endswith((".mp4", ".mov")):
            dest_path += ".mp4"

        (
            ffmpeg.input(
                f"{temp_dir}/frame_%6d.png", pattern_type="sequence", framerate=fps
            )
            .output(dest_path, crf=18, pix_fmt="yuv420p")
            .overwrite_output()
            .run()
        )
    finally:
        # Clean up: remove temp directory and its contents
        shutil.rmtree(temp_dir)
        print("Done")


def video_to_seq_list(video_input, seq_output_folder, fps):
    """
    Convert an MP4 video file into a sequence of images.

    :param video_input: The input MP4 video file name
    :param seq_output_folder: The output directory to save the image sequences
    :param fps: Frames per second for the output image sequence
    """

    # Create output directory if it doesn't exist
    os.makedirs(seq_output_folder, exist_ok=True)

    try:
        # Set the input video file and output image sequence format
        input_video = ffmpeg.input(video_input)
        output_sequence = os.path.join(seq_output_folder, "frame_%06d.png")

        # Define the input and output streams
        output_stream = ffmpeg.output(input_video, output_sequence, r=fps)

        # Run the conversion process
        ffmpeg.run(output_stream)

    finally:
        print("Done")
