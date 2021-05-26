# -*- coding: utf-8 -*-\
import datetime

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


class TourDetail(models.Model):
    _name = 'cd.travel.tour.detail'
    _description = 'cd travel tour guide'
    _rec_name = 'name'

    code = fields.Char(string='Mã chi tiết', default=lambda self: _('New'), readonly=True)
    name = fields.Char(string='Tên chi tiết', compute='compute_set_name', required=True)
    date_start = fields.Date(string='Ngày đi', required=True)
    date_end = fields.Date(string='Ngày về', required=True)
    time_focus = fields.Char(string='Thời gian tập trung')
    deposit_ratio = fields.Integer(string='Tỷ lệ cọc(%)')
    revenue = fields.Float(string='Tổng thu', compute='compute_revenue')
    debt = fields.Float(string='Tiền còn thiếu', compute='compute_debt')
    seats_min = fields.Integer(string='Số ghế thấp nhất', readonly=True, compute='compute_seats_min')
    price = fields.Float(string='Giá', compute='compute_price', readonly=True)
    total_guests = fields.Float(string='Tổng khách phục vụ', compute='compute_total_guests')
    note = fields.Text(string='Ghi chú')

    list_booking_detail = fields.One2many('cd.travel.tour.booking', 'tour_detail_name', string='Danh sách booking',
                                          domain=[('state', '!=', 'cancel')])

    booking_seats = fields.Integer(string='Số ghế đã đặt', compute='compute_seats')
    remaining_seats = fields.Integer(string='Số ghế còn lại', compute='compute_seats')

    travel_tour_name = fields.Many2one('cd.travel.tour.travel', string='Tên tour', required=True)
    travel_tour_time_visit = fields.Char(string='Thời gian', related='travel_tour_name.time_visit')
    travel_tour_address_start = fields.Char(string='Điểm đón', related='travel_tour_name.address_start')
    travel_tour_time_start = fields.Char(string='Thời gian khởi hành', related='travel_tour_name.time_start')
    travel_tour_time_drop_off = fields.Char(string='Thời gian đến', related='travel_tour_name.time_drop_off')
    travel_tour_time_address_come = fields.Char(string='Điểm đến', related='travel_tour_name.address_come')
    travel_tour_time_come = fields.Char(string='Thời gian về', related='travel_tour_name.time_come')
    travel_tour_time_pick_up = fields.Char(string='Thời gian kết thúc', related='travel_tour_name.time_pick_up')
    travel_tour_price = fields.Float(string='Giá tour', related='travel_tour_name.price', readonly=True)
    travel_tour_vehicle = fields.Selection([
        ('planes', 'Máy bay'),
        ('coach', 'xe khách')],
        string='Phương tiện', related='travel_tour_name.vehicle', readonly=True
    )

    vehicle_name = fields.Many2one('cd.travel.vehicle', string='Mã chuyến bay or biển số xe',
                                   domain=[('state', '=', 'free_time')])
    vehicle_seats = fields.Integer(string='Số ghế tối đa', related='vehicle_name.seats', readonly=True)
    vehicle_driver_name = fields.Many2one(string='Tên tài xế', related='vehicle_name.driver_name', readonly=True, )
    vehicle_driver_phone = fields.Char(string='Điện thoại tài xế', related='vehicle_name.driver_name.phone')

    name_tour_guide = fields.Many2one('cd.travel.employee', string='Tên hướng dẫn viên',
                                      domain=[('position_name', '=', 'guide'), ('state', '=', 'free_time')])
    phone_tour_guide = fields.Char(string='Điện thoại', related='name_tour_guide.phone')

    sale_name = fields.Many2one('cd.travel.info.sale', string='Tên sale')
    sale_type = fields.Selection([
        ('phantram', 'Phần trăm'),
        ('vnd', 'VND')],
        string='Đơn vị', related='sale_name.type', readonly=True)
    sale_amount = fields.Float(string='sale', related='sale_name.amount', readonly=True)

    state = fields.Selection([
        ('still_empty', 'Còn chỗ'),
        ('full', 'Đã đủ'),
        ('end', 'Đã kết thúc')],
        string='Trạng thái', default='still_empty', track_visibility='onchange'
        # , compute='compute_seats'
    )
    active = fields.Boolean(default=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['code'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code(
                    'tour.detail.sequence') or _('New')
            else:
                vals['code'] = self.env['ir.sequence'].next_by_code('tour.detail.sequence') or _('New')
        result = super(TourDetail, self).create(vals)
        return result

    @api.multi
    @api.depends('list_booking_detail', 'list_booking_detail.total_converts')
    def compute_total_guests(self):
        for record in self:
            for r in record.list_booking_detail:
                record.total_guests += r.total_converts

    @api.multi
    @api.depends('vehicle_seats')
    def compute_seats_min(self):
        for record in self:
            record.seats_min = (record.vehicle_seats * 60) / 100

    @api.multi
    @api.depends('travel_tour_price', 'sale_type', 'sale_amount')
    def compute_price(self):
        for record in self:
            record.price = record.travel_tour_price
            if record.sale_type == 'phantram':
                record.price = record.travel_tour_price - (record.travel_tour_price * record.sale_amount) / 100
            if record.sale_type == 'vnd':
                record.price = record.travel_tour_price - record.sale_amount

    @api.multi
    @api.depends('list_booking_detail', 'list_booking_detail.guest_number', 'vehicle_seats',
                 'list_booking_detail.state')
    def compute_seats(self):
        for record in self:
            for r in record.list_booking_detail:
                if r.state == 'active' or r.state == 'pay_off':
                    record.booking_seats += r.guest_number - r.baby
            record.remaining_seats = record.vehicle_seats - record.booking_seats
            # for r in record.travel_tour_name:
            #     if record.booking_seats == r.seats_number:
            #         record.state = 'full'
            #     else:
            #         record.state = 'still_empty'

    @api.multi
    @api.depends('travel_tour_name', 'travel_tour_name.code', 'date_start')
    def compute_set_name(self):
        for record in self:
            record.name = str(record.travel_tour_name.code) + '/' + str(record.date_start)

    @api.multi
    def open_invoice_appointment(self):
        return {
            'name': _('Invoice'),
            'domain': [('booking_tour_detail_code', '=', self.code)],
            'view_type': 'form',
            'view_mode': 'tree, from',
            'res_model': 'cd.travel.invoice',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new'
        }

    @api.multi
    @api.depends('list_booking_detail', 'list_booking_detail.total_payment')
    def compute_revenue(self):
        for record in self:
            for r in record.list_booking_detail:
                record.revenue += r.total_payment

    @api.multi
    @api.depends('list_booking_detail', 'list_booking_detail.remaining_amount')
    def compute_debt(self):
        for record in self:
            for r in record.list_booking_detail:
                record.debt += r.remaining_amount

    # @api.constrains('go_time', 'arrival_time')
    # def validate_arrival_time(self):
    #     if datetime.datetime.strptime(self.arrival_time, '%Y-%m-%d %H:%M:%S') < datetime.datetime.strptime(
    #             self.go_time, '%Y-%m-%d %H:%M:%S'):
    #         raise UserError('thời gian đến phải sau thời gian đi')
    #
    # @api.constrains('arrival_time', 'time_back')
    # def validate_time_back(self):
    #     if datetime.datetime.strptime(self.time_back, '%Y-%m-%d %H:%M:%S') < datetime.datetime.strptime(
    #             self.arrival_time, '%Y-%m-%d %H:%M:%S'):
    #         raise UserError('thời gian về phải sau thời gian đến')
    #
    # @api.constrains('time_back', 'time_end')
    # def validate_time_end(self):
    #     if datetime.datetime.strptime(self.time_end, '%Y-%m-%d %H:%M:%S') < datetime.datetime.strptime(
    #             self.time_back, '%Y-%m-%d %H:%M:%S'):
    #         raise UserError('thời gian kết thúc phải sau thời gian về')
    #
    # @api.constrains('go_time', 'time_focus')
    # def validate_time_focus(self):
    #     if datetime.datetime.strptime(self.go_time, '%Y-%m-%d %H:%M:%S') < datetime.datetime.strptime(
    #             self.time_focus, '%Y-%m-%d %H:%M:%S'):
    #         raise UserError('thời gian tập trung phải trước thời gian đi')
