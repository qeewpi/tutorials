# -*- coding: utf-8 -*-

from odoo import fields, models, api, tools
from datetime import datetime
from dateutil import relativedelta
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=datetime.today() + relativedelta.relativedelta(months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
    active = fields.Boolean(default=True)
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
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area")

    _sql_constraints = [
        (
            "positive_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be positive and greater than zero.",
        ),
        (
            "positive_selling_price",
            "CHECK(selling_price > 0)",
            "The selling price must be positive and greater than zero.",
        ),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = (
                record.offer_ids and max(record.offer_ids.mapped("price")) or 0
            )

    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = "north"

    def action_mark_sold(self):
        for record in self:
            if self.state == "canceled":
                raise UserError("Canceled properties cannot be sold.")
            else:
                self.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if self.state == "sold":
                raise UserError("Sold properties cannot be canceled.")
            else:
                self.state = "canceled"
                self.offer_ids.write({"status": "refused"})
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        SELLING_PRICE_THRESHOLD = 0.9
        for record in self:
            if record.state == "offer_accepted":
                if (
                    tools.float_compare(
                        record.selling_price,
                        SELLING_PRICE_THRESHOLD * record.expected_price,
                        precision_digits=2,
                    )
                    == -1
                ):
                    raise ValidationError(
                        "The selling price cannot be lower than 90% of the expected price."
                    )
            else:
                if not tools.float_is_zero(record.selling_price, precision_digits=2):
                    raise ValidationError(
                        "The property must be in state 'Offer Accepted' to set a selling price."
                    )

    def unlink(self):
        for record in self:
            if record.state not in ["new", "canceled"]:
                raise UserError(
                    "You cannot delete a property that is not new or canceled."
                )
        return super(EstateProperty, self).unlink()
