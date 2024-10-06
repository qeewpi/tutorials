# -*- coding: utf-8 -*-

from odoo import fields, models, api
from dateutil import relativedelta
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    validity = fields.Integer(default=7)

    _sql_constraints = [
        (
            "positive_price",
            "CHECK(price > 0)",
            "The offer price must be positive and greater than zero.",
        ),
    ]

    @api.model
    def create(self, vals):
        property_id = vals.get("property_id")

        if property_id:
            property = self.env["estate.property"].browse(property_id)

            if property.state == "offer_accepted":
                raise ValidationError(
                    "Cannot add new offers when the property state is 'offer_accepted'."
                )

            new_offer_price = vals.get("price")
            if new_offer_price:
                for offer in property.offer_ids:
                    if new_offer_price <= offer.price:
                        raise ValidationError(
                            "The offer price must be higher than the price of an existing offer."
                        )

            property.state = "offer_received"

        return super(EstatePropertyOffer, self).create(vals)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta.relativedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = (
                    fields.Date.today()
                    + relativedelta.relativedelta(days=record.validity)
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            if record.property_id.state == "offer_accepted":
                raise UserError("An offer has already been accepted for this property.")
            else:
                record.property_id.write(
                    {"state": "offer_accepted", "partner_id": record.partner_id.id}
                )
                record.status = "accepted"
                record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            record.status = "refused"
            record.property_id.state = "new"
            record.property_id.partner_id = False
