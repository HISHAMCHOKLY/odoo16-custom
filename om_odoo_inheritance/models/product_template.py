from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    age = fields.Integer(string="Age")
    delivery_charge=fields.Boolean(
        string="Delivery", store=False)

    default_delivery_service = fields.Boolean(string='Set Default Delivery Service')

    @api.onchange('default_delivery_service')
    def _onchange_default_delivery_service(self):
        if self.default_delivery_service:
            # Find all records with is_active = True and set is_active = False
            self.env['product.template'].search([('default_delivery_service', '=', True)]).write({'default_delivery_service': False})

