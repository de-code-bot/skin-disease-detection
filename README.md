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

# Edits in the code

1. download the dataset and unzip it.
2. Then upload it in the respective folder on google drive .
3. Copy the path of respective folder in the respective paths:

> [!IMPORTANT]
> train = train_datagen.flow_from_directory('path of the train set',

> [!IMPORTANT]
>val = val_datagen.flow_from_directory('path of the test set',
               
> [!IMPORTANT]
>model = load_model('Path  of the model stored in drive')

> [!IMPORTANT]
> img_path= 'Path of the image to detected'




