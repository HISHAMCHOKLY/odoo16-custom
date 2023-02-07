from odoo import api, fields, models, exceptions


class AccountMove(models.Model):
    _inherit = 'account.move'

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    excise_tax=fields.Float(string="Excise Tax")
