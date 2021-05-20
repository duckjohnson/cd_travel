from odoo import models, fields, api, exceptions, _


class Position(models.Model):
    _name = 'cd.travel.position'
    _description = 'Position Of Employee'

    name = fields.Char(string='Tên chức vụ', required=True)
    description = fields.Char(string='Mô tả')
