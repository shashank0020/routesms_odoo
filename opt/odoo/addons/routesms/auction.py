# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2012 OpenERP SA (<http://openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import datetime,time
from lxml import etree
import math
import pytz
import urlparse
import openerp
from openerp import tools, api
from openerp.osv import osv, fields
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _
from openerp import models, fields, api, _
import csv
import urllib2
import string


class res_partner_auction(models.Model):
    _name = "res.partner.auction"
    _description= "Partners For Auction"
    _order ='name'    
    partner_id=fields.Many2one('res.partner',string='Partner Id')
    name= fields.Char(string='Partner')
    partner_active= fields.Char(string='Partner Active')
    creation_date=fields.Datetime(string='Posted On')
    customer=fields.Char(string='Is customer')
    supplier=fields.Char(string='Is supplier')
    bid=fields.Boolean(string='Bid ?',default=False)
    odoo_id=fields.Char(string='Odoo Id')
    account_type=fields.Char(string='Account Type')
    country=fields.Char(string='Country')
    lead_status=fields.Char(string='Lead Status')
    participants = fields.Many2many(
        comodel_name='res.users',
        relation='participants_rel',
        column1='partner_auction_id',
        column2='user_id',
        string='Participants',
        help="Salespersons Bidding",
    ) 
    participants_names = fields.Char(string='Participants')
    
    total_participant=fields.Integer(string='No. Of Participants')
    time_left=fields.Char(compute='_compute_bid_time',string='Time Left For Bid')
    user_id=fields.Char(compute='_salesperson',string='Salesperson')


    @api.one
    @api.depends('partner_id')

    def _salesperson(self):
        '''display salesperson of partner dynamically '''
        self.user_id=self.sudo().partner_id.user_id.name


    @api.one
    def _compute_bid_time(self):
        '''time left to bid '''
        
        deadline='2016 04 01 23 00 33'#phase 1
        td=datetime.datetime.strptime(deadline, '%Y %m %d %H %M %S')-datetime.datetime.now()
        days, hours, minutes = td.days, td.seconds // 3600, td.seconds % 3600 / 60.0
        timing='{} days,{} hours'.format(days,hours)
        self.time_left =timing
        
    @api.multi
    def bid_on_partner(self): 
        '''User has bided '''

        auction=self.sudo().browse(self.id)
        self.sudo().participants=[self.env.uid]
        participants_names= str( [str(user.name) for user in auction.participants] ).\
                translate(string.maketrans( '', '', ),"[]'")        
        vals=dict(bid = True,participants_names = participants_names ,total_participant = len(auction.participants)   )
        return self.sudo().write(vals)
        
        
        
        
        
        
