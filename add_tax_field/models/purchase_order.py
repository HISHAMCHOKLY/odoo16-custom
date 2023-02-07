from odoo import api, fields, models, exceptions


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.depends('order_line.price_total')
    def _compute_grand_total(self):
        # print(self.amount_untaxed)
        # print(self.total_tax)

        record = self.env['purchase.order'].search([],limit=1, order='id desc')
        print(record)
        tax_totals = {'amount_untaxed': 999.0, 'amount_total': 999.0, 'formatted_amount_total': '₹\xa0999.00','formatted_amount_untaxed': '₹\xa0999.00', 'subtotals': [], 'subtotals_order': [], 'display_tax_base': False}

        # self.tax_totals.update({'tax_totals': tax_totals})
        print(self.tax_totals['amount_total'])

        # print(self.tax_totals['groups_by_subtotal'])
        # self.tax_totals = {'amount_total': new_value}
        # self.write({'tax_totals': self.tax_totals})
        # self.total_tax=self.amount_total-self.amount_untaxed

        for order in self:
            order.grand_total = sum(line.price_total for line in order.order_line)
            # order.excise_tax = sum(line.excise_tax for line in order.order_line)
            order.total_tax = sum(line.price_tax for line in order.order_line)
            order.untaxed_amount = sum(line.price_subtotal for line in order.order_line)
        self.tax_totals['amount_total']=1222222222222222
        self.tax_totals['price_tax']=1222222222222222
        print(self.tax_totals['amount_total'])
        print(self.tax_totals['price_tax'])

        # self.tax_totals['amount_total']=self.grand_total

    grand_total = fields.Float(compute='_compute_grand_total', store=True)
    # excise_tax = fields.Float(compute='_compute_grand_total', store=True)
    untaxed_amount=fields.Float(compute='_compute_grand_total', store=True)
    total_tax = fields.Float(string="Total Tax", compute='_compute_grand_total', store=True)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    excise_tax = fields.Integer(string="Excise Tax")

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'excise_tax')
    def _compute_amount(self):
        for line in self:
            tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
            totals = list(tax_results['totals'].values())[0]
            amount_untaxed = totals['amount_untaxed']
            amount_tax = totals['amount_tax'] + self.excise_tax

            line.update({
                'price_subtotal': amount_untaxed,
                'price_tax': amount_tax,
                'price_total': amount_untaxed + amount_tax,
            })


    def _prepare_account_move_line(self, move=False):
        res = super()._prepare_account_move_line()
        res.update({'excise_tax': self.excise_tax})
        return res
