# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


class TravelHandBook(models.Model):
    _name = 'cd.travel.handbook'
    _inherit = ['mail.thread']
    _description = 'cd travel handbook'
    _rec_name = 'name'

    code = fields.Char(string='Mã cẩm nang', default=lambda self: _('New'), readonly=True)
    name = fields.Char(string='Tên cẩm nang', required=True)
    content = fields.Text(string='Nội dung', required=True)
    time_handbook = fields.Date(string='Thời gian')
    image = fields.Binary(string='Hình ảnh')
    active = fields.Boolean(default=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['code'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code(
                    'handbook.sequence') or _('New')
            else:
                vals['code'] = self.env['ir.sequence'].next_by_code('handbook.sequence') or _('New')
        result = super(TravelHandBook, self).create(vals)
        return result
