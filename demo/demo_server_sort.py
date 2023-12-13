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
    XL: "34.173.182.67:80"
}

stored_results = []

def retrieval_request(model_radio, input_text, start_date, end_date, summarize_articles, num_matches):
    global stored_results

    with grpc.insecure_channel(rpc_endpoint_map[model_radio]) as channel:
        stub = text_embedding_pb2_grpc.TextEmbeddingStub(channel)

        start_time, end_time = Timestamp(), Timestamp()
        start_time.FromDatetime(start_date)
        end_time.FromDatetime(end_date)

        print(summarize_articles)

        response = stub.GetPreferenceArticles(
            text_embedding_pb2.GetPreferenceArticlesRequest(
                preference_text=input_text,
                start_time=start_time,
                end_time=end_time,
                summarize_articles=summarize_articles,
                num_matches=num_matches
        ))

        results = []
        for article in response.article:
            results.append((article.url, article.title, article.summary, article.published_on, article.similarity))

        stored_results = results

    return stored_results

def update_output_on_sort_change(sort_order):
    # Function to handle sort order change
    if sort_order == "Most Recent First":
        sorted_results = sorted(stored_results, key=lambda x: x[3].seconds, reverse=True)
    elif sort_order == "Oldest First":
        sorted_results = sorted(stored_results, key=lambda x: x[3].seconds)
    else:
        sorted_results = sorted(stored_results, key=lambda x: x[4], reverse=True)

    return display_html_output(sorted_results)

def display_html_output(results):
    html_output = "<div style='display: grid; grid-template-rows: auto; grid-auto-flow: row; gap: 10px; overflow-x: auto;'>"
    for url, title, text, published_on, similarity in results:
        card = f"""
        <div style='border: 1px solid #ddd; border-radius: 10px; padding: 10px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); min-width: 300px;'>
            <a href='{url}' target='_blank' style='text-decoration: none; color: black;'>
                <h4>{title}</h4>
            </a>
            <p style='font-size: small; color: grey;'>{datetime.fromtimestamp(published_on.seconds).strftime('%b. %d, %Y %I:%M %p ET')}</p>
            <p>{text}</p>
        </div>
        """
        html_output += card
    html_output += "</div>"
    
    return html_output

def display_results(model_radio, input_text, start_date, end_date, summarize_articles, num_matches, sort_order):
    results = retrieval_request(model_radio, input_text, start_date, end_date, summarize_articles, num_matches)
    
    return update_output_on_sort_change(results)

with gr.Blocks() as demo:
    gr.Markdown("<h2 style='text-align: center;'>RAG Demo Interface</h2>")
    with gr.Row():
        model_radio = gr.Radio(["base", "large", "xl"], label="Which retrieval model would you like to choose?", value="large", scale=4)
        summary_checkbox = gr.Checkbox(label="Summarize articles (takes time to load)", scale=2)
        num_matches = gr.Dropdown(choices=[1, 2, 5, 10, 15, 25, 50], value=5, interactive=True, label="Number of articles", scale=2)
        sort_order = gr.Dropdown(choices=["Best Match", "Most Recent First", "Oldest First"], value="Best Match", interactive=True, label="Sort Order", scale=2)
    with gr.Row():
        text_input = gr.Textbox(lines=2, label="Retrieval Text", placeholder="Enter text here...", scale=4)
        start_date = Calendar(type="datetime", label="Start Date", scale=1, value="2023-11-24"),
        end_date = Calendar(type="datetime", label="End Date", scale=1, value="2023-11-30"),
    submit_button = gr.Button("Submit")
    output_html = gr.HTML()

    sort_order.input(fn=update_output_on_sort_change, inputs=sort_order, outputs=output_html)

    submit_button.click(fn=display_results, inputs=[model_radio, text_input, start_date[0], end_date[0], summary_checkbox, num_matches, sort_order], outputs=output_html)

demo.launch()

# I am interested in investing in us treasury bonds which are risk free over long term, for example bonds that are greater than 10 years. Show me necessary maro economic trends and SOFR rates.
