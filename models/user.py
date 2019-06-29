#!/usr/bin/python3
"""module for User class"""


from models.base_model import BaseModel


class User (BaseModel):
    """class for storing user data"""
    email = ''
    password = ''
    first_name = ''
    last_name = ''
