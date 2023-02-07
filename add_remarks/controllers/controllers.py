# -*- coding: utf-8 -*-
# from odoo import http


# class AddRemarks(http.Controller):
#     @http.route('/add_remarks/add_remarks', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/add_remarks/add_remarks/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('add_remarks.listing', {
#             'root': '/add_remarks/add_remarks',
#             'objects': http.request.env['add_remarks.add_remarks'].search([]),
#         })

#     @http.route('/add_remarks/add_remarks/objects/<model("add_remarks.add_remarks"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('add_remarks.object', {
#             'object': obj
#         })
