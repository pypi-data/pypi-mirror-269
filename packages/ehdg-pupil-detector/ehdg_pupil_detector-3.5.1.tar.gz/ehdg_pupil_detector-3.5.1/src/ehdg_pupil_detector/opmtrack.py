import csv
import math
import os
import argparse
import importlib.metadata
from importlib.resources import files
import cv2
import commentjson
from ehdg_pupil_detector import ehdg_pupil_detector
from ehdg_tools.ehdg_buffers import TinyFillBuffer
from ehdg_tools.ehdg_plotter import raw_plot
from ehdg_tools.ehdg_functions import string_to_bgr_tuple
import numpy as np
from datetime import datetime


# This function is to get built-in config location with new library (from importlib.resources import files)
def get_config_location(module_name, config_file_name):
    config_dir = files(module_name).joinpath(config_file_name)
    return str(config_dir)


# This function is create the data dict by given data, frame info, event id and trial direction
def get_data_dict(data_input, frame_rate, frame_width, frame_height, direction_input=None):
    d_ts = float(data_input["timestamp"])
    record_timestamp = float(data_input["record_timestamp"])
    x_value = float(data_input["x_value"])
    y_value = float(data_input["y_value"])
    major_axis = float(data_input["major_axis"])
    minor_axis = float(data_input["minor_axis"])
    angle_of_pupil = float(data_input["angle_of_pupil"])
    diameter_of_pupil = float(data_input["diameter_of_pupil"])
    confidence = float(data_input["confidence"])
    ellipse_axis_a = major_axis
    ellipse_axis_b = minor_axis
    ellipse_angle = angle_of_pupil
    diameter = diameter_of_pupil
    frame_rate_input = float(frame_rate)
    sensor_time_stamp = d_ts
    temp_dict = {}
    temp_dict["x_value"] = x_value
    temp_dict["y_value"] = y_value
    temp_dict["x_nom"] = x_value / frame_width
    temp_dict["y_nom"] = 1 - (y_value / frame_height)
    temp_dict["record_timestamp"] = record_timestamp
    temp_dict["sensor_timestamp"] = sensor_time_stamp
    temp_dict["frame_rate"] = frame_rate_input
    if direction_input is not None:
        temp_dict["direction"] = direction_input
    temp_dict["confidence"] = confidence
    temp_dict["diameter"] = diameter
    temp_dict["ellipse_axis_a"] = ellipse_axis_a
    temp_dict["ellipse_axis_b"] = ellipse_axis_b
    temp_dict["ellipse_angle"] = ellipse_angle

    return temp_dict


def print_and_save(file_input, string_input):
    now = datetime.now()
    date_time_string = now.strftime("%d-%m-%Y %H:%M:%S")
    file = open(str(file_input), "a")
    file.write(date_time_string + " | " + string_input + "\n")
    print(string_input)


# This function is to redetect with pupil detector by given detector and tiny fill buffer
# rrt = reflection removal threshold
def opm_detect(trial_video, out_folder, config_dict, plot_dict,
               buffer_length_input, reflection_removal=True,
               rrt_lower_limit=0, rrt_upper_limit=255,
               gaussian_blur=True, binary_fill=True,
               direction_input=None, min_max_circle=True,
               min_circle_color="green", max_circle_color="orange",
               pupil_circle_color="red"):
    out_csv_dir = os.path.join(out_folder, "result.csv")
    out_video_dir = os.path.join(out_folder, "result.mp4")
    log_dir = os.path.join(out_folder, "result.log")
    pupil_circle_color_tuple = string_to_bgr_tuple(pupil_circle_color)
    min_circle_color_tuple = string_to_bgr_tuple(min_circle_color)
    max_circle_color_tuple = string_to_bgr_tuple(max_circle_color)

    detector = ehdg_pupil_detector.Detector(reflection_removal=reflection_removal,
                                            reflection_removal_lower_limit=rrt_lower_limit,
                                            reflection_removal_upper_limit=rrt_upper_limit,
                                            gaussian_blur=gaussian_blur,
                                            binary_fill_hole=binary_fill)

    buffer = TinyFillBuffer(buffer_length_input)
    detector.update_config(config_dict)
    updated_properties = detector.get_config_info()
    print("")
    print("<Detector Properties>")
    for info in updated_properties:
        print(f"{info} : {updated_properties[info]}")
    min_pupil_size = detector.min_pupil_size
    max_pupil_size = detector.max_pupil_size

    print("")
    print(f"Reflection removal : {reflection_removal}")
    print(f"Reflection removal lower threshold : {rrt_lower_limit}")
    print(f"Reflection removal upper threshold : {rrt_upper_limit}")
    print(f"Gaussian blur : {gaussian_blur}")
    print(f"Binary fill : {binary_fill}")

    cap = cv2.VideoCapture(trial_video)
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    print("")
    print(f"frame_rate:{frame_rate}")
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print(f"frame_width:{frame_width}")
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"frame_height:{frame_height}")
    frame_count = 0

    print("")
    print(f"Detecting {trial_video} with opm detector")

    if direction_input is None:
        column_header_array = ["x_value", "y_value", "x_nom", "y_nom",
                               "record_timestamp", "sensor_timestamp",
                               "frame_rate", "confidence", "diameter",
                               "ellipse_axis_a", "ellipse_axis_b",
                               "ellipse_angle"]
    else:
        column_header_array = ["x_value", "y_value", "x_nom", "y_nom",
                               "record_timestamp", "sensor_timestamp",
                               "frame_rate", "direction", "confidence", "diameter",
                               "ellipse_axis_a", "ellipse_axis_b",
                               "ellipse_angle"]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    v_writer = cv2.VideoWriter(out_video_dir, fourcc, frame_rate, (frame_width, frame_height))
    with open(out_csv_dir, mode='w', newline="") as destination_file:
        header_names = column_header_array
        csv_writer = csv.DictWriter(destination_file, fieldnames=header_names)
        csv_writer.writeheader()

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame_count += 1
                frame_time = frame_count / frame_rate
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                result = detector.detect(gray)
                d_ts = result["detector_timestamp"]
                center_of_pupil = result["center_of_pupil"]
                center_of_pupil_x = int(center_of_pupil[0])
                center_of_pupil_y = int(center_of_pupil[1])
                reversed_center_of_pupil = result["reversed_center_of_pupil"]
                x_value = float(reversed_center_of_pupil[0])
                y_value = float(reversed_center_of_pupil[1])
                axes_of_pupil = result["axes_of_pupil"]
                major_axis = float(axes_of_pupil[0])
                minor_axis = float(axes_of_pupil[1])
                angle_of_pupil = float(result["angle_of_pupil"])
                diameter_of_pupil = float(result["average_diameter_of_pupil"])
                confidence = 0 if x_value <= 0 and y_value <= 0 else 1

                center_of_pupil = (int(center_of_pupil_x), int(center_of_pupil_y))
                min_axis = (int(min_pupil_size / 2), int(min_pupil_size / 2))
                max_axis = (int(max_pupil_size / 2), int(max_pupil_size / 2))
                detected_frame = np.copy(frame)
                if center_of_pupil != (0, 0):
                    detected_axis = (math.ceil(major_axis), math.ceil(minor_axis))
                    cv2.ellipse(
                        detected_frame,
                        center_of_pupil,
                        detected_axis,
                        int(angle_of_pupil),
                        0, 360,  # start/end angle for drawing
                        pupil_circle_color_tuple
                    )
                    if min_max_circle:
                        cv2.ellipse(
                            detected_frame,
                            center_of_pupil,
                            min_axis,
                            int(angle_of_pupil),
                            0, 360,  # start/end angle for drawing
                            min_circle_color_tuple
                        )
                        cv2.ellipse(
                            detected_frame,
                            center_of_pupil,
                            max_axis,
                            int(angle_of_pupil),
                            0, 360,  # start/end angle for drawing
                            max_circle_color_tuple
                        )
                else:
                    middle_of_width = int(frame_width / 2)
                    middle_of_height = int(frame_height / 2)
                    min_max_area = (middle_of_width, middle_of_height)
                    if min_max_circle:
                        cv2.ellipse(
                            detected_frame,
                            min_max_area,
                            min_axis,
                            int(angle_of_pupil),
                            0, 360,  # start/end angle for drawing
                            min_circle_color_tuple
                        )
                        cv2.ellipse(
                            detected_frame,
                            min_max_area,
                            max_axis,
                            int(angle_of_pupil),
                            0, 360,  # start/end angle for drawing
                            max_circle_color_tuple
                        )

                v_writer.write(detected_frame)

                pupil_data = {}
                pupil_data["x_value"] = x_value
                pupil_data["y_value"] = y_value
                pupil_data["major_axis"] = major_axis
                pupil_data["minor_axis"] = minor_axis
                pupil_data["angle_of_pupil"] = angle_of_pupil
                pupil_data["diameter_of_pupil"] = diameter_of_pupil
                pupil_data["confidence"] = confidence
                pupil_data["timestamp"] = d_ts
                pupil_data["record_timestamp"] = frame_time
                return_data = buffer.add(pupil_data)
                if return_data is not None:
                    temp_dict = get_data_dict(return_data, frame_rate, frame_width, frame_height, direction_input)
                    csv_writer.writerow(temp_dict)
            else:
                got_first_data = False
                for return_data in buffer.buffer:
                    if not got_first_data:
                        got_first_data = True
                    else:
                        temp_dict = get_data_dict(return_data, frame_rate, frame_width, frame_height, direction_input)
                        csv_writer.writerow(temp_dict)
                destination_file.close()
                v_writer.release()
                print(f"Result folder dir: {out_folder}.")
                print(f"Result csv dir: {out_csv_dir}.")
                print(f"Result video dir: {out_video_dir}.")
                print_and_save(log_dir, f"Min detected pupil size : {round(detector.min_detected_pupil, 2)}")
                print_and_save(log_dir, f"Max detected pupil size : {round(detector.max_detected_pupil, 2)}")
                print_and_save(log_dir, f"Average detected pupil size : {round(detector.avg_detected_pupil, 2)}")
                print_and_save(log_dir, f"Number of detections rejected "
                                        f"by circular ratio : {detector.rejected_by_circular_ratio}")
                print_and_save(log_dir, f"Number of detections rejected by pupil size : {detector.rejected_by_pupil_size}")
                break

    raw_plot_info = plot_dict["raw_plot"]
    out_image_dir = raw_plot(out_csv_dir, raw_plot_info)
    print(f"Result plot image dir: {out_image_dir}.")


def main():
    parser = argparse.ArgumentParser(prog='opmtrack',
                                     description='OKNTRACK program')
    opmtrack_version = importlib.metadata.version('ehdg_pupil_detector')
    parser.add_argument('--version', action='version', version=opmtrack_version),
    parser.add_argument("-i", dest="input_video", required=False, default=None,
                        metavar="input video", help="input video")
    parser.add_argument("-o", dest="output_folder", required=False, default=None,
                        metavar="output folder", help="output folder")
    parser.add_argument("-c", dest="opm_config", required=False, default=None,
                        metavar="opm config", help="opm detector config")
    parser.add_argument("-d", dest="direction_input", required=False, default=None,
                        metavar="direction", help="direction input")
    parser.add_argument("-bl", dest="buffer_length", required=False, default=None,
                        metavar="buffer length", help="buffer length")
    parser.add_argument("-p", dest="plot_config", required=False, default=None,
                        metavar="plot config", help="plot config")
    # store_true action cannot have metavar
    parser.add_argument("-rrr", dest="remove_reflection_removal", required=False,
                        help="remove reflection removal", action="store_false")
    parser.add_argument("-rgb", dest="remove_gaussian_blur", required=False,
                        help="remove gaussian blur", action="store_false")
    parser.add_argument("-rbf", dest="remove_binary_fill_hole", required=False,
                        help="remove binary fill hole", action="store_false")

    parser.add_argument("-rrt", dest="reflection_removal_threshold",
                        required=False, default=None, metavar="",
                        help="reflection removal threshold")

    parser.add_argument("-hmmc", dest="hide_min_max_circle", required=False,
                        help="hide min max circle", action="store_true")

    parser.add_argument("-pmmcc", dest="pupil_min_max_circles_color",
                        required=False, default=None, metavar="",
                        help="pupil min max circles color")

    args = parser.parse_args()
    input_video = args.input_video
    if input_video is None:
        print("opmtrack needs -i argument to accept input video directory.")
        return
    output_folder = args.output_folder
    if output_folder is None:
        print("opmtrack needs -o argument to accept output folder name.")
        return
    opm_config = args.opm_config
    direction_input = args.direction_input
    buffer_length = args.buffer_length
    plot_config = args.plot_config
    remove_reflection_removal = args.remove_reflection_removal
    reflection_removal_threshold = args.reflection_removal_threshold
    if reflection_removal_threshold is not None:
        threshold_string = str(reflection_removal_threshold)
        if "," in threshold_string:
            lower_limit_raw, upper_limit_raw = threshold_string.split(",", 1)
            try:
                lower_limit = int(lower_limit_raw)
                if 0 <= lower_limit <= 255:
                    print(f"Reflection removal threshold lower limit : {lower_limit}")
                else:
                    print("Invalid reflection removal threshold input.")
                    print(f"Reflection removal threshold input : {threshold_string}.")
                    print(f"Invalid lower threshold limit : {lower_limit}")
                    print(f"It must be between 0 and 255.")
                    return
            except ValueError:
                print("Invalid reflection removal threshold input.")
                print(f"Reflection removal threshold input : {threshold_string}.")
                print(f"Invalid lower threshold limit : {lower_limit_raw}")
                return
            try:
                upper_limit = int(upper_limit_raw)
                if 0 <= upper_limit <= 255:
                    print(f"Reflection removal threshold upper limit : {upper_limit}")
                else:
                    print("Invalid reflection removal threshold input.")
                    print(f"Reflection removal threshold input : {threshold_string}.")
                    print(f"Invalid upper threshold limit : {upper_limit}")
                    print(f"It must be between 0 and 255.")
                    return
            except ValueError:
                print("Invalid reflection removal threshold input.")
                print(f"Reflection removal threshold input : {threshold_string}.")
                print(f"Invalid upper threshold limit : {upper_limit_raw}")
                return
            if upper_limit > lower_limit:
                pass
            else:
                print("Invalid reflection removal threshold input.")
                print(f"Reflection removal threshold input : {threshold_string}.")
                print("Threshold upper limit must be greater than lower limit.")
                return
        else:
            print("Invalid reflection removal threshold input.")
            print(f"Reflection removal threshold input : {threshold_string}.")
            return
    else:
        lower_limit = 0
        upper_limit = 255
    remove_gaussian_blur = args.remove_gaussian_blur
    remove_binary_fill = args.remove_binary_fill_hole

    default_buffer_length = 7

    if not os.path.isfile(input_video):
        print(f"Input video is invalid.")
        print(f"Input video: {input_video} is invalid.")
        return

    input_video_name = os.path.basename(input_video)
    output_directory = str(input_video).replace(input_video_name, str(output_folder))

    if os.path.isfile(output_directory):
        print(f"Output directory must be directory not file.")
        print(f"Output directory: {output_directory}.")
        return
    else:
        if not os.path.isdir(output_directory):
            try:
                os.mkdir(output_directory)
                print(f"Output directory is created.")
                print(f"Output directory: {output_directory}.")
            except FileNotFoundError:
                print(f"Output directory cannot be created.")
                print(f"Output directory: {output_directory}.")
                return
            except OSError:
                print(f"Output directory cannot be created.")
                print(f"Output directory: {output_directory}.")
                print(f"Invalid output folder input.")
                print(f"Output folder input: {output_folder}.")
                return

    if opm_config is None:
        opm_config = get_config_location("ehdg_pupil_detector", "opm_detector_config.json")
        try:
            with open(opm_config) as opm_config_info:
                opm_config_dict = commentjson.load(opm_config_info)
                print("There is no custom opm detector config input.")
                print("Therefore, built-in opm detector config will be used.")
                print(f"Location: {opm_config}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Error opening built-in opm config file:{opm_config}!")
    else:
        try:
            with open(opm_config) as opm_config_info:
                opm_config_dict = commentjson.load(opm_config_info)
                print("There is custom opm detector config input.")
                print(f"Location: {opm_config}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Error opening opm config file:{opm_config}!")

    if plot_config is None:
        plot_config = get_config_location("ehdg_pupil_detector", "opmtrack_plot.json")
        try:
            with open(plot_config) as plot_info:
                plot_info_dict = commentjson.load(plot_info)
                print("There is no custom plot info input.")
                print("Therefore, built-in plot info config will be used.")
                print(f"Location: {plot_config}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Error opening built-in opm plot config file:{plot_config}!")
    else:
        try:
            with open(plot_config) as plot_info:
                plot_info_dict = commentjson.load(plot_info)
                print("There is custom plot info input.")
                print(f"Location: {plot_config}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Error opening opm plot config file:{plot_config}!")

    if direction_input is not None:
        if str(direction_input).lower() == "right":
            direction_to_be_used = 1
        elif str(direction_input).lower() == "left":
            direction_to_be_used = -1
        else:
            try:
                direction_to_be_used = int(direction_input)
                if direction_to_be_used == 1 or direction_to_be_used == -1:
                    pass
                else:
                    raise ValueError(f"Invalid direction input {direction_input}.")
            except ValueError:
                raise ValueError(f"Invalid direction input {direction_input}.")
        print(f"There is direction input {direction_input}.")
        print(f"Therefore, direction: {direction_to_be_used} will be added to csv as a column.")
    else:
        print(f"There is no direction input.")
        print(f"Therefore, there will be no direction column in result.csv.")
        direction_to_be_used = None

    if buffer_length is not None:
        try:
            buffer_length_to_be_used = int(buffer_length)
            print("There is buffer length input.")
            print(f"OPM detector will be using Tiny Fill Buffer with length:{buffer_length_to_be_used}.")
        except ValueError:
            buffer_length_to_be_used = default_buffer_length
            print(f"There is buffer length input but it is invalid: {buffer_length}.")
            print(f"OPM detector will be using Tiny Fill Buffer with default length:{buffer_length_to_be_used}.")
    else:
        buffer_length_to_be_used = default_buffer_length
        print("There is no buffer length input.")
        print(f"OPM detector will be using Tiny Fill Buffer with default length:{buffer_length_to_be_used}.")

    hide_min_max_circle = args.hide_min_max_circle
    pupil_min_max_circles_color = args.pupil_min_max_circles_color

    pupil_color_string = "red"
    min_color_string = "green"
    max_color_string = "orange"
    if pupil_min_max_circles_color is not None:
        if "," in pupil_min_max_circles_color:
            color_string_array = str(pupil_min_max_circles_color).split(",")
            if len(color_string_array) == 3:
                pupil_color_string = color_string_array[0]
                pupil_color_string = str(pupil_color_string).replace("-", " ")
                min_color_string = color_string_array[1]
                min_color_string = str(min_color_string).replace("-", " ")
                max_color_string = color_string_array[2]
                max_color_string = str(max_color_string).replace("-", " ")
                print(f"Pupil circle color will be {pupil_color_string}.")
                print(f"Min circle color will be {min_color_string}.")
                print(f"Max circle color will be {max_color_string}.")
            else:
                print("Invalid pupil_min_max_circles_color input.")
                print(f"The pupil_min_max_circles_color input : {pupil_min_max_circles_color}.")
                print("Example input:")
                print("-pmmcc red,green,orange")
                return
        else:
            print("Invalid pupil_min_max_circles_color input.")
            print(f"The pupil_min_max_circles_color input : {pupil_min_max_circles_color}.")
            print("Example input:")
            print("-pmmcc red,green,orange")
            return

    opm_detect(input_video, output_directory, opm_config_dict, plot_info_dict,
               buffer_length_to_be_used,
               reflection_removal=remove_reflection_removal,
               rrt_lower_limit=lower_limit,
               rrt_upper_limit=upper_limit,
               gaussian_blur=remove_gaussian_blur,
               binary_fill=remove_binary_fill,
               direction_input=direction_to_be_used,
               min_max_circle=not hide_min_max_circle,
               min_circle_color=min_color_string,
               max_circle_color=max_color_string,
               pupil_circle_color=pupil_color_string)
