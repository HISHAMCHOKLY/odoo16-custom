from odoo import api, fields, models, exceptions
from odoo.tools.misc import formatLang



class AccountMove(models.Model):
    _inherit = 'account.move'

    excise_tax = fields.Monetary( store=True ,readonly=True, compute='_compute_amount')


    @api.model
    def create(self, vals):
        move = super(AccountMove, self).create(vals)
        # print('move--->',move)
        a = self.env['account.account'].sudo().search([('code', '=', 300001)])
        lines = []
        val = {
            'name': 'Excise Tax',
            'journal_id': move.journal_id,  # ID of the journal
            'account_id': a.id,  # ID of the account
            'debit': self.excise_tax,  # Debit amount
            'credit': 0,  # Credit amount
            'move_id': move.journal_id,  # ID of the journal entry,
            'move_type': 'entry',
            'quantity': 1,  # the quantity of the product
            'price_unit': self.excise_tax,
        }
        lines.append((0, 0, val))
        move.line_ids = lines

        for a in move.line_ids:
            print(a.display_type,a.name,a.price_unit)
            if a.name=='':
                # a.credit+=move.excise_tax
                a.price_unit =+ move.excise_tax
            if a.name=='Excise Tax':
                a.price_unit=move.excise_tax
                a.tax_ids=False
                # a.display_type='payment_term'
        return move
    def _compute_tax_totals(self):
        super()._compute_tax_totals()
        for move in self:
            purchase_journal = self.env['account.journal'].search([('type', '=', 'purchase')])
            # move.tax_totals['amount_total'] += move.excise_tax
            # move.tax_totals['formatted_amount_total'] = formatLang(self.env, move.tax_totals['amount_total'],
            #                                                         currency_obj=move.company_id.currency_id)
            # print(move.tax_totals['groups_by_subtotal'])
            # tax_group = move.tax_totals['groups_by_subtotal']
            # new_group = {
            #     'name': 'New Tax Group',
            #     'base': 100,
            #     'amount': 10,
            #     'balance': 110,
            #     'sequence': 10,
            # }
            # tax_group.append(new_group)






class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    excise_tax=fields.Monetary(string="Excise Tax",compute='_compute_totals', store=True,currency_field='currency_id',)

    # @api.depends('move_id')
    # def _compute_balance(self):
    #     pass
        # for line in self:
        #     if line.display_type in ('line_section', 'line_note'):
        #         line.balance = False
        #     elif not line.move_id.is_invoice(include_receipts=True):
        #         # Only act as a default value when none of balance/debit/credit is specified
        #         # balance is always the written field because of `_sanitize_vals`
        #         line.balance = -sum((line.move_id.line_ids - line).mapped('balance'))
        #         line.balance = 0
    # @api.depends('balance', 'move_id.is_storno')
    # def _compute_debit_credit(self):
    #     pass
        # a = self.env['account.account'].sudo().search([('code', '=', 300001)])
        # for line in self:
        #         line.debit = line.balance if line.balance > 0.0 else 0.0
        #         line.credit = -line.balance if line.balance < 0.0 else 0.0
        #     else:
        #         line.debit = line.balance if line.balance < 0.0 else 0.0
        #         line.credit = -line.balance if line.balance > 0.0 else 0.0




    @api.depends('product_id', 'product_uom_id')
    def _compute_tax_ids(self):
        res=super()._compute_tax_ids()
        print(res,'ssssssssssssssssss')

    @api.depends('quantity', 'discount', 'price_unit', 'tax_ids', 'currency_id', 'excise_tax')
    def _compute_totals(self):
        for line in self:
            if line.display_type != 'product':
                line.price_total = line.price_subtotal = False
            # Compute 'price_subtotal'.
            line_discount_price_unit = line.price_unit * (1 - (line.discount / 100.0))
            subtotal = line.quantity * line_discount_price_unit

            # Compute 'price_total'.
            if line.tax_ids:
                taxes_res = line.tax_ids.compute_all(
                    line_discount_price_unit,
                    quantity=line.quantity,
                    currency=line.currency_id,
                    product=line.product_id,
                    partner=line.partner_id,
                    is_refund=line.is_refund,
                )
                line.price_subtotal = taxes_res['total_excluded']
                taxes_res.update({'excise_tax': line.excise_tax})
                line.price_total = taxes_res['total_included']+taxes_res['excise_tax']

            else:
                line.price_total = line.price_subtotal = subtotal







# //////////////////in account.move
    # def _compute_amount(self):
    #     for move in self:
    #         print('ac move working')
    #         total_untaxed, total_untaxed_currency = 0.0, 0.0
    #         total_tax, total_tax_currency = 0.0, 0.0
    #         total_residual, total_residual_currency = 0.0, 0.0
    #         total, total_currency = 0.0, 0.0
    #
    #         for line in move.line_ids:
    #             if move.is_invoice(True):
    #                 # === Invoices ===
    #                 if line.display_type == 'tax' or (line.display_type == 'rounding' and line.tax_repartition_line_id):
    #                     # Tax amount.
    #                     total_tax += line.balance
    #                     total_tax_currency += line.amount_currency
    #                     total += line.balance
    #                     total_currency += line.amount_currency
    #                 elif line.display_type in ('product', 'rounding'):
    #                     # Untaxed amount.
    #                     total_untaxed += line.balance
    #                     total_untaxed_currency += line.amount_currency
    #                     total += line.balance
    #                     total_currency += line.amount_currency
    #                 elif line.display_type == 'payment_term':
    #                     # Residual amount.
    #                     total_residual += line.amount_residual
    #                     total_residual_currency += line.amount_residual_currency
    #             else:
    #                 # === Miscellaneous journal entry ===
    #                 if line.debit:
    #                     total += line.balance
    #                     total_currency += line.amount_currency
    #
    #         sign = move.direction_sign
    #         move.amount_untaxed = sign * total_untaxed_currency
    #         move.amount_tax = sign * total_tax_currency
    #         move.amount_total = sign * total_currency + self.excise_tax
    #         move.amount_residual = -sign * total_residual_currency
    #         move.amount_untaxed_signed = -total_untaxed
    #         move.amount_tax_signed = -total_tax
    #         move.amount_total_signed = abs(total) if move.move_type == 'entry' else -total
    #         move.amount_residual_signed = total_residual
    #         move.amount_total_in_currency_signed = abs(move.amount_total) if move.move_type == 'entry' else -(
    #                 sign * move.amount_total)
    #








