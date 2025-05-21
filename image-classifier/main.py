import cv2
import numpy as np
import streamlit as st
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)
from PIL import Image

def load_model():
    model = MobileNetV2(weights='imagenet')
    return model

def preprocess_image(image):
    img = np.array(image)
    img =  cv2.resize(img, (224,224))
    img = preprocess_input(img)
    # taking a single image and expanding it to a batch of 1 (list of images)
    img = np.expand_dims(img, axis=0)
    return img

def classify_image(model, image):
    try:
        # Ensure image is in RGB mode (discard alpha if present)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image)
        # take numeric predictions and convert them to a list of labels
        decoded_predictions = decode_predictions(predictions, top=3)[0]
        return decoded_predictions
    except Exception as e:
        st.error(f"Error classifying image: {str(e)}")
        return None


def main():
    st.set_page_config(
        page_title="Image Classifier",
        page_icon="📷",
        layout="centered",
    )
    st.title("AI Image Classifier")
    st.write("Upload an image to classify it")
    
    # cache the model for faster loading - not necessary to rerun
    # the app at eache resource change
    @st.cache_resource
    def load_cached_model():
        return load_model()

    model = load_cached_model()

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = st.image(
            uploaded_file,
            caption="Uploaded Image",
            use_container_width=True,
        )

        btn = st.button("Classify Image")

        if btn:
            with st.spinner("Classifying Image..."):
                image = Image.open(uploaded_file)
                predictions = classify_image(model, image)
                if predictions is not None:
                    st.subheader("Predictions")
                    for _, label, confidence in predictions:
                        st.write(f"**{label}**: {confidence:.2%}")
                else:
                    st.write("No predictions found")


if __name__ == "__main__":
    main()
