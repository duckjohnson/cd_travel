# -*- coding: utf-8 -*-

import json
from odoo import http
from odoo.http import request, Response


class Controller(http.Controller):

    # @http.route('/', type='http', auth="public", website=True)
    # def view_home_data(self, **kw):
    #     tour_ids = request.env['cd.travel.tour.travel'].sudo().search([])
    #     return http.request.render('cd-travel.exp_page', {
    #         'data_exp': tour_ids
    #     })

    @http.route('/experience', type='http', auth="public", website=True)
    def experience_data(self, **kw):
        experience_ids = request.env['cd.travel.experience'].sudo().search([])
        return http.request.render('cd-travel.exp_page', {
            'data_exp': experience_ids
        })

    @http.route('/contact', type='http', auth="public", website=True)
    def contact_data(self, **kw):
        contact_ids = request.env['cd.travel.contact'].sudo().search([])
        data_contact = []
        for ct in contact_ids:
            data_contact.append({'code': ct.code, 'name': ct.name, 'address': ct.address, 'hotline': ct.hotline,
                                 'fax': ct.fax, 'email': ct.email, 'active': ct.active})
        values = {"data": data_contact}
        response = Response(json.dumps(values), content_type='application/json')

        return http.request.render('cd-travel.contact_page', {
            'data_ct': contact_ids
        })
