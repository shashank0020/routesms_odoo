# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name' : 'ROUTESMS',
    'version': '1.0',
    'author' : 'BISTA SOLUTIONS',
    'website' : 'http://bistasolutions.com/',
    'category': 'Dependency',
    'depends' : ['base','account','hr','sale','crm','product','mail','sale_crm','account_financial_report_webkit'],
    'description': """
Module for ROUTESMS.
    """,
    'data': [
        'data/report_paperformat.xml',             
        'templates.xml',
        'res_partner_sequence.xml',
        'res_partner_view.xml',
        'vertical_view.xml',
        'res_company_view.xml',
         'account_view.xml',
#         'fiscal_rule_view.xml',
        'sale_view.xml',
	'hr_view.xml',
        'crm_view.xml',
        'res_user_view.xml',
        'travel_view.xml',
        'authenticate_view.xml',
        'security/routesms_security.xml',
        'wizard/routesms_wizard_view.xml',
        'wizard/send_mail_wizard_view.xml',
        'product_view.xml',
        'account_invoice_sequence.xml',
        'res_bank_partner_view.xml',
        'setting_view.xml',
#        'auction_view.xml',
        'views/report_cheque.xml',
        'views/routesms_invoice.xml',
#        'views/report_check.xml',
        'views/report_sale_order.xml',
        'views/report_petty_cash.xml',
        'views/report_petty_cash2.xml',
        'views/report_petty_cash3.xml',
        'views/report_petty_pnr.xml',
        'views/report_source_document.xml',        
        #'views/print_cheque_updated.xml',
        'views/report_sale_purchase.xml',
        'views/icic_bank_report.xml',
        'views/hdfc_bank_report.xml',
        'views/routesms_header_footer.xml',
        'account_voucher_sequence.xml',
        'routesms_report_view.xml',
        'mail.xml'
        
        
      #  'security/ir.model.access.csv',
        
    ],
#    'qweb': [
#        "static/src/xml/web.xml",
#    ],
    'qweb': ['static/src/xml/*.xml'],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
