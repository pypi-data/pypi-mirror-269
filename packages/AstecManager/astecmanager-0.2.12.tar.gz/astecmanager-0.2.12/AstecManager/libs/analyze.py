import os
from os import listdir
import numpy as np
import re
from os.path import isfile, join
from AstecManager.libs.data import imread
import matplotlib.pyplot as plt
from AstecManager.libs.lineage import temporal_alignment, get_aligned_time, build_all_leaves, count_cells,Get_Cell_Contact_Surface, Get_Cell_Names, get_id_t
from AstecManager.libs.jsonlib import addDictToMetadata


def apply_analysis(list_lineage, list_noms, folder_out, embryo_name, begin, end,
                   is_post=False, ref_lineage=None, data_path=None):
    """

    :param list_lineage: 
    :param list_noms: 
    :param folder_out: 
    :param embryo_name: 
    :param begin: 
    :param end: 
    :param is_post:  (Default value = False)
    :param ref_lineage:  (Default value = None)
    :param data_path:  (Default value = None)

    """
    print("-> Compute of the cell count plot")
    generate_compare(list_noms, list_lineage, folder_out=folder_out, embryo_name=embryo_name,
                     ref_lineage_path=ref_lineage, data_path=data_path)

    folder_exp = folder_out

    print("-> compute all min max leaves in for ")

    begin_temp = begin
    end_temp = end
    if is_post:
        plotminmaxleaves_post(list_lineage[0], list_noms[0], begin_temp, end_temp, folder_out, data_path=None)
    else:
        plotminmaxleaves(list_lineage, list_noms, begin_temp, end_temp, embryo_name, folder_out, data_path=None)

    os.system("cd " + folder_exp + ' && `for f in *.py; do python3 "$f"; done`')
    os.system("cd " + folder_out + ' && rm generate_cell_count_multiples_.py')


def is_uncompressed_image(f):
    """

    :param f: 

    """
    return ".nii" in f or ".mha" in f or ".h5" in f or ".inr" in f


def generate_compare(input_names, list_lineage, folder_out="DATA/OUT/", embryo_name="",
                     remove_times=None, only_times=None,ref_lineage_path=None,
                     data_path=None):
    """

    :param input_names: 
    :param list_lineage: 
    :param folder_out:  (Default value = "DATA/OUT/")
    :param embryo_name:  (Default value = "")
    :param remove_times:  (Default value = None)
    :param only_times:  (Default value = None)
    :param ref_lineage_path:  (Default value = None)
    :param data_path:  (Default value = None)

    """
    folder_exp = ""
    for embryoname in input_names:
        if embryoname is not None:
            folder_exp += embryoname + "_"

    for lineage in list_lineage:
        if not os.path.isfile(lineage):
            print(lineage + " is not a file , check for typos")
            return

    if data_path is not None:
        if not os.path.isdir(data_path):
            os.makedirs(data_path)
    list_count = {}
    list_name = []
    list_histo = []
    ref_cell_count = None
    if ref_lineage_path != None:
        ref_cell_count = count_cells(ref_lineage_path, remove_time=([] if remove_times is None else remove_times),
                                     only_times=[] if only_times is None else only_times)
    for i in range(0, len(list_lineage)):
        count = count_cells(list_lineage[i], remove_time=([] if remove_times is None else remove_times),
                            only_times=[] if only_times is None else only_times)
        txt = ""
        for key in count:
            txt += str(key) + ":" + str(count[key]) + ";"
        if data_path is not None:
            f = open(os.path.join(data_path, str(input_names[i]) + "-cell-count.csv"), "w+")
            f.write(txt)
            f.close()

        if ref_lineage_path != None:
            a, b = temporal_alignment(ref_lineage_path, list_lineage[i])
            temp_count = {}
            for time in count:
                print("aligned time : " + str(get_aligned_time(time, a, b)) + " get count " + str(
                    count[time]) + " from time init : " + str(time))
                # TODO : verifier si on doit pas prendre le temps aligné de l'embryon
                temp_count[get_aligned_time(time, a, b)] = count[time]
            count = temp_count
        list_histo.append(count)
        for t in count:
            list_count[input_names[i]] = [count[t]]
        list_name.append(input_names[i].replace("SEG_test_", ""))
        parameters = {}
        parameters["list_embryo_name"] = plot_variables(list_name, False)
        parameters["list_cell_count_by_time"] = plot_variables(list_histo, False)
        if embryo_name != "":
            parameters["embryo_name"] = plot_variables(embryo_name, True)
        if ref_lineage_path != None:
            save_cell_count_plot("cell_count_multiples", list_name, list_histo, folder_out,
                                 cell_count_ref=ref_cell_count)
        else:
            save_cell_count_plot("cell_count_multiples", list_name, list_histo, folder_out)
        parameters = {}
        # addDictToMetadata(path, parameters)


def save_cell_count_plot(plot_title, list_names, list_count, folder_out, cell_count_ref=None):
    """

    :param plot_title: 
    :param list_names: 
    :param list_count: 
    :param folder_out: 
    :param cell_count_ref:  (Default value = None)

    """
    list_cell_count_by_time = list_count
    import matplotlib.transforms as transforms
    folder_out = folder_out
    list_embryo_name = list_names
    if not os.path.isdir(folder_out):
        os.makedirs(folder_out)

    print(">>Cells counted, saving to image result")
    title = "cell_count"
    plt.figure(figsize=(10, 6))
    plt.title("Cell count along time" + "_" + title)
    plt.xlabel("Time")
    plt.ylabel("Cell count")
    for i in range(0, len(list_cell_count_by_time)):
        print(str(list_embryo_name[i]) + " -> " + str(list_cell_count_by_time[i]))
        times = []
        cell_counts = []
        cell_count_by_time = list_cell_count_by_time[i]
        for time in cell_count_by_time:
            times.append(time)
            cell_counts.append(cell_count_by_time[time])
        plt.plot(times, cell_counts, '-', label=list_embryo_name[i], alpha=0.5)
    if cell_count_ref is not None:
        timesref = []
        cell_countsref = []
        for time in cell_count_ref:
            timesref.append(time)
            cell_countsref.append(cell_count_ref[time])
        plt.plot(timesref, cell_countsref, '-', label="reference", color='grey', alpha=0.5)
    trans = transforms.blended_transform_factory(
        plt.gca().get_yticklabels()[0].get_transform(), plt.gca().transData)
    stages = [64,72,116,184]
    for stage in stages:
        plt.axhline(y=stage,color='grey',alpha=0.3)
        plt.text(0, stage, "{:.0f}".format(stage), color="grey", transform=trans,
                ha="right", va="center")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(folder_out, title + ".png"))
    plt.clf()


def plotminmaxleaves(lineage_list, embryo_name_list, start_time, end_time, embryo_name, folder_out="DATA/OUT/",
                     data_path=None):
    """

    :param lineage_list: 
    :param embryo_name_list: 
    :param start_time: 
    :param end_time: 
    :param embryo_name: 
    :param folder_out:  (Default value = "DATA/OUT/")
    :param data_path:  (Default value = None)

    """
    if folder_out != "":
        if not os.path.exists(folder_out):
            os.makedirs(folder_out)

    if data_path is not None:
        if not os.path.isdir(data_path):
            os.makedirs(data_path)
    fig, ax = plt.subplots(2, 2)

    fig.suptitle("Early cell death detection in branch")
    cell_keys_info = {}
    timefor64cells = start_time
    finalx = []
    current_axis_x = 0
    current_axis_y = 0
    for i in range(0, len(lineage_list)):
        lineage = lineage_list[i]
        if has_info_lineage(lineage, "cell_name") or has_info_lineage(lineage, "cell_contact_surface") and False:
            timefor64cells = -1
            cellcountfortime = 64
            cellforlineage = dict(sorted(count_cells(lineage).items()))
            for time in cellforlineage:
                if cellforlineage[time] >= 64:
                    timefor64cells = int(time)
                    cellcountfortime = int(cellforlineage[time])
                break
        cell_keys_by_time, final_proportion, mars_ids1, all_leaves = build_all_leaves(lineage, timefor64cells,
                                                                                      end_time)
        txt = ""
        if data_path is not None:
            for i in range(0, len(all_leaves)):
                txt += str(mars_ids1[i]) + ":" + str(all_leaves[i]) + ";"
            txt += str(final_proportion)
            f = open(os.path.join(data_path, str(embryo_name)) + "-early-cell-death.csv", "w+")
            f.write(txt)
            f.close()
        cell_keys_info[lineage] = cell_keys_by_time

        finalx = []
        lineagepath = None
        if has_info_lineage(lineage, "cell_name") and False:
            nameinit = get_cell_names(lineage, mars_ids1)
            finalx = nameinit
        elif has_info_lineage(lineage, "cell_contact_surface") and False:
            lineagepath = auto_name_time(lineage, cellcountfortime)
            nameinit = get_cell_names(lineagepath, mars_ids1)
            finalx = nameinit
        else:
            for idcell in mars_ids1:
                finalx.append(format_cell_id(idcell))
        if lineagepath is not None:
            os.system("rm " + str(lineagepath))
        ax[current_axis_x, current_axis_y].plot([], [], ' ',
                                                label="early cell missing:" + str(round(final_proportion, 3)) + "%")
        print(str(len(all_leaves)) + " - " + str(len(finalx)))
        if len(all_leaves) > 0:
            ax[current_axis_x, current_axis_y].boxplot(all_leaves, labels=finalx)
        ax[current_axis_x, current_axis_y].set_ylim([start_time, end_time])
        ax[current_axis_x, current_axis_y].set_title(embryo_name_list[i].replace("SEG_test_", ""))
        ax[current_axis_x, current_axis_y].set_xticklabels([])
        if current_axis_y == 0:
            ax[current_axis_x, current_axis_y].set_ylabel("Time of cell missing")
        if current_axis_x == 1:
            ax[current_axis_x, current_axis_y].set_xlabel("Lineage branch")
        ax[current_axis_x, current_axis_y].legend()
        current_axis_x = (current_axis_x + 1) % 2
        if current_axis_x == 0:
            current_axis_y += 1 % 2

    print("Saving to identity card")
    fig.tight_layout()
    fig.set_size_inches(18.5, 10.5)
    fig.suptitle("Early cell missing for " + str(embryo_name), fontsize=14)
    fig.savefig(folder_out + "/early_cell_death.png")


def plotminmaxleaves_post(lineage, embryo_name, start_time, end_time, folder_out="DATA/OUT/", data_path=None):
    """

    :param lineage: 
    :param embryo_name: 
    :param start_time: 
    :param end_time: 
    :param folder_out:  (Default value = "DATA/OUT/")
    :param data_path:  (Default value = None)

    """
    if folder_out != "":
        if not os.path.exists(folder_out):
            os.makedirs(folder_out)
    if data_path is not None:
        if not os.path.isdir(data_path):
            os.makedirs(data_path)
    fig = plt.figure()

    fig.suptitle("Early cell death detection in branch")
    cell_keys_info = {}
    timefor64cells = start_time
    finalx = []
    if has_info_lineage(lineage, "cell_name") or has_info_lineage(lineage, "cell_contact_surface") and False:
        timefor64cells = -1
        cellcountfortime = 64
        cellforlineage = dict(sorted(count_cells(lineage).items()))
        for time in cellforlineage:
            if cellforlineage[time] >= 64:
                timefor64cells = int(time)
                cellcountfortime = int(cellforlineage[time])
            break
    cell_keys_by_time, final_proportion, mars_ids1, all_leaves = build_all_leaves(lineage, timefor64cells,
                                                                                  end_time)

    txt = ""
    if data_path is not None:
        for i in range(0, len(all_leaves)):
            txt += str(mars_ids1[i]) + ":" + str(all_leaves[i]) + ";"
        txt += str(final_proportion)
        f = open(os.path.join(data_path, str(embryo_name)) + "-early-cell-death.csv", "w+")
        f.write(txt)
        f.close()
        name = lineage.replace("\\", "/").split("/")[-1]
    cell_keys_info[lineage] = cell_keys_by_time

    finalx = []
    lineagepath = None
    if has_info_lineage(lineage, "cell_name") and False:
        nameinit = get_cell_names(lineage, mars_ids1)
        finalx = nameinit
    elif has_info_lineage(lineage, "cell_contact_surface") and False:
        lineagepath = auto_name_time(lineage, cellcountfortime)
        nameinit = get_cell_names(lineagepath, mars_ids1)
        finalx = nameinit
    else:
        for idcell in mars_ids1:
            finalx.append(format_cell_id(idcell))
    if lineagepath is not None:
        os.system("rm " + str(lineagepath))
    plt.plot([], [], ' ', label="early cell missing:" + str(round(final_proportion, 3)) + "%")
    if len(all_leaves) > 0:
        plt.boxplot(all_leaves, labels=finalx)
    plt.ylim([start_time, end_time])
    plt.title(embryo_name.replace("SEG_test_", ""))
    plt.xticks(rotation=90)
    plt.legend()
    plt.xlabel("Lineage branch")
    plt.ylabel("Time of cell missing")

    print("Saving to identity card")
    # fig.tight_layout()
    # fig.set_size_inches(18.5, 10.5)
    plt.title("Early cell missing for " + str(embryo_name), fontsize=14)
    fig.savefig(folder_out + "/early_cell_death.png")


def camerastacksignaltonoise(axis, folder_images, analysisfolder, title, boundaries=None, display_x_label=True,
                             display_y_label=True):
    """

    :param axis: 
    :param folder_images: 
    :param analysisfolder: 
    :param title: 
    :param boundaries:  (Default value = None)
    :param display_x_label:  (Default value = True)
    :param display_y_label:  (Default value = True)

    """
    print("     -> Intensities analysis for folder : " + str(folder_images))
    if boundaries is None:
        boundaries = [0, 2000]
    average_by_time = {}
    max_by_time = {}
    if not os.path.isdir(join(analysisfolder, "raw")):
        os.makedirs(join(analysisfolder, "raw"))
    csv_data = join(join(analysisfolder, "raw"), title.replace(" ", "_") + ".csv")
    if os.path.isfile(csv_data):
        f = open(csv_data, "r")
        datacsv = f.read()
        f.close()
        for line in datacsv.split(":"):
            if line != "":
                data = line.split(";")
                time = int(data[0])
                mean = float(data[1])
                std = float(data[2])
                average_by_time[time] = mean
                max_by_time[time] = std

    else:
        image_name_list = [f for f in listdir(folder_images) if isfile(join(folder_images, f)) and is_uncompressed_image(f)]
        image_name_list.sort()
        csv = ""
        for image_name in image_name_list:
            image_path = join(folder_images, image_name)
            image_time = int(re.findall(r'\d+', image_name.split(".")[0])[-1])
            image_np = imread(image_path)
            mean = np.mean(image_np)
            intensities = list(np.unique(image_np.reshape(-1)))
            intensities.sort()
            intensities.reverse()
            cumulated = []
            for intensity in intensities:
                if len(cumulated) < 0.05 * len(intensities):
                    cumulated.append(intensity)
            max_cumulated = min(cumulated)
            maxt = np.max(image_np)
            print("Image max : " + str(maxt) + " cumulated max : " + str(max_cumulated))
            # Get the list of intensities in images
            # Sort them
            # Take the one at 95%
            average_by_time[image_time] = mean
            max_by_time[image_time] = max_cumulated
            csv += str(image_time) + ";" + str(mean) + ";" + str(max_cumulated) + ":"
        f = open(csv_data, "w+")
        f.write(csv)
        f.close()
    data_means = list(average_by_time.values())
    data_std = list(max_by_time.values())
    times = list(average_by_time.keys())
    axis.plot(times, data_means, '-')
    mins = min([a - b for a, b in zip(data_means, data_std)])
    maxs = max([a + b for a, b in zip(data_means, data_std)])
    axis.fill_between(times, [a + b for a, b in zip(data_means, data_std)], [a for a in data_means], alpha=0.2)
    axis.set_ylim(boundaries)
    if display_x_label:
        axis.set_xlabel("Time")
    if display_y_label:
        axis.set_ylabel("Signal mean (line) and amplitude")
    axis.legend()
    axis.set_title(title)
    return mins, maxs, csv_data

def generate_plots_signal_to_noise(stack_0_left_cam,stack_0_right_cam,stack_1_left_cam,stack_1_right_cam,export_folder):
    mins = []
    maxs = []
    if export_folder != "":
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)
        fig, ax = plt.subplots(2, 2)
        if stack_0_left_cam is not None:
            miny, maxy, csv = camerastacksignaltonoise(ax[0, 0], stack_0_left_cam, export_folder, "Left camera of stack 0",
                                                       display_x_label=False,
                                                       display_y_label=True)
            mins.append(miny)
            maxs.append(maxy)
        if stack_0_right_cam is not None:
            miny, maxy, csv = camerastacksignaltonoise(ax[0, 1], stack_0_right_cam, export_folder, "Right camera of stack 0",
                                                       display_x_label=False,
                                                       display_y_label=False)
            mins.append(miny)
            maxs.append(maxy)
        if stack_1_left_cam is not None:
            miny, maxy, csv = camerastacksignaltonoise(ax[1, 0], stack_1_left_cam, export_folder, "Left camera of stack 1",
                                                       display_x_label=True,
                                                       display_y_label=True)
            mins.append(miny)
            maxs.append(maxy)
        if stack_1_right_cam is not None:
            miny, maxy, csv = camerastacksignaltonoise(ax[1, 1], stack_1_right_cam, export_folder, "Right camera of stack 1",
                                                       display_x_label=True,
                                                       display_y_label=False)
            mins.append(miny)
            maxs.append(maxy)
        realmin = min(mins)
        realmax = max(maxs)
        ax[0, 0].set_ylim([0, realmax])
        ax[0, 1].set_ylim([0, realmax])
        ax[1, 0].set_ylim([0, realmax])
        ax[1, 1].set_ylim([0, realmax])
        fig.tight_layout()
        fig.set_size_inches(18.5, 10.5)
        fig.suptitle("Signal mean and amplitude though time in raw images", fontsize=14)
        fig.savefig(export_folder, "raw_images_intensities.png")
def plotsignaltonoise(embryo_name, parameters, one_stack_only=False, stack_chosen=0,add_to_metadata=True):
    """

    :param embryo_name: 
    :param parameters: 
    :param one_stack_only:  (Default value = False)
    :param stack_chosen:  (Default value = 0)

    """

    stack_0_left_cam = None
    stack_0_right_cam = None
    stack_1_right_cam = None
    stack_1_left_cam = None
    path = "."
    folder_out = os.path.join(path, "analysis","raw")
    raw_path = os.path.join(path, parameters["DIR_RAWDATA"].replace('"', '').replace("'", ""))
    if (one_stack_only and stack_chosen == 0) or not one_stack_only:
        stack_0_left_cam = os.path.join(raw_path, parameters["DIR_LEFTCAM_STACKZERO"].replace('"', '').replace("'", ""))
        stack_0_right_cam = os.path.join(raw_path,
                                         parameters["DIR_RIGHTCAM_STACKZERO"].replace('"', '').replace("'", ""))
    if (one_stack_only and stack_chosen == 1) or not one_stack_only:
        stack_1_left_cam = os.path.join(raw_path, parameters["DIR_LEFTCAM_STACKONE"].replace('"', '').replace("'", ""))
        stack_1_right_cam = os.path.join(raw_path,
                                         parameters["DIR_RIGHTCAM_STACKONE"].replace('"', '').replace("'", ""))
    generate_plots_signal_to_noise(stack_0_left_cam, stack_0_right_cam, stack_1_left_cam,
                                   stack_1_right_cam, folder_out)
    if add_to_metadata:
        parameters["step"] = "rawdata_intensities_plot"
        parameters["embryo_name "] = embryo_name
        addDictToMetadata(path, parameters)


def plotsignaltonoise_tofolder(folder, one_stack_only=False, stack_chosen=0):
    """

    :param folder: 
    :param one_stack_only:  (Default value = False)
    :param stack_chosen:  (Default value = 0)

    """
    folder_out = os.path.join(folder, "analysis")
    if folder_out != "":
        if not os.path.exists(folder_out):
            os.makedirs(folder_out)
    raw_path = os.path.join(folder, "RAWDATA")
    stack_0_left_cam = None
    stack_0_right_cam = None
    stack_1_left_cam = None
    stack_1_right_cam = None
    if (one_stack_only and stack_chosen == 0) or not one_stack_only:
        stack_0_left_cam = os.path.join(raw_path, "stack_0_channel_0_obj_left")
        stack_0_right_cam = os.path.join(raw_path, "stack_0_channel_0_obj_right")
    if (one_stack_only and stack_chosen == 1) or not one_stack_only:
        stack_1_left_cam = os.path.join(raw_path, "stack_1_channel_0_obj_left")
        stack_1_right_cam = os.path.join(raw_path, "stack_1_channel_0_obj_right")
    generate_plots_signal_to_noise(stack_0_left_cam, stack_0_right_cam, stack_1_left_cam,
                                   stack_1_right_cam, folder_out)

class plot_variables:
    """ """
    def __init__(self, value, isstring):
        self.value = value

        self.isstring = isstring

def format_cell_id(cellid):
    """

    :param cellid:

    """
    tc, idc = get_id_t(int(cellid))
    return str(tc) + "," + str(idc)

def has_info_lineage(lineage, info_name):
    """

    :param lineage:
    :param info_name:

    """
    return Get_Cell_Contact_Surface(lineage, info_name) is not None

def get_cell_names(lineage, cells):
    """

    :param lineage:
    :param cells:

    """
    result_names = []
    names = Get_Cell_Names(lineage)
    for cell in cells:
        if cell in names:
            namesplitted = names[cell].split('.')
            result_names.append(namesplitted[0] + "." + namesplitted[1].lstrip("0").replace("_", "-"))
        else:
            result_names.append(str(format_cell_id(cell)))
    return result_names

def lineage_path_with_names(lineagepath):
    """

    :param lineagepath:

    """
    lineagepathsplited = lineagepath.split('.')
    return lineagepathsplited[0] + "_minmaxnamed" + "." + lineagepathsplited[1]


def auto_name_time(lineage, cellcount):
    from AstecManager.Manager import compute_atlas
    """

    :param lineage: 
    :param cellcount: 

    """
    outlineage = lineage_path_with_names(lineage)
    parameters = ""
    parameters += 'cell_number=' + str(cellcount) + '\n'
    parameters += 'inputFile="' + str(lineage) + '"\n'
    parameters += 'outputFile="' + str(outlineage) + '"\n'
    parameters += "atlasFiles=" + str(compute_atlas()) + "\n"
    f = open("parameters_naming.py", "w+")
    f.write(parameters)
    f.close()
    os.system("conda run -n astec astec_atlas_init_naming -p parameters_naming.py")
    os.remove("parameters_naming.py")
    os.system("rm *.log")
    return outlineage