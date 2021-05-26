# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


class TravelType(models.Model):
    _name = 'cd.travel.type.travel'
    _inherit = ['mail.thread']
    _description = 'cd travel type travel'
    _rec_name = 'name'

    code = fields.Char(string='Mã loại du lịch', default=lambda self: _('New'), readonly=True)
    name = fields.Char(string='Tên loại du lịch', required=True)
    description = fields.Text(string='Mô tả')
    active = fields.Boolean(default=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['code'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code(
                    'type.travel.sequence') or _('New')
            else:
                vals['code'] = self.env['ir.sequence'].next_by_code('type.travel.sequence') or _('New')
        result = super(TravelType, self).create(vals)
        return result
