from odoo import api, fields, models, exceptions


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'



    @api.depends('order_line.price_total')
    def _compute_grand_total(self):
        # print(self.amount_untaxed)
        # print(self.amount_total)
        # print(self.tax_totals)
        # self.total_tax=self.amount_total-self.amount_untaxed

        for order in self:
            order.grand_total = sum(line.price_total for line in order.order_line)
            order.excise_tax = sum(line.excise_tax for line in order.order_line)

    grand_total = fields.Float(compute='_compute_grand_total', store=True)
    excise_tax = fields.Float(compute='_compute_grand_total', store=True)
    total_tax=fields.Float(string="Total Tax",compute='_compute_grand_total', store=True)





class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    excise_tax = fields.Integer(string="Excise Tax")

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'excise_tax')
    def _compute_amount(self):
        for line in self:
            tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
            totals = list(tax_results['totals'].values())[0]
            amount_untaxed = totals['amount_untaxed']
            amount_tax = totals['amount_tax'] +self.excise_tax

            line.update({
                'price_subtotal': amount_untaxed,
                'price_tax': amount_tax,
                'price_total': amount_untaxed + amount_tax,
            })

    def _convert_to_tax_base_line_dict(self):
        """ Convert the current record to a dictionary in order to use the generic taxes computation method
        defined on account.tax.

        :return: A python dictionary.
        """
        self.ensure_one()
        return self.env['account.tax']._convert_to_tax_base_line_dict(
            self,
            partner=self.order_id.partner_id,
            currency=self.order_id.currency_id,
            product=self.product_id,
            taxes=self.taxes_id,
            price_unit=self.price_unit,
            quantity=self.product_qty,
            price_subtotal=self.price_subtotal,
        )





    def _prepare_account_move_line(self, move=False):
        res = super()._prepare_account_move_line()
        res.update({'excise_tax': self.excise_tax})
        return res
