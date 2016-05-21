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
#import ipdb;ipdb.set_trace()
import datetime
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
from datetime import date
import csv
from num2words import num2words
import urllib2
import datetime,time
import requests
import string
SUPERUSERID=1


class authenticate_users(models.Model): 
    _name = "authenticate.users"
    _description = "Authenticate User Account Applications "
    _inherit = ['ir.needaction_mixin']
    _order ='creation_date desc'

    creation_date=fields.Datetime(string='Creation Date')   
    updation_date=fields.Datetime(string='Updated On')
    create_record=fields.Boolean(string='Create Record',default=False)
    type=fields.Selection([('pending', 'Pending'),('approved','Approved'),('rejected','Rejected')],string='Type') 
    name=fields.Char(string='Partner')
    odoo_id=fields.Char(string='Odoo Id') 
    account_type=fields.Char(string='Account Type')
    partner_id=fields.Many2one('res.partner',string='Partner Id')
    user_obj=fields.Many2one('res.partner.add.user',string='User Obj')
    user_name=fields.Char(string='User')
    server = fields.Many2one('server',string='Server')
    local_price = fields.Float(string='Local Price',digits=(32, 4))
    od_limit = fields.Float(string='OD Limit') 
    credit_limit = fields.Float(string='Credit Limit')
    user_id = fields.Many2one('res.users',string='Salesperson')
    employee_id = fields.Many2one('hr.employee',string='Employee')
    reason_to_reject = fields.Char(string='Rejection Reason')
    rejected_by = fields.Many2one('res.users',string='Rejected By')
    rejected_by_name = fields.Char(string='Rejected By')
    record_read = fields.Boolean(string='Read Message',default=False)
    reseller_code = fields.Char(string='Reseller Code',size=4)
    distributor_code = fields.Char(string='Distributor Code',size=4)
    route_type = fields.Selection([('promotional', 'Promotional'),('transactional','Transactional'),\
                                 ('both','Both'), ('transcrub','TranScrub')],string='Route Type')
    routesms_notes = fields.Text(string='Comments',size=100)
    is_local_server = fields.Boolean(string='Local Server?',default=False)
    business_manager=fields.Many2one('res.users',string='Salesperson')
    is_active = fields.Boolean(string='Active')
    agreement=fields.Selection([('yes','Yes'),('no','No')],string='Agreement')
    approved_by_name = fields.Char(string='Approved By')
    user_email_temp = fields.Char(string='User Email') 

    commercial_name_phone = fields.Char(string='Commercial Name/Phone')    
    commercial_email = fields.Text(string='Commercial Email')

    price_notification_name_phone = fields.Char(string='Price Notification Name/Phone')    
    price_notification_email = fields.Text(string='Accounts Email')
        
    account_name_phone = fields.Char(string='Accounts Name/Phone')    
    account_email = fields.Text(string='Account Email')
    
    technical_name_phone = fields.Char(string='Technical Name/Phone')    
    technical_email = fields.Text(string='Technical Email')
    user_account_phone_number = fields.Char(string='Phone')
    manage_subroute=fields.Many2one('subroute',string='Manage Subroute')



    @api.model
    def create(self,values): 
        ''' inherit self create'''
        
        try :
             
            assert values.get('create_record'),'You Cannot Create This Document'
            result=super(authenticate_users,self).create(values)
          
        except Exception as E : 
            raise osv.except_osv(_('Error'),
                            _('{} ').format(E.message))        
        return result

    @api.multi
    def write(self,values): 

        try : 
            
            if 'od_limit' in values or 'local_price' in values :
                 
                credit_limit=self.validate_pricing(values)
                values['credit_limit']=credit_limit

        except Exception as E : 
            raise osv.except_osv(_('Error'),
                            _('{} ').format(E.message))        
            
        return super(authenticate_users,self).write(values)

    @api.multi
    def browse_list(self):
        '''holds list of all browse objects for resuse code purpose '''
        def get_browse_obj(self,func):
            ''' get browse object on demand'''
            func.partner_obj=self.env['res.partner']
            func.add_user_obj=self.env['res.partner.add.user']
            func.hr_obj=self.env['hr.employee']
            func.odoo_rsl_api_obj=self.env['odoo.rsl.api']
            return func
        return get_browse_obj(self,get_browse_obj)

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
        
        try : 
            if view_type=='tree' and view_id:
                request_type=self.env.context['type']
                assert request_type,'Technical Issue\nFail To Load Page\nRequest Type NoT Found In Context\n\
                Contact Odoo Team'
                if request_type=='pending' :
                    self.env.cr.execute('''update authenticate_users set record_read=True where user_id=%s and \
                    type='pending' ''',(self.env.uid,))
                    
                    
                elif request_type=='approved' : 
                    self.env.cr.execute('''update authenticate_users set record_read=True where user_id=%s and \
                    type='approved' ''',(self.env.uid,)) 
    
                elif request_type=='rejected' :
                    self.env.cr.execute('''update authenticate_users set record_read=True where user_id=%s and \
                    type='rejected' ''',(self.env.uid,))                 
                                
                else :
                    raise osv.except_osv(_('Error!'), _('Technical Issue\nFail To Load Page\nContact Odoo Team'))
                
        except Exception as E:
            if not E.message : 
                E.message=E.value   
                           
            raise osv.except_osv(_('Error'),_('{} ').format(E.message))
        res = super(authenticate_users, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        return res
    
    @api.model
    def _needaction_domain_get(self):
        res=super(authenticate_users,self)._needaction_domain_get()
        return [('record_read', '=', False)]

        
    @api.multi
    def validate_pricing(self,pricing):
        '''validate price price as per buisness flow '''
        credit_limit = 0.0
        assert pricing.get('od_limit', 0.0 ) >= 0,'Invalid OD Limit Amount\nOD Limit Must Be Greater Than 0.0'   
        if self.server.type in ["reseller", "distributor"] and self.server.locality == "local" : 
            assert pricing.get('local_price', 0.0 ) >= 0,'Invalid Local Price\nNegative Amount Not Allowed'
        if self.sudo().partner_id.postpaid :   
            credit_limit= pricing.get('od_limit')  
        return credit_limit
        
    @api.multi    
    def manage_subrouting(self, user_obj, mode):
        '''create manage subroute link for only india reseller and distributor server '''
        subroute_obj = self.env["subroute"]
        subroute_line_obj = self.env["subroute.line"]
        subroute_id = False        
        # IF REJECT CHANGE STATUS OF SUBROUTE TO REJECT FOR ROUTENAME !=APPROVED
        
        try :
            if mode == "reject" :
                # REJECTING FRESH USER ACCOUNT 
                if not user_obj.manage_subroute : 
                    return True
                
                subrouting = user_obj.manage_subroute
                # GETTING PROMOTIONAL DATA
                subroute_line_promotional = subroute_line_obj.search([("subroute_id_promotional","=",subrouting.id), ("status","=","pending")])

                for promotional_line in  subroute_line_promotional :
                    promotional_line.write({"status" : "rejected"})
                    
                # GETTING TRANSACTIONAL DATA
                subroute_line_transactional = subroute_line_obj.search([("subroute_id_transactional","=",subrouting.id), ("status","=","pending")])
                for transactional_line in  subroute_line_transactional :
                    import ipdb;ipdb.set_trace() 
                    transactional_line.write({"status" : "rejected"})
                                
                return True 

         

            if not user_obj.manage_subroute  :
                
                if user_obj.server_domain.type in ["reseller", "distributor"] and user_obj.server_domain.locality == "local" :  
                    # CREATE NEW RECORD OF SUBROUTE AND LINK IT TO USER ACCOUNT 
                    values = dict (name = "Manage Subroute" + " " + user_obj.username, username = user_obj.username,\
                                   server = user_obj.server_domain.id, res_partner_add_user_id = user_obj.id,
                                   )
                    # SUBROUTE CREATED SUCCESSFULLY AND MAPPED WITH USER ACCOUNT
                    subroute_id = subroute_obj.sudo().create(values).id
            else : 
                
                #manage_subroute = subroute_obj.sudo().browse(user_obj.manage_subroute)
                # CONFIRM SUBROUTE DETAILS AND USER THEN CANNOT MODIFY AGAIN

                subroute_id = user_obj.manage_subroute.id
                    
        except Exception as E : 
            raise osv.except_osv(_('Error'),_('{} ').format(E.message))
        return subroute_id
        
    @api.multi
    def approve(self) : 
        ''' approve user form '''
        try :
            
            obj=self.browse_list()
            high_authority=['Director Sales','CEO','BOD']
            self=self.sudo()
            
            assert not self.reason_to_reject,'You Cannot Specify Rejection Reason During Approval'
            
            if self.employee_id.job_id.name in high_authority :
                # THIS IS FINAL APPROVE FROM TOP LEVEL USER 
                
                partner_user=obj.add_user_obj.sudo().browse(self.user_obj.id)
                partner_user.approved_by=[self.user_id.id]
                partner_user.status='approved'
                approved_by = str([str(user_id.name) for user_id in partner_user.approved_by  ] ).\
                translate(string.maketrans( '', '', ),"[]'")
                partner_user.approved_by_name = approved_by
                partner_user.local_price= self.local_price
                partner_user.od_limit= self.od_limit
                partner_user.credit_limit=self.credit_limit
                user_created_by_emp=obj.hr_obj.get_user_detail(self.partner_id.user_id.id)
                
                partner_user.manage_subroute = self.manage_subrouting (self.user_obj, mode="approve")
                
                vals={'type':'approved','user_id':self.partner_id.user_id.id,\
                      'employee_id':user_created_by_emp.id,'record_read':False, 'approved_by_name' : approved_by}

                self.write(vals)
                # THIS IS FINAL APPROVAL -POST DATA TO RSL SERVER
		
                obj.odoo_rsl_api_obj.user_account_post_data(self.server, partner_user, user_created_by_emp,\
                                "create" if not self.updation_date else "update") 

                # REMOVE RESTORED STATE OF USER ACCOUNT LIKE PRICES
                if self.updation_date : 
                    obj.partner_obj.unlink_restore_user_detail_directly (self.user_obj)
                
                return { 
                    'type': 'ir.actions.client',
                    'tag': 'reload_context',
                }
    
            else:
                # THIS IS APPROVAL FROM MID LEVEL USERS
                partner_user=obj.add_user_obj.sudo().browse(self.user_obj.id)
                partner_user.approved_by=[self.user_id.id]
                approved_by = str([str(user_id.name) for user_id in partner_user.approved_by  ] ).\
                translate(string.maketrans( '', '', ),"[]")
                partner_user.approved_by_name = approved_by
               
                self.write({'user_id':self.employee_id.parent_id.user_id.id,\
                            'employee_id':self.employee_id.parent_id.id,'record_read':False})
                return True
            raise osv.except_osv(_("Error!"), _("User Form Approval Failed\nTechnical Error\nContact Odoo Team"))
        except Exception as E : 
            if not E.message : 
                E.message=E.value   
                           
            raise osv.except_osv(_('Error'),_('{} ').format(E.message))            
            

    @api.multi
    def reject(self) : 
        '''reject user form '''
        try :
            
            obj=self.browse_list()
            self=self.sudo()
            
            #################Delete user from users lists################
            assert self.reason_to_reject,'Enter Rejection Reason'
            # RESTORE PREVIOUS STATE OF USER ACCOUNT LIKE PRICES
            if self.updation_date : 
                obj.partner_obj.restore_user_detail (self.user_obj)
            
            else : 
                obj.add_user_obj.sudo().browse(self.user_obj.id).unlink()
            #############delete user form#################3
            user_created_by_emp=obj.hr_obj.get_user_detail(self.partner_id.user_id.id)
            vals={'user_id':self.partner_id.user_id.id,'employee_id':user_created_by_emp.id,'type':'rejected',\
                  'rejected_by':self.user_id.id,'rejected_by_name':self.user_id.name}
            
            # UPDATE SUBROUTE STATUS
            self.manage_subrouting (self.user_obj, mode="reject")
            
            self.write(vals)
        except Exception as E : 
            if not E.message : 
                E.message=E.value   
                           
            raise osv.except_osv(_('Error'),_('{} ').format(E.message))        
        
        return True
         

