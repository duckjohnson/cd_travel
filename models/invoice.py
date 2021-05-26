# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


class Invoice(models.Model):
    _name = 'cd.travel.invoice'
    _inherit = ['mail.thread']
    _description = 'cd travel invoice'
    _rec_name = 'code_invoice'

    code = fields.Char(string='Mã hóa đơn', default=lambda self: _('New'), readonly=True)
    code_invoice = fields.Char(string='Mã hóa đơn', readonly=True, compute='compute_set_code_invoice')
    payment_amount = fields.Float(string='Số tiền thanh toán')

    booking_code = fields.Many2one('cd.travel.tour.booking', string='Mã đặt tour', required=True,
                                   domain=['|', ('state', '=', 'inactive'), ('state', '=', 'active')])

    booking_tour_adults = fields.Integer(string='Người lớn', related='booking_code.adults', readonly=True)
    booking_tour_child = fields.Integer(string='Trẻ em', related='booking_code.child', readonly=True)
    booking_tour_kid = fields.Integer(string='Trẻ nhỏ', related='booking_code.kid', readonly=True)
    booking_tour_baby = fields.Integer(string='Sơ sinh', related='booking_code.baby', readonly=True)
    booking_tour_single_room = fields.Integer(string='Phòng đơn', related='booking_code.single_room', readonly=True)
    booking_tour_guest_number = fields.Integer(string='Số khách', related='booking_code.guest_number', readonly=True)
    booking_tour_sale = fields.Char(string='Sale', related='booking_code.sale', readonly=True)
    booking_tour_amount = fields.Float(string='Thành tiền', related='booking_code.amount', readonly=True)

    booking_tour_detail_name = fields.Many2one(string='tên chi tiết', related='booking_code.tour_detail_name',
                                               readonly=True)
    booking_tour_detail_code = fields.Char(string='mã chi tiết', related='booking_code.tour_detail_name.code')

    booking_tour_name = fields.Many2one(string='Tên chuyến', related='booking_code.tour_detail_name', readonly=True)
    booking_tour_code = fields.Char(string='Mã chuyến', related='booking_code.tour_detail_code', readonly=True)
    booking_tour_time_visit = fields.Char(string='Thời gian', related='booking_code.tour_detail_time_visit',
                                          readonly=True)
    booking_tour_time_start = fields.Date(string='Khởi hành', related='booking_code.tour_detail_date_start',
                                          readonly=True)
    booking_tour_address_start = fields.Char(string='Nơi khởi hành', readonly=True,
                                             related='booking_code.tour_detail_address_start')
    booking_tour_price = fields.Float(string='Giá tour', related='booking_code.tour_detail_price', readonly=True)
    booking_tour_deposit = fields.Float(string='Tiền Cọc', related='booking_code.deposit', readonly=True)
    booking_total_payment = fields.Float(string='Tiền đã thanh toán', related='booking_code.total_payment')
    booking_remaining_amount = fields.Float(string='Số tiền còn lại', related='booking_code.remaining_amount')

    booking_customer_name = fields.Many2one(string='Tên khách hàng', related='booking_code.customer_name',
                                            readonly=True)
    booking_customer_identity = fields.Char(string='CCCD or Passport', related='booking_code.customer_identity')
    booking_customer_DOB = fields.Date(string='Ngày sinh', related='booking_code.customer_DOB')
    booking_customer_phone = fields.Char(string='SĐT', related='booking_code.customer_phone')
    booking_customer_email = fields.Char(string='Email', related='booking_code.customer_email')
    booking_customer_address = fields.Char(string='Địa chỉ', related='booking_code.customer_address')
    booking_customer_gender = fields.Selection([
        ('boy', 'Nam'),
        ('girl', 'Nữ')],
        string='Giới tính', related='booking_code.customer_gender'
    )

    booking_vehicle_code = fields.Many2one(related='booking_code.tour_detail_name.vehicle_name', readonly=True)
    booking_driver_name = fields.Many2one(string='Tên tài xế',
                                          related='booking_code.tour_detail_name.vehicle_driver_name')
    booking_driver_phone = fields.Char(string='SĐT tài xế', readonly=True,
                                       related='booking_code.tour_detail_name.vehicle_driver_phone')

    booking_guide_name = fields.Many2one(string='Tên hướng dẫn viên', readonly=True,
                                         related='booking_code.tour_detail_name.name_tour_guide')
    booking_guide_phone = fields.Char(string='SĐT hướng dẫn viên', readonly=True,
                                      related='booking_code.tour_detail_name.phone_tour_guide')

    state = fields.Selection([
        ('unpaid', 'Chưa thanh toán'),
        ('paid', 'Đã thanh toán')],
        string='Trạng thái', default='unpaid', track_visibility='onchange'
    )

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['code'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code(
                    'invoice.sequence') or _('New')
            else:
                vals['code'] = self.env['ir.sequence'].next_by_code('invoice.sequence') or _('New')
        result = super(Invoice, self).create(vals)
        return result

    @api.multi
    def print_report(self):
        return self.env.ref('cd-travel.report_invoice_card').report_action(self)

    def action_send_card(self):
        template_id = self.env.ref('cd-travel.email_template_cd_travel_invoice').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)

    @api.multi
    @api.depends('code', 'booking_code', 'booking_code.code_booking')
    def compute_set_code_invoice(self):
        for record in self:
            record.code_invoice = str(record.booking_code.code_booking) + '/' + str(record.code)
