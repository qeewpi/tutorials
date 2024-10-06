# -*- coding: utf-8 -*-

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Property tag name must be unique.")
    ]
