# -*- coding: utf-8 -*-
# from odoo import http


# class Task1(http.Controller):
#     @http.route('/task1/task1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/task1/task1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('task1.listing', {
#             'root': '/task1/task1',
#             'objects': http.request.env['task1.task1'].search([]),
#         })

#     @http.route('/task1/task1/objects/<model("task1.task1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('task1.object', {
#             'object': obj
#         })
