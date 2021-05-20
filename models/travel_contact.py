# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


class TravelContact(models.Model):
    _name = 'cd.travel.contact'
    _inherit = ['mail.thread']
    _description = 'cd travel contact'
    _rec_name = 'name'

    code = fields.Char(string='Mã liên hệ', default=lambda self: _('New'), readonly=True)
    name = fields.Char(string='Tên chi nhánh', required=True)
    address = fields.Char(string='Địa chỉ', required=True)
    hotline = fields.Char(string='SĐT', required=True)
    fax = fields.Char(string='Fax')
    email = fields.Char(string='Email')
    active = fields.Boolean(default=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['code'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code(
                    'contact.sequence') or _('New')
            else:
                vals['code'] = self.env['ir.sequence'].next_by_code('contact.sequence') or _('New')
        result = super(TravelContact, self).create(vals)
        return result
