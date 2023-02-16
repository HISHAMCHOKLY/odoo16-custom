# -*- coding: utf-8 -*-
# from odoo import http


# class PosRefund(http.Controller):
#     @http.route('/pos_refund/pos_refund', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_refund/pos_refund/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_refund.listing', {
#             'root': '/pos_refund/pos_refund',
#             'objects': http.request.env['pos_refund.pos_refund'].search([]),
#         })

#     @http.route('/pos_refund/pos_refund/objects/<model("pos_refund.pos_refund"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_refund.object', {
#             'object': obj
#         })
