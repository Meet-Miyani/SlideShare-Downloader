import streamlit as st
import requests
from bs4 import BeautifulSoup
import re


# Function to fetch and extract image links
def extract_slide_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        new_player_div = soup.find("div", id="new-player")
        slide_divs = new_player_div.find_all("div", id=re.compile(r"slide\d+"))

        image_links = []
        for slide_div in slide_divs:
            img_tag = slide_div.find("img")
            if img_tag and img_tag.get("srcset"):
                srcset = img_tag["srcset"]
                srcset_entries = [entry.strip().split(" ")[0] for entry in srcset.split(",")]
                highest_res_image = srcset_entries[-1]
                image_links.append(highest_res_image)
        return image_links
    else:
        st.error("Failed to fetch the webpage. Please check the URL.")
        return []


st.title("SlideShare Downloader")
url = st.text_input("Enter slide url")

if st.button("Fetch Slide"):
    if url:
        with st.spinner("In progress"):  # Loader here
            # Extract image links
            image_links = extract_slide_links(url)

        if image_links:
            st.session_state.image_links = image_links  # Save in session state
            st.session_state.index = 0  # Initialize slide index
            st.success(f"Total Slides Extracted: {len(image_links)}")
        else:
            st.error("No slides found.")
    else:
        st.warning("Please enter a valid SlideShare URL.")

# Initialize session state for image_links and index if not already done
if 'image_links' not in st.session_state:
    st.session_state.image_links = []  # Empty list initially

if 'index' not in st.session_state:
    st.session_state.index = 0


# Function to display the current image
def display_image(index):
    if st.session_state.image_links:  # Check if image_links exists
        st.image(st.session_state.image_links[index], use_container_width=True)
    else:
        st.warning("No images to display. Please fetch slides first.")


st.image(st.session_state.image_links, use_container_width=True)
