import openai
import streamlit as st
from io import StringIO

# Set up your OpenAI API key securely
# openai.api_key = "YOUR_API_KEY" # Instead of hardcoding, set it as an environment variable or use Streamlit secrets

def get_panel_descriptions(story):
    prompt_message1 = ("Provide a text description for each panel that I could give to "
                       "an illustrator to turn into a comic. Each panel has to include "
                       "the background, main content, and the text bubble. Limit to 5 panels" + story)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_message1}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as error:
        st.error(f"An error occurred: {error}")
        return None

def generate_comic_panels(descriptions):
    panels = []
    panel_texts = descriptions.split('\n\n')  # Adjust the split as needed based on the format
    panel_texts = panel_texts[:-1]  # Assumes the last element is not a panel description

    for i in range(len(panel_texts)):
        if i == 0:
            prompt_message2 = "Create an image for my comic series " + panel_texts[i]
        else:
            prompt_message2 = ("Create this panel of my comic series, matching the graphic style "
                               "of the previous images. The previous panel is also provided for "
                               "reference " + panel_texts[i-1] + " " + panel_texts[i])
        
        response = openai.Image.create(
            prompt=prompt_message2,
            n=1,
            size="1024x1024"
        )
        panels.append(response['data'][0]['url'])
    return panels

def main():
    st.title("Comic Panel Generator")

    # Input for the API key
    api_key = st.text_input("Enter your OpenAI API key", type="password")

    if api_key:
        openai.api_key = api_key

        uploaded_file = st.file_uploader("Choose a text file", type="txt")
        if uploaded_file is not None:
            # To read file as string:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            string_data = stringio.read()

            # Get panel descriptions
            st.write("Generating descriptions...")
            panel_descriptions = get_panel_descriptions(string_data)
            
            if panel_descriptions:
                st.text_area("Panel Descriptions", panel_descriptions, height=250)

                # Generate comic panels
                st.write("Generating comic panels...")
                comic_image_urls = generate_comic_panels(panel_descriptions)
                
                for idx, url in enumerate(comic_image_urls, start=1):
                    st.write(f"Panel {idx}:")
                    st.image(url)
    else:
        st.warning("Please enter your OpenAI API key to proceed.")

if __name__ == "__main__":
    main()
