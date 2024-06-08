# from quart import Quart, request, jsonify
# import asyncio
# from queue import Queue
# from threading import Thread
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch
#
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
#
# # Load model and tokenizer
# model_name = "Qwen/Qwen2-1.5B-Instruct"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)
#
# # Queue to hold incoming requests
# request_queue = Queue()
#
#
# # Function to process batch of requests
# async def process_requests():
#     while True:
#         batch = []
#         while not request_queue.empty() and len(batch) < 1:  # Batch size of 8
#             batch.append(request_queue.get())
#
#         if batch:
#             texts = [req['text'] for req in batch]
#             inputs = tokenizer(texts, return_tensors="pt", padding=True)
#             with torch.no_grad():
#                 outputs = model(**inputs)
#
#             # Process the outputs
#             scores = outputs.logits.softmax(dim=-1).tolist()
#             for req, score in zip(batch, scores):
#                 req['future'].set_result(score)
#
#         await asyncio.sleep(0.1)  # Adjust sleep time as needed
#
#
# # Start background thread for processing requests
# def start_background_loop(loop):
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(process_requests())
#
#
# new_loop = asyncio.new_event_loop()
# t = Thread(target=start_background_loop, args=(new_loop,), daemon=True)
# t.start()
#
#
# @app.route('/predict', methods=['POST'])
# async def predict():
#     data = await request.get_json()
#     if 'text' not in data:
#         return jsonify({"error": "No text provided"}), 400
#
#     future = asyncio.get_event_loop().create_future()
#     response_holder = {'text': data['text'], 'future': future}
#     request_queue.put(response_holder)
#
#     result = await future
#     return jsonify({"result": result})
#
# @app.route('/hello', methods=['GET'])
# async def hello():
#     return 'hello'
#
# @app.post("/echo")
# async def echo():
#     data = await request.get_json()
#     return {"input": data, "extra": True}
#
#
#
# app = Quart(__name__)
# if __name__ == '__main__':
#     app.run(debug=True, port=5005)