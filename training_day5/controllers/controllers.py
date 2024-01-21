# -*- coding: utf-8 -*-
# from odoo import http


# class TrainingDay5(http.Controller):
#     @http.route('/training_day5/training_day5', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/training_day5/training_day5/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('training_day5.listing', {
#             'root': '/training_day5/training_day5',
#             'objects': http.request.env['training_day5.training_day5'].search([]),
#         })

#     @http.route('/training_day5/training_day5/objects/<model("training_day5.training_day5"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('training_day5.object', {
#             'object': obj
#         })

