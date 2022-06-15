# -*- coding: utf-8 -*-
# from odoo import http


# class RecruitmentExtend(http.Controller):
#     @http.route('/recruitment_extend/recruitment_extend/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/recruitment_extend/recruitment_extend/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('recruitment_extend.listing', {
#             'root': '/recruitment_extend/recruitment_extend',
#             'objects': http.request.env['recruitment_extend.recruitment_extend'].search([]),
#         })

#     @http.route('/recruitment_extend/recruitment_extend/objects/<model("recruitment_extend.recruitment_extend"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('recruitment_extend.object', {
#             'object': obj
#         })
