# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Real Estate Advertisement Module",
    "summary": "Real Estate Advertisement Module",
    "depends": ["base"],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/res_users_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
        "reports/estate_property_reports_actions.xml",
        "reports/estate_property_reports_templates.xml",
        "reports/estate_property_reports_inherit.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "estate/static/src/fonts/inter.scss",
        ],
    },
    "demo": ["demo/estate_demo.xml"],
}
