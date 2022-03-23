import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS
import json
from models import setup_db, Movie, Actor, db
from auth import AuthError, requires_auth
from flask_migrate import Migrate

ITEM_PER_PAGE = 10


def paginate_items(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEM_PER_PAGE
    end = start + ITEM_PER_PAGE

    items = [item.format() for item in selection]
    current_items = items[start:end]

    return current_items


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PUT, POST, DELETE, PATCH, OPTIONS')

        return response

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        selection = Movie.query.order_by('id').all()
        current_movies = paginate_items(request, selection)

        if len(current_movies) == 0:
            # not found
            abort(404)

        return jsonify({
            'success': True,
            'movies': current_movies,
            'total_movies': len(Movie.query.all()),
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        item = Movie.query.get(movie_id)

        if item is None:
            # unprocessable
            abort(422)

        item.delete()

        return jsonify({
            'success': True,
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json(force=True)

        title = body["title"]
        release_date = body["release_date"]
        try:
            movie = Movie(title=title, release_date=release_date)
            movie.insert()

            return jsonify({
                'success': True,
            })
        except BaseException:
            abort(405)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        try:
            body = request.get_json()
            movie = Movie.query.get(movie_id)

            if movie is None:
              # unprocessable
                abort(422)

            if 'title' in body:
                movie.title = body['title']
            movie.update()

            if 'release_date' in body:
                movie.release_date = body['release_date']
            movie.update()

            return jsonify({
                'success': True,
            })
        except BaseException:
            abort(422)

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        selection = Actor.query.order_by('id').all()
        current_actors = paginate_items(request, selection)

        if len(current_actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': current_actors,
            'total_actors': len(Actor.query.all()),
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        item = Actor.query.get(actor_id)

        if item is None:
            abort(422)

        item.delete()

        return jsonify({
            'success': True,
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        try:
            body = request.get_json(force=True)

            new_name = body["name"]
            new_age = body["age"]
            new_gender = body["gender"]

            actor = Actor(name=new_name, age=new_age, gender=new_gender)
            actor.insert()

            return jsonify({
                'success': True,
            })
        except BaseException:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        try:
            body = request.get_json()
            actor = Actor.query.get(actor_id)

            if actor is None:
                abort(422)

            if 'name' in body:
                actor.name = body["name"]

            if 'age' in body:
                actor.age = body["age"]

            if 'gender' in body:
                actor.gender = body["gender"]

            actor.update()

            return jsonify({
                'success': True,
            })
        except BaseException:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not found',
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable',
        }), 422

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed',
        }), 405

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    # APP.run(host='0.0.0.0', port=8080, debug=True)
    app.debug = True
    app.run()
