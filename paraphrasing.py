import os
from openai import OpenAI
import streamlit as st
import PyPDF2

openai = OpenAI(api_key="")

st.title(':blue[Paraphrase]')
st.divider()

def paraphrase_text(input_text):
    prompt = f"You are an expert at paraphrasing texts. You will be given a text and need to provide a paraphrased version.\n" \
             f"Text: {input_text}\n\nParaphrased:"
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": input_text,
                }
            ],
            max_tokens=150
        )
        paraphrased_text = response.choices[0].message.content
        return paraphrased_text
    except Exception as e:
        st.write(f"Error paraphrasing text: {e}")
        return None

def paraphrase_pdf(input_pdf):
    pdf_reader = PyPDF2.PdfReader(input_pdf)
    paraphrased_pdf_writer = PyPDF2.PdfWriter()
    
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        paraphrased_text = paraphrase_text(page.extractText())
        
        if paraphrased_text:
            paraphrased_page = pdf_reader.add_page(page)
            paraphrased_page.mergePage(paraphrased_text)
            paraphrased_pdf_writer.addPage(paraphrased_page)
    
    return paraphrased_pdf_writer

def main():
    st.text("Paraphrase Text:")
    input_text = st.text_area("Enter text to paraphrase:")
    
    if st.button("Paraphrase"):
        paraphrased_text = paraphrase_text(input_text)
        if paraphrased_text:
            st.write("Paraphrased Text:")
            st.write(paraphrased_text)
    
    st.text("Paraphrase PDF:")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("Paraphrase PDF"):
            paraphrased_pdf_writer = paraphrase_pdf(uploaded_file)
            st.write("Paraphrased PDF:")
            st.download_button(
                label="Download Paraphrased PDF",
                data=paraphrased_pdf_writer,
                key="download_button",
                file_name="paraphrased_pdf.pdf",
            )

if __name__ == "__main__":
    main()