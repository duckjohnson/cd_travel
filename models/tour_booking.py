# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError
from datetime import date
from dateutil.parser import parse


class TourBooking(models.Model):
    _name = 'cd.travel.tour.booking'
    _inherit = ['mail.thread']
    _description = 'cd travel tour booking'
    _rec_name = 'code_booking'

    code = fields.Char(string='id', default=lambda self: _('New'), readonly=True)
    code_booking = fields.Char(string='Mã đặt tour', readonly=True, compute='compute_set_code_booking')

    adults = fields.Integer(string='Người lớn')
    adults_price = fields.Float(string='Giá người lớn', readonly=True, compute='compute_price_adults')
    child = fields.Integer(string='Trẻ em')
    child_price = fields.Float(string='Giá trẻ em', readonly=True, compute='compute_price_child')
    kid = fields.Integer(string='Trẻ nhỏ')
    kid_price = fields.Float(string='Giá Trẻ nhỏ', readonly=True, compute='compute_price_kid')
    baby = fields.Integer(string='Sơ sinh')
    baby_price = fields.Float(string='Giá sơ sinh', readonly=True, compute='compute_price_baby')
    single_room = fields.Integer(string='Phòng đơn')
    single_room_price = fields.Float(string='Phụ thu phòng đơn', compute='compute_price_single_room')
    guest_number = fields.Integer(string='Số khách', readonly=True, compute='compute_guest_number')
    tmp_seats = fields.Integer(string='số ghế còn', readonly=True, compute='compute_guest_number')
    total_converts = fields.Integer(string='tổng số người chuyển đổi', readonly=True, compute='compute_guest_number')
    amount = fields.Float(string='Tổng tiền', readonly=True, compute='compute_amount_final')
    deposit = fields.Float(string='Số tiền cọc', readonly=True, compute='compute_amount_final')
    deposit_lost = fields.Float(string='Phí hủy tour', readonly=True, compute='compute_deposit_lost')
    total_payment = fields.Float(string='Tổng tiền đã thanh toán', readonly=True, compute='compute_total_payment')
    remaining_amount = fields.Float(string='Số tiền còn lại', compute='compute_remaining_amount')
    payment_to_customer = fields.Float(string='Số tiền trả lại', compute='compute_payment_to_customer')

    sale = fields.Char(string='sale', compute='compute_sale', readonly=True)

    tour_detail_name = fields.Many2one('cd.travel.tour.detail', string='Tên chuyến', required=True)
    tour_detail_code = fields.Char(string='Mã chuyến', related='tour_detail_name.code', readonly=True)
    tour_detail_deposit = fields.Integer(string='Tỷ lệ cọc(%)', related='tour_detail_name.deposit_ratio', readonly=True)
    tour_detail_date_start = fields.Date(string='Ngày khởi hành', related='tour_detail_name.date_start', readonly=True)
    tour_detail_date_end = fields.Date(string='Ngày kết thúc', related='tour_detail_name.date_end', readonly=True)
    tour_detail_time_visit = fields.Char(string='Thời gian', related='tour_detail_name.travel_tour_time_visit',
                                         readonly=True)
    tour_detail_address_start = fields.Char(string='Điểm đón', related='tour_detail_name.travel_tour_address_start',
                                            readonly=True)
    tour_detail_time_start = fields.Char(string='Thời gian khởi hành', readonly=True,
                                         related='tour_detail_name.travel_tour_time_start')
    tour_detail_time_drop_off = fields.Char(string='Thời gian đến', readonly=True,
                                            related='tour_detail_name.travel_tour_time_drop_off')
    tour_detail_time_address_come = fields.Char(string='Điểm đến', readonly=True,
                                                related='tour_detail_name.travel_tour_time_address_come')
    tour_detail_time_come = fields.Char(string='Thời gian về', related='tour_detail_name.travel_tour_time_come',
                                        readonly=True)
    tour_detail_time_pick_up = fields.Char(string='Thời gian kết thúc', readonly=True,
                                           related='tour_detail_name.travel_tour_time_pick_up')
    tour_detail_remaining_seats = fields.Integer(string='Số ghế còn lại', related='tour_detail_name.remaining_seats',
                                                 readonly=True)
    tour_detail_seats_number = fields.Integer(string='Số ghế', related='tour_detail_name.vehicle_seats',
                                              readonly=True)
    tour_detail_price = fields.Float(string='Giá tour', related='tour_detail_name.price', readonly=True)

    customer_name = fields.Many2one('cd.travel.customer', string='Tên khách hàng')
    customer_identity = fields.Char(string='CCCD or Passport', related='customer_name.identity', readonly=True)
    customer_DOB = fields.Date(string='Ngày sinh', related='customer_name.DOB', readonly=True)
    customer_phone = fields.Char(string='SĐT', related='customer_name.phone', readonly=True)
    customer_email = fields.Char(string='Email', related='customer_name.email', readonly=True)
    customer_address = fields.Char(string='Địa chỉ', related='customer_name.address', readonly=True)
    customer_gender = fields.Selection([
        ('boy', 'Nam'),
        ('girl', 'Nữ')],
        string='Giới tính', related='customer_name.gender', readonly=True
    )

    list_invoice_booking = fields.One2many('cd.travel.invoice', 'booking_code', string='Danh sách thanh toán',
                                           domain=[('state', '=', 'paid')])

    state = fields.Selection([
        ('inactive', 'Chưa xác nhận'),
        ('active', 'Đã xác nhận'),
        ('pay_off', 'Đã thanh toán'),
        ('cancel', 'Đã hủy'), ],
        string='Trạng thái', default='inactive', track_visibility='onchange'
        #     compute='compute_change_state',
    )

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['code'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code(
                    'tour.booking.sequence') or _('New')
            else:
                vals['code'] = self.env['ir.sequence'].next_by_code('tour.booking.sequence') or _('New')
        result = super(TourBooking, self).create(vals)
        return result

    @api.multi
    @api.depends('total_payment', 'deposit_lost')
    def compute_payment_to_customer(self):
        for record in self:
            if record.state == 'cancel':
                record.payment_to_customer = record.total_payment - record.deposit_lost

    @api.multi
    @api.depends('amount', 'total_payment')
    def compute_remaining_amount(self):
        for record in self:
            record.remaining_amount = record.amount - record.total_payment

    @api.multi
    @api.depends('list_invoice_booking', 'list_invoice_booking.payment_amount')
    def compute_total_payment(self):
        for record in self:
            for r in record.list_invoice_booking:
                record.total_payment += r.payment_amount

    @api.multi
    @api.depends('state', 'tour_detail_date_start')
    def compute_deposit_lost(self):
        for record in self:
            if record.state == 'cancel':
                if parse(record.tour_detail_date_start).day - date.today().day < 20 and parse(
                        record.tour_detail_date_start).day - date.today().day >= 10:
                    record.deposit_lost = (record.deposit * 30) / 100
                if parse(record.tour_detail_date_start).day - date.today().day < 10 and parse(
                        record.tour_detail_date_start).day - date.today().day >= 3:
                    record.deposit_lost = (record.deposit * 50) / 100
                if parse(record.tour_detail_date_start).day - date.today().day < 3 and parse(
                        record.tour_detail_date_start).day - date.today().day >= 0:
                    record.deposit_lost = record.deposit

    @api.multi
    @api.depends('code', 'tour_detail_name', 'tour_detail_name.name')
    def compute_set_code_booking(self):
        for record in self:
            record.code_booking = str(record.tour_detail_name.name) + '/' + str(record.code)

    @api.multi
    @api.depends('tour_detail_name', )
    def compute_sale(self):
        for record in self:
            if record.tour_detail_name.sale_type == 'phantram':
                record.sale = str(record.tour_detail_name.sale_amount) + '  %'
            if record.tour_detail_name.sale_type == 'vnd':
                record.sale = str(record.tour_detail_name.sale_amount) + '  vnd'

    @api.multi
    @api.depends('tour_detail_price', 'adults')
    def compute_price_adults(self):
        for record in self:
            record.adults_price = record.tour_detail_price * record.adults

    @api.multi
    @api.depends('tour_detail_price', 'child')
    def compute_price_child(self):
        for record in self:
            record.child_price = (record.tour_detail_price - (record.tour_detail_price * 25) / 100) * record.child

    @api.multi
    @api.depends('tour_detail_price', 'kid')
    def compute_price_kid(self):
        for record in self:
            record.kid_price = (record.tour_detail_price - (record.tour_detail_price * 75) / 100) * record.kid

    @api.multi
    @api.depends('tour_detail_price', 'baby')
    def compute_price_baby(self):
        for record in self:
            record.baby_price = (record.tour_detail_price - (record.tour_detail_price * 97) / 100) * record.baby

    @api.multi
    @api.depends('tour_detail_price', 'single_room')
    def compute_price_single_room(self):
        for record in self:
            record.single_room_price = (record.tour_detail_price - (
                    record.tour_detail_price * 65) / 100) * record.single_room

    @api.multi
    @api.depends('adults_price', 'child_price', 'kid_price', 'baby_price', 'single_room_price', 'tour_detail_name',
                 'tour_detail_name.sale_type', 'tour_detail_name.sale_amount')
    def compute_amount_final(self):
        for record in self:
            price_sale = 0
            for r in record.tour_detail_name:
                if r.sale_type == 'phantram':
                    price_sale = (record.tour_detail_price * r.sale_amount) / 100
                if r.sale_type == 'vnd':
                    price_sale = r.sale_amount
                record.amount = record.adults_price + record.child_price + record.kid_price + record.baby_price \
                                + record.single_room_price - price_sale
                record.deposit = (record.amount * record.tour_detail_deposit) / 100

    @api.multi
    @api.depends('adults', 'child', 'kid', 'baby', 'tour_detail_remaining_seats')
    def compute_guest_number(self):
        for record in self:
            record.guest_number = record.adults + record.child + record.kid + record.baby
            record.total_converts = record.adults + record.child + record.kid / 2 + record.baby / 4
            record.tmp_seats = record.tour_detail_seats_number - record.total_converts
            # if record.tour_detail_remaining_seats < 0:
            #     raise UserError('số khách vượt quá số lượng ghế trống vui lòng chọn lại')

    # def compute_change_state(self):
    #     for record in self:
    #         count = self.env['cd.travel.invoice'].search_count([('booking_code', '=', record.code)])
    #         if count != 0:
    #             record.state = 'active'
    #         else:
    #             record.state = 'inactive'

    # @api.constrains('adults')
    # def validate_adults(self):
    #     if self.adults < 0:
    #         raise UserError('Số người lớn sai định dạng, vui lòng nhập giá trị lớn hơn hoặc bằng 1')
    #
    # @api.constrains('child')
    # def validate_child(self):
    #     if self.child < 0:
    #         raise UserError('Số trẻ em sai định dạng, Vui lòng nhập giá trị lớn hơn hoặc bằng 1')
    #
    # @api.constrains('kid')
    # def validate_kid(self):
    #     if self.kid < 0:
    #         raise UserError('Số trẻ nhỏ sai định dạng, Vui lòng nhập giá trị lớn hơn hoặc bằng 1')
    #
    # @api.constrains('baby')
    # def validate_baby(self):
    #     if self.baby < 0:
    #         raise UserError('Số sơ sinh sai định dạng,Vui lòng nhập giá trị lớn hơn hoặc bằng 1')

    # @api.constrains('guest_number')
    # def validate_guest_number(self):
    #     if self.guest_number > self.tour_detail_remaining_seats:
    #         raise UserError('Số khách phải nhỏ hơn or bằng số ghế trống')
