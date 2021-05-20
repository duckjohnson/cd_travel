# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


class TravelTour(models.Model):
    _name = 'cd.travel.tour.travel'
    _inherit = ['mail.thread']
    _description = 'cd travel tour travel'
    _rec_name = 'name'

    code = fields.Char(string='Mã tour', default=lambda self: _('New'), readonly=True)
    name = fields.Char(string='Tên tour', required=True)
    time_visit = fields.Char(string='Thời gian', required=True)
    address_start = fields.Char(string='Điểm đón', required=True)
    address_come = fields.Char(string='Điểm đến', required=True)
    time_start = fields.Char(string='Thời gian khởi hành', required=True)
    time_drop_off = fields.Char(string='Thời gian trả khách', required=True)
    time_come = fields.Char(string='Thời gian đón về', required=True)
    time_pick_up = fields.Char(string='Thời gian kết thúc', required=True)
    schedule = fields.Text(string='Lịch trình', required=True)
    service = fields.Text(string='Dịch vụ bao gồm và không bao gồm', required=True)
    note = fields.Text(string='Ghi chú')
    price = fields.Float(string='Giá', required=True)
    revenue = fields.Float(string='Giá', compute='compute_revenue')
    vehicle = fields.Selection([
        ('planes', 'Máy bay'),
        ('coach', 'xe khách')],
        string='Phương tiện', default='coach', required=True
    )

    image_name = fields.One2many('cd.travel.tour.image', 'img_tour_name', string='Tên ảnh')
    image = fields.Binary(string='Ảnh', relate='image_name.image')

    name_travel_address = fields.Many2one('cd.travel.address.travel', string='Loại hình du lịch')

    list_detail = fields.One2many('cd.travel.tour.detail', 'travel_tour_name', string='Chi tiết tour')

    active = fields.Boolean(default=True, track_visibility='onchange')

    @api.multi
    @api.depends('list_detail')
    def compute_revenue(self):
        for record in self:
            for r in record.list_detail:
                record.revenue += r.revenue

    @api.constrains('price')
    def validate_price(self):
        if self.price <= 0:
            raise UserError('Giá phải lớn hơn hoặc là 0')
        if self.price % 1000 != 0:
            raise UserError('giá là bội của 1000')

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['code'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code(
                    'tour.travel.sequence') or _('New')
            else:
                vals['code'] = self.env['ir.sequence'].next_by_code('tour.travel.sequence') or _('New')
        result = super(TravelTour, self).create(vals)
        return result
