from odoo import api, fields, models, exceptions
from odoo.tools.misc import formatLang


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    excise_tax_tot = fields.Float(string="Excise Tax")


    @api.depends('order_line.price_total')
    def _compute_grand_total(self):
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            order.excise_tax = sum(order_lines.mapped('excise_tax'))
            order.total_tax = sum(order_lines.mapped('price_tax'))
            order.untaxed_amount = sum(order_lines.mapped('price_subtotal')) - sum(order_lines.mapped('excise_tax'))

    excise_tax = fields.Float(compute='_compute_grand_total', store=True)
    untaxed_amount = fields.Float(compute='_compute_grand_total', store=True)
    total_tax = fields.Float(string="Taxes", compute='_compute_grand_total', store=True)

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals['excise_tax'] = self.excise_tax
        invoice_vals['untaxed_amount'] = self.untaxed_amount
        invoice_vals['total_tax'] = self.total_tax
        invoice_vals['amount_total'] = self.amount_total+self.excise_tax
        return invoice_vals





class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    excise_tax = fields.Integer(string="Excise Tax")

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'excise_tax')
    def _compute_amount(self):
        for line in self:
            tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
            totals = list(tax_results['totals'].values())[0]
            amount_untaxed = totals['amount_untaxed'] + self.excise_tax
            amount_tax = totals['amount_tax']

            line.update({
                'price_subtotal': amount_untaxed,
                'price_tax': amount_tax,
                'price_total': amount_untaxed + amount_tax,
            })

    def _prepare_account_move_line(self, move=False):
        res = super()._prepare_account_move_line()
        res.update({'excise_tax': self.excise_tax})

        return res








