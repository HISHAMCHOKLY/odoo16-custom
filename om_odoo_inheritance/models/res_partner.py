from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    age = fields.Integer(string="Age")
    employee = fields.Many2one('hr.employee', string='Employee')
    product_lines_ids = fields.One2many('res.partner.lines', 'appointment_id', string='Product Lines')

class ResPartnerLines(models.Model):
    _name = 'res.partner.lines'
    _description ='Partner Products'

    product_id = fields.Many2one('product.product', string="Product", required=True)
    product_price = fields.Integer(string="Price")

    appointment_id = fields.Many2one('res.partner', string="Appointment Id")



