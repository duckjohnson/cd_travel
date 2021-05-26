# -*- coding: utf-8 -*-


import datetime

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


class BaseSalary(models.Model):
    _name = 'cd.travel.base.salary'
    _description = 'Base salary employees'
    _rec_name = 'name'

    name = fields.Char(string='Tên hợp đồng', required=True)
    from_date = fields.Date(string='Ngày áp dụng', required=True)
    to_date = fields.Date(string='Ngày hết hạn')
    money = fields.Float(string='Lương cơ bản', required=True)

    emp_name = fields.Many2one('cd.travel.employee', string='Tên nhân viên', required=True,
                               domain=['|', ('position_name', '=', 'driver'), ('position_name', '=', 'guide')])
    emp_position = fields.Many2one(string='Chức vụ', related='emp_name.position_name', readonly=True)

    state = fields.Selection([
        ('use', 'Đang sử dụng'),
        ('stop', 'Ngưng sử dụng')],
        string='Trạng thái', default='use'
    )
