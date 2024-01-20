Flora Scan: Plant Identification and Image Display

Flora Scan is a Streamlit-based application for plant identification and image display. It leverages the Plant.id API to identify plants based on uploaded images, providing users with detailed information such as scientific name, common name, and related images.

Key Features:-


Plant Identification: Upload an image, and Flora Scan will identify the plant using the Plant.id API, displaying information such as the best match, scientific name, and common name.

Image Display: Explore related images of the identified plant, showcasing its diversity and aiding in visual recognition.

Home Sustainability Insights: Get sustainability-related information about the identified plant, generated by OpenAI's GPT-3.5 Turbo model, offering insights into growing the plant at home.

Similar Plant Recommendations: Discover similar plant names, either from a locally stored CSV file or generated on-the-fly using OpenAI's API. Explore related images of similar plants to enhance the user experience.


Usage

Upload an image of a plant.

View detailed information about the identified plant.

Explore related images of the identified plant.

Receive insights on growing the plant at home.

Discover similar plant names and explore related images.


Requirements:-


Python

Streamlit

Requests

OpenAI GPT-3.5 Turbo

PIL (Pillow)

Base64


Getting Started:-


Download Pl@ntNet dataset from this link :- https://zenodo.org/records/5645731#.Yuehg3ZBxPY

Download the repository python files and also download all the required libraries

Obtain API keys for Pl@ntNet and OpenAI GPT-3.5 Turbo, Use those API keys in the code where there are required and Save it.

Also fill in the directory locations of the dataset and background image(optional) in the code accordingly.

Run the application by using commands "streamlit run flora_scan.py" in the terminal.

Now provide plant images to website and wait for the results.

THANK YOU...
