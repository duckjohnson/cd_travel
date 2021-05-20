# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError


class Sale(models.Model):
    _name = 'cd.travel.info.sale'
    _description = 'Sale'
    _rec_name = 'name'

    name = fields.Char(string='Tên sale', required=True)
    type = fields.Selection([('phantram', 'Phần trăm'), ('vnd', 'VND')], string='Đơn vị', required=True)
    amount = fields.Float(string='Giá trị', required=True)
    active = fields.Boolean(default=True, track_visibility='onchange')

    @api.multi
    def go_to_website(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return {
            'type': 'ir.actions.act_url',
            'url': base_url + '/experience',
            'target': 'new'

        }
