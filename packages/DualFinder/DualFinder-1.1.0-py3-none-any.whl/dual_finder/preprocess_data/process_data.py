import numpy as np
import tensorflow as tf
from tqdm import tqdm
from astropy.io import fits
import glob

def crop_center(img, cropx, cropy):

    y, x, *_ = img.shape
    startx = x // 2 - (cropx // 2)
    #print(startx)
    starty = y // 2 - (cropy // 2)
    #print(starty)
    return img[starty:starty + cropy, startx:startx + cropx, ...]

def augment_dataset(images, num_augmented_images=20):
    augmented_images = []

    for i, image in tqdm(enumerate(images)):
        augmented_images.append(image)

        # Perform data augmentation multiple times to create more augmented images
        for _ in range(num_augmented_images):

            # Random rotation (angle in radians)
            angle = tf.random.uniform(shape=[], minval=-0.5*np.pi, maxval=0.5*np.pi)
            augmented_image = tf.image.rot90(image, k=tf.cast(angle / (0.5*np.pi), tf.int32))

            augmented_images.append(augmented_image)

    augmented_images = np.array(augmented_images)

    return augmented_images

def compileRealImages():
    asecSeparations = ["2.0","1.9", "1.8", "1.7", "1.6", "1.4", "1.3", "1.2", "1.1","1.0", "0.8", "0.7", "0.6", "0.5"]
    composite_images = []
    singleImages = []
    doubleAGNLabels = []
    singleAGNLabels = []
    for j in tqdm(asecSeparations):
        for images in glob.glob("dual_finder/dual_finder/preprocess_data/Double_AGN_CNN/simulated_double_AGN_images_spring/" + j + "_asec_separations/*.fits"):
            with fits.open(images, memmap=False) as hdul:
                #hdu1 = fits.open(images)
                comp_img = hdul[0].data
                comp_img = crop_center(comp_img, 60, 60)
                comp_img = np.expand_dims(comp_img, axis = -1)
    
                composite_images.append(comp_img)
            #print("Closed file", images)
                #hdu1.close()


    print("Compiling: confirmed_single_AGN_spring")
    for singles_spring in tqdm(glob.glob("dual_finder/dual_finder/preprocess_data/confirmed_single_AGN_spring/*.fits")):
        try:
            with fits.open(singles_spring, memmap=False) as hdu2:
                img_spring = hdu2[0].data
                img_spring = crop_center(img_spring, 60, 60)
                img_spring = np.expand_dims(img_spring, axis=-1)
                singleImages.append(img_spring)
        except Exception as e:
            print(f"Error processing {singles_spring}: {e}")

    print("Compiling: confirmed_single_AGN_fall")
    for singles_fall in tqdm(glob.glob("dual_finder/dual_finder/preprocess_data/confirmed_single_AGN_fall/*.fits")):
        try:
            with fits.open(singles_fall, memmap = False) as hdu3:
                #hdu3 = fits.open(singles_fall)
                #img_fall = fits.getdata(singles_fall)
                img_fall = hdu3[1].data
        
                img_fall = crop_center(img_fall, 60, 60)
                img_fall = np.expand_dims(img_fall, axis = -1)
                singleImages.append(img_fall)
        except Exception as e:
            print(f"Error processing {singles_fall}: {e}")
        #hdu3.close()
   
    print(f"Shape of composite images: {np.shape(composite_images)}")
    print(f"Shape of all single real AGN images: {np.shape(singleImages)}")
    return singleImages, composite_images
    
def create_dataset():
    simulatedGaussianSingle = []
    simulatedGaussianDouble = []

    for singleImage in tqdm(glob.glob("dual_finder/dual_finder/preprocess_data/Gaussian_simulated_images/single_point_sources_real_psf/*.fits")):
        # Read the FITS data without loading it into memory
        with fits.open(singleImage, memmap = False) as hdul:
            img = hdul[0].data
            img = crop_center(img, 60, 60)
        simulatedGaussianSingle.append(img)

    for doubleImage in tqdm(glob.glob("dual_finder/dual_finder/preprocess_data/Gaussian_simulated_images/double_point_sources_real_psf/*.fits")):
        with fits.open(doubleImage, memmap = False) as hdul:
            img = hdul[0].data
            img = crop_center(img, 60, 60)
        simulatedGaussianDouble.append(img)
    simulatedGaussianSingle = np.asarray([arr.reshape((60, 60, 1)) for arr in simulatedGaussianSingle])
    simulatedGaussianDouble = np.asarray([arr.reshape((60, 60, 1)) for arr in simulatedGaussianDouble])


    #loading real images
    real_singleImages, composite_images = compileRealImages()
    augmented_single_images = augment_dataset(real_singleImages, num_augmented_images = 15)
    #augmented_double_images = augment_dataset(composite_images)

    augmented_single_images = augmented_single_images[:,:,:,-1]
    #augmented_double_images = augmented_single_images[:,:,:,-1]
    print(f"Shape of augmented single images: {np.shape(augmented_single_images)}")
    #print(f"Shape of augmented double images: {np.shape(augmented_double_images)}")

    # Tensorflow's Sequential model accepts image arrays of the shape (batch_size, x_size, y_size, channels), so we need to add a channels dimension
    # since we are working with monochromatic data here, we only need a value of 1 in the channel's dimension.
    augmented_single_images = np.expand_dims(augmented_single_images, axis = -1)

    all_singleImages = np.concatenate((augmented_single_images, simulatedGaussianSingle), axis = 0)
    all_single_labels = []

    # Create labels to assign all training and validation images. The two possible categories an image can fall into for this
    # demonstration is a 'single AGN' or a 'double AGN'.

    for _ in range(len(all_singleImages)):
        all_single_labels.append("single AGN")
    all_doubleImages = np.concatenate((composite_images, simulatedGaussianDouble), axis = 0)

    all_double_labels = []
    for _ in range(len(all_doubleImages)):
        all_double_labels.append("double AGN")

    modelA_training_data = np.concatenate((all_singleImages, all_doubleImages), axis = 0)
    modelB_training_data_1 = np.concatenate((simulatedGaussianSingle, simulatedGaussianDouble), axis = 0)
    modelB_training_data_2 = np.concatenate((augmented_single_images, composite_images), axis = 0)

    # The percentage of total images used for training. The rest will be used in the validation dataset to test the results.
    train_ratio = 0.75

    modelA_labels = np.concatenate((all_single_labels, all_double_labels), axis = 0)

    # Model B is trained in two separate iterations, so we create separate labels for each step.
    modelB_labels_simulated = []
    for _ in range(len(simulatedGaussianSingle)):
        modelB_labels_simulated.append("single AGN") 
    for _ in range(len(simulatedGaussianDouble)):
        modelB_labels_simulated.append("double AGN")

    modelB_labels_real = []
    print("shape of augmented single images: ", np.shape(augmented_single_images))
    for _ in tqdm(range(len(augmented_single_images))):
        modelB_labels_real.append("single AGN")
    for _ in range(len(composite_images)):
        modelB_labels_real.append("double AGN")
    modelB_labels_simulated = np.asarray(modelB_labels_simulated)
    modelB_labels_real = np.asarray(modelB_labels_real)
    print(f"modelB_labels_real: {modelB_labels_real}")

    # Shuffle Model A
    indicesA = np.random.permutation(len(modelA_training_data))
    shuffled_modelA_dataset = modelA_training_data[indicesA]
    shuffled_modelA_labels = modelA_labels[indicesA]
    
    # Shuffle Model B (Simulated)
    indicesB1 = np.random.permutation(len(modelB_training_data_1))
    shuffled_modelB_1_dataset = modelB_training_data_1[indicesB1]
    shuffled_modelB_labels_simulated = modelB_labels_simulated[indicesB1]
    
    # Shuffle Model B (Real)
    indicesB2 = np.random.permutation(len(modelB_training_data_2))
    shuffled_modelB_2_dataset = modelB_training_data_2[indicesB2]
    shuffled_modelB_labels_real = modelB_labels_real[indicesB2]

    split_index_modelA = int(train_ratio * len(shuffled_modelA_dataset))
    train_dataset_modelA = shuffled_modelA_dataset[:split_index_modelA]
    train_labels_modelA = shuffled_modelA_labels[:split_index_modelA]
    validation_dataset_modelA = shuffled_modelA_dataset[split_index_modelA:]
    validation_labels_modelA = shuffled_modelA_labels[split_index_modelA:]
    
    # Splitting the shuffled Model B (Simulated) data
    split_index_modelB = int(train_ratio * len(shuffled_modelB_1_dataset))
    train_dataset_modelB_1 = shuffled_modelB_1_dataset[:split_index_modelB]
    train_labels_modelB_1 = shuffled_modelB_labels_simulated[:split_index_modelB]
    validation_dataset_modelB_1 = shuffled_modelB_1_dataset[split_index_modelB:]
    validation_labels_modelB_simulated = shuffled_modelB_labels_simulated[split_index_modelB:]
    
    # Splitting the shuffled Model B (Real) data
    split_index_modelB2 = int(train_ratio * len(shuffled_modelB_2_dataset))
    train_dataset_modelB_2 = shuffled_modelB_2_dataset[:split_index_modelB2]
    train_labels_modelB_2 = shuffled_modelB_labels_real[:split_index_modelB2]
    validation_dataset_modelB_2 = shuffled_modelB_2_dataset[split_index_modelB2:]
    validation_labels_modelB_2 = shuffled_modelB_labels_real[split_index_modelB2:]

    

    print(f"Shape of real model B training data: {np.shape(train_dataset_modelB_2)}")
    print(f"Shape of real model B training labels: {np.shape(train_labels_modelB_2)}")
    print(f"Shape of real model B validation data: {np.shape(validation_dataset_modelB_2)}")
    print(f"Shape of real model B validation labels: {np.shape(validation_labels_modelB_2)}")

    print(f"Shape of simulated model B training data: {np.shape(train_dataset_modelB_1)}")
    print(f"Shape of simulated model B training labels: {np.shape(train_labels_modelB_1)}")
    print(f"Shape of simulated model B validation data: {np.shape(validation_dataset_modelB_1)}")
    print(f"Shape of simulated model B validation labels: {np.shape(validation_labels_modelB_simulated)}")

    return (train_dataset_modelB_1, train_labels_modelB_1), (validation_dataset_modelB_1, validation_labels_modelB_simulated), (train_dataset_modelB_2, train_labels_modelB_2), (validation_dataset_modelB_2, validation_labels_modelB_2), (train_dataset_modelA, train_labels_modelA), (validation_dataset_modelA, validation_labels_modelA)
