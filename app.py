from flask import Flask, request, jsonify
from pymongo import MongoClient

import secrets

app = Flask(__name__)
client = MongoClient('mongodb+srv://arvi7894:arvi7894@cluster0.26i7ymj.mongodb.net/intern')
db = client['intern']



# here  api to create a tasks
@app.route('/api/tasks', methods=['POST'])
def create_task():
    task_data = request.get_json()
    title = task_data['title']
    description = task_data['description']
    due_date = task_data['due_date']
    status = task_data['status']

    task_id = secrets.token_hex(3).upper()

    task = {
       
        '_id': task_id,
        'title': title,
        'description': description,
        'due_date': due_date,
        'status': status
    }

    db['tasks'].insert_one(task)

    return jsonify( message="Tasks created successfully!",statuscode=200 , errormessage = "", data = [task]), 201






# here api to get single task with uniqui task_id
@app.route('/api/getsingle/task', methods=['GET'])
def get_task():
    task_id = request.args.get('task_id')
    if task_id:
        task =db['tasks'].find_one({'_id': task_id})
        if task:
            task['_id'] = str(task['_id']) 
            return jsonify( message="Task found successfully!",statuscode=200 , errormessage = "", data = [task]), 201
        return jsonify( message=" ",statuscode=404 , errormessage = "Task not found! ", data = []), 404
    return jsonify( message=" ",statuscode=400 , errormessage = "Task ID not provided ", data = []), 400




# Hare update api with uniqui task_id 
@app.route('/api/update/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = db['tasks'].find_one({'_id': task_id})

    if not task:
        return jsonify( message=" ",statuscode=404 , errormessage = "Task not found! ", data = []), 404

    task_data = request.get_json()
    updated_task = {
        'title': task_data.get('title', task['title']),
        'description': task_data.get('description', task['description']),
        'due_date': task_data.get('due_date', task['due_date']),
        'status': task_data.get('status', task['status'])
    }

    db['tasks'].update_one({'_id': task_id}, {'$set': updated_task})

    return jsonify( message="Task updated successfully!",statuscode=200 , errormessage = "", data = []), 200





# Here delete api with a uniqui task_Id

@app.route('/api/delete/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = db['tasks'].delete_one({'_id': task_id})

    if result.deleted_count == 0:
        return jsonify( message=" ",statuscode=404 , errormessage = "Task not found! ", data = []), 404

    return jsonify( message="Task deleted successfully!",statuscode=200 , errormessage = "", data = []), 200




# Here api is List of all task with pagination

@app.route('/api/all/tasks', methods=['GET'])
def get_all_tasks():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    skip = (page - 1) * limit

    tasks = list(db['tasks'].find().skip(skip).limit(limit))
    total_tasks = db['tasks'].count_documents({})

    return jsonify({
        'tasks': tasks,
        'total_tasks': total_tasks,
        'page': page,
        'limit': limit
    }), 200

if __name__ == '__main__':
    app.run(debug=True)



