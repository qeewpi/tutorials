# -*- coding: utf-8 -*-

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(
        "Sequence", default=10, help="Used to order property types"
    )
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Property type name must be unique.")
    ]

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)


class EstatePropertyTypeLine(models.Model):
    _name = "estate.property.type.line"
    _description = "Real Estate Property Type Line"

    property_type_id = fields.Many2one("estate.property.type")
    name = fields.Char()
    expected_price = fields.Float()
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
        copy=False,
    )
