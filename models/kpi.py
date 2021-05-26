# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError


class KPI(models.Model):
    _name = 'cd.travel.kpi'
    _description = 'Key Performance Indicator'
    _rec_name = 'name'

    name = fields.Char(string='Tên level', required=True)
    number = fields.Integer(string='Mục tiêu', required=True)

    planning_name = fields.Many2one('cd.travel.planning.kpi', string='tên kế hoạch')

    calculation_method = fields.Selection([
        ('phantram', 'Phần trăm'),
        ('vnd', 'VND')],
        string='Cách tính', required=True
    )
    money = fields.Float(string='Giá trị', required=True)
    active = fields.Boolean(default=True, track_visibility='onchange')
