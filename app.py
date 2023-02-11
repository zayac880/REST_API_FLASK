# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()

class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()

class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()

# schemas
movie_schema = MovieSchema()
director_schema = DirectorSchema()
genre_schema = GenreSchema()


# namespace
api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')

# Movies
@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        stmt = Movie.query
        if director_id:
            stmt = stmt.filter(Movie.director_id == director_id)
        if genre_id:
            stmt = stmt.filter(Movie.genre_id == genre_id)
        movies = stmt.all()
        return movie_schema.dump(movies, many=True), 200

    def post(self):
        movie_data = request.json
        new_movie = Movie(**movie_data)
        db.session.add(new_movie)
        db.session.commit()
        return '', 201



@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            return '', 404
        return movie_schema.dump(movie), 200

    def put(self, mid: int):
        movie = Movie.query.get(mid)

        if not movie:
            return '', 404

        movie_data = request.json

        movie.title = movie_data.get('title')
        movie.description = movie_data.get('description')
        movie.trailer = movie_data.get('trailer')
        movie.year = movie_data.get('year')
        movie.rating = movie_data.get('rating')
        movie.genre_id = movie_data.get('genre_id')
        movie.director_id = movie_data.get('director_id')

        db.session.add(movie)
        db.session.commit()
        return '', 204

    def delete(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            return '', 204
        db.session.delete(movie)
        db.session.commit()


# Directors
@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return director_schema.dump(directors, many=True), 200

    def post(self):
        director_data = request.json
        new_director = Director(**director_data)
        db.session.add(new_director)
        db.session.commit()
        return '', 201



@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did: int):
        director = Director.query.get(did)
        if not director:
            return '', 404
        return director_schema.dump(director), 200

    def put(self, did: int):
        director = Director.query.get(did)

        if not director:
            return '', 404

        director_data = request.json

        director.name = director_data.get('name')

        db.session.add(director)
        db.session.commit()
        return '', 204

    def delete(self, did: int):
        director = Director.query.get(did)
        if not director:
            return '', 404
        db.session.delete(director)
        db.session.commit()
        return '', 204


# Genres
@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = Genre.query.all()
        return genre_schema.dump(genres, many=True), 200

    def post(self):
        genre_data = request.json
        new_genre = Genre(**genre_data)
        db.session.add(new_genre)
        db.session.commit()
        return '', 201



@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid: int):
        genre = Genre.query.get(gid)
        if not genre:
            return '', 404
        return genre_schema.dump(genre), 200

    def put(self, gid: int):
        genre = Genre.query.get(gid)

        if not genre:
            return '', 404

        genre_data = request.json

        genre.name = genre_data.get('name')

        db.session.add(genre)
        db.session.commit()
        return '', 204

    def delete(self, gid: int):
        genre = Genre.query.get(gid)
        if not genre:
            return '', 404
        db.session.delete(genre)
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)
