#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging.config

import falcon

import messages
import middlewares
from falcon_multipart.middleware import MultipartMiddleware
from settings import configure_logging
from resources import account_resources, common_resources, user_resources, event_resources,tasques_resources

# LOGGING
mylogger = logging.getLogger(__name__)
configure_logging()


# DEFAULT 404
# noinspection PyUnusedLocal
def handle_404(req, resp):
    resp.media = messages.resource_not_found
    resp.status = falcon.HTTP_404


# FALCON
app = application = falcon.API(
    middleware=[
        middlewares.DBSessionManager(),
        middlewares.Falconi18n(),
        MultipartMiddleware()
    ]
)
application.add_route("/", common_resources.ResourceHome())
'''
application.add_route("/account/profile", account_resources.ResourceAccountUserProfile())
application.add_route("/account/profile/update_profile_image", account_resources.ResourceAccountUpdateProfileImage())
application.add_route("/account/create_token", account_resources.ResourceCreateUserToken())
application.add_route("/account/delete_token", account_resources.ResourceDeleteUserToken())

application.add_route("/users/register", user_resources.ResourceRegisterUser())
application.add_route("/users/show/{username}", user_resources.ResourceGetUserProfile())

application.add_route("/events", event_resources.ResourceGetEvents())
application.add_route("/events/show/{id:int}", event_resources.ResourceGetEvent())
'''


'''
#CRUD
application.add_route("/books/register", book_resources.ResourceCreateBook()) #POST
application.add_route("/books/show", book_resources.ResourceFindBookById()) #GET
application.add_route("/books/update", book_resources.ResourceUpdateBook()) #UPDATE
application.add_route("/books/delete", book_resources.ResourceDeleteBook()) #DELETE

#LIST
application.add_route("/books", book_resources.ResourceGetBook()) #DELETE
application.add_route("/books/advance", book_resources.ResourceGetBookAdvance()) #DELETE
'''
#EXAMEN
application.add_route("/tasks/register", book_resources.ResourceCreateTask()) #POST



application.add_sink(handle_404, "")
