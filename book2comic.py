import streamlit as st
import openai
import tkinter as tk
from tkinter import filedialog

openai.api_key = "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"
def get_panel_descriptions(txt_input):
    #story = txt_input

    prompt_message1 = "Provide a text description for each panel that I could give to an illustrator to turn into a comic.Each panel has to include the background, main content, and the text bubble. Limit to 5 panels" + txt_input
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
        print(f"An error occurred: {error}")

def generate_comic_panels(descriptions):
  panels = []
  # Split the description into individual panel descriptions
  panel_texts = descriptions.split('\n\n')  # Adjust the split as needed based on the format
  panel_texts = panel_texts[:-1]

  for i in range(len(panel_texts)):
    if i == 0:
      prompt_message2 = "Create an image for my comic series" + panel_texts[i]
    else:
      prompt_message2 = "Create this panel of my comic series, matching the graphic style of the previous images. The previous panel is also provided for reference" + panel_texts[i-1] + panel_texts[i]

    response = openai.Image.create(
      prompt=prompt_message2,
      n=1,
      size="1024x1024"
    )
    panels.append(response['data'][0]['url'])
  return panels

def generate_response(txt_input):
  panel_descriptions = get_panel_descriptions(txt_input)
  comic_image_url = generate_comic_panels(panel_descriptions)
  print(comic_image_url)

# Page title
st.set_page_config(page_title='Book2Comic App')
st.title('📚🎨 Book2Comic App')

# Txt file input
txt_input = st.text_area('Enter your text', '', height=200))



# Form to accept user's text input for summarization
result = []
with st.form('convert_form', clear_on_submit=True):
    openai_api_key = st.text_input('OpenAI API Key', type = 'password', disabled=not txt_input)
    submitted = st.form_submit_button('Submit')
    if submitted and openai_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response = generate_response(txt_input)
            result.append(response)
            del openai_api_key

if len(result):
    st.info(response)