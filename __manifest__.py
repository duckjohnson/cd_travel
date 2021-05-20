# -*- coding: utf-8 -*-

{
    'name': 'CD travel',
    'version': '0.1',
    'author': 'congnguyen',
    'category': 'CD travel',
    'license': 'AGPL-3',
    'sequence': 1,
    'summary': 'CD travel',
    'description': """CD travel""",
    'website': 'http://www.cdtravel.com',
    'images': [],
    'depends': ['base', 'mail'],
    'data': ['data/ir_sequence_data.xml',
             'data/mail_template.xml',
             # 'data/web_data.xml',
             'security/cd_travel_security.xml',
             'security/ir.model.access.csv',
             'views/travel_type.xml',
             'views/travel_region.xml',
             'views/travel_address.xml',
             'views/travel_tour.xml',
             'views/travel_news.xml',
             'views/travel_handbook.xml',
             'views/travel_exp.xml',
             'views/travel_contact.xml',
             'views/tour_guide.xml',
             'views/tour_detail.xml',
             'views/tour_image.xml',
             'views/customer.xml',
             'views/sale.xml',
             'views/tour_booking.xml',
             'views/invoice.xml',
             'views/vehicle.xml',
             'views/vehicle_operating_fee.xml',
             'views/employee.xml',
             'views/position.xml',
             # 'views/web_home.xml',
             'views/web_contact.xml',
             'reports/report.xml',
             'reports/invoice_card.xml',
             ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
