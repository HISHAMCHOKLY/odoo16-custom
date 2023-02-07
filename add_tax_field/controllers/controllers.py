# -*- coding: utf-8 -*-
# from odoo import http


# class AddTaxField(http.Controller):
#     @http.route('/add_tax_field/add_tax_field', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/add_tax_field/add_tax_field/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('add_tax_field.listing', {
#             'root': '/add_tax_field/add_tax_field',
#             'objects': http.request.env['add_tax_field.add_tax_field'].search([]),
#         })

#     @http.route('/add_tax_field/add_tax_field/objects/<model("add_tax_field.add_tax_field"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('add_tax_field.object', {
#             'object': obj
#         })
