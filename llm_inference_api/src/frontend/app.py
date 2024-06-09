# from datetime import datetime
#
# from quart import Quart, request
# from backend.tasks import collect_data
#
# app = Quart(__name__)
#
#
# @app.route('/prompts', methods=['POST'])
# async def submit():
#     data = await request.get_json()
#     prompts_list = data.get('prompts')
#     prompts = tuple(prompts_list)
#     print(f"Prompts: {prompts}")
#     if not prompts or len(prompts) == 0:
#         return {'status': 'error', 'message': 'No prompts provided'}, 400
#
#     task = collect_data.apply_async(args=(prompts,))
#
#     # Wait for the task to complete and get the result
#     result = task.get(timeout=10)
#     csv_result = ','.join([r.replace(',', '\,') for r in result])
#     # write csv result to a timestamped file
#     with open(f"/tmp/results_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv", 'w') as f:
#         f.write(csv_result)
#     return {'status': 'Data processed', 'result': result}
#
#
# if __name__ == '__main__':
#     app.run(threading=True, port=5005)
