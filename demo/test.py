import sys
sys.path.append('../gcp/generated/')

from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

import gradio as gr
import grpc
import text_embedding_pb2
import text_embedding_pb2_grpc

def retrieval_request(input_text):
    with grpc.insecure_channel('localhost:50051') as channel:
    # with grpc.insecure_channel('34.74.89.40:80') as channel:
    # with grpc.insecure_channel('34.170.251.52:80') as channel:
        stub = text_embedding_pb2_grpc.TextEmbeddingStub(channel)

        response = stub.GetPreferenceArticles(
            text_embedding_pb2.GetPreferenceArticlesRequest(
                preference_text=input_text
        ))

        results = []
        for article in response.article:
            published_on = article.published_on

            # Convert the Timestamp to a datetime object
            publish_date = datetime.fromtimestamp(published_on.seconds)
            # publish_date_str = publish_date.strftime('%Y-%m-%d %H:%M:%S')
            publish_date_str = publish_date.strftime('%b. %d, %Y %I:%M %p ET')

            results.append((article.url, article.summary, publish_date_str))

    return results

def display_results(input_text):
    results = retrieval_request(input_text)
    html_output = "<div style='display: grid; grid-template-rows: auto; grid-auto-flow: row; gap: 10px; overflow-x: auto;'>"
    for url, text, published_on in results:
        card = f"""
        <div style='border: 1px solid #ddd; border-radius: 10px; padding: 10px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); min-width: 300px;'>
            <a href='{url}' target='_blank' style='text-decoration: none; color: black;'>
                <h4>{url}</h4>
            </a>
            <p style='font-size: small; color: grey;'>{published_on}</p>
            <p>{text}</p>
        </div>
        """
        html_output += card
    html_output += "</div>"
    return html_output


iface = gr.Interface(
    fn=display_results,
    inputs=gr.Textbox(lines=2, placeholder="Enter text here..."),
    outputs="html",
    title="API Request Interface",
    description="Enter text to make an API request and display results as clickable links.",
    allow_flagging="never"
)

iface.launch()


# with gr.Blocks() as demo:
#     gr.Markdown("API Request Interface\n---\nEnter text to make an API request and display results as clickable links.")
#     text_input = gr.Textbox(lines=2, placeholder="Enter text here...")
#     output_html = gr.HTML()
#     text_input.change(fn=display_results, inputs=text_input, outputs=output_html)

# demo.launch()
