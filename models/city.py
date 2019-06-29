#!/usr/bin/python3
"""module for city class"""


from models.base_model import BaseModel


class City (BaseModel):
    """class for stoing US city information"""

    state_id = ''
    name = ''
