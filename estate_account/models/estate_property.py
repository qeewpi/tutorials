from odoo import models, fields
import pdb


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_mark_sold(self):

        res = super().action_mark_sold()

        # Create an account move
        for record in self:
            self.env["account.move"].create(
                {
                    "partner_id": record.partner_id.id,
                    "move_type": "out_invoice",
                    "invoice_date": fields.Date.today(),
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": record.name,
                                "quantity": 1,
                                "price_unit": record.selling_price * 6.0 / 100,
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "name": "Administrative Fees",
                                "quantity": 1,
                                "price_unit": 100,
                            },
                        ),
                    ],
                }
            )
