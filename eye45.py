import streamlit as st
from PIL import Image
import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
tf.compat.v1.enable_v2_behavior()
tf.reset_default_graph()  # Now using tf.compat.v1
from fpdf import FPDF
import os
import base64
from streamlit_lottie import st_lottie
import json
import requests
import time
from datetime import datetime
import pandas as pd
import os
import base64
from datetime import datetime
from fpdf import FPDF

from PIL import Image

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit





# Set page configuration
st.set_page_config(
    page_title="Eye Disease Detection",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load and display Lottie animations
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Function to add background image
def add_bg_from_url(url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function for custom CSS
def local_css():
    st.markdown("""
    <style>
    /* Main container styling */
    .main .block-container {
        background-color: black; /* Light gray */
    }

        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        margin: 1rem;
        transition: all 0.3s ease;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Arial', sans-serif;
        margin-bottom: 1.5rem;
    }
    
    h1 {
        text-align: center;
        padding-bottom: 1rem;
        border-bottom: 2px solid #3498db;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* File uploader */
    .uploadedFile {
        border: 2px dashed #3498db;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    /* Success message */
    .stSuccess {
        background-color: #d1f0d1 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-in;
    }
    
    /* Error message */
    .stError {
        background-color: #f0d1d1 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-in;
    }
    
    /* Animation keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Text inputs */
    .stTextInput input, .stNumberInput input {
        border-radius: 10px;
        border: 1px solid #bdc3c7;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: blue;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.3);
    }
    
    /* Radio buttons */
    .stRadio > div {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    
    /* Card for image display */
    .image-card {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    /* Container for two columns */
    .two-column {
        display: flex;
        flex-direction: row;
        gap: 2rem;
    }
    
    /* Loading animation */
    .loading-animation {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    /* Report summary card */
    .report-card {
        background-color: blue;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #3498db;
        transition: all 0.3s ease;
    }
    
    /* Enhanced sidebar styling */
    .css-1d391kg, .css-hxt7ib {
        background-image: linear-gradient(to bottom, #2c3e50, #3498db) !important;
    }
    
    .sidebar .sidebar-content {
        background-image: linear-gradient(to bottom, #2c3e50, #3498db);
    }
    
    /* Sidebar title */
    .sidebar h2 {
        color: white !important;
        font-size: 1.5rem !important;
        margin-top: 1rem !important;
        margin-bottom: 1.5rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3) !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Sidebar text */
    .sidebar p, .sidebar li {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Sidebar headings */
    .sidebar h3 {
        color: #fff !important;
        font-size: 1.2rem !important;
        margin-top: 1.5rem !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Sidebar list items */
    .sidebar li {
        margin-bottom: 0.5rem !important;
        transition: all 0.2s ease !important;
    }
    
    .sidebar li:hover {
        transform: translateX(5px) !important;
    }
    
    /* Disease info card */
    .disease-info-card {
        background: linear-gradient(135deg, #fce4ec, #f8bbd0); /* Lighter gradient background */
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-left: 5px solid #e91e63; /* Pink border for emphasis */
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        animation: slideIn 0.5s ease-out;
        color: #212121; /* Darker font color for better contrast */
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Section headers for disease info */
    .section-header {
        background-color: #edf2f7;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: bold;
        color: #2c3e50;
        border-left: 4px solid #3498db;
        transition: all 0.3s ease;
    }
    
    .section-header:hover {
        background-color: #e0e8f0;
        transform: translateX(3px);
    }
    
    /* Properties within sections */
    .property-card {
        background-color: #eef2f7;
    }

        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .property-card:hover {
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 8px 8px 0 0;
        border: 1px solid #e2e8f0;
        border-bottom: none;
        padding: 10px 20px;
        font-weight: 600;
        color: #2c3e50;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        border-top: 3px solid #3498db;
    }
    
    /* Badge for severity */
    .severity-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        margin-left: 10px;
        font-size: 0.8rem;
    }
    
    .severity-low {
        background-color: #d1f5d3;
        color: #2c662d;
    }
    
    .severity-medium {
        background-color: #f9e79f;
        color: #8a5700;
    }
    
    .severity-high {
        background-color: #f5b7b1;
        color: #7f2200;
    }
    
    /* Animation for page transitions */
    @keyframes pageTransition {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .animate-in {
        animation: pageTransition 0.5s ease-out forwards;
    }
    /* Sidebar gradient with animation */
    .css-1d391kg, .css-hxt7ib {
        background: linear-gradient(270deg, #2c3e50, #3498db, #8e44ad, #2ecc71);
        background-size: 800% 800%;
        animation: gradientAnimation 10s ease infinite;
        transition: all 0.3s ease-in-out;
    }

    @keyframes gradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Sidebar hover effect */
    .css-1d391kg:hover, .css-hxt7ib:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model(model_path):
    try:
        model = tf.keras.models.load_model(model_path)
        return model, None
    except Exception as e:
        return None, str(e)

# Set background image and CSS
add_bg_from_url("https://img.freepik.com/free-photo/blue-background-banner-perfect-canva_1361-3591.jpg?t=st=1743913590~exp=1743917190~hmac=7c955865446e74dbbb9c1f9247d7dd3f65055ab0c8a2cf8d5f4f6f58f29d347a&w=1380")
local_css()

# Load Lottie animations
lottie_eye = load_lottieurl("https://assets5.lottiefiles.com/private_files/lf30_TBKozE.json")
lottie_scanning = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_qjosmr4w.json")
lottie_doctor = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_5tl1xxnz.json")
lottie_report = load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_t26194jr.json")

# App title with animation
st.markdown("""
<div class="animate-in" style="text-align: center;">
    <h1>👁️ Advanced Eye Disease Detection System</h1>
</div>
""", unsafe_allow_html=True)

# Enhanced sidebar with interactive elements and animations
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="color: black;">👨‍⚕️ Medical AI Assistant</h2> <!-- Ensure white font for contrast -->
    </div>
    """, unsafe_allow_html=True)
    
    if lottie_doctor:
        st_lottie(lottie_doctor, speed=1, height=180, key="doctor_animation")
    
    st.markdown("### About This Application")
    st.info("This advanced AI system uses deep learning to analyze eye scan images and detect common eye diseases with high accuracy.")
    
    st.markdown("### Detectable Diseases:")
    disease_tabs = st.selectbox("Click to explore diseases", 
                               ["Choose a disease", "Diabetic Retinopathy", "Glaucoma", "Macular Edema", "Cataract"])
    
    # Update disease description background color
    if disease_tabs == "Diabetic Retinopathy":
        st.markdown("""
        <div style="background-color: rgba(200, 230, 200, 0.8); padding: 10px; border-radius: 10px; border-left: 3px solid #3498db;">
            <h4 style="color: #2c3e50;">Diabetic Retinopathy</h4> <!-- Darker font for better contrast -->
            <p style="color: #2c3e50;">A diabetes complication affecting blood vessels in the retina. Can lead to vision loss if untreated.</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif disease_tabs == "Glaucoma":
        st.markdown("""
        <div style="background-color: rgba(200, 230, 200, 0.8); padding: 10px; border-radius: 10px; border-left: 3px solid #3498db;">
            <h4 style="color: #2c3e50;">Glaucoma</h4> <!-- Darker font for better contrast -->
            <p style="color: #2c3e50;">A group of eye conditions that damage the optic nerve, often due to abnormally high pressure in the eye.</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif disease_tabs == "Macular Edema":
        st.markdown("""
        <div style="background-color: rgba(200, 230, 200, 0.8); padding: 10px; border-radius: 10px; border-left: 3px solid #3498db;">
            <h4 style="color: #2c3e50;">Macular Edema</h4> <!-- Darker font for better contrast -->
            <p style="color: #2c3e50;">Swelling in the macula, the central part of the retina responsible for sharp, straight-ahead vision.</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif disease_tabs == "Cataract":
        st.markdown("""
        <div style="background-color: rgba(200, 230, 200, 0.8); padding: 10px; border-radius: 10px; border-left: 3px solid #3498db;">
            <h4 style="color: #2c3e50;">Cataract</h4> <!-- Darker font for better contrast -->
            <p style="color: #2c3e50;">A clouding of the lens in the eye leading to a decrease in vision, affecting one or both eyes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### How to Use:")
    st.markdown("""
    <ol style="color: black;"> <!-- Ensure black font for contrast -->
        <li>Upload a clear eye scan image</li>
        <li>Fill in patient details</li>
        <li>Click 'Analyze and Generate Report'</li>
        <li>Review the detailed diagnosis</li>
        <li>Download the medical report</li>
    </ol>
    """, unsafe_allow_html=True)
    
    st.markdown("### Need Help?")
    if st.button("Show Tutorial", key="tutorial_button"):
        st.markdown("""
        <div style="background-color: rgba(200, 230, 250, 0.8); padding: 15px; border-radius: 10px; margin-top: 10px;">
            <p style="color: #2c3e50; font-weight: bold;">Quick Tutorial:</p> <!-- Darker font for better contrast -->
            <ol style="color: #2c3e50;"> <!-- Darker font for better contrast -->
                <li>Upload a fundus or retinal scan image using the upload button</li>
                <li>Enter patient's name, age, and select gender</li>
                <li>Add any relevant medical history in the optional section</li>
                <li>Click "Analyze" to process the image</li>
                <li>Review the diagnostic information and download the report</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    if lottie_eye:
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        st_lottie(lottie_eye, speed=1, height=150, key="eye_animation")

# Load the trained model
MODEL_PATH = "C:/Users/Shilpa/OneDrive/Desktop/EYE DISEASE DETECTION PROJECT/EYE DISEASE MODEL 01.h5"
model, model_error = load_model(MODEL_PATH)

if model_error:
    st.error(f"Error loading model: {model_error}")
    st.stop()

# List of diseases
DISEASES = ["Diabetic Retinopathy", "Glaucoma", "Macular Edema", "Cataract"]

# Disease information dictionary with detailed medical properties
DISEASE_INFO = {
    "Diabetic Retinopathy": {
        "description": "A diabetes complication that affects the eyes. It's caused by damage to the blood vessels in the retina. Regular eye exams are important for early detection.",
        "symptoms": ["Blurred vision", "Fluctuating vision", "Impaired color vision", "Dark or empty areas in vision", "Vision loss"],
        "risk_factors": ["Duration of diabetes", "Poor blood sugar control", "High blood pressure", "High cholesterol", "Pregnancy", "Tobacco use"],
        "medical_details": {
            "Hemorrhages": "May include dot and blot hemorrhages (small red spots within retinal layers) or flame-shaped hemorrhages from superficial retinal layers.",
            "Microaneurysms": "Small red dots that are often the first sign of diabetic retinopathy.",
            "Retinal Layer Thickness": "Thickening indicates macular edema, while thinning suggests nerve fiber layer loss or ischemic damage.",
            "Exudates": "Hard exudates (yellow deposits) or cotton wool spots (white, fluffy patches) may be present.",
            "Stage Classification": ["Mild NPDR", "Moderate NPDR", "Severe NPDR", "Proliferative Diabetic Retinopathy (PDR)"]
        }
    },
    "Glaucoma": {
        "description": "A group of eye conditions that damage the optic nerve, often caused by abnormally high pressure in the eye. It can lead to vision loss if not treated early.",
        "symptoms": ["Patchy blind spots", "Tunnel vision", "Severe headache", "Eye pain", "Nausea and vomiting", "Blurred vision", "Halos around lights"],
        "risk_factors": ["Age over 60", "Family history", "Medical conditions (diabetes, heart disease)", "High intraocular pressure", "Thin corneas", "Ethnicity (higher risk in Black, Asian, and Hispanic populations)"],
        "medical_details": {
            "Optic Disc Appearance": "Increased Cup-to-Disc Ratio (CDR) above 0.6 is suspicious for glaucoma. Vertical cup enlargement is common in glaucomatous damage.",
            "Neuroretinal Rim": "Thinning of the rim, especially in inferior and superior regions. Notching may be present at superior or inferior poles.",
            "Retinal Nerve Fiber Layer": "May show diffuse thinning or localized wedge-shaped defects radiating from the optic disc.",
            "Peripapillary Atrophy": "Zone beta (closer to disc) indicates glaucomatous damage. Zone alpha may suggest early progression.",
            "Hemorrhages": "Drance hemorrhages may appear as small, flame-shaped hemorrhages at the optic disc margin.",
            "Structural Damage Signs": ["Bayoneting of vessels", "Laminar dot sign"]
        }
    },
    "Macular Edema": {
        "description": "Swelling or thickening of the macula, a small area in the center of the retina that is responsible for detailed central vision.",
        "symptoms": ["Blurred or wavy central vision", "Colors appear washed out or faded", "Vision loss", "Objects may appear to be a different size or shape than they actually are"],
        "risk_factors": ["Diabetes", "Age-related macular degeneration", "Inflammatory diseases", "Eye surgery", "Medications", "Retinal vein occlusion"],
        "medical_details": {
            "Macula Condition": "Swelling or thickening indicates fluid accumulation. Loss of macular clarity suggests possible cystoid macular edema.",
            "Foveal Reflex": "Reduced or absent foveal reflex indicates fluid accumulation and macular disruption.",
            "Retinal Vessels": "May show microaneurysms, dilated vessels, or exudates (yellowish deposits around the macula).",
            "Retinal Hemorrhages": "Dot, blot, or flame-shaped hemorrhages may be present due to weakened vessel walls.",
            "Macular Cyst Formation": "Presence of cystoid spaces indicates fluid accumulation, which contributes to central vision loss.",
            "Optic Disc Condition": "May show edema at disc margin or blurred disc borders.",
            "Secondary Complications": ["Ischemia", "Vitreomacular traction"]
        }
    },
    "Cataract": {
        "description": "A clouding of the lens in the eye leading to a decrease in vision. It can affect one or both eyes and often develops slowly.",
        "symptoms": ["Cloudy or blurry vision", "Difficulty seeing at night", "Sensitivity to light and glare", "Need for brighter light for reading", "Seeing halos around lights", "Fading or yellowing of colors"],
        "risk_factors": ["Aging", "Diabetes", "Smoking", "Alcohol use", "Prolonged sunlight exposure", "Obesity", "High blood pressure", "Previous eye injury or inflammation", "Previous eye surgery", "Prolonged use of corticosteroids"],
        "medical_details": {
            "Lens Opacity": "Ranges from mild (slight haziness with visible retinal details) to severe (poor visibility of optic disc and vessels).",
            "Optic Disc": "Reduced clarity and potentially pale or washed-out appearance with significant cataract progression.",
            "Retinal Blood Vessels": "Visibility ranges from clear (mild cataract) to blurred or complete loss of detail (severe cataract).",
            "Foveal and Macular Region": "May show loss of central reflex and color distortion due to light scattering from lens opacity.",
            "Lens-Induced Changes": ["Posterior Subcapsular Cataract (PSC)", "Nuclear Sclerosis", "Cortical Cataract"],
            "Secondary Complications": "May include elevated intraocular pressure or increased risk of retinal detachment."
        }
    }
}

# Function to preprocess the image for the model
def preprocess_image(image):
    # Extract expected dimensions from model
    expected_height = model.input_shape[1]
    expected_width = model.input_shape[2]
    expected_channels = model.input_shape[3]
    
    # Resize to model's expected dimensions
    image = image.resize((expected_width, expected_height))
    
    # Convert to appropriate color mode
    if expected_channels == 1:
        image = image.convert("L")  # Grayscale
    else:
        image = image.convert("RGB")  # RGB
    
    # Convert to numpy array and normalize
    image = np.array(image) / 255.0
    
    # Ensure correct shape for channels
    if expected_channels == 1 and len(image.shape) == 2:
        image = np.expand_dims(image, axis=-1)
    
    # Add batch dimension
    image = np.expand_dims(image, axis=0)
    
    return image

# Function to predict disease
def predict_disease(image):
    try:
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image)
        predicted_class = np.argmax(predictions)
        confidence = predictions[0][predicted_class] * 100
        return DISEASES[predicted_class], confidence, None
    except Exception as e:
        return None, None, str(e)



# Disease Details
disease_details = {
    "Glaucoma": """Optic Disc Appearance:
    - Increased Cup-to-Disc Ratio:** Suspicious for glaucoma (≥ 0.6), indicating possible loss of retinal nerve fibers.
    - Vertical Cup Enlargement:** Elongated.

    Neuroretinal Rim Condition:
    - Thinning of the Neuroretinal Rim: Significant thinning observed, particularly in the inferior and superior regions.
    - Notching: Localized loss of the neuroretinal rim detected at the superior pole.

    Retinal Nerve Fiber Layer (RNFL) Loss:
    - Diffuse RNFL Thinning: Noted, with reduced brightness around the optic disc.
    - Localized RNFL Defects: Wedge-shaped dark areas radiating from the optic disc, with corresponding visual field loss.

    Peripapillary Atrophy (PPA):
    - Presence of PPA: Zone beta changes indicate glaucomatous damage.

    Hemorrhages:
    - Drance Hemorrhages: Present, suggesting glaucoma progression.

    Intraocular Pressure (IOP) Status:
    - Elevated IOP (>21 mmHg), indicating possible risk of glaucoma.

    Signs of Structural Damage:
    - Bayoneting of Vessels: Present, indicating sharp angulation of vessels at the disc margin due to cupping.

    **Conclusion:
    - Stage of Glaucoma: Moderate stage with significant rim thinning, RNFL defects, and mild visual field loss.
    - Recommendation: Immediate follow-up with IOP monitoring and potential medical or laser therapy.
    """,

    "Diabetic Retinopathy": """Presence of Hemorrhages:
    - **Dot and Blot Hemorrhages:** Small red spots indicating capillary damage.
    - **Flame-Shaped Hemorrhages:** Present, suggesting bleeding from superficial retinal layers.

    Presence of Microaneurysms:
    - Numerous microaneurysms observed, indicating early diabetic retinopathy.

    Retinal Layer Thickness:
    - Thickened retina suggests macular edema, a common complication.

    Optic Cup Ratio:
    - Increased, requiring further evaluation.

    Presence of Exudates:
    - Hard Exudates: Yellow deposits near the macula indicating leakage from damaged capillaries.
    - Cotton Wool Spots: Present, suggesting nerve fiber damage due to ischemia.

    Stage of Diabetic Retinopathy:
    - Moderate Non-Proliferative Diabetic Retinopathy (NPDR).

    Recommendation:
    - Regular monitoring, with possible anti-VEGF injections or laser therapy if macular edema worsens.
    """,

    "Cataract": """Lens Opacity:
    - Opacity Level: Severe, leading to reduced clarity and brightness in the fundus image.

    Optic Disc:
    - Disc Clarity: Less defined due to light penetration issues.
    - Color of Optic Disc: Washed out, indicating significant cataract progression.

    Retinal Blood Vessels:
    - Visibility of Blood Vessels: Complete loss of detail due to lens opacity.

    Foveal and Macular Region:
    - Loss of Central Reflex: Obscured foveal reflex.
    - Color Distortion: Alteration in macular color due to light scattering.

    Lens-Induced Retinal Changes:
    - Cortical Cataract:** Radial white streaks affecting vision.

    **Signs of Secondary Complications:
    - Elevated Intraocular Pressure (IOP): Indicating coexisting glaucoma risk.
    - Retinal Detachment Risk: Advanced cataract increases risk of posterior vitreous detachment (PVD).

    Conclusion:
    - Stage of Cataract: Advanced stage.
    - Recommendation: Surgical intervention recommended.
    """
}


# Replace unsupported characters in text
def sanitize_text(text):
    replacements = {
        "•": "-",
        "→": "->",
        "'": "'",
        "≥": ">=",  # Replace ≥ with >=
        "–": "-",   # Replace en dash with hyphen
        """: "\"",  # Replace curly quotes
        """: "\"",
        "…": "..."  # Replace ellipsis
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text
# Function to split text properly (missing in original code)
def simple_split(pdf, text, font, font_size, width):
    lines = []
    words = text.split(' ')
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        test_width = pdf.get_string_width(test_line)
        
        if test_width > width:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    
    if current_line:
        lines.append(current_line)
    
    return lines

# Function to generate a detailed PDF report
def generate_pdf(patient_details, disease_predictions, confidence_scores, image, detailed_analysis=True, output_path="Ocular_Examination_Report.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Add a blue header bar
    pdf.set_fill_color(41, 128, 185)  # A professional blue color
    pdf.rect(0, 0, 210, 25, 'F')
    
    # Title
    pdf.set_font("Arial", style='B', size=18)
    pdf.set_text_color(255, 255, 255)  # White text for header
    pdf.cell(0, 20, txt="Ocular Examination Report", ln=True, align="C")
    pdf.ln(5)
    
    # Reset text color to black
    pdf.set_text_color(0, 0, 0)
    
    # Patient Details
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(0, 10, txt="Patient Basic Information:", ln=True)
    
    # Create a light blue background for patient info section
    start_y = pdf.get_y()
    pdf.set_font("Arial", size=12)
    
    info_height = len(patient_details) * 8 + 5
    pdf.set_fill_color(235, 245, 251)  # Light blue background
    pdf.rect(10, start_y, 190, info_height, 'F')
    
    # Add patient details over the background
    pdf.set_y(start_y + 2)  # Small padding
    for key, value in patient_details.items():
        pdf.cell(0, 8, txt=f"   {key}: {value}", ln=True)
    
    pdf.ln(5)  # Line break
    
    # Diagnosis Section (Only detected diseases)
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(0, 10, txt="Diagnosis:", ln=True)
    
    # Fix the disease predictions handling
    detected_diseases = {}

    if isinstance(disease_predictions, dict):
        detected_diseases = {disease: status for disease, status in disease_predictions.items() if status == "Yes"}
        filtered_confidence = {}
        for disease, conf in confidence_scores.items():
            if disease in detected_diseases:
                filtered_confidence[disease] = conf
        confidence_scores = filtered_confidence
    else:
        # Handle case where disease_predictions might be a single string
        if disease_predictions and disease_predictions != "No":
            detected_diseases = {disease_predictions: "Yes"}
            if not isinstance(confidence_scores, dict):
                confidence_scores = {disease_predictions: confidence_scores}

    # Ensure confidence_scores is correctly populated
    if not isinstance(confidence_scores, dict):
        confidence_scores = {}

    # Display diseases with a visual indicator for confidence
    if not detected_diseases:
        pdf.cell(0, 8, txt="No ocular disease detected.", ln=True)
    else:
        # Create a more visually appealing disease section
        start_y = pdf.get_y()
        disease_height = len(detected_diseases) * 20 + 5

        pdf.set_fill_color(255, 240, 245)  # Light pink/red for disease warning
        pdf.rect(10, start_y, 190, disease_height, 'F')

        pdf.set_y(start_y + 5)
        for disease, status in detected_diseases.items():
            confidence = confidence_scores.get(disease, 100)  # Default to 100% confidence if not available
            if not isinstance(confidence, (int, float)):
                confidence = 100  # Ensure confidence is set to 100% if invalid

            pdf.set_font("Arial", style='B', size=12)
            pdf.cell(120, 8, txt=f"   Disease: {disease}", ln=0)
            pdf.cell(70, 8, txt=f"Confidence: {confidence:.1f}%", ln=1)

            # Add a confidence bar
            bar_y = pdf.get_y()
            bar_width = 150 * (confidence / 100)  # Correctly calculate bar width based on confidence
            pdf.set_fill_color(192, 57, 43)  # Red for the confidence bar
            pdf.rect(30, bar_y, bar_width, 5, 'F')  # Draw the confidence bar
            pdf.set_fill_color(220, 220, 220)  # Gray for the remaining bar
            pdf.rect(30 + bar_width, bar_y, 150 - bar_width, 5, 'F')
            pdf.ln(10)
    
    pdf.ln(10)  # Line break
    
    # Default Sections for Every Report with improved styling
    section_titles = ["Optic Disc Information", "Blood Vessels Information", "Retina Information"]
    section_contents = [
        {
            "Description": "The bright circular region where the optic nerve exits the eye.",
            "Size": "An enlarged disc could suggest glaucoma.",
            "Shape": "Irregular shapes may indicate damage or pressure issues."
        },
        {
            "Thickness and Branching": "Can indicate hypertension, diabetic retinopathy, or vascular issues.",
            "Hemorrhages": "Small bleeding points can suggest diabetes or hypertension.",
            "A/V Ratio": "Normally around 2:3. A reduced ratio may indicate hypertension."
        },
        {
            "Retinal Thickness": "Thinning may suggest glaucoma, macular degeneration, or retinal detachment.",
            "Color and Pigmentation": "Pale Retina: Poor blood flow (ischemia); Dark Spots: Retinal degeneration or hemorrhages"
        }
    ]
    
    # Section colors
    section_colors = [
        [142, 68, 173],  # Purple
        [41, 128, 185],  # Blue
        [39, 174, 96]    # Green
    ]
    
    for i, title in enumerate(section_titles):
        # Add a colored header for each section
        pdf.set_fill_color(*section_colors[i])
        pdf.set_text_color(255, 255, 255)  # White text
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(0, 10, txt="  " + title, ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)  # Reset to black text
        
        content = section_contents[i]
        pdf.set_font("Arial", size=12)
        
        if isinstance(content, dict):
            for key, value in content.items():
                pdf.set_font("Arial", style='B', size=12)
                pdf.cell(60, 8, txt=f"   {key}:", ln=0)
                pdf.set_font("Arial", size=12)
                
                # Handle nested dictionaries for more complex sections
                if isinstance(value, dict):
                    pdf.ln()
                    for subkey, subvalue in value.items():
                        pdf.cell(0, 6, txt=f"      - {subkey}: {subvalue}", ln=True)
                else:
                    # Split long text if needed
                    width = pdf.get_string_width(value)
                    if width > 120:
                        pdf.ln()
                        lines = simple_split(pdf, value, "Arial", 12, 180)
                        for line in lines:
                            pdf.cell(0, 6, txt=f"      {line}", ln=True)
                    else:
                        pdf.cell(0, 8, txt=f"{value}", ln=True)
        else:
            lines = simple_split(pdf, str(content), "Arial", 12, 180)
            for line in lines:
                pdf.cell(0, 6, txt=f"   {line}", ln=True)
        
        pdf.ln(5)  # Extra space between sections
    
    # Process Disease-Specific Details
    if detailed_analysis and detected_diseases:
        pdf.add_page()
        pdf.set_fill_color(41, 128, 185)  # Blue header
        pdf.set_text_color(255, 255, 255)  # White text
        pdf.set_font("Arial", style='B', size=16)
        pdf.cell(0, 10, txt="Detailed Disease Analysis", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)  # Reset to black
        pdf.ln(5)

        for disease in detected_diseases:
            if disease in disease_details:
                # Add a colored bar for the disease name
                pdf.set_fill_color(52, 152, 219)  # Light blue
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", style='B', size=14)
                pdf.cell(0, 8, txt=f"  {disease}", ln=True, fill=True)
                pdf.set_text_color(0, 0, 0)
                
                text = sanitize_text(disease_details[disease])
                lines = text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        pdf.ln(3)
                        continue
                        
                    # Format headings differently from list items
                    if line.startswith("- "):
                        pdf.set_font("Arial", size=11)
                        pdf.cell(0, 6, txt=f"    {line}", ln=True)
                    elif line.startswith("  - "):
                        pdf.set_font("Arial", size=10)
                        pdf.cell(0, 6, txt=f"      {line}", ln=True)
                    else:
                        pdf.set_font("Arial", style='B', size=12)
                        pdf.cell(0, 7, txt=f"  {line}", ln=True)
                
                pdf.ln(5)

    # Add Eye Scan Image
    if image:
        try:
            pdf.add_page()
            pdf.set_fill_color(41, 128, 185)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", style='B', size=16)
            pdf.cell(0, 10, txt="Eye Scan Image", ln=True, fill=True)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(5)

            temp_img_path = "temp_eye_scan.jpg"
            image.save(temp_img_path)

            # Add a border around the image
            img_y = pdf.get_y()
            pdf.image(temp_img_path, x=15, y=img_y, w=180)
            pdf.rect(15, img_y, 180, 180, 'D')  # Draw a rectangle around the image

            os.remove(temp_img_path)  # Clean up
        except Exception as e:
            pdf.cell(0, 8, txt=f"Error adding image: {str(e)}", ln=True)

    # Add a footer
    pdf.set_y(-20)
    pdf.set_font("Arial", style='I', size=8)
    pdf.set_text_color(128, 128, 128)  # Gray text for footer
    pdf.cell(0, 10, txt="This report is generated for medical reference purposes only.", ln=True, align="C")
    pdf.cell(0, 5, txt=f"Generated on {pd.Timestamp.now().strftime('%Y-%m-%d')}", ln=True, align="C")

    # Save PDF
    pdf.output(output_path)
    print(f"Report saved at {output_path}")
    return output_path


    
# Main application layout
tab1, tab2 = st.tabs(["📊 Disease Detection", "ℹ️ Disease Information"])

with tab1:
    st.markdown("""
    <div class="animate-in">
        <p class="section-header">Upload an eye scan image for analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Two-column layout for upload and patient details
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Choose a retinal or fundus image...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Eye Scan", use_container_width=True, clamp=True)
    
    with col2:
        st.markdown("""
        <div class="section-header">Patient Information</div>
        """, unsafe_allow_html=True)
        
        patient_name = st.text_input("**Patient Name**")  # Bold font for label
        
        col_age, col_gender = st.columns(2)
        with col_age:
            patient_age = st.number_input("**Age**", min_value=0, max_value=120, step=1)  # Bold font for label
        with col_gender:
            patient_gender = st.selectbox("**Gender**", ["Male", "Female", "Other"])  # Bold font for label
        
        st.markdown("""
        <div class="section-header">Medical History (Optional)</div>
        """, unsafe_allow_html=True)
        
        medical_history = st.text_area("**Relevant Medical History**", height=100)  # Bold font for label
        
        # Additional medical information
        conditions = st.multiselect("**Existing Conditions**",  # Bold font for label
                                   ["Diabetes", "Hypertension", "Cardiovascular Disease", 
                                    "Renal Disease", "None"],
                                   default=["None"])
        
        medications = st.text_input("**Current Medications (separated by commas)**")  # Bold font for label
    
    # Process button
    if st.button("Analyze and Generate Report", type="primary"):
        if uploaded_file is None:
            st.warning("Please upload an eye scan image")
        elif not patient_name or patient_age == 0:
            st.warning("Please fill in patient name and age")
        else:
            with st.spinner("Processing image..."):
                if lottie_scanning:
                    st_lottie(lottie_scanning, speed=1, height=150, key="scanning_animation")
                
                # Adding a slight delay to make the scanning animation visible
                time.sleep(2)
                
                # Predict disease
                disease, confidence, error = predict_disease(image)
                
                if error:
                    st.error(f"Error during prediction: {error}")
                else:
                    # Prepare patient details for report
                    patient_details = {
                        "name": patient_name,
                        "age": patient_age,
                        "sex": patient_gender,
                        "medical_history": medical_history,
                        "existing_conditions": conditions if "None" not in conditions else [],
                        "medications": medications,
                        "id": f"PT-{int(time.time())}"[-6:]  # Generate a simple ID
                    }
                    
                    # Generate detailed analysis
                    detailed_analysis = {
                        "disease": disease,
                        "confidence": confidence,
                        "severity": "High" if confidence > 70 else "Medium" if confidence > 40 else "Low",
                        # Additional analysis fields would be added here based on the disease
                    }
                    
                    # Display results
                    st.success("Analysis completed!")
                    
                    # Display diagnostic results
                    st.markdown("""
                    <div class="section-header">Diagnostic Results</div>
                    """, unsafe_allow_html=True)
                    
                    # Create a nice result box
                    st.markdown(f"""
                    <div class="disease-info-card">
                        <h3>Detected Disease: {disease}</h3>
                        <p>Confidence: <strong>{confidence:.2f}%</strong></p>
                        <p>Severity: <span class="severity-badge severity-{'high' if confidence > 70 else 'medium' if confidence > 40 else 'low'}">
                            {detailed_analysis['severity']}
                        </span></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display additional disease information
                    if disease in DISEASE_INFO:
                        info = DISEASE_INFO[disease]
                        
                        with st.expander("See Disease Information", expanded=True):
                            st.markdown(f"### About {disease}")
                            st.markdown(info["description"])
                            
                            st.markdown("#### Common Symptoms")
                            for symptom in info["symptoms"]:
                                st.markdown(f"- {symptom}")
                            
                            st.markdown("#### Risk Factors")
                            for factor in info["risk_factors"]:
                                st.markdown(f"- {factor}")
                    
                    # Generate PDF report
                    with st.spinner("Generating medical report..."):
                        if lottie_report:
                            st_lottie(lottie_report, speed=1, height=120, key="report_animation")
                            
                        # Add slight delay for animation
                        time.sleep(1.5)
                        
                        pdf_data = generate_pdf(patient_details, disease, confidence, image, detailed_analysis)
                        
                        # Create download button for the report
                        st.markdown("""
                        <div class="section-header">Medical Report</div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class="report-card">
                            <p>✅ A comprehensive medical report has been generated for <strong>{patient_name}</strong>.</p>
                            <p>🔍 The report includes detailed analysis of the {disease} detection.</p>
                            <p>📋 Please download the report for complete findings and recommendations.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Correctly use pdf_output_path instead of pdf_path
                        with open(pdf_data, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()

                        st.download_button(
                            label="📥 Download Medical Report",
                            data=pdf_bytes,
                            file_name=f"Eye_Disease_Report_{patient_name.replace(' ', '_')}.pdf",
                            mime="application/pdf"
                        )

with tab2:
    st.markdown("""
    <div class="animate-in">
        <h2 style="color: #2c3e50;">Eye Disease Information Center</h2> <!-- Darker font for better contrast -->
        <p style="color: #2c3e50;">Learn about common eye diseases detected by our system</p> <!-- Darker font for better contrast -->
    </div>
    """, unsafe_allow_html=True)
    
    # Disease selection
    selected_disease = st.selectbox(
        "Select a disease to learn more",
        list(DISEASE_INFO.keys())
    )
    
    # Display disease information
    if selected_disease:
        disease_data = DISEASE_INFO[selected_disease]
        
        st.markdown(f"""
        <div class="disease-info-card" style="background: rgba(240, 240, 240, 0.9); color: #2c3e50;"> <!-- Adjusted background and font color -->
            <h2>{selected_disease}</h2>
            <p>{disease_data['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="section-header" style="background-color: #edf2f7; color: #2c3e50;">Common Symptoms</div> <!-- Adjusted font color -->
            """, unsafe_allow_html=True)
            
            for symptom in disease_data["symptoms"]:
                st.markdown(f"""
                <div class="property-card" style="background-color: #f8f9fa; color: #2c3e50;"> <!-- Adjusted background and font color -->
                    ● {symptom}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="section-header" style="background-color: #edf2f7; color: #2c3e50;">Risk Factors</div> <!-- Adjusted font color -->
            """, unsafe_allow_html=True)
            
            for factor in disease_data["risk_factors"]:
                st.markdown(f"""
                <div class="property-card" style="background-color: #f8f9fa; color: #2c3e50;"> <!-- Adjusted background and font color -->
                    ● {factor}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="section-header" style="background-color: #edf2f7; color: #2c3e50;">Medical Details</div> <!-- Adjusted font color -->
            """, unsafe_allow_html=True)
            
            for key, value in disease_data["medical_details"].items():
                st.markdown(f"""
                <div class="property-card" style="background-color: #f8f9fa; color: #2c3e50;"> <!-- Adjusted background and font color -->
                    <strong>{key}</strong>: {value if isinstance(value, str) else ', '.join(value)}
                </div>
                """, unsafe_allow_html=True)
        
        # Add a section for treatment options
        st.markdown("""
        <div class="section-header">Common Treatment Approaches</div>
        """, unsafe_allow_html=True)
        
        if selected_disease == "Diabetic Retinopathy":
            treatments = [
                "Anti-VEGF injections to reduce abnormal blood vessel growth",
                "Laser treatment (photocoagulation) to seal leaking blood vessels",
                "Vitrectomy surgery for advanced cases with bleeding",
                "Blood sugar control to slow progression",
                "Regular eye examinations for early detection of changes"
            ]
        elif selected_disease == "Glaucoma":
            treatments = [
                "Eye drops to reduce intraocular pressure",
                "Oral medications to decrease fluid production or increase drainage",
                "Laser treatments like trabeculoplasty or iridotomy",
                "Minimally invasive glaucoma surgery (MIGS)",
                "Traditional surgery such as trabeculectomy for advanced cases"
            ]
        elif selected_disease == "Macular Edema":
            treatments = [
                "Anti-VEGF injections to reduce fluid leakage",
                "Corticosteroid injections to reduce inflammation",
                "Focal laser treatment to seal leaking blood vessels",
                "Treatment of underlying conditions (diabetes, hypertension)",
                "Vitrectomy surgery for cases with vitreomacular traction"
            ]
        elif selected_disease == "Cataract":
            treatments = [
                "Cataract surgery with intraocular lens implantation",
                "Phacoemulsification (ultrasound to break up the lens)",
                "Extracapsular cataract extraction for advanced cases",
                "New eyeglasses prescription for early cases",
                "Prevention strategies like UV protection and smoking cessation"
            ]
        
        col_treat1, col_treat2 = st.columns(2)
        
        with col_treat1:
            for treatment in treatments[:3]:
                st.markdown(f"""
                <div class="property-card">
                {treatment}
                </div>
                """, unsafe_allow_html=True)
        
        with col_treat2:
            for treatment in treatments[3:]:
                st.markdown(f"""
                <div class="property-card">
                    ● {treatment}
                </div>
                """, unsafe_allow_html=True)
        
        # Add a note about seeking professional advice
        st.info("Note: This information is provided for educational purposes only. Always consult a healthcare professional for medical advice and treatment options.")

# Add a footer
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding: 20px; border-top: 1px solid #e0e0e0;">
    <p>© 2025 Advanced Eye Disease Detection System | Powered by AI</p>
    <p style="font-size: 0.8rem;">This application is for educational and screening purposes only and is not intended to replace professional medical advice.</p>
</div>
""", unsafe_allow_html=True)
