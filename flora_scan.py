import streamlit as st
import requests
import openai
import csv
import os
from PIL import Image
import base64
import time
import openai

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local(#Add background image loaction here
                  ) 

# Function to write data to a CSV file
def write_to_csv(file_path, data):
    if not os.path.exists(file_path):
        # If CSV file doesn't exist, create and assign default values
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Plant Name", "Similar Plant 1", "Similar Plant 2", "Similar Plant 3"])

    existing_data = []
    updated = False
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            existing_data.append(row)
            if row and row[0] == data[0]:
                # Update existing row if plant name exists
                row[1:4] = data[1:4]
                updated = True

    if not updated:
        # If plant name doesn't exist, add a new row
        existing_data.append(data)

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(existing_data)

# Function to identify the plant using Plant.id API
def identify_plant(image_path):
    api_url = #Enter the Pl@nt Net API URL Here
    headers = {"Api-Key": #Enter the Pl@nt Net API Here
        }
    image_file = open(image_path, "rb")
    files = {"images": image_file}
    response = requests.post(api_url, headers=headers, files=files)
    image_file.close()

    if response.status_code == 200:
        result = response.json()
        best_match = result['bestMatch']
        sci_name = result['results'][0]['species']['scientificName']
        pl_name = result['results'][0]['species']['commonNames'][0]
        sci_name_without_author = result['results'][0]['species']['scientificNameWithoutAuthor']
        names = [best_match, sci_name, pl_name, sci_name_without_author]
        return names
    else:
        print("Error:", response.status_code, response.text)

# Set OpenAI API key
openai.api_key = #Enter Your OpenAI Key here

# Function to retrieve similar plant names from the CSV file
def retrieve_similar_plant_names(csv_path, target_plant_name):
    similar_plant_names = []
    with open(csv_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skip header row
        for row in reader:
            if row and row[0] == target_plant_name:
                similar_plant_names = row[1:4]
                break
    return similar_plant_names

# Function to get images for a plant based on its name
def get_images_for_plant(csv_path, images_dir, plant_name):
    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        id_to_plant = {row['ID']: row['Plant_Name'] for row in reader}

    matching_ids = [key for key, value in id_to_plant.items() if plant_name.lower() in value.lower()]

    if not matching_ids:
        print(f"No matching ID found for plant name: {plant_name}")
        return

    selected_id = matching_ids[0]
    plant_dir = os.path.join(images_dir, selected_id)
    image_files = [f for f in os.listdir(plant_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    return [os.path.join(plant_dir, image_file) for image_file in image_files[:6]]

# Streamlit app
def main():
    st.title("Flora Scan : Plant Identification and Image Display")

    uploaded_file = st.file_uploader("Choose an image...", type="jpg")

    if uploaded_file is not None:
        # Save the uploaded file
        image_path = f"uploads/{uploaded_file.name}"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Identify the plant
        plant_name = identify_plant(image_path)
        
        with st.container():
            # Display the identified plant name
            st.subheader("Plant Details:")
            st.write("Best Match:", plant_name[0])
            st.write("Scientific Name: ", plant_name[1])
            st.write("Common Name: ", plant_name[2])
            st.write("Scientific Name Without Author: ", plant_name[3])

        # Button to generate and display related images
        if st.button("Generate Related Images",use_container_width=True):
            # Get and display images for the identified plant
            st.subheader("Plant Images:")
            plant_images = get_images_for_plant('C:/Plant_Iden_Mini_Project/output.csv', 'C:/Mini Project/plantnet_300K/images/train', plant_name[3])

            if plant_images is None:
                st.write("No images found for the specified plant.")
            else:
                # Display images in rows of three
                for i in range(0, len(plant_images), 3):
                    row_images = plant_images[i:i+3]
                    col1, col2, col3 = st.columns(3)
                    for idx, image_path in enumerate(row_images):
                        with locals()[f"col{idx + 1}"]:
                            img = Image.open(image_path)
                            st.image(img, caption=os.path.basename(image_path), width=110, clamp=True)

        
        # Ask a question related to the plant
        question = f"Can we grow {plant_name[2]} at home?"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": question},
            ]
        )
        
        progress_text = "Generating Plant Details. Please Wait"
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
        
        # Display the response from OpenAI
        st.subheader("Home Sustainability:")
        st.write(response['choices'][0]['message']['content'])
        
        csv_file_path = 'similar_plants.csv'
        if not os.path.exists(csv_file_path):
            # If CSV file doesn't exist, create and assign default values
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(["Plant Name", "Similar Plant 1", "Similar Plant 2", "Similar Plant 3"])

        
        # Use the CSV file to get similar plant names
        matching_row = None
        for row in csv.reader(open(csv_file_path, 'r')):
            if row[0] == plant_name[2]:
                matching_row = row
                break
        
        if matching_row:
            # Display similar plant names from CSV
            similar_pl_names = retrieve_similar_plant_names(csv_file_path, plant_name[2])
            st.subheader(f"Similar Plant Names from CSV for {plant_name[2]}:")
            for name in similar_pl_names:
                st.write(name)
        else:
            # Use OpenAI API to get similar plant names
            question = f"Give me the 3 scientifc plant names similar to {plant_name[3]}, and only provide the names without 'certainly' seperated with a comma"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": question},
                ]
            )

            str_pl_names = response['choices'][0]['message']['content']
            similar_pl_names = str_pl_names.split(sep=',')

            # Display and save the similar plant names
            st.subheader(f"Similar Plants as {plant_name[2]} :")
            for i in range(min(3, len(similar_pl_names))):
                st.write(similar_pl_names[i])
                # Write to CSV file
                csv_data = [plant_name[2]] + similar_pl_names[:3]
                csv_file_path = 'similar_plants.csv'
                write_to_csv(csv_file_path, csv_data)
        
        for i in range(min(3, len(similar_pl_names))):
            plant_images = get_images_for_plant('Enter the created json to csv file path here', 'Enter the path to training images from dataset', similar_pl_names[i])

            if plant_images is None:
                continue
            else:
                # Display one image for the current plant name
                for idx, image_path in enumerate(plant_images[:1]):
                    img = Image.open(image_path)
                    st.image(img, caption=os.path.basename(image_path), width=110, clamp=True)
                    st.text(similar_pl_names[i])
        
                
if __name__ == "__main__":
    main()