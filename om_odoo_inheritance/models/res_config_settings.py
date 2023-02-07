from odoo import api, models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    # default_product_id = fields.Many2one('product.product', string='Default Product',default_model='product.product')


    delivery_default_product_id = fields.Many2one(
        'product.product',
        'Delivery Product',
        domain="[('type', '=', 'service')]",
        config_parameter='sale.default_delivery_product_id',
        help='Default product used for Delivery')



