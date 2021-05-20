# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError


class Sale(models.Model):
    _name = 'cd.travel.vehicle.fee'
    _description = 'Vehicle operating fee'
    _rec_name = 'name'

    name = fields.Many2one('cd.travel.vehicle', string='Biển số xe', required=True,
                           domain=[('type_vehicle', '=', 'coach')])
    date_fee = fields.Date(string='Ngày', required=True)
    content = fields.Text(string='Nội dung', required=True)
    price = fields.Float(string='Giá', required=True)
