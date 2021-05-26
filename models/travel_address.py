# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


class TravelAddress(models.Model):
    _name = 'cd.travel.address.travel'
    _inherit = ['mail.thread']
    _description = 'cd travel address travel'
    _rec_name = 'name'

    code = fields.Char(string='Mã địa điểm du lịch', default=lambda self: _('New'), readonly=True)
    name = fields.Char(string='Tên địa điểm du lịch', required=True)
    description = fields.Text(string='Mô tả')

    name_travel_region = fields.Many2one('cd.travel.region.travel', string='Vùng du lịch')

    active = fields.Boolean(default=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['code'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code(
                    'address.travel.sequence') or _('New')
            else:
                vals['code'] = self.env['ir.sequence'].next_by_code('address.travel.sequence') or _('New')
        result = super(TravelAddress, self).create(vals)
        return result
