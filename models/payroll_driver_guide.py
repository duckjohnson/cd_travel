# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
from dateutil.parser import parse


class PayrollDriverGuide(models.Model):
    _name = 'cd.travel.payroll.driver.guide'
    _description = 'Payroll driver and guide'
    _rec_name = 'name'

    name = fields.Char(string='Tên báo cáo', required=True)
    from_date = fields.Date(string='Từ ngày', required=True)
    to_date = fields.Date(string='Đến ngày', required=True)
    total_salary = fields.Float(string='Lương', compute='compute_salary')
    personal_income_tax = fields.Float(string='Thuế thu nhập cá nhân', compute='compute_salary')
    achieve_kpi = fields.Integer(string='Mốc kpi đạt được', compute='compute_salary')
    total_revenue_detail = fields.Float(string='Tổng doanh thu tour', compute='compute_working_time_and_total_guests')

    emp_name = fields.Many2one('cd.travel.employee', string='Tên nhân viên', required=True,
                               domain=['|', ('position_name', '=', 'driver'), ('position_name', '=', 'guide')])
    emp_position = fields.Many2one(string='Chức vụ', related='emp_name.position_name', readonly=True)
    emp_salary = fields.Float(string='Lương cơ bản', related='emp_name.base_money', readonly=True)

    working_time = fields.Float(string='Thời gian làm việc', compute='compute_working_time_and_total_guests')
    total_guests = fields.Float(string='Tổng khách phục vụ', compute='compute_working_time_and_total_guests')
    count_tour = fields.Integer(string='Số tour phục vụ', compute='compute_working_time_and_total_guests')

    planning_name = fields.Many2one('cd.travel.planning.kpi', string='Tên kế hoạch')
    planning_kpi_type = fields.kpi_type = fields.Selection([
        ('tour', 'Tour'),
        ('people', 'Số người')],
        string='Áp dụng theo', related='planning_name.kpi_type'
    )
    planning_list_kpi = fields.One2many('cd.travel.kpi', 'planning_name', string='Danh sách level',
                                        related='planning_name.list_kpi')

    @api.multi
    @api.depends('from_date', 'to_date', 'emp_name', 'emp_position')
    def compute_working_time_and_total_guests(self):
        for record in self:
            if record.emp_position.name == 'driver':
                list_detail = self.env['cd.travel.tour.detail'].search(
                    [('vehicle_driver_name', '=', record.emp_name.name),
                     ('date_start', '>=', record.from_date),
                     ('date_end', '<=', record.to_date)])
                record.count_tour = 0
                for r in list_detail:
                    record.working_time += parse(r.date_end).day - parse(r.date_start).day
                    record.total_guests += r.total_guests
                    record.count_tour += 1
                    record.total_revenue_detail += r.revenue

            if record.emp_position.name == 'guide':
                list_detail = self.env['cd.travel.tour.detail'].search(
                    [('name_tour_guide', '=', record.emp_name.name),
                     ('date_start', '>=', record.from_date),
                     ('date_end', '<=', record.to_date)])
                record.count_tour = 0
                for r in list_detail:
                    record.working_time += parse(r.date_end).day - parse(r.date_start).day
                    record.total_guests += r.total_guests
                    record.count_tour += 1

    @api.multi
    @api.depends('planning_name', 'emp_salary', 'planning_list_kpi')
    def compute_salary(self):
        for record in self:
            record.total_salary = record.emp_salary
            for r in record.planning_list_kpi:
                if record.planning_kpi_type == 'tour':
                    if record.count_tour >= r.number:
                        record.achieve_kpi = r.number
                        if r.calculation_method == 'phantram':
                            record.total_salary = record.emp_salary + (record.emp_salary * r.money) / 100
                        if r.calculation_method == 'vnd':
                            record.total_salary = record.emp_salary + r.money
                if record.planning_kpi_type == 'people':
                    if record.total_guests >= r.number:
                        if r.calculation_method == 'phantram':
                            record.total_salary = record.emp_salary + (record.emp_salary * r.money) / 100
                        if r.calculation_method == 'vnd':
                            record.total_salary = record.emp_salary + r.money
                        record.achieve_kpi = r.number

            # Lương sau khi đóng thuế thu nhập cá nhân
            if record.total_salary <= 5000000:
                record.personal_income_tax = (record.total_salary * 5) / 100
            if 5000000 < record.total_salary <= 10000000:
                record.personal_income_tax = (record.total_salary * 10) / 100
            if 10000000 < record.total_salary <= 18000000:
                record.personal_income_tax = (record.total_salary * 15) / 100
            if 18000000 < record.total_salary <= 32000000:
                record.personal_income_tax = (record.total_salary * 20) / 100
            if 32000000 < record.total_salary <= 52000000:
                record.personal_income_tax = (record.total_salary * 25) / 100
            if 52000000 < record.total_salary <= 80000000:
                record.personal_income_tax = (record.total_salary * 30) / 100
            if record.total_salary > 80000000:
                record.personal_income_tax = (record.total_salary * 35) / 100

            record.total_salary = record.total_salary - record.personal_income_tax
