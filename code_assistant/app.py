import requests
import gradio as gr

url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}

history = []

def generate_response(prompt):
    history.append(f"User: {prompt}")
    final_prompt = "\n".join(history) + "\nAssistant:"

    data = {
        "model": "codeAssistant",
        "prompt": final_prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        reply = response.json().get("response", "")
        history.append(f"Assistant: {reply}")
        return reply
    return "Error generating response"


with gr.Blocks(fill_height=True) as demo:
    gr.Markdown("## 🤖 Ollama Text Generator")

    with gr.Row():
        prompt = gr.Textbox(
            lines=6,
            placeholder="Enter your prompt...",
            scale=1
        )
        output = gr.Textbox(
            lines=25,
            label="Output",
            scale=2    
        )

    submit = gr.Button("Submit", variant="primary")
    submit.click(generate_response, prompt, output)

demo.launch()
