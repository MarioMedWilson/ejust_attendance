import os
import cv2
import face_recognition
import pandas as pd
import pickle
from imageio import imread

def load_model(file_path):
    """
    Load model from a file.

    Parameters:
    - file_path (str): Path to the file containing the SVM model (default: 'svm_model.pkl').

    Returns:
    - loaded_model: The loaded SVM model.
    """
    with open(file_path, 'rb') as file:
        loaded_model = pickle.load(file)
    return loaded_model


def recognize_faces(image_path, model):
    """
    Detect faces in an image, draw rectangles around them, and save results to CSV.

    Parameters:
    - image_path (str): Path to the input image file.
    - model: Face recognition classifier (replace with your actual classifier).

    Returns:
    None

    This function reads an image, detects faces using face_recognition library,
    draws rectangles around the detected faces, and saves the results to a CSV file
    along with an image file with rectangles drawn around faces.

    The output files are saved in a directory named 'results' within the current
    working directory.
    """
    
    # Read the image from the specified path
    img = imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Process the image 
    faces_loc = face_recognition.face_locations(img, model="hog")
    encodings = face_recognition.face_encodings(img, faces_loc)

    face_names = []
    for encoding in encodings:
        # Assuming clf is your face recognition classifier
        name = model.predict([encoding])

        face_names.extend(name)

    data = {'data': face_names}

    for (top, right, bottom, left), name in zip(faces_loc, face_names):
        # Drawing a rectangle around the detected faces in the image
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(
            img, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED
        )
        
        font = cv2.FONT_HERSHEY_DUPLEX
        # Displaying the person(s) name(s) under the person(s) face(s)
        cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    
    parsed_data = []

    for face_name in data['data']:
        # Splitting the name into "name" and "id" components
        name_parts = face_name.split('_')
        
        # Creating a dictionary with "name" and "id"
        parsed_entry = {
            "name": name_parts[0],
            "id": int(name_parts[1])
        }
        
        # Appending the dictionary to the parsed_data list
        parsed_data.append(parsed_entry)

    # Updating the original data dictionary
    data['data'] = parsed_data

    # Create a directory if it doesn't exist
    output_dir = 'results'
    os.makedirs(output_dir, exist_ok=True)

    # Save the image with rectangles drawn around faces
    img_path = os.path.join(output_dir, 'detected_faces_image.jpg')
    cv2.imwrite(img_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    # Save data to CSV
    csv_path = os.path.join(output_dir, 'detected_faces.csv')
    df = pd.DataFrame(data)
    df[['name', 'id']] = pd.DataFrame(df['data'].tolist(), index=df.index)
    df = df.drop(columns=['data'])
    df.to_csv(csv_path, index=False)
    return data 


def main():
    # Load the model
    model_path = './members/model/svm_model.pkl'
    model = load_model(model_path)

    # Replace the path with the path to your image file
    image_path = "./test.jpg"

    # Recognize faces using the loaded SVM model
    recognize_faces(image_path, model)

if __name__ == "__main__":
    main()

