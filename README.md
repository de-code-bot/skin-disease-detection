# skin-disease-detection
This is the backend of the skin disease detection using image processing on google colab

# Abstract
 Using image processing and machine learning technology, the diagnosis of skin diseases has been
 already proven to have promising prospects of helping doctors make better dermatology examinations.
 The possibilities for extension of this model entail several areas of concern for development and
 improvement. Extending the training data set applying to the model creates the possibility of including a
 multitude of skin types. It also helps to improve the model's capability of perceiving and recognizing a
 broader variety of conditions. Alongside advanced imaging processing techniques, the ability to locate
 more accurate features of the skin lesion images and an improvement of accuracy in skin disease
 diagnosis and classification can be explored. Integration of one or the other machine learning algorithms
 like ensemble learning or transfer learning can intensify the sharing of the model's performance and
 acceptance. Moreover, the model will be able to sync with telemedicine platforms and mobile
 applications, bringing the possibility of remote diagnosis and observation of skin diseases, which in turn
 will result in the broadening of reach and penetration of healthcare services. These advances could be of
 great importance for dermatology due to the possibility of finding reliable and effortless data processing
 tools to differentiate skin diseases based on image processing techniques

 # problem statement
  Skin diseases are common health problems that affect people's lives. Early
 detection and correct diagnosis of skin diseases are very important for
 effective treatment and prevention of complications. However, manual
 analysis by medical professionals is time-consuming and subjective.
 Therefore, an automated system is needed to support the detection and
 classification of skin diseases. This project aims to develop a skin disease
 detection method using image processing technology. The system takes
 digital photos of the affected skin area for input and uses image analysis to
 identify the type of infection. 


 # METHODOLOGY AND IMPLEMENTATION
This section outlines the methods of the suggested approach for the extraction, identification, and categorization of photos showing skin-diseased conditions. The technique will be very helpful in identifying cases of chickenpox, shingles, cellulitis, impetigo, athlete's foot, nail fungus, ringworm, and cutaneous larva migrans.
Preprocessing, feature extraction, and classification makes up the entirety of the architecture. 
3.1 Block diagram
![Block diagram]()
3.2 Algorithm
Image Acquisition: In this step, digital images of the skin are acquired using different imaging modalities, such as cameras, dermatoscopes. The quality of the acquired images can significantly impact the accuracy of subsequent analysis. These images are then stored in folders and thus it creates a Dataset. This Dataset contains 2 types of images: Train images : Consist of images to train the model.
Validation images: Consists of images to validate the model in every epoch.
After uploading the Dataset to Google Drive, it is required to mount the drive to the colab notebook. The following code can be used to mount it to drive:
from google.colab import drive
drive.mount('/content/drive')

Table 1. Dataset Details


number of images
belonging to classes
train set
924
8
test set
233
8
total
1057
8


Pre-processing: Pre-processing involves enhancing the acquired images and reducing noise or artifacts that might affect the analysis. This step includes techniques such as filtering, image enhancement, and color correction.
train = train_datagen.flow_from_directory(‘path of the train directory’,
                                          target_size = (224, 224),
                                          batch_size = 32
                                          )


val = val_datagen.flow_from_directory('path of the validation directory',
                                      target_size = (224, 224),
                                       batch_size = 16
                                      )
in the above snippet 
target_size= Sets the size of the input image
batch_size= Sets the size of the batches of data

def plotImage(img_arr, label):
  for im , l in zip(img_arr, label):
    plt.figure(figsize=(5,5))
    plt.imshow(im/200)
    plt.show()
 
This function helps in applying filters to the image


Segmentation: Skin lesion segmentation is the process of distinguishing the lesions from the surrounding healthy skin areas. Segmentation plays a vital role in accurately analyzing the disease characteristics and measuring its size, shape, or color. The process of dividing an image into segments makes image analysis easier. Segments are made up of sets of one or more pixels.  In the Implementation, we have Segmented the lesions using the CNN architecture. 

Feature Extraction: After segmentation, relevant features are extracted from the segmented regions. These features can include texture, color, shape, or statistical descriptors that represent the distinguishing characteristics of different skin diseases.


The above image shows how the features are extracted from an image when it is passed through the first layer. Similarly, more features are extracted when the image is passed on to the successive layer after the image is further segmented.

Classification: In the final step, the extracted features are used to classify the skin lesions into different disease categories. Machine learning algorithms, such as support vector machines, neural networks, or decision trees, can be trained and utilized to perform this classification task. By training these algorithms we can achieve a much higher accuracy of our model's prediction. 
In our implementation, we have created a neural network that is trained 50 times to attain a higher level of accuracy and help in the accurate classification of the 8 classes of disease mentioned above.

 

