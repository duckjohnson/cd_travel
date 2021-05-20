# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


class TourImage(models.Model):
    _name = 'cd.travel.tour.image'
    _description = 'cd travel tour image'
    _rec_name = 'name'

    code = fields.Char(string='Mã ảnh', default=lambda self: _('New'), readonly=True)
    name = fields.Char(string='Tên ảnh', required=True)
    image = fields.Binary(string='Hình ảnh', required=True)

    img_tour_name = fields.Many2one('cd.travel.tour.travel', string='Tên tour')

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['code'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code(
                    'tour.image.sequence') or _('New')
            else:
                vals['code'] = self.env['ir.sequence'].next_by_code('tour.image.sequence') or _('New')
        result = super(TourImage, self).create(vals)
        return result
