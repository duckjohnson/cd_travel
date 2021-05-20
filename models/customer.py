# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


class Customer(models.Model):
    _name = 'cd.travel.customer'
    _description = 'cd travel type travel'
    _rec_name = 'name'

    name = fields.Char(string='Tên khách hàng', required=True)
    identity = fields.Char(string='CCCD or Passport', required=True)
    DOB = fields.Date(string='Ngày sinh')
    phone = fields.Char(string='SĐT', required=True)
    email = fields.Char(string='Email')
    address = fields.Char(string='Địa chỉ')
    gender = fields.Selection([
        ('boy', 'Nam'),
        ('girl', 'Nữ')],
        string='Giới tính', default='girl'
    )

