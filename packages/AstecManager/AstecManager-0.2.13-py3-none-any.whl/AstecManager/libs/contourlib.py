import os
import numpy as np
from AstecManager.libs.data import imread,imsave
from scipy import ndimage as nd
def fill_image(imagein, folderin):
    """ Threshold a given background image and fill the holes in the background using skimage morphology tool

    :param imagein: Name of the image to be filled
    :type imagein: str
    :param folderin: Folder of the image
    :type folderin: str
    :return: The image array after being filled , and the voxel size of the image
    :rtype: tuple

    """
    from skimage import morphology
    arraynp, vsize = imread(os.path.join(folderin, imagein), voxel_size=True)
    im_bin = (arraynp < 150)
    try :
        im_bin = morphology.remove_small_holes(im_bin)
    except :
        print("skimage morphology not found")
    return im_bin, vsize


def apply_morphological_changes(condition, type, structural_connectivity=3):
    """ In order to create the  contour from the background image, its needed to erode and dilate the image a certain
    number of times. Depending on a strategy given in parameter, applies the strategy to the image, using a specific
    connectivity.The different strategies change the thickness of the created contour.

    :param condition: The input image where contour is determined
    :type condition: numpy.ndarray
    :param type: The strategy to create contour
    :type type: str
    :param structural_connectivity: The connectivity structuring element  (Default value = 3)
    :type structural_connectivity: int

    :return: The modified image
    :rtype: numpy.ndarray

    """
    # binary structure 6 connectivity  : nd.generate_binary_structure(3, 1)
    struct1 = nd.generate_binary_structure(3, structural_connectivity)
    if type == "twice-d":
        return np.logical_xor(nd.binary_dilation(condition, struct1, iterations=2),
                              nd.binary_dilation(condition, struct1, iterations=1))
    elif type == "noerod":
        return np.logical_xor(nd.binary_dilation(condition, struct1, iterations=1), condition)
    else:
        return np.logical_xor(condition,
                              nd.binary_dilation(condition, struct1, iterations=2))


def generate_contour(imagein, arraydata, voxelsize, folderout, type, sigma=1, connectivity=3,target_normalization_max=255):
    """ Generate the contour for a given image in parameter , using a strategy and a structuring element. This function
    saves the image to a new folder , replacing "background" by "contour" in its name. A normalization should be provided
    for output intensities.

    :param imagein: Path to the input image
    :type imagein: str
    :param arraydata: Numpy array of the image
    :type arraydata: numpy.ndarray
    :param voxelsize: The voxel size of the input image, will be the same for output
    :type voxelsize: float
    :param folderout: Folder where the images will be saved
    :type folderout: str
    :param type: Type of contour generation geometric transform (for contour thickness). Current best is "normal"
    :type type: str
    :param sigma: Value of the gaussian for smoothing of output contour (to simulate membrane intensities (Default value = 1)
    :type sigma: int
    :param connectivity: Size of the structuring element for contour geometric changes (Default value = 3)
    :type connectivity: int
    :param target_normalization_max: Value max for intensities in output contour images (Default value = 255)
    :type target_normalization_max: int

    """
    result = np.zeros(arraydata.shape, dtype=np.float64)
    im_cyto_erod = apply_morphological_changes(arraydata, type, structural_connectivity=connectivity)
    result[im_cyto_erod == True] = 1
    #imsave(os.path.join(folderout, imagein.replace("_background", "_result")), result, voxel_size=voxelsize)
    smoothed = nd.gaussian_filter(result, sigma=sigma)
    smoothed *= target_normalization_max
    del im_cyto_erod
    imsave(os.path.join(folderout, imagein.replace("_background", "_contour")), smoothed.astype(np.uint16), voxel_size=voxelsize)
    del result


def compute_contour(embryo_folder,backgroundinput,reducvoxelsize=0.3,target_normalization_max=255,correction_vsize=False):
    """ Generate the contour images from all the background images found in an embryo folder. Details on methods and
    parameters are given in the documentation of each specific function

    :param embryo_folder: Path to the embryo folder
    :type embryo_folder: str
    :param backgroundinput: Name of the background folder to compute the contour from
    :type backgroundinput: str
    :param reducvoxelsize: If voxel size should be changed (either because it's incorrect or we want to reduce resolution), value of the new voxel size (Default value = 0.3)
    :type reducvoxelsize: float
    :param target_normalization_max: Maximum value for the intensities of the output contour images (Default value = 255)
    :type target_normalization_max: int
    :param correction_vsize: If true , apply the voxel size specified in parameter to the input images (Default value = False)
    :type correction_vsize: bool

    :returns: The path to the contour folder generated
    :rtype: str

    """
    background_folders = os.path.join(embryo_folder, "BACKGROUND/")
    folder_raw = os.path.join(background_folders, backgroundinput)
    contour_suffix ="RELEASE_"+str(reducvoxelsize).split('.')[1]
    if not os.path.exists(folder_raw):
        print("Input images path does not exist")
        exit()
    if not os.path.exists(folder_raw):
        print("Input templates path does not exist")

    res = []
    for path in os.listdir(folder_raw): # List all background images to process
        # check if current path is a file
        if os.path.isfile(os.path.join(folder_raw, path)) and ".mha" in path or ".nii" in path:
            res.append(path)


    res.sort()
    # Correction of networks voxel size errors
    if correction_vsize: #If we need to correct voxel size , do it with ASTEC package setVoxelSize command
        print("Correction of the image voxel size")
        for image in res:
            print("     - " + str(image))
            os.system("conda run -n astec setVoxelSize " + str(os.path.join(folder_raw, image)) + " "+str(reducvoxelsize)+" "+str(reducvoxelsize)+" "+str(reducvoxelsize))

    folder_contour = os.path.join(embryo_folder, "CONTOUR/CONTOUR_"+str(contour_suffix)+"/")


    if not os.path.exists(folder_contour):
        os.makedirs(folder_contour)

    print("Filling and creating contour for normal size")
    for image in res: # Process the contour creation for each image
        print("     -" + str(image))
        image_filled, voxelsize = fill_image(image, folder_raw) # Binarize and fill the holes of the background images
        generate_contour(image, image_filled, voxelsize, folder_contour, "normal", sigma=2, connectivity=1,target_normalization_max=target_normalization_max) #Generating the contour
    return folder_contour



