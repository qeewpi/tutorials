# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Users(models.Model):
    _name = "res.users"
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "user_id",
        string="Properties",
        domain=[
            "|",
            ("state", "=", "offer_accepted"),
            ("state", "=", "new"),
        ],
    )
