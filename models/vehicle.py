# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
from dateutil.parser import parse


class Vehicle(models.Model):
    _name = 'cd.travel.vehicle'
    _description = 'Vehicle'
    _inherit = ['mail.thread']
    _rec_name = 'name'

    name = fields.Char(string='Biển số or mã chuyến bay')
    type_vehicle = fields.Selection([
        ('planes', 'Máy bay'),
        ('coach', 'xe khách')],
        string='Phương tiện', default='coach'
    )
    seats = fields.Integer(string='Số ghế')

    driver_name = fields.Many2one('cd.travel.employee', string='Tài xế', domain=[('position_name', '=', 'driver')])
    driver_phone = fields.Char(string='Số điện thoại', related='driver_name.phone')

    list_tour_detail = fields.One2many('cd.travel.tour.detail', 'vehicle_name')
    list_detail_revenue = fields.Float(string='Tổng thu', related='list_tour_detail.revenue')

    list_vehicle_operating_fee = fields.One2many('cd.travel.vehicle.fee', 'name', string='vehicle operating fee')

    active = fields.Boolean(default=True, track_visibility='onchange')
    state = fields.Selection([
        ('free_time', 'Đang chờ'),
        ('working', 'Đang chạy')],
        string='Trạng thái', default='free_time', track_visibility='onchange'
    )
