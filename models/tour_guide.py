# -*- coding: utf-8 -*-
import datetime
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError
from dateutil.parser import parse


class TourGuide(models.Model):
    _name = 'cd.travel.tour.guide'
    _inherit = ['mail.thread']
    _description = 'salary tour guide'
    _rec_name = 'guide_name'

    guide_name = fields.Many2one('cd.travel.employee', string='Tên hướng dẫn viên', required=True,
                                 domain=[('position_name', '=', 'guide')])
    working_time = fields.Float(string='Thời gian làm việc', compute='compute_working_time')
    total_guests = fields.Float(string='Tổng khách phục vụ', compute='compute_total_guests')
    revenue = fields.Float(string='Thu nhập', compute='compute_get_revenue')

    list_tour_detail = fields.One2many('cd.travel.tour.detail', 'name_tour_guide', string='danh sách tour đã đi')
    list_detail_revenue = fields.Float(string='Tổng thu', related='list_tour_detail.revenue')

    state = fields.Selection([
        ('free_time', 'Đang chờ'),
        ('working', 'Đang làm việc'), ],
        string='Trạng thái', default='free_time', track_visibility='onchange'
        # , compute='compute_change_state'
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
    @api.depends('list_tour_detail', 'list_detail_revenue', 'guide_name', 'guide_name.salary')
    def compute_get_revenue(self):
        for record in self:
            for r in record.guide_name:
                record.revenue = r.salary
                if record.total_guests >= 100:
                    record.revenue = r.salary + (record.list_detail_revenue * 3) / 100
                if record.total_guests >= 150:
                    record.revenue = r.salary + (record.list_detail_revenue * 5) / 100
                if record.total_guests >= 250:
                    record.revenue = r.salary + (record.list_detail_revenue * 10) / 100

    # @api.multi
    # @api.depends('list_tour_detail', 'list_tour_detail.date_start', 'list_tour_detail.date_end')
    # def compute_change_state(self):
    #     for record in self:
    #         record.state = 'free_time'
    #         for r in record.list_tour_detail:
    #             if datetime.date.strptime(r.date_start, '%Y-%m-%d') < datetime.date.now() \
    #                     and datetime.date.now() < datetime.date.strptime(r.date_end, '%Y-%m-%d'):
    #                 record.state = 'working'
    #             else:
    #                 record.state = 'free_time'

    @api.multi
    @api.depends('list_tour_detail', 'list_tour_detail.name')
    def compute_get_salary(self):
        for record in self:
            record.salary += 1
