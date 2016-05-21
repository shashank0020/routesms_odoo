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
SUPERUSERID=1
BOD = 1

class hr_employee(models.Model):
    _inherit = "hr.employee"
    
    routesms_username= fields.Char(string='RouteSmS Username')
    role = fields.Selection([
        ('SA', 'SuperAdmin'),
        ('AD', 'Admin'),
        ('RET', 'Retail'),
        ('ENT', 'Enterprise'),
        ('SUP', 'Support'),
        ('TECH', 'Technical'),
        ('ACC', 'Accounts'),
        ('IND', 'Independent'),
        ('SACC', 'Super Account'),
        ('junior account', 'Junior Account'),
        ], "Division",
       )    
    last_sync_date=fields.Datetime(string='Last Sync Date')
    
    @api.multi
    def get_user_detail(self,user_id): 
        ''' get employee id'''
        self=self.sudo()
        
        emp_id=self.search([('user_id','=',user_id)])
        assert emp_id,'Approving Form Failed\nEmployee Record Not Found For:{}\
            \nContact HR Department'\
            .format(emp_id.user_id.name)
        return emp_id
    
    @api.model
    def create(self,values): 
        ''' inherit employee create'''
        
        try : 
            assert values.get('user_id'),'Select Related User'
            assert values.get('department_id'),'Select Department'
            assert values.get('job_id'),'Select Job Title'
            assert values.get('role'),'Select Division'
            assert values.get('routesms_username'),'Enter RouteSmS Username'
            if values.get('job_id') != BOD : 
                assert values.get('parent_id'),'Select Manager'

            hr_ids=[  hr.user_id for hr in  self.search([('user_id','=',values['user_id'])])   ]
            assert not hr_ids,'Employee Record For {} Already Exist'.format(hr_ids[0].name)
            result=super(hr_employee,self).create(values)

          
        except Exception as E : 
            raise osv.except_osv(_('Error'),
                            _('{} ').format(E.message))        

        return result

    @api.multi
    def write(self,values): 
        ''' inherit employee create'''
        
        try : 
            
            result=super(hr_employee,self).write(values)

            assert self.user_id,'Select Related User'
            assert self.department_id,'Select Department'
            assert self.job_id,'Select Job Title'
            assert self.role,'Select Division'
            assert self.routesms_username,'Enter RouteSmS Username'
            if self.job_id.name !=  "BOD" : 
                assert self.parent_id,'Select Manager' 
            if self.active:
                hr_ids=[  hr.user_id for hr in  self.search([('user_id','=',self.user_id.id)])   ]
                assert len(hr_ids)==1,'Employee Record For {} Already Exist'.format(self.user_id.name)            
          
        except Exception as E : 
            raise osv.except_osv(_('Error'),
                            _('{} ').format(E.message))        

        return result

    @api.multi
    def post_data_to_server(self,vals):
        '''Post Data To BMXPIN '''
        post_data = vals
	#return True
        #url='http://192.168.0.13/odooapi/Controllers/controller.php' #Local
        url='http://121.241.242.102/odooapi/Controllers/controller.php' ##Live
	#import ipdb;ipdb.set_trace()
        post_response = requests.post(url=url, data=post_data)
        if post_response.json().get('error')=='Already this odoo id is assigned to manager.' : 
            return True

        assert post_response.json().get('success'),post_response.json().get('error')
        return True   


    @api.multi
    def insert_sync_date(self,employee_record):  
        '''store sync date'''
        self=employee_record
        assert self.id,'Employee Record Not Found'
        return self.write({'last_sync_date':(datetime.datetime.now() + datetime.timedelta(hours=0,minutes=0)).strftime('%Y-%m-%d %H:%M:%S')})



    @api.multi
    def sync_bm_swap(self,**kargs) : 
        '''use BM swap API to sync employee details '''
        vals=dict()
        user_obj=self.env['res.users']
        partner_record=kargs.get('partner_record')
        user_id=kargs.get('new_bm_id')
        
        assert partner_record,'Auto Synchronization To BMXPIN Failed\nPartner Record Not Found'
        assert user_id,'Auto Synchronization To BMXPIN Failed\nBusiness Manager Record Not Found'
        assert partner_record.partner_sequence,'Auto Synchronization To BMXPIN Failed\nPartner Odoo Id Not Found'
        employee_record=self.search([('user_id','=',user_id)])
        assert employee_record,'Auto Synchronization To BMXPIN Failed\nEmployee Record Not Found'
        assert len(employee_record)==1,'Auto Synchronization To BMXPIN Failed\nMultiple Employee Record Found'

        vals.update({'name':employee_record.routesms_username,\
                     'odoo_id':kargs.get('partner_record').partner_sequence,'bm_swap':'bm_swap',\
                     'old_bm':self.search([('user_id','=',kargs.get('old_bm_id'))]).routesms_username,'session_user':user_obj.browse(kargs.get('responsible')).name })
        
       ##post data to BMXPIN server
        self.post_data_to_server(vals)

        return True


    @api.multi
    def get_access_token(self,employee_rec) : 
        '''get access token of user '''
        international_user_obj=self.env['int.user']
        india_user_obj=self.env['ind.user']
        user=employee_rec.user_id
        assert user.partner_type,'Synchronization To BMXPIN Failed\nPartner Type Not Set'
        international_user=international_user_obj.search([('name','=',user.id)])
        if international_user :
            assert len(international_user)==1,'Auto Synchronization To BMXPIN Failed\nMuiltple Type International Account Found' 
            access_token=international_user.access_token
        else :
            indian_user=india_user_obj.search([('name','=',user.id)]) 
            assert indian_user,'Synchronization To BMXPIN Failed\nPartner Type Issue'
            assert len(indian_user)==1,'Synchronization To BMXPIN Failed\nMuiltple Type India Account Found'
            access_token=indian_user.access_token

        return access_token
            
         
    @api.multi
    def get_division(self,employee_record):
        role=''

        for division in employee_record.fields_get(['role']).get('role').get('selection') : 
            if employee_record.role==division[0] :
                role=division[1]
        return role
    
    @api.multi
    def get_role(self,employee_record):
        
        bmxpin_role_ids={'BOD' : 3,'Director Sales':2,'Team Leader':1,'Business Manager':0}
        role=employee_record.job_id.name
        role_id=[bmxpin_role_ids[x] for x in bmxpin_role_ids.iterkeys() if x==role ]
        if not role_id:
            return ''
        return role_id[0]
            

    @api.multi
    def sync_create_employee(self,**kargs) : 
        '''Use Employee creation API to sync employee details  '''
        user_obj=self.env['res.users']
        vals=dict()
        partner_employee_record=kargs.get('partner_employee_record')
        assert partner_employee_record,'Auto Synchronization To BMXPIN Failed\nPartner Id Of Odoo Account Not Found'
        assert partner_employee_record.partner_sequence,'Auto Synchronization To BMXPIN Failed\nUser Account Odoo Id Not Found'
        user_record=user_obj.search([('partner_id','=',partner_employee_record.id)])
        assert user_record,'Auto Synchronization To BMXPIN Failed\nUser Account Not Found'
        assert len(user_record)==1,'Auto Synchronization To BMXPIN Failed\nMultiple User Account Found'
        
        employee_record=self.search([('user_id','=',user_record.id)])
        assert employee_record,'Auto Synchronization To BMXPIN Failed\nEmployee Record Not Found'
        assert len(employee_record)==1,'Auto Synchronization To BMXPIN Failed\nMultiple Employee Record Found'
        
        access_token=self.get_access_token(employee_record)
        role=self.get_role(employee_record)
        division=self.get_division(employee_record)
        if division not in ['Retail','Enterprise']:
            return True
        
        
        vals.update({'employee_name':employee_record.routesms_username,\
                     'username':user_record.login,'tlid':employee_record.parent_id.routesms_username,
                     'role':role,'division':division,
                     'odoo_id':kargs.get('partner_employee_record').partner_sequence,\
                     'access_token':access_token,'emp_create':'emp_create','mode':'insert'})

        ##store sync time##########
        self.insert_sync_date(employee_record)
        ##post data to BMXPIN server
        self.post_data_to_server(vals)
        return True

#     @api.multi
#     def test(self):
#         import ipdb;ipdb.set_trace()
#         dd
#         return True

    @api.multi
    def sync_update_employee(self,**kargs) :
        #import ipdb;ipdb.set_trace() 
        '''Use Employee updation API to sync employee details '''
        user_obj=self.env['res.users']
        vals=dict()
        employee_rec=kargs.get('employee_record')

        assert employee_rec,'Auto Synchronization To BMXPIN Failed\nTechnical Issue\nContact Odoo Team'
        assert employee_rec.user_id,'Auto Synchronization To BMXPIN Failed\nRelated User Not Found'
        
        assert employee_rec.user_id.partner_id,'Auto Synchronization To BMXPIN Failed\nRelated Partner On User Account Not Found'
        assert employee_rec.user_id.partner_id.partner_sequence,'Auto Synchronization To BMXPIN Failed\nUser Odoo Id Not Found'
        
        access_token=self.get_access_token(employee_rec)
        division=self.get_division(employee_rec)
        if division not in ['Retail','Enterprise'] :
            return True        

        role=self.get_role(employee_rec)
        
        vals.update({'odoo_id':kargs.get('employee_record').user_id.partner_id.partner_sequence,\
                     'employee_name':kargs.get('employee_record').routesms_username,\
                     'username':kargs.get('employee_record').user_id.login,\
                     'tlid':kargs.get('employee_record').parent_id.routesms_username,
                     'role':role,'division':division,
                     'access_token':access_token,'iActive':1 if employee_rec.active else 0,'emp_create':'emp_create','mode':'update'})
        ##store sync time##########
        self.insert_sync_date(employee_rec)
        ##post data to BMXPIN server
        self.post_data_to_server(vals)
        return True


    @api.multi
    def synchronise_employee_record(self,**kargs): 
        ''' synchronize odoo employee & user details to 3rd party'''
        
        try :
            
            if kargs.get('api_type')=='bm_swapping':
                self.sync_bm_swap(**kargs)
                            
            elif kargs.get('api_type')=='create_employee':
                self.sync_create_employee(**kargs)
                
            elif kargs.get('api_type')=='update_employee':
                self.sync_update_employee(**kargs)
            else:
                raise osv.except_osv(_('Error!'), _('Synchronization Failed! API Method Not Found\nContact Odoo Team'))

        except Exception as E:
            if not E.message : 
                E.message=E.value   
                           
            raise osv.except_osv(_('Error'),_('{} ').format(E.message))

        return True


    
    
    
    


