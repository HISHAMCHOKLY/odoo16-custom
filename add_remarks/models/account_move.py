from odoo import api, fields, models, exceptions


class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_remark = fields.Text(string="Customer Remarks")
    manager_remark = fields.Text(string="Manager Remarks")
    is_manager = fields.Boolean(string="is Manager")
    is_customer = fields.Boolean(string="is customer")

    @api.model
    def default_get(self, fields):
        if self.env.user.has_group("add_remarks.group_account_customer"):
            self.is_customer = True
        else:
            self.is_customer = False
        if self.env.user.has_group("add_remarks.group_account_manager"):
            self.is_manager = True
        else:
            self.is_manager = False
        defaults = super().default_get(fields)
        return defaults


    @api.model
    def action_post(self):
        if not self.customer_remark or not self.manager_remark:
            raise exceptions.UserError("The Remarks field must be filled before confirming the account move.")
        res = super().action_post()
        return res


