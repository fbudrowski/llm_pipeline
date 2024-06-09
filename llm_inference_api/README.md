To test the first version, open three terminals, and `cd llm_inference_api` in all. Do the following in terminal 1:
```bash
poetry run hypercorn frontend -w 2
```

In terminal 2, do the following:
```bash
poetry run celery -A backend.celery_config worker --loglevel=info
```

In terminal 3, do the following:
```bash
curl -X POST http://localhost:5005/prompts --json '{"prompts":["prompt1","prompt2","prompt3","prompt4","prompt5","prompt6","prompt7","prompt8","prompt9","prompt10"]}'
```

