from odoo import fields, models


class AttachmentWizard(models.TransientModel):
    _name = 'attachment.wizard'

    attachment = fields.Binary('Attachment')
    name = fields.Char('Name')

    def attach_to_order(self):
        order_ids = self._context.get('active_ids')
        for order_id in order_ids:
            attachment_vals = {
                'datas': self.attachment,
                'name': self.name,
                'res_model': 'sale.order',
                'res_id': order_id,
            }
            self.env['ir.attachment'].create(attachment_vals)



    # def attach_to_order(self):
    #     order_id = self._context.get('active_id')
    #     print(order_id)
    #     attachment_vals = {
    #         'datas': self.attachment,
    #         'name': self.name,
    #         'res_model': 'sale.order',
    #         'res_id': order_id,
    #     }
    #     self.env['ir.attachment'].create(attachment_vals)
