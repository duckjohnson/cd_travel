# -*- coding: utf-8 -*-


import datetime

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


class Employee(models.Model):
    _name = 'cd.travel.employee'
    _description = 'Employee  Of Cd Travel'

    code = fields.Char(string='Mã nhân viên', required=True, index=True,
                       default=lambda self: _('New'),
                       readonly=True)
    name = fields.Char(string='Tên nhân viên', required=True)
    DOB = fields.Date(string='Ngày sinh', required=True)
    gender = fields.Selection([
        ('boy', 'Nam'),
        ('girl', 'Nữ')],
        string='Giới tính', default='boy', required=True
    )
    identify = fields.Char(string='Số căn cước công dân', required=True)
    phone = fields.Char(string='Số điện thoại', required=True)
    address = fields.Char(string='Địa chỉ')
    salary = fields.Float(string='Lương cứng')

    position_name = fields.Many2one('cd.travel.position', string='Chức vụ', required=True)

    account = fields.Many2one('res.users', required=True)
    account_login = fields.Char(related='account.login', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['code'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code(
                    'employee.sequence') or _('New')
            else:
                vals['code'] = self.env['ir.sequence'].next_by_code('employee.sequence') or _('New')
        result = super(Employee, self).create(vals)
        return result

    @api.constrains('DOB')
    def validate_DOB(self):
        if self.DOB >= str(datetime.date.today()):
            raise UserError('Ngày sinh phải trước ngày hiện tại')
