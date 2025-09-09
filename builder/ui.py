import gradio as gr
from builder.agent_runner import run_agent

def build_ui(app, tracer):
    with gr.Blocks() as demo:
        gr.Markdown("# Datum : Autonomous Data Analysis Agent")
        chatbot = gr.Chatbot(type="messages")
        user_input = gr.Textbox(label="Ask a question", placeholder="Ex: Show me marketing spend by channel")
        submit_btn = gr.Button("Send", variant='primary')

        state = gr.State([])

        user_input.submit(
            lambda m, h: run_agent(app, tracer, m, h),
            inputs=[user_input, state],
            outputs=[chatbot, state, user_input]
        )

        submit_btn.click(
            lambda m, h: run_agent(app, tracer, m, h),
            inputs=[user_input, state],
            outputs=[chatbot, state, user_input]
        )

    return demo
