import gradio as gr
from scripts.query import ask


def handle_query(question):
    result = ask(question)
    sources = "\n".join(f"• {source}" for source in result["sources"])
    return result["answer"], sources


with gr.Blocks() as demo:
    gr.Markdown("# UW Tacoma CSS Professor Review Guide")
    gr.Markdown("Ask a question about UW Tacoma CSS professors based on the collected review documents.")

    inp = gr.Textbox(label="Your question")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=5)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()