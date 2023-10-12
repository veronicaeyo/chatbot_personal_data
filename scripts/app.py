import gradio as gr
from backend import load_db


with gr.Blocks()as demo:
    gr.Markdown("<h1><center>PDF QUERY </center></h1>")
    with gr.Column(scale=0.9):
        with gr.Row():
            file = gr.File(type="file", label="Upload a PDF", file_types=[".pdf"])
            chatbot = gr.Chatbot()
    with gr.Column(scale=0.9):
        text = gr.Textbox(label="\n", placeholder="Write a question and submit")
        with gr.Column(scale=0.9):
            with gr.Row():
                btn = gr.Button(value="Submit")
            # with gr.Column(scale=0.9):
                clear = gr.ClearButton([file, btn])
    

    btn.click(fn=load_db, inputs=[file, text], outputs=chatbot)

if __name__ == "__main__":
    demo.launch()