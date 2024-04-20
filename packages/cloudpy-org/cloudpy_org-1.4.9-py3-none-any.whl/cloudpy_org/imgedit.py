from PIL import Image, ImageSequence
import os
class colors:
    def __init__(self):
        self.cloudpy_org_palette = {}
        self.cloudpy_org_palette["logo_blue"] = 'rgb(66,133,234)'
        self.cloudpy_org_palette["logo_yellow"] = 'rgb(248,208,67)'
        self.cloudpy_org_palette["logo_dark"] = 'rgb(46,46,46)'
        self.cloudpy_org_palette["sky_blue"] = 'rgb(153,204,255)'
        self.cloudpy_org_palette["input_gray_background"] = 'rgb(230,230,230)'
        self.cloudpy_org_palette["input_gray_background"] = 'rgb(230,230,230)'

    def rgb_color_distance(self,color1, color2):
        return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)) ** 0.5

    def change_similar_rgb_in_gif(self,input_path, output_path, source_color, target_color, tolerance=30):
        # Open the GIF file
        with Image.open(input_path) as img:
            # Create a list to store the modified frames
            modified_frames = []

            # Iterate through each frame in the GIF
            for frame in ImageSequence.Iterator(img):
                # Convert the frame to RGBA mode (if not already in that mode)
                frame = frame.convert("RGBA")

                # Get the disposal method and duration of the original frame
                disposal_method = frame.info.get("dispose", 0)
                duration = frame.info.get("duration", 100)

                # Get the image data as a list of tuples
                data = list(frame.getdata())

                # Replace colors similar to the source color with the target color in each pixel
                new_data = [
                    (target_color[0], target_color[1], target_color[2], pixel[3])
                    if rgb_color_distance((pixel[0], pixel[1], pixel[2]), source_color) <= tolerance
                    else pixel
                    for pixel in data
                ]

                # Create a new frame with the modified pixel data, copy the disposal method and duration
                modified_frame = Image.new("RGBA", frame.size)
                modified_frame.putdata(new_data)
                modified_frame.info["dispose"] = disposal_method
                modified_frame.info["duration"] = duration

                # Append the modified frame to the list
                modified_frames.append(modified_frame)

            # Save the modified frames as a new GIF
            loop_value = img.info.get("loop", 0)
            modified_frames[0].save(output_path, "GIF", save_all=True, append_images=modified_frames[1:],
                                    duration=img.info["duration"], loop=loop_value)