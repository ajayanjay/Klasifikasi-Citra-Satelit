# **Capture and Classification of Roofs for Building Characterization from High-Resolution Images** 

**Luisa Fernanda RODRÍGUEZ OCAÑO, Alexander PAEZ LANCHEROS, Johan Andrés AVENDAÑO ARIAS, Colombia** 

**Key words** : Orthoimage, Classify Roofs, Segmentation, Machine Learning Detect Constructions, Satellite Images, SAM. 

## **SUMMARY:** 

In this study, the methodology of a project developed by the Agustín Codazzi Geographic Institute (IGAC) within the framework of multipurpose cadastre is presented as input for the assessment of buildings. The main objective is to explore, through remote sensing techniques, the identification and classification of roofing materials in urban buildings in Colombia, based on very high-resolution orthoimages. Additionally, a label bank is presented, containing different types of building roofs that are of interest for this methodology. The methodology begins with the segmentation of orthoimages of urban areas in the municipalities of San Andrés, Carmen de Bolívar, and Quimbaya (Colombia). The _SAM_ model ( _Segmentation Anything Model_ ) was employed to identify different structures in the image, including roofs. Subsequently, non-relevant objects were removed based on size, and through unsupervised segmentation algorithms, objects that did not correspond to the roofs of interest were eliminated. Each of the roof polygons resulting from the segmentation was labeled by experts, according to construction materials in the classes: zinc (new, oxidized), asbestos, clay, shingle (red, blue, and green), and others. The sets of labels corresponding to each urban area were used to train Machine Learning models, specifically _Random Forest_ . The results obtained on the effectiveness of the models for the classification of roof materials allowed achieving accuracy higher than 70%. The recall was higher than 75% except for the oxidized zinc category, which showed greater variability with values around 50%. These results are promising, opening opportunities for decision-making using machine learning techniques in urban settings, specifically in obtaining physical characteristics of buildings for property valuation purposes. 

## **RESUMEN:** 

En este estudio se presenta la metodología de un proyecto desarrollado por el Instituto Geográfico Agustín Codazzi (IGAC) en el marco del catastro multipropósito como insumo para la evaluación de edificaciones. El objetivo principal es explorar, mediante técnicas de teledetección, la identificación y clasificación de materiales de cubierta en edificaciones urbanas en Colombia, a partir de orto-imágenes de muy alta resolución. Adicionalmente, se presenta un 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 

Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

banco de etiquetas que contiene diferentes tipos de cubiertas de edificios que son de interés para esta metodología. La metodología parte de la segmentación de ortoimágenes de áreas urbanas de los municipios de San Andrés, Carmen de Bolívar y Quimbaya (Colombia). 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

Se empleó el modelo _Segmentation Anything Model (SAM)_ para identificar las diferentes estructuras en la imagen, incluyendo los techos. Posteriormente, se eliminaron los objetos no relevantes en función del tamaño y, mediante algoritmos de segmentación no supervisada, se eliminaron los objetos que no correspondían a los tejados de interés. Cada uno de los polígonos de tejado resultantes de la segmentación fue etiquetado por expertos, según los materiales de construcción en las clases: zinc (nuevo, oxidado), amianto, arcilla, teja (roja, azul y verde) y otros. Los conjuntos de etiquetas correspondientes a cada zona urbana se utilizaron para entrenar modelos de aprendizaje automático, concretamente _Random Forest_ . Los resultados obtenidos sobre la eficacia de los modelos para la clasificación de los materiales de los tejados permitieron alcanzar una precisión superior al 70%. El _recall_ fue superior al 75% excepto para la categoría de zinc oxidado, que mostró una mayor variabilidad con valores en torno al 50%. Estos resultados son prometedores, abriendo oportunidades para la toma de decisiones utilizando técnicas de aprendizaje automático en entornos urbanos, concretamente en la obtención de características físicas de los edificios con fines de valoración inmobiliaria. 

## **Capture and Classification of Roofs for Building Characterization from High-Resolution Images** 

## **Luisa Fernanda RODRÍGUEZ OCAÑO, Alexander PAEZ LANCHEROS, Johan Andrés AVENDAÑO ARIAS, Colombia** 

## **1. INTRODUCTION:** 

Updated cadastral information is crucial for strengthening governance in territory administration. Various methods, including direct, indirect, declarative, and collaborative approaches, can be employed to gather data on the physical, legal, and economic components of properties within a territory. In direct methods, information is collected through on-site visits and identification of each property, involving slow and costly processes. On the other hand, indirect methods allow for obtaining information about property attributes through secondary sources, particularly remote sensing images that offer increasingly higher spatial and temporal resolution (IGAC, 2023). The value of properties is a key component of cadastral information for enhancing municipal finances, as it forms the basis for property taxes. The property value is determined through various methods, some of which separately assess the value of the land and buildings (IGAC, 2017).The type of materials and the condition of roofs are attributes that contribute to determining the value of buildings. 

The use of remote sensing techniques for the detection and classification of building roofs through artificial intelligence is an alternative that enables the implementation of methods for massive capture of such attributes. Advances in this field focus on the development of algorithms to identify types of materials and roof shapes present in properties. (Cai, y otros, 2021) conducted a comparative study of three deep learning methods for roof detection in high spatial resolution orthoimages (12 cm): Convolutional Neural Network (CNN), Deep Convolutional Neural Network (DCNN), and pre-trained DCNN. The models were trained based on manual labeling and validation of roof accuracy for building with 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

different shapes and sizes, covering an area of 205.83 km2 in the rural and urban areas of Kitchener-Waterloo. The best metrics were obtained using the pre-trained DeepLabv3 DCNN with an accuracy of 0.92 and Intersection over Union (IoU) of 63.8%. 

In another study, (Krapf, Bogenrieder, Netzler, Balke, & Lienkamp, 2022) developed a model using U-Net (Ronneberger, Fischer, & Brox, 2015) a type of neural network commonly used for image segmentation. They utilized aerial images with a resolution of 10cm from the rural area of Wartenberg, Germany, manually labeling objects such as photovoltaic modules, attic, window, staircase, chimney, tree, among others, with the assistance of the Google Maps API and a computer vision tool (Nikita, 2021). Subsequently, an independent team validated the data to reduce bias. The average Intersection over Union (IoU) performance obtained for image segmentation was 0.58. An important challenge faced by the authors was the lack of properly labeled data for this specific task. 

Buyukdemircioglu and Kocman (2021) developed an automatic classifier for urban roofs using cutouts extracted from a mosaic of orthophotos with a resolution of 10 cm/pixel employing FME software (Safe Software, s.f.).They labeled 10,000 images into categories: flat, hipped, gabled, shed, pyramidal, and complex roofs, excluding roofs with vegetative coverings that could partially or completely affect visibility or cast shadows (Buyukdemircioglu, Can, & Kocaman, 2021). _Transfer learning_ was employed with pre-trained DCNNs VGG-16, EfficientNetB4, and Resnet. 

Due to the high data requirement of this technique, they used data augmentation techniques with the _Data Augmentation_ library (Shorten & Khoshgoftaar, 2019). The best accuracy achieved was 0.86 with VGG16. Conversely, (Saad, y otros, 2021)employed contrastive and supervised learning methods to create a model for building roof classification. They used 20,189 aerial images containing nine different roof types: hipped, gabled, flat, monoslope, pyramidal, dome, arched, and mansard. Tests were conducted by varying the amount of labeled data from 5% to 75%, and the best results were obtained with accuracies of 0.84 and 0.85 for the contrastive and supervised models, respectively. 

On one hand, there are studies focused on the classification of roof materials. In a study by (Chisense, 2012), hyperspectral data (125 bands ranging from 0.4 μm to 2.5 μm) from an area of approximately 2.0 x 1.1 km2 in the city of Ludwigsburg were used to identify surface materials of the roofs, resulting in 10 classes. Three materials were identified by name through on-site visits (bitumen, red roof, and zinc sheet), while arbitrary names were assigned to the remaining categories. The processing involved the _Discriminant Analysis Feature Extraction_ (DAFE) technique. Subsequently, the data were classified using the _Extended Classifier for Higher Order Stat_ istics (ECHO). The maximum value obtained was 0.914 for the _Average Likelihood Probability_ (ALP) metric. 

On the other hand, (Widipaminto, y otros, 2021) proposed the classification of roof materials, such as aluminum, amianto, ceramic tiles, concrete, and sand-coated metal tiles, based high spatial resolution multispectral satellite images (Pleiades). The spectral response of the near-infrared (NIR) bands showed a sufficiently wide standard deviation, which appears to be distinctive for each material. However, they found similar spectral responses between the sand-coated metal tile and vegetation, posing challenges in their classification. The classification was performed using _Support Vector Machines_ , achieving an average accuracy of 0.92. 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

Finally, (Abriha, y otros, 2018) developed models for roof classification into three and six classes (red tile, brown tile, and amianto), dividing the data into sections of sunny and shaded roofs. For modeling, they used multispectral images with 2m spatial resolution and a panchromatic band with a resolution of 0.5m from the _WorldView-2_ (WV2) satellite. These images consist of eight spectral bands (coastal blue, blue, green, yellow, red, red edge, and two near-infrared bands). They concluded that _Random Forest_ was the most effective model, achieving accuracies exceeding 0.85 for both three and six classes. They observed that the coastal blue and blue bands (B1, B2) were not suitable for identifying roof types due to the similarity in pixel value ranges. The green band (B3) allowed for some differentiation, but similarity persisted between amianto and red tiles. However, the yellow band (B4, 585 nm) enabled clear distinction among the three roof material types. Similarity persisted in shaded segments of asbestos and sunny segments of brown tiles, except in the B8 band. 

Given the need to increase efficiency in capturing information for the characterization of constructions to implement in mass property valuation processes, this study proposes an automatic classification of roof materials based on high-resolution orthoimages with spectral resolution in the visible range. To achieve this, orthoimages from the urban areas of the municipalities of Carmen de Bolívar, Quimbaya, and San Andrés in Colombia were used. The project unfolded in four phases: the selection of study areas, image segmentation, cleaning unwanted polygons (those not corresponding to roofs), and the modeling of roof classification. Finally, considering the type and limited quantity of labeled data available, _Random Forest_ was used. The automation of roof classification can contribute to a faster on-site data capture, reducing costs and time associated with property recognition, while simultaneously implementing machine learning techniques in cadastral and territorial management. 

## **2. MATERIALS:** 

## **2.1 Data:** 

High-resolution orthoimages from urban areas of three municipalities in Colombia were selected, representing diverse conditions in construction characteristics. The features of these orthoimages, obtained from the database on the _Colombia en Mapas_ platform (IGAC, 2023), are described in Table 1. 

|**MUNICIPALITY**|**YEAR**|**AREA (Ha)**|**SPATIAL**<br>**RESOLUTION**|**SENSOR**|
|---|---|---|---|---|
|**SAN ANDRES**|2020|2845,4253|10cm|sensor ADS 120|
|**QUIMBAYA**|2018|321,81|15cm|sensor WILD RC-30|
|**CARMEN DE BOLIVAR**|2021|600.72|10cm|sensor S.O.D.A.|



**Table 1. Orthoimages for the Study.** 

The data was standardized to three bands (RGB), with the resolution also adjusted to 20 cm. This decision was made considering that the SAM algorithm requires three bands for its operation. Additionally, it was considered that the IGAC establishes the standard for 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

cartographic inputs in RGB format. The objective of this choice is to achieve experiment replicability, allowing the use of available inputs in the institute. 

## **2.2 Development Environment:** 

For the development of this research, Python programming language version 3.8, ARCGIS 10.8.1, and a computer with 16 GB RAM, an AMD Ryzen 5 3600G processor at 3.60 GHz, and a 64-bit operating system were utilized. 

## **3. METHODOLOGY:** 

The methodology was developed in 4 main phases. The first involved selecting the study area and standardizing the orthoimages with resampling to a resolution of 20 cm. In the second phase, segmentation was carried out using the SAM. For the next phase, unwanted polygons were removed, resulting in a final segmentation of the roofs. In the final phase, pixel-level modeling based on _Random Forest_ was implemented to classify roofs based on construction material. A label bank with different types of building roof covers and a model for each region were generated. Specific models for each municipality were then trained using processed images and generated polygons, with the dataset divided into 70% for training and 30% for testing. The parameters used were a maximum of 50 trees, a maximum depth of 30, and a maximum of 3000 examples per class. 

**==> picture [443 x 239] intentionally omitted <==**

**Figure 1. Methodology.** 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

## **3.1 Roof Detection Segment Anything Model (SAM) and Filtering:** 

For the segmentation of images from the three municipalities under study, the SAM was utilized. SAM is a model developed by Meta AI designed to address object segmentation tasks in images and videos (Kirillov, Mintun, Ravi, Mao, & Rollan, 2023). It is known for its adaptability and application to various segmentation problems in fields as diverse as computer vision, medical image segmentation, and remote sensing. In a recent analysis (Wu & Prado, 2023), the capabilities of SAM for processing remote sensing images using aerial and satellite data were demonstrated, leading to the development of a new package called SAMgeo. The results concluded that SAM performs exceptionally well in remote sensing segmentation tasks. The implementation proceeded, and in Illustration 2, an image of the segmentation of San Andrés is observed. 

**==> picture [452 x 211] intentionally omitted <==**

**Figure 2. SAM Segmentation in San Andrés.** 

Given that SAM segments various objects in the images such as cars, boats, trees, green areas, among others, a filtering process was applied to specifically identify polygons representing building roofs. The first filter eliminates polygons with an area smaller than 20 �㕚[2] to discard objects related to trees, cars, or other unwanted structures. It also removes polygons larger than 9000 �㕚[2] to exclude large objects like green areas and some bodies of water. 

To exclude polygons associated with vegetation, an unsupervised clustering algorithm was implemented on the polygons using the _ISO Cluster Unsupervised Classification_ tool in ArcGIS. This tool automatically identifies pixel clusters in an image and generates a classified image based on these clusters. Through this analysis, it is determined whether vegetation is grouped in a single cluster or shares clusters with another structure. Subsequently, the clusters are generalized by applying the _Majority Filter_ tool in ArcGIS to eliminate noise and smaller classifications in the resulting image. For the municipalities of Quimbaya and Carmen de Bolívar, the algorithm detected only vegetation in one cluster, facilitating the vegetation cleaning task in the image. As shown in Illustration 3. 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

**==> picture [457 x 203] intentionally omitted <==**

**Figure 1. Sample results of the cluster for Quimbaya (above) and Carmen de Bolivar (below).** 

In San Andrés (Illustration 4), the classification showed confusion between the roofs and vegetation. Consequently, random forest was applied to the polygons of interest with various categories. In this context, green pixels were designated to represent vegetation, while other colors represented different types of roofs. The application of this classification in the image provided satisfactory visual results. Subsequently, the vegetation was cleaned based on this classification. 

**==> picture [462 x 184] intentionally omitted <==**

**Figure 2. Sample of San Andrés classification.** 

To validate the results obtained in the roof detection phase, a representative sample of 35 blocks in Carmen de Bolívar was taken, covering a total area of 186,578 20 �㕚[2] . The roofs of the sample were digitized, generating 948 polygons. The roof detection for this sample generated 1060 polygons in the sampled blocks, representing 16% more than those obtained by digitization. This discrepancy can be mainly attributed to two causes: i) the limited capability 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

in some cases of SAM to identify two or more water roofs as a single unit, and ii) the presence of roofs with two types of materials or in different states of conservation, such as oxidized zinc and zinc. See Illustration 5. 

**==> picture [457 x 263] intentionally omitted <==**

**Figure 3. Examples of divided roof into multiple polygons: A). Hipped roofs and, B). Multiple materials.** 

On the other hand, there was an omission of 124 polygons compared to digitization, corresponding to 13%. This discrepancy was observed mainly in situations such as polygons associated with atypical constructions like kiosks and roofs with a high density of surrounding trees. Additionally, another explanation for this omission is the filtering applied to eliminate polygons with areas less than 20 �㕚[2] . 

## **4. ROOF CLASSIFICATION BY MATERIAL:** 

## **4.1 Labels:** 

The roof classification is applied to the polygons from the detection stage, covering eigth categories: amianto, zinc, oxidized zinc, shingle (green, red, and blue), clay, and clay imitation, as shown in Illustration 6. These categories are not uniformly applied across all municipalities, considering that there is a predominance of some of them based on the climate and geographical location of the country. 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

**==> picture [457 x 217] intentionally omitted <==**

**Figure 4. Roof Materials.** 

The labeling of the roofs was done manually on the digital orthoimages, under the supervision of expert evaluators from IGAC. In this process, a representative sample of polygons was labeled. For the municipality of Carmen de Bolívar, the labeling was done with a field visit, allowing the verification of the assigned labels in the office. The following is the list of labeled polygons by municipality. (Table 2) 

|**Municipality**|**Labels**|
|---|---|
|**Quimbaya**|976|
|**San Andrés**|1015|
|**Carmen de Bolívar**|678|



**Table 2. Number of Labeled Polygons.** 

## **4.2 Image Processing:** 

Digital processing is carried out on the orthoimages with the aim of correcting color issues and reducing noise to facilitate the identification of roof types through _machine learning_ algorithms. Two approaches are used for this purpose. In the first approach (processing 1), the following sequential steps were applied: white balance adjustment, anisotropic diffusion filter, and Gaussian filter. In the second approach (processing 2), only a Gaussian filter was applied. Finally, for San Andrés, due to overexposure in the original image, only processing 2 was applied. Illustration 7 presents an example of the processing results for the municipality of Quimbaya. 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

**==> picture [456 x 164] intentionally omitted <==**

**Figure 7. Processed images of Quimbaya.** 

## **5. RESULTS:** 

Next, the results are presented for each municipality and data group (original, processing 1, and processing 2) 

## **5.1 Quimbaya:** 

In the municipality of Quimbaya, the following labels were used: zinc, amianto, clay, imitation clay, and oxidized zinc. The obtained metrics on the test sets are presented below. 

|**Roof**|**Original**<br>**Processing 1**<br>**Processing 2**|
|---|---|
||**acuraccy**<br>**acuraccy**<br>**acuraccy**|
||0.77<br>0.78<br>0.80|
||**Precision**<br>**Recall f1-score**<br>**Precision**<br>**Recall**<br>**f1-score**<br>**Precision**<br>**Recall**<br>**f1-score**|
|**CLAY**<br>**ZINC**<br>**ZINC**<br>**AMIANTO**<br>**CLAY**<br>**IMITATION**<br>**OXIDIZED**|0.76<br>0.70<br>0.73<br>0.81<br>0.67<br>0.73<br>0.80<br>0.70<br>0.75<br>0.88<br>0.87<br>0.87<br>0.89<br>0.89<br>0.89<br>0.89<br>0.87<br>0.88<br>0.77<br>0.76<br>0.77<br>0.77<br>0.80<br>0.78<br>0.91<br>0.78<br>0.84<br> <br>0.26<br>0.75<br>0.39<br>0.40<br>0.77<br>0.53<br>0.36<br>0.73<br>0.48<br>0.35<br>0.36<br>0.35<br>0.26<br>0.29<br>0.27<br>0.40<br>0.65<br>0.49|



**Table 3. Metrics on Quimbaya Test Sets.** 

||**Original**|**Processing 1**|**Processing 2**|
|---|---|---|---|
|**Roof**|1<br>2<br>3<br>4<br>5|1<br>2<br>3<br>4<br>5|1<br>2<br>3<br>4<br>5|
|**ZINC (1)**<br>**AMIANTO (2)**<br>**CLAY (3)**<br>**IMITATION CLAY**<br>**(4)**<br>**OXIDIZED ZINC (5)**|649<br>170<br>5<br>5<br>90<br>127<br>1884<br>48<br>6<br>109<br>3<br>30<br>617<br>88<br>51<br>0<br>51<br>12<br>50<br>2<br>74<br>36<br>105<br>19<br>133|637<br>165<br>8<br>0<br>145<br>104 1984<br>33<br>0<br>98<br>8<br>26<br>657<br>65<br>63<br>3<br>0<br>1<br>48<br>10<br>35<br>66<br>156<br>7<br>109|652<br>181<br>4<br>3<br>97<br>110<br>1904<br>15<br>3<br>152<br>0<br>16<br>629<br>62<br>104<br>0<br>0<br>6<br>43<br>10<br>51<br>29<br>40<br>8<br>238|



**Table 4. Confusion matrix on the Quimbaya test sets.** 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 

Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

**==> picture [445 x 199] intentionally omitted <==**

**Figure 8. Classification Processing 2.** 

The trained model shows improvements with image processing 1 and 2. The most notable performance was achieved with processing 2, obtaining an accuracy of 0.80 in the test set. The recall for most categories is above 0.70 (Table 3). The best precision was achieved in amianto, clay, and zinc roofs, while imitation clay and oxidized zinc had the lowest metrics. From Table 4, it can be observed that the imitation clay class faces difficulties with several instances misassigned to other classes, such as clay and rusted zinc. This suggests, on one hand, that imitation clay may have spectral (color) and pattern characteristics that resemble other roofs materials, mainly clay. On the other hand, although a high number of oxidized zinc is correctly classified, there are some confusions, especially with clay and amianto. This could be attributable to shared spectral patterns among these materials. 

## **5.2 San Andrés:** 

For the municipality of San Andrés, the assigned labels were green shingle, red shingle, blue shingle, amianto, zinc, and oxidized zinc. The obtained metrics on the test sets are presented below. 

|**Roof**|**Original**<br>**Processing 2**|
|---|---|
||**acuraccy**<br>**acuraccy**|
||0.75<br>0.78|
||**Precision**<br>**Recall**<br>**f1-score**<br>**Precision**<br>**Recall**<br>**f1-score**|
|**GREEN SHINGLE**<br>**ZINC**<br>**AMIANTO**<br>**RED SHINGLE**<br>**OXIDIZED ZINC**<br>**BLUE SHINGLE**|0.29<br>0.88<br>0.93<br>0.31<br>0.87<br>0.46<br>0.95<br>0.88<br>0.88<br>0.97<br>0.91<br>0.94<br>0.91<br>0.92<br>0.91<br>0.92<br>0.52<br>0.66<br>0.17<br>0.97<br>0.96<br>0.09<br>0.86<br>0.16<br>0.35<br>0.68<br>0.46<br>0.36<br>0.57<br>0.44<br>0.86<br>0.94<br>0.96<br>0.92<br>0.95<br>0.94|



**Table 3. Metrics on San Andrés Test Sets.** 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

||**Original**|**Procesamiento 2**|
|---|---|---|
|**Cubierta**|**1**<br>**2**<br>**3**<br>**4**<br>**5**<br>**6**|**1**<br>**2**<br>**3**<br>**4**<br>**5**<br>**6**|
|**GREEN SHINGLE (1)**<br>**ZINC (2)**<br>**AMIANTO (3)**<br>**RED SHINGLE (4)**<br>**OXIDIZED ZINC (5)**<br>**BLUE SHINGLE (6)**|71<br>0<br>4<br>0<br>4<br>5<br>11<br>1757<br>10<br>2<br>79<br>63<br>143<br>30<br>438<br>9<br>452<br>18<br>0<br>0<br>0<br>15<br>5<br>2<br>14<br>39<br>26<br>62<br>254<br>13<br>10<br>18<br>4<br>1<br>11<br>629|73<br>0<br>1<br>1<br>7<br>2<br>14<br>1756<br>5<br>33<br>66<br>48<br>122<br>20<br>563<br>54<br>331<br>0<br>0<br>0<br>1<br>19<br>2<br>0<br>15<br>25<br>41<br>90<br>232<br>2<br>9<br>8<br>1<br>12<br>6<br>637|



**Table 6. Confusion matrix on the San Andrés test sets.** 

**==> picture [450 x 287] intentionally omitted <==**

**Figure 9. Classification Processing 2.** 

Although the models show an overall acceptable accuracy, precision, and recall exhibit high variability. Amianto, shingle, and zinc are the roofing materials that demonstrate higher precision in identification, with precision values exceeding 0.9 in these cases. The other materials (green and red shingle, and oxidized zinc) exhibit confusion levels with precision below 0.3. These three materials are especially confused with amianto, which may be attributed to the significant influence of the radiometric quality of the source image on the model's performance. Therefore, the importance of having inputs with good spectral quality is emphasized, and the need for complementary field validation work is stressed to assess the external quality of the model results. 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

## **5.3 Carmen de Bolívar:** 

The assigned labels for the municipality of Carmen de Bolívar are amianto, zinc, and oxidized zinc, with these being the predominant roofing materials. The obtained metrics on the test sets are presented below. 

|||**Original**|||**Processing**|**1**||**Processing**|**2**||
|---|---|---|---|---|---|---|---|---|---|---|
|||**acuraccy**|||**acuraccy**|||**acuraccy**|||
|**Roof**|||||||||||
|||0.83|||0.85|||0.85|||
||**Precision**|**Recall**|**f1-score**|**Precision**|<br>**Recall**|**f1-score**|**Precision**|<br>**Recall**||**f1-score**|
|**ZINC**|0.9|0.75|0.82|0.91|0.8|0.85|0.91|0.78||0.84|
|**AMIANTO**|0.88|0.92|0.9|0.89|0.88|0.88|0.9|0.92||0.91|
|**ZINC**<br>**OXIDIZED**|0.7|0.87|0.77|0.71|0.89|0.79|0.72|0.89||0.8|



**Table 7. Metrics on San Andrés Test Sets.** 

||**Original**|**Procesamiento 1**|**Procesamiento 1**|
|---|---|---|---|
|**Roof**|**1**<br>**2**<br>**3**|**1**<br>**2**<br>**3**|**1**<br>**2**<br>**3**|
|**ZINC (1)**<br>**AMIANTO (2)**<br>**OXIDIZED ZINC (3)**|988<br>96<br>240<br>51<br>892<br>29<br>59<br>31<br>613|1055<br>83<br>186<br>46<br>853<br>73<br>53<br>21<br>629|1034<br>76<br>214<br>49<br>893<br>30<br>49<br>26<br>628|



**Table 8. Confusion matrix on the San Andrés test sets.** 

**==> picture [459 x 236] intentionally omitted <==**

**Figure 5. Classification Processing 1.** 

The models on the processed images achieved an accuracy of 0.85 on the test set. The best performance was achieved with processing procedure 2, obtaining a superior F1 Score 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

of 0.8 in all categories (Table 7). A good balance between precision and recall is observed in all three categories. Table 8 shows that a high number of rusted oxidized zinc roofs are classified correctly, although there are some confusions, especially with zinc. These two types of roofs can be quite similar, especially if the level of oxidation is not very pronounced. Both could share spectral characteristics that are difficult to distinguish.In a comparison between the three study areas, it was evident that the most common materials are zinc and amianto, and they also showed better results in identification. The oxidation of zinc is a characteristic that poses greater difficulty for its identification, as it tends to be confused with other materials. 

This study has emphasized the use of images with three spectral bands (RGB), which is characteristic of the inputs available for carrying out property recognition tasks for multipurpose cadastre. Other studies have reported higher metrics, such as (Widipaminto, y otros, 2021) with an accuracy of 0.92, which used the near-infrared band, and the study conducted by (Abriha, y otros, 2018)) with an accuracy of 0.85 using nine bands. In contrast, in our case, even with RGB images, we achieved an average accuracy of 0.81 through _Random Forest_ . Another important consideration is the coverage of three urban areas with different construction characteristics, allowing for a broader contrast of results, with the future intention of ensuring the replicability of the experiment with the available inputs. Another innovative element in this study is the capture of roofs using the SAM algorithm, which facilitated the identification of building roofs to eliminate other land covers from the dataset, such as vegetation, roads, water, and soil. 

## **6. CONCLUSIONS AND RECOMMENDATIONS:** 

The roof detection using the Segment Anything Model (SAM) and the filtering process has shown positive results in solving the problem. Although there is a 16% increase in generated polygons compared to manual digitization, this difference is attributed to the model's ability to detect separately roofs with two or more waters in some cases. Roofs with different types of materials on the same structure also influence the identification and separation of roofs. SAM's ability to understand specific details in the roofs, such as materials, is presented as a valuable aspect that enriches our study and contributes to a more detailed detection of roof characteristics. The validation was carried out only in one of the three municipalities, so it cannot be considered conclusive for the entire exercise. The results highlight the importance of image processing in the performance of the _Random Forest_ models trained for each case. 

The choice of different image processing approaches (processing 1 and 2) shows significant improvements in the models' ability to classify roof types. The implementation of the _Random Forest_ algorithm for pixel-level roof classification in three municipalities with different construction characteristics demonstrated the model's adaptability to various geographical and climatic conditions reflected in the images. While the model achieves accuracies above 75% for pixel classification in urban contexts, specific challenges were identified in the detection of particular materials, such as oxidized zinc, which exhibits confusion with clay. Field validation of the labels was crucial for the proper labeling of roofs, which had an impact on the model's performance. In this regard, it is suggested to extend fieldwork to various areas of the country with representative building characteristics for each region to increase the performance and quality of the models. 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

## **REFERENCIAS:** 

- Abriha, D., Kovács, Z., Ninsawat, S., Bertalan, L., Bertalan-Balazs, B., & Szabo, S. (2018). Identification of roofing materials with Discriminant Function Analysis and Random Forest classifiers on pan-sharpened WorldView-2 imagery – a comparison. _Hungarian Geographical Bulletin_ , 375-392. doi:http://dx.doi.org/10.15201/hungeobull.67.4.6 

- Bhardwaj, R., & Haneef, A. (2023). Use of Segment Anything Model (SAM) and MedSAM in the optic disc Segmentation of colour retinal fundus images: Experimental Finding. _Indian Journal of Health Care, Medical & Pharmacy Practice_ . doi:10.59551/ijhmp/2023.4.9 

- Buyukdemircioglu, M., Can, R., & Kocaman, S. (2021). DEEP LEARNING BASED ROOF TYPE CLASSIFICATION USING VERY HIGH RESOLUTION AERIAL IMAGERY. _The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences_ , 55-60. doi:10.5194/isprs-archives-XLIII-B3-2021-552021 

- Cai, Y., He, H., Yang, K., Fatholahi, S. N., Ma, L., Xu, L., & Li, J. (2021). A Comparative Study of Deep Learning Approaches to Rooftop Detection in Aerial Images. _Canadian Journal of Remote Sensing_ , 1-19. doi:10.1080/07038992.2021.1915756 

- Chisense,    C.     (2012).     CLASSIFICATION     OF     ROOF     MATERIALS     USING HYPERSPECTRAL DATA. _ISPRS - International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences_ , 103-107. doi:10.5194/isprsarchivesXXXIX-B7-103-2012 

- Fan, H., Yao, W., & Fu, Q. (2014). Segmentation of Sloped Roofs from Airborne LiDAR Point Clouds Using Ridge-Based Hierarchical Decomposition. _Remote Sens_ , 3284-3301. doi:https://doi.org/10.3390/rs6043284 

- IGAC. (2017). METODOLOGÍA ELABORACIÓN DEL ESTUDIO DE ZONAS HOMOGÉNEAS FÍSICAS Y GEOECONÓMICAS Y DETERMINACIÓN DEL VALOR UNITARIO POR TIPO DE CONSTRUCCIÓN. Instituto Grográfico Agustín Codazzi (IGAC). 

- IGAC. (2023). Instructivo seguimiento,Monitoreo y Control de proyectos de formacion y/o Actualización catastral con enfoque multipropósito. Instituto Geográfico Agustín Codazzi (IGAC). 

- Ji, W., Li, J., Bi, Q., Liu, T., Li , W., & Li, C. (May de 2023). Segment Anything Is Not Always Perfect:. doi: https://doi.org/10.48550/arXiv. 

- Kim, J., Bae, H., Kang, H., & Lee, S. (2021). NN Algorithm for Roof Detection and Material Classification in Satellite Images. _Electronics_ . doi:https://doi.org/10.3390/electronics10131592 

- Kirillov, A., Mintun, E., Ravi, N., Mao, H., & Rollan, C. (5 de Apr de 2023). Segment Anything. Obtenido de https://arxiv.org/abs/2304.02643 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

- Krapf, S., Bogenrieder, L., Netzler, F., Balke, G., & Lienkamp, M. (2022). RID - Roof Information Dataset for Computer Vision-Based Photovoltaic Potential Assessment. _Remote Sens_ , 14. doi: https://doi.org/10.3390/rs14102299 

- Nikita, M. (2021). _Computer Vision Annotation Tool (CVAT)._ Obtenido de Github. 

- Prado, L., Wu, Q., Lopes de Lemos, E., Nunes, W., Marques, A., Li, J., & Marcato, J. (2023). The Segment Anything Model (SAM) for remote sensing applications: From zero to one shot. _International Journal of Applied Earth Observation and Geoinformation_ . doi:https://doi.org/10.1016/j.jag.2023.103540 

- Ronneberger, O., Fischer, P., & Brox, T. (2015). U-Net: Convolutional Networks for Biomedical Image Segmentation. _Medical Image Computing and Computer-Assisted Intervention_ . doi:https://doi.org/10.1007/978-3-319-24574-4_28 

- Saad, A. B., Drouyer, S., Hell, B., Gavoille, S., Gaiffas, S., & Facciolo, G. (2021). A Review on Contrastive Learning Methods and Applications to Roof-Type Classification on Aerial Images. _2021 IEEE International Geoscience and Remote Sensing Symposium IGARSS_ , 4960-4963. doi:10.1109/IGARSS47720.2021.9553778 

_Safe Software_ . (s.f.). Obtenido de https://www.safe.com/ 

Shorten, C., & Khoshgoftaar, T. M. (2019). A survey on Image Data Augmentation for Deep Learning. _Journal of Big Data_ . doi:https://doi.org/10.1186/s40537-019-0197-0 

- Widipaminto, A., Hestrio, Y., Safitri, Y., Monica, D., Irawadi, D., Rokhmatuloh, R., . . . Adiningsih, E. (2021). Roof materials identification based on pleiades spectral responses using supervised classification. _TELKOMNIKA (Telecommunication Computing Electronics and Control)_ . doi:http://dx.doi.org/10.12928/telkomnika.v19i2.18155 

- Wu, Q., & Prado, L. (2023). samgeo: A Python package for segmenting geospatial. _Journal of Open Source Software_ . doi:https://doi.org/10.21105/joss.05663 

## **BIOGRAPHICAL REFERENCES:** 

## **Alexander Páez Lancheros** 

Specialized Professional of the Directorate of Research and Prospective of the IGAC. Cadastral and Geodesy Engineer from the Universidad Distrital Francisco José de Caldas (UDFJC), specialist in University Teaching from the Universidad Santo Tomás, Master in Management and Evaluation of Geographic Information Universidad de Jaén and in Information Management and Geospatial Technologies of the Universidad Sergio Arboleda. 

## **Luisa Fernanda Rodríguez Ocaño** 

Professional in Mathematics of the UDFJC and Master in Data Analytics of the Universidad Central. With experience as a researcher at the IGAC and at the Secretaría Distrital de Movilidad. 

## **Nelson Andrés Nieto Valencia** 

Professional in Environmental Engineering, with specialization in Geographic Information Systems (GIS) of the UDFJC, and Master in Geography of the Universidad Pedagógica y 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

Tecnológica de Colombia (UPTC). With experience as an official researcher in the IGAC and other public and private entities, such as universities and other public institutions. 

## **CONTACTS:** 

## **Alexander Páez Lancheros** 

Institute of Geography Agustín Codazzi (IGAC) Carrera 30 # 48-51 Bogotá DC, Colombia Tel. (+57) 301 4101504 Email: alexander.paez@igac.gov.co Web site: https://www.igac.gov.co/ 

## **Luisa Rodríguez Ocaño** 

Institute of Geography Agustín Codazzi (IGAC) Carrera 30 # 48-51 Bogotá DC, Colombia Tel. (+57) 601 653 18 88 Email: luisaf.rodriguez@igac.gov.co Web site: https://www.igac.gov.co/ 

## **Nelson Andrés Nieto Valencia** 

Institute of Geography Agustín Codazzi (IGAC) Carrera 30 # 48-51 Bogotá DC, Colombia Tel. (+57) 311 4626315 Email: nelson.nieto@igac.gov.co Web site: https://www.igac.gov.co/ 

Roof Capture and Classification for Building Characterization from High-Resolution Images (12653) Luisa Rodríguez Ocaño, Alexander Paez Lancheros and Johan Andrés Avendaño (Colombia) 

FIG Working Week 2024 

Your World, Our World: Resilient Environment and Sustainable Resource Management for all Accra, Ghana, 19–24 May 2024 

