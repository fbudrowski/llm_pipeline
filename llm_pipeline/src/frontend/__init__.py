import time
from datetime import datetime

from prometheus_client import Counter, Histogram, generate_latest
from quart import g, Quart, request

from backend.celery_config import celery

app = Quart(__name__)

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP Request Latency', ['method', 'endpoint'])

@app.route('/prompts', methods=['POST'])
async def submit():
    data = await request.get_json()
    prompts_list = data.get('prompts')
    prompts = tuple(prompts_list)
    print(f"Prompts: {prompts}")
    if not prompts or len(prompts) == 0:
        return {'status': 'error', 'message': 'No prompts provided'}, 400

    task = celery.tasks['batch_processing'].apply_async(args=(prompts,))

    result = task.get(timeout=40)
    # the below is far from ideal
    csv_result = ','.join([r.replace(',', '\,') for r in result])
    # write csv result to a timestamped file
    with open(f"/tmp/results_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv", 'w') as f:
        f.write(csv_result)
    return {'status': 'Data processed', 'result': result}

@app.route('/metrics')
def metrics():
    return generate_latest()

@app.route('/test')
def test():
    return "abcd"


@app.before_request
async def before_requet():
    g.start_time = time.time()

@app.after_request
async def after_request(response):
    request_latency = time.time() - g.start_time
    REQUEST_LATENCY.labels(request.method, request.path).observe(request_latency)
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response


if __name__ == '__main__':
    app.run(threading=True, port=8000)
