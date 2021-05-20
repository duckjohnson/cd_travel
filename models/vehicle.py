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
    working_time = fields.Float(string='Thời gian làm việc', compute='compute_working_time')
    total_guests = fields.Float(string='Tổng khách phục vụ', compute='compute_total_guests')

    driver_name = fields.Many2one('cd.travel.employee', string='Tài xế', domain=[('position_name', '=', 'driver')])
    driver_phone = fields.Char(string='Số điện thoại', related='driver_name.phone')

    revenue = fields.Float(string='thu nhập', compute='compute_get_revenue')

    list_tour_detail = fields.One2many('cd.travel.tour.detail', 'vehicle_name')
    list_detail_revenue = fields.Float(string='Tổng thu', related='list_tour_detail.revenue')

    list_vehicle_operating_fee = fields.One2many('cd.travel.vehicle.fee', 'name')

    active = fields.Boolean(default=True, track_visibility='onchange')
    state = fields.Selection([
        ('free_time', 'Đang chờ'),
        ('working', 'Đang chạy')],
        string='Trạng thái', default='free_time', track_visibility='onchange'
    )

    @api.multi
    @api.depends('list_tour_detail', 'list_tour_detail.total_guests')
    def compute_total_guests(self):
        for record in self:
            for r in record.list_tour_detail:
                record.total_guests = r.total_guests

    @api.multi
    @api.depends('list_tour_detail', 'list_tour_detail.date_start', 'list_tour_detail.date_end')
    def compute_working_time(self):
        for record in self:
            for r in record.list_tour_detail:
                record.working_time += parse(record.list_tour_detail.date_end).day - parse(
                    record.list_tour_detail.date_start).day

    @api.multi
    @api.depends('list_tour_detail', 'list_detail_revenue', 'driver_name', 'driver_name.salary')
    def compute_get_revenue(self):
        for record in self:
            for r in record.driver_name:
                record.revenue = r.salary
                if record.total_guests >= 100:
                    record.revenue = r.salary + (record.list_detail_revenue * 3) / 100
                if record.total_guests >= 150:
                    record.revenue = r.salary + (record.list_detail_revenue * 5) / 100
                if record.total_guests >= 250:
                    record.revenue = r.salary + (record.list_detail_revenue * 10) / 100
