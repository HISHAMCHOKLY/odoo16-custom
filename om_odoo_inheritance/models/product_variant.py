from odoo import api, fields, models


class ProductVariant(models.Model):
    _inherit = 'product.product'

    abc = fields.Integer(string="ABC")
