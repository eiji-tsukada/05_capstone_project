import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
      response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization,true')
      response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,PATCH,POST,DELETE,OPTIONS')
      return response


    # API Endpoints
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_all_movies(payload):
        selection = Movie.query.order_by(Movie.id).all()
        if len(selection) == 0:
            abort(404)
        
        movies = [movie.format() for movie in selection]
        
        return jsonify({
            'success': True,
            'movies': {
                movie['id']: movie['title'] for movie in movies
            }
        }), 200

    
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        if (new_title is None) or (new_release_date is None):
            abort(422)

        try:
            movie = Movie(
                title=new_title,
                release_date=new_release_date
            )
            movie.insert()

            return jsonify({
                'success': True,
                'created': movie.id,
                'movie': movie.format()
            }), 200

        except:
            abort(422)


    @app.route('/movies/<int:movies_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(paylpad, movie_id):
        try:
            movie = Movie.query.filter_by(id=movie_id).one_or_none()
            if movie is None:
                abort(404)

            body = request.get_json()
            title = body.get('title', None)
            release_date = body.get('release_date', None)

            if title is not None:
                movie.title = title
            if release_date is not None:
                movie.release_date = release_date

            movie.update()

            return jsonify({
                'success': True,
                'updated': movie.id,
                'movie': movie.format()
            }), 200

        except:
            abort(422)


    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        try:
            movie = Movie.query.filter_by(id=movie_id).one_or_none()
            if movie is None:
                abort(404)
            else:
                movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie_id
            }), 200

        except:
            abort(422)

    
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_all_actors(payload):
        selection = Actor.query.order_by(Actor.id).all()
        if len(selection) == 0:
            abort(404)
        
        actors = [actor.format() for actor in selection]

        return jsonify({
            'success': True,
            'actors': {
                actor['id']: actor['name'] for actor in actors
            }
        }), 200


    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        if (new_name is None) or\
            (new_age is None) or\
            (new_gender is None):
            abort(422)

        try:
            actor = Actor(
                name=new_name,
                age=new_age,
                gender=new_gender
            )
            actor.insert()

            return jsonify({
                'success': True,
                'created': actor.id,
                'actor': actor.format()
            }), 200

        except:
            abort(422)


    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(payload, actor_id):
        try:
            actor = Actor.query.filter_by(id=actor_id).one_or_none()
            if actor is None:
                abort(404)

            body = request.get_json()
            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)

            if name is not None:
                actor.name = name
            if age is not None:
                actor.age = age
            if gender is not None:
                actor.gender = gender

            actor.update()

            return jsonify({
                'success': True,
                'updated': actor.id,
                'actor': actor.format()
            }), 200

        except:
            abort(422)


    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        try:
            actor = Actor.query.filter_by(id=actor_id).one_or_none()
            if actor is None:
                abort(404)
            else:
                actor.delete()

            return jsonify({
                'success': True,
                'deleted': actor_id
            }), 200

        except:
            abort(422)


    # Error Handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400


    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'unauthorized'
        }), 401


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    
    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify({
            'success': False,
            'error': e.status_code,
            'message': e.error['description']
        }), e.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
