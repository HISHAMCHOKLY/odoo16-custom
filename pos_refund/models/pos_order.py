from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    refund_reason=fields.Many2one(comodel_name='pos.refund', string="Refund Reason")
