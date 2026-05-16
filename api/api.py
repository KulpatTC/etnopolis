import json
import os.path

import flask
from flask import jsonify

from ..data import db_session
from ..data.tasks import Task
from ..data.tags import Tag

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='templates'
)


def load_nations():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'nations.json')
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def load_events():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'events.json')
    with open(path, encoding='utf-8') as f:
        return json.load(f)


@blueprint.route('/api/tasks')
def get_tasks():
    db_sess = db_session.create_session()
    tasks = db_sess.query(Task).all()
    tasks_returning = []
    for el in tasks:
        tasks_returning.append({
            "id": el.id,
            "question": el.question,
            "answer 1": el.answer1,
            "answer 2": el.answer2,
            "answer 3": el.answer3,
            "correct answer": el.correct,
            "creator": el.user_id,
            "tag": el.tag_id
        })
    return jsonify(tasks_returning)


@blueprint.route('/api/tasks/<int:id>')
def get_task_by_id(id):
    db_sess = db_session.create_session()
    task = db_sess.query(Task).get(id)
    if not task:
        return jsonify({"error": "task not found"}), 404
    return jsonify({
        "id": task.id,
        "question": task.question,
        "answer 1": task.answer1,
        "answer 2": task.answer2,
        "answer 3": task.answer3,
        "correct answer": task.correct,
        "creator": task.user_id,
        "tag": task.tag_id
    })


@blueprint.route('/api/tags')
def get_tags():
    db_sess = db_session.create_session()
    tags = db_sess.query(Tag).all()
    tags_returning = []
    for el in tags:
        tags_returning.append({
            "id": el.id,
            "tag": el.title
        })
    return jsonify(tags_returning)


@blueprint.route("/api/tags/<int:id>")
def get_tag_by_id(id):
    db_sess = db_session.create_session()
    tag = db_sess.query(Tag).get(id)
    if not tag:
        return jsonify({"error": "Tag not found"}), 404
    return jsonify({
        "id": tag.id,
        "tag": tag.title
    })


@blueprint.route('/api/nations')
def get_nations():
    return jsonify(load_nations())


@blueprint.route('/api/nations/by-name/<name>')
def get_nation_by_name(name):
    perfect_name = name.strip().lower().capitalize()
    nations = load_nations()
    nation = next((i for i in nations if i["name"] == perfect_name), None)
    if not nation:
        return jsonify({"error": "No nations with this name"}), 404
    return jsonify(nation)


@blueprint.route('/api/nations/<int:id>')
def get_nation_by_id(id):
    nations = load_nations()
    nation = next((i for i in nations if i["id"] == id), None)
    if not nation:
        return jsonify({"error": "No nations with this id"}), 404
    return jsonify(nation)


@blueprint.route('/api/events')
def get_events():
    return jsonify(load_events())


@blueprint.route('/api/events/<city>')
def get_event_by_city(city):
    perfect_city = city.strip().lower().capitalize()
    events = load_events()
    events_in_city = [i for i in events if i["city"] == perfect_city]
    if not events_in_city:
        return jsonify({"error": "No events in this city"}), 404
    return jsonify(events_in_city)
