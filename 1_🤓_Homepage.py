import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Multipage App",
    page_icon="👋",
)

# Set background image
background_image = "image/adon.jpg"
background_style = f"""
    <style>
        .stApp {{
            background-image: url('{background_image}');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
    </style>
"""
st.markdown(background_style, unsafe_allow_html=True)

# Main content
st.markdown("<h1 style='text-align: center; color: green;'>Proof Of Concept By Adon_inover</h1> ", unsafe_allow_html=True)
st.header("Proof Of Concept (POC) Presented to Mr. Eyad And Mr. Issam.")
st.subheader(" Presented By Talat Mohammad")

title_text = "Disclaimer: Customer/or any other person will not have permission to show this Proof of Concept to any other party apart from the above mentioned presentee"
underlined_title = f"*{title_text}*"
st.markdown(underlined_title, unsafe_allow_html=True)


# Sidebar
st.sidebar.success("Select a page above.")
