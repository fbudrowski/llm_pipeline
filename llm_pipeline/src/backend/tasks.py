import torch.cuda
from celery import Task
from transformers import AutoTokenizer, AutoModelForCausalLM

batch_data = []
# batch_size = 4


class BatchProcessing(Task):
    name = 'batch_processing'
    def __init__(self):
        self.device = None
        self.tokenizer = None
        self.model = None
        self._initialized = False

    def run(self, data_batch: list[str]):
        if not self._initialized:
            self.device = "cuda" if torch.cuda.is_available() else 'cpu'
            self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-1.5B-Instruct")
            self.model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2-1.5B-Instruct").to(self.device)
            self._initialized = True

        print(f"Got data {data_batch}")

        prompts = data_batch

        inputs = self.tokenizer(prompts, return_tensors="pt", padding=True, truncation=True).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=15)

        responses = tuple(self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs)

        print(f"Result: {responses}")
        return responses

