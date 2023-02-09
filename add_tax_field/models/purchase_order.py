from odoo import api, fields, models, exceptions
from odoo.tools.misc import formatLang


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    excise_tax = fields.Monetary(compute='_amount_all,_compute_tax_totals', store=True)

    @api.depends('order_line.price_total')
    def _amount_all(self):
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            excise_tax = sum(order_lines.mapped('excise_tax'))
            amount_untaxed = sum(order_lines.mapped('price_subtotal'))
            # amount_total = sum(order_lines.mapped('price_total'))
            amount_tax = sum(order_lines.mapped('price_tax'))
            order.update({
                'excise_tax': order.currency_id.round(excise_tax),
                'amount_untaxed':order.currency_id.round(amount_untaxed),
                'amount_tax':order.currency_id.round(amount_tax),
                'amount_total':amount_untaxed+amount_tax,
            })

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals['excise_tax'] = self.excise_tax
        invoice_vals['amount_untaxed'] = self.amount_untaxed
        invoice_vals['amount_tax'] = self.amount_tax
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








