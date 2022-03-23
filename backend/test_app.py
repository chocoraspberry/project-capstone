import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class CastingTestCase(unittest.TestCase):
    def setUp(self):
        self.assist_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IllSdl9LbDRwd1diSDJfMHpWLWphQyJ9.eyJpc3MiOiJodHRwczovL3UtY2FzdGluZy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjIzN2VmNWM0ODgzY2EwMDY5Y2ZhNjE4IiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNjQ3OTkyOTc4LCJleHAiOjE2NDgwNzkzNzgsImF6cCI6ImJqeW1IS2FOcDE4eFdLa1duU0tITHRlRDZkbWd0dWFvIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.l595MriIe6GXekruAxx2EcmtELEyWONj2AYIzE2hqGw37WckIFL_TdBIOWKVgGK1EZkmj3vqRlQehgPEPRdFiGgPAaR995h_qyPcODeO2BjX6eWydPUTzNVJxz5oUouThPX-BsnxErjbsMsNP9CLAlcY3oU7orxMsQd1M-2vTTczk7ee98RMN5fMr69v91X35QTTW_8B51yt4c32pFo3Yglc5pzfthtkxCpMrgB4xh7PAjuk36gv_BIyeRzE0mbkJmkjhvrRK92tTySeVcBUFjNsR6G8ZxKnemCUBxq2Gl3ykOzL575gh6pM4Ldj8fExB5FeZhTRc-Lp-jp4cg5F3g'
        self.director_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IllSdl9LbDRwd1diSDJfMHpWLWphQyJ9.eyJpc3MiOiJodHRwczovL3UtY2FzdGluZy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjIzN2VmZDUwZjRiOTIwMDY5MjQzNTkxIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNjQ3OTkyODg1LCJleHAiOjE2NDgwNzkyODUsImF6cCI6ImJqeW1IS2FOcDE4eFdLa1duU0tITHRlRDZkbWd0dWFvIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.Gt-EiUAYvw-KnMpuZLpPn95x2eidqPSv2gz7DGycPqY4H1WMMbq5qy-L_wpwWxF2tc3dF_CVchRg7X7p727WAqfdo_fjx_ygvzR8cbs_mC47lUKoH_w-_MWS8OiI9skSg0aepqd2XAAl278EKx81fyEPIuxXYlOC1hGjT9u9FKK1iwPxlIADKoexJydiHaVG4VFswyos4JJSqNY-aqPRjlBY3ljUygEjILT183wwPFv1OaPzoOG45iPBeNpvMhgkGJG6h2HFIbfr6wlrRGM0xmuZ9j9q6RiawgWIy80tYx96ZYAQ2P0JqgJDzU8t_Iemyx2_uu7mQOYqFXG2fuow6g'
        self.executive_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IllSdl9LbDRwd1diSDJfMHpWLWphQyJ9.eyJpc3MiOiJodHRwczovL3UtY2FzdGluZy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjIzN2YzMjU0ODgzY2EwMDY5Y2ZhNmM0IiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNjQ3OTg5MzMxLCJleHAiOjE2NDgwNzU3MzEsImF6cCI6ImJqeW1IS2FOcDE4eFdLa1duU0tITHRlRDZkbWd0dWFvIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.0Uk4ShJcaTHSfKloh_WFg0_yp9OImtVi1vI-hNB78HxwTmWZtaOZODqpsZAD6YMUvnKbz6ikNyD74LOpYcethoaitLIH8F_2gpEbTqI5sO1UhRa-xgES3KoNzJ_Izx2iZy94eKrAhTk72ji0xTRXF_SkBpIsjp5nGiSheCPEk8u-P8KcmwcnJoH2vwSJHiPpTjQQh4NKTQSSydrUhh2B-w6HJ4KZ4ixXo66VBqnLTcYzeVAd22zhdvYgfX1TpQpDfG3BlG1vUz2eOMFJuZ13UdZ7BTATTBvMsZJ6dnP33rj9fvx8RVCFitSEMbV7mbYvden4DrlmKT9VYnEKHz-Tzg'
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    # test GET requests for movies

    def test_get_movies(self):
        res = self.client().get(
            '/movies',
            headers={
                "Authorization": f"Bearer {self.director_token}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))
        self.assertTrue(data['total_movies'])

    def test_404_movie_beyond_page(self):
        res = self.client().get('/movies?page=10000',
                                headers={"Authorization": f"Bearer {self.director_token}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_get_movies_no_token(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(
            data['description'],
            'Authorization header is expected.')

    # test DELETE a movie using movie ID

    def test_delete_movie_success(self):
        res = self.client().delete('/movies/10',
                                   headers={"Authorization": f"Bearer {self.executive_token}"})
        data = json.loads(res.data)

        item = Movie.query.filter(Movie.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_movie_does_not_exist(self):
        res = self.client().delete('/movies/10000',
                                   headers={"Authorization": f"Bearer {self.executive_token}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_movie_unauthorized(self):
        res = self.client().delete('/movies/9',
                                   headers={"Authorization": f"Bearer {self.director_token}"})
        data = json.loads(res.data)

        item = Movie.query.filter(Movie.id == 9).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # test POST a new movie

    def test_create_movie_success(self):
        res = self.client().post(
            '/movies',
            json={
                "title": "marry me",
                "release_date": "2011-09-22"},
            headers={
                "Authorization": f"Bearer {self.executive_token}"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_create_not_allowed(self):
        res = self.client().post(
            '/movies/3',
            json={
                "title": "luca",
                "release_date": "2012-09-22"},
            headers={
                "Authorization": f"Bearer {self.executive_token}"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_create_movie_unauthorized(self):
        res = self.client().post(
            '/movies',
            json={
                "title": "spiderman",
                "release_date": "2008-09-22"},
            headers={
                "Authorization": f"Bearer {self.assist_token}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # test update a movie

    def test_update_movie_success(self):
        res = self.client().patch(
            '/movies/5',
            json={
                "release_date": "1900-09-22"},
            headers={
                "Authorization": f"Bearer {self.director_token}"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_movie_does_not_exist(self):
        res = self.client().patch(
            '/movies/100000',
            json={
                "release_date": "2011-09-22"},
            headers={
                "Authorization": f"Bearer {self.director_token}"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_movie_unauthorized(self):
        res = self.client().patch(
            '/movies/15',
            json={
                "release_date": "1999-09-22"},
            headers={
                "Authorization": f"Bearer {self.assist_token}"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

  # test GET requests for actors

    def test_get_actors(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": f"Bearer {self.assist_token}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        self.assertTrue(data['total_actors'])

    def test_404_actor_beyond_page(self):
        res = self.client().get('/actors?page=10000',
                                headers={"Authorization": f"Bearer {self.assist_token}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_get_actors_no_token(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(
            data['description'],
            'Authorization header is expected.')

    # test DELETE an actor using actor ID

    def test_delete_actor_success(self):
        res = self.client().delete('/actors/1',
                                   headers={"Authorization": f"Bearer {self.executive_token}"})
        data = json.loads(res.data)

        item = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_actor_does_not_exist(self):
        res = self.client().delete('/actors/10000',
                                   headers={"Authorization": f"Bearer {self.executive_token}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_actor_unauthorized(self):
        res = self.client().delete('/actors/34',
                                   headers={"Authorization": f"Bearer {self.assist_token}"})
        data = json.loads(res.data)

        item = Actor.query.filter(Actor.id == 34).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # test POST a new actor

    def test_create_actor_success(self):
        res = self.client().post(
            '/actors',
            json={
                "name": "Sheldon Cooper",
                "age": "38",
                "gender": "male"},
            headers={
                "Authorization": f"Bearer {self.director_token}"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_create_not_allowed(self):
        res = self.client().post(
            '/actors/43',
            json={
                "name": "Leonard Dip",
                "age": "48",
                "gender": "male"},
            headers={
                "Authorization": f"Bearer {self.director_token}"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_create_actor_unauthorized(self):
        res = self.client().post(
            '/actors',
            json={
                "name": "Leonard Dip",
                "age": "48",
                "gender": "male"},
            headers={
                "Authorization": f"Bearer {self.assist_token}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # test update an actor

    def test_update_actor_success(self):
        res = self.client().patch(
            '/actors/36',
            json={
                "gender": "male"},
            headers={
                "Authorization": f"Bearer {self.executive_token}"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_actor_does_not_exist(self):
        res = self.client().patch(
            '/actors/100000',
            json={
                "gender": "female"},
            headers={
                "Authorization": f"Bearer {self.director_token}"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_actor_unauthorized(self):
        res = self.client().patch(
            '/actors/44',
            json={
                "gender": "female"},
            headers={
                "Authorization": f"Bearer {self.assist_token}"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


# # fengexia
#     def test_get_actors(self):
#         res = self.client().get('/actors')
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertTrue(len(data['actors']))
#         self.assertTrue(data['total_actors'])


#     def test_404_actor_beyond_page(self):
#         res = self.client().get('/actors?page=10000')
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'not found')

#     # test DELETE an actor using actor ID
#     def test_delete_actor(self):
#         res = self.client().delete('/actors/40')
#         data = json.loads(res.data)

#         item = Actor.query.filter(Actor.id == 40).one_or_none()

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)

#     def test_422_actor_does_not_exist(self):
#         res = self.client().delete('/actors/10000')
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 422)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'unprocessable')

#     # test POST a new actor
#     def test_create_actor(self):
#         res = self.client().post(
#             '/actors',
#             json={
#                 "name": "Jlo",
#                 "age": "52",
#                 "gender": "female"})
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)

#     def test_405_create_not_allowed(self):
#         res = self.client().post(
#             '/actors/1',
#             json={
#                 "name": "Jlo",
#                 "age": "52",
#                 "gender": "female"})
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 405)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'method not allowed')

#     # test update an actor
#     def test_update_actor(self):
#         res = self.client().patch(
#             '/actors/34',
#             json={
#                 "gender": "female"})
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)

#     def test_422_actor_does_not_exist(self):
#         res = self.client().patch(
#             '/actors/100000',
#             json={
#                 "gender": "female"})
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 422)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'unprocessable')

#     # test the RBAC-casting director
#     def test_casting_director__403_unauthorized(self):
#         casting_director_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IllSdl9LbDRwd1diSDJfMHpWLWphQyJ9.eyJpc3MiOiJodHRwczovL3UtY2FzdGluZy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjIzN2VmZDUwZjRiOTIwMDY5MjQzNTkxIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNjQ3OTAwNjQxLCJleHAiOjE2NDc5ODcwNDEsImF6cCI6ImJqeW1IS2FOcDE4eFdLa1duU0tITHRlRDZkbWd0dWFvIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.simTY4db18ERMgJNR7HqKuuiklhVpgQ_HmdcJbAYfzL-hI7sNRTP2H2HWpgYye-0MKAhN3DCjLxriiLGh-l_PgM47wP6JkuCgYvj5OBmD_ay0ATjznu7JzTFAX79nfUtGGpWgcEmMAn2z0IhfEbX1s7WoT5mvkkDPulQrPL16wpcQ-gLuRgsPXaOm8lI5EFTUa6ZcLJxDe3gi8U2m6_hSO-TOa2V9MkQHnH8A6QcN_336fWnlI-xJNETc_ibbJFG0BbhZIb7_UoqOFmKXkA63IQtSqK0edT-5Fy8YhsSrMZCD67tX4aD9beBypFadjkYo27qaaEvURH0T4h-PbfF-g"
#         res = self.client().post('/actors',
#         json={
#                 "name": "Big Mouth",
#                 "age": "23",
#                 "gender": "male"},
#         headers={
#             "Authorization" : f"Bearer {self.casting_director_token}"

#         })
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 403)
#         self.assertEqual(data['code'], 'unauthorized')
#         self.assertEqual(data['description'], 'Permission not found.')
#     def test_casting_director(self):
#         casting_director_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IllSdl9LbDRwd1diSDJfMHpWLWphQyJ9.eyJpc3MiOiJodHRwczovL3UtY2FzdGluZy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjIzN2VmZDUwZjRiOTIwMDY5MjQzNTkxIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNjQ3OTAwNjQxLCJleHAiOjE2NDc5ODcwNDEsImF6cCI6ImJqeW1IS2FOcDE4eFdLa1duU0tITHRlRDZkbWd0dWFvIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.simTY4db18ERMgJNR7HqKuuiklhVpgQ_HmdcJbAYfzL-hI7sNRTP2H2HWpgYye-0MKAhN3DCjLxriiLGh-l_PgM47wP6JkuCgYvj5OBmD_ay0ATjznu7JzTFAX79nfUtGGpWgcEmMAn2z0IhfEbX1s7WoT5mvkkDPulQrPL16wpcQ-gLuRgsPXaOm8lI5EFTUa6ZcLJxDe3gi8U2m6_hSO-TOa2V9MkQHnH8A6QcN_336fWnlI-xJNETc_ibbJFG0BbhZIb7_UoqOFmKXkA63IQtSqK0edT-5Fy8YhsSrMZCD67tX4aD9beBypFadjkYo27qaaEvURH0T4h-PbfF-g"
#         res = self.client().post('/movies',
#         json={
#                 "release_date": "1998-03-01",
#                 "title": "Lucifa"},
#         headers={
#             "Authorization" : f"Bearer {self.casting_director_token}"
#         })
#         data = json.loads(res.data)
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
