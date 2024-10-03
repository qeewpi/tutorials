# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = "res.partner"
    