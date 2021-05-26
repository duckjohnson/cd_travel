# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError


class PlanningKPI(models.Model):
    _name = 'cd.travel.planning.kpi'
    _description = 'Planning Key Performance Indicator'
    _rec_name = 'name'

    name = fields.Char(string='Kế hoạch', required=True)
    from_date = fields.Date(string='Từ ngày', required=True)
    to_date = fields.Date(string='Đến ngày', required=True)
    type = fields.Selection([
        ('day', 'Theo ngày'),
        ('month', 'Theo tháng'),
        ('year', 'Theo năm')],
        string='Hình thức áp dụng', required=True
    )
    kpi_type = fields.Selection([
        ('tour', 'Tour'),
        ('people', 'Số người')],
        string='Áp dụng theo', required=True
    )
    list_kpi = fields.One2many('cd.travel.kpi', 'planning_name', string='Danh sách level')

    active = fields.Boolean(default=True, track_visibility='onchange')
