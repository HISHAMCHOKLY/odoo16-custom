from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    age = fields.Integer(string="Age", related='partner_id.age', tracking=True)
    employee = fields.Many2one('hr.employee', string="Employee")
    confirmed_user_id = fields.Many2one('res.partner', string='confirmed User')
    delivery_charge=fields.Integer(string="Delivery Charge")


    @api.onchange('partner_id')
    def onchange_partner_id(self):
        lines = [(5, 0, 0)]
        # print(self.partner_id.product_lines_ids.product_id)
        for line in self.partner_id.product_lines_ids:
            val={
                'product_id': line.product_id,
                'product_uom_qty': 1,
                'price_unit': line.product_price
            }
            lines.append((0, 0, val))
        # print(lines)
        self.order_line = lines

    @api.onchange('delivery_charge')
    def onchange_delivery_charge(self):
        delivery_product_id = int(self.env['ir.config_parameter'].sudo().get_param('sale.default_delivery_product_id'))
        delivery = self.order_line.filtered(lambda r: r.product_id.id == delivery_product_id)
        if delivery:
            delivery.price_unit = self.delivery_charge
        else:
            lines = []
            val = {
                'product_id': delivery_product_id,
                'product_uom_qty': 1,
                'price_unit': self.delivery_charge
            }
            lines.append((0, 0, val))
            self.order_line = lines

    @api.onchange('order_line')
    def onchange_order_line(self):
        delivery_product_id = int(self.env['ir.config_parameter'].sudo().get_param('sale.default_delivery_product_id'))
        delivery = self.order_line.filtered(lambda r: r.product_id.id == delivery_product_id)
        if delivery.price_unit != self.delivery_charge:
            self.delivery_charge = delivery.price_unit
