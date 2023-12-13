import sys
sys.path.append('../gcp/generated/')

from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from gradio_calendar import Calendar

import gradio as gr
import grpc
import text_embedding_pb2
import text_embedding_pb2_grpc

BASE = "base"
LARGE = "large"
XL = "xl"

# rpc_endpoint_map = {
#     BASE: "localhost:50051",
#     LARGE: "localhost:50051",
#     XL: "localhost:50051"
# }

rpc_endpoint_map = {
    BASE: "34.42.49.197:80",
    LARGE: "34.69.192.208:80",
    XL: "34.173.182.67"
}

def retrieval_request(model_radio, input_text, start_date, end_date):
    with grpc.insecure_channel(rpc_endpoint_map[model_radio]) as channel:
        stub = text_embedding_pb2_grpc.TextEmbeddingStub(channel)

        start_time, end_time = Timestamp(), Timestamp()
        start_time.FromDatetime(start_date)
        end_time.FromDatetime(end_date)

        response = stub.GetPreferenceArticles(
            text_embedding_pb2.GetPreferenceArticlesRequest(
                preference_text=input_text,
                start_time=start_time,
                end_time=end_time
        ))

        results = []
        for article in response.article:
            published_on = article.published_on

            # Convert the Timestamp to a datetime object
            publish_date = datetime.fromtimestamp(published_on.seconds)
            publish_date_str = publish_date.strftime('%b. %d, %Y %I:%M %p ET')

            results.append((article.url, article.title, article.summary, publish_date_str))

    return results

def display_results(model_radio, input_text, start_date, end_date):
    results = retrieval_request(model_radio, input_text, start_date, end_date)
    html_output = "<div style='display: grid; grid-template-rows: auto; grid-auto-flow: row; gap: 10px; overflow-x: auto;'>"
    for url, title, text, published_on in results:
        card = f"""
        <div style='border: 1px solid #ddd; border-radius: 10px; padding: 10px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); min-width: 300px;'>
            <a href='{url}' target='_blank' style='text-decoration: none; color: black;'>
                <h4>{title}</h4>
            </a>
            <p style='font-size: small; color: grey;'>{published_on}</p>
            <p>{text}</p>
        </div>
        """
        html_output += card
    html_output += "</div>"
    return html_output

with gr.Blocks() as demo:
    gr.Markdown("<h2 style='text-align: center;'>RAG Demo Interface</h2>")
    model_radio = gr.Radio(
        ["base", "large", "xl"], label="Which retrieval model would you like to choose?"
    )
    with gr.Row():
        text_input = gr.Textbox(lines=2, label="Retrieval Text", placeholder="Enter text here...", scale=4)
        start_date = Calendar(type="datetime", label="Start Date", scale=1, value="2023-11-24"),
        end_date = Calendar(type="datetime", label="End Date", scale=1, value="2023-11-30"),
    submit_button = gr.Button("Submit")
    output_html = gr.HTML()

    submit_button.click(fn=display_results, inputs=[model_radio, text_input, start_date[0], end_date[0]], outputs=output_html)

demo.launch()

# I am interested in investing in us treasury bonds which are risk free over long term, for example bonds that are greater than 10 years. Show me necessary maro economic trends and SOFR rates.
