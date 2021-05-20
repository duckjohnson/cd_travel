# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


class TravelRegion(models.Model):
    _name = 'cd.travel.region.travel'
    _inherit = ['mail.thread']
    _description = 'cd travel region travel'
    _rec_name = 'name'

    code = fields.Char(string='Mã vùng du lịch', default=lambda self: _('New'), readonly=True)
    name = fields.Char(string='Tên vùng du lịch', required=True)
    description = fields.Text(string='Mô tả', required=True)

    name_travel_type = fields.Many2one('cd.travel.type.travel', string='Loại du lịch', required=True)

    active = fields.Boolean(default=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['code'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code(
                    'region.travel.sequence') or _('New')
            else:
                vals['code'] = self.env['ir.sequence'].next_by_code('region.travel.sequence') or _('New')
        result = super(TravelRegion, self).create(vals)
        return result

