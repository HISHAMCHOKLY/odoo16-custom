from odoo import api,fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    delivery_charge = fields.Float(string="Delivery Charge")


    @api.model
    def default_get(self, fields):
        defaults = super().default_get(fields)
        if self.delivery_charge == 0 :
            delivery_product_id = int(self.env['ir.config_parameter'].sudo().get_param('sale.default_delivery_product_id'))
            delivery = self.line_ids.filtered(lambda r: r.product_id.id == delivery_product_id)
            self.delivery_charge = delivery.price_unit
        return defaults


