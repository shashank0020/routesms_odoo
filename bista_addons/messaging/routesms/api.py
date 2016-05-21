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
import string
SUPERUSER = 1

class odoo_rsl_api(models.Model): 
    _name = "odoo.rsl.api"
    _description = "Integrate Odoo With Other Web Applications"
    
    result={}
    Promotional = "0"
    Transactional = "1"
    Both ="2"
    Transcrub ="4"

    @api.multi
    def check_user_account_code(self, post_data): 
        '''post user account code to rsl server '''
	#import ipdb;ipdb.set_trace()
#        url = "http://192.168.0.243/routesms/smpp1/odoo/check_code/" #LOCAL
	url = "http://121.241.242.102/odoo/check_code/" #LIVE
        post_response = requests.post(url=url, data=post_data)
        print post_data
        return post_response.text        
         
        
        
        
    
    @api.multi
    def partner_account_swap_post_to_server(self, vals):
        '''Post Partner Account Type Data To RSL Servers '''
        post_data = vals
        try : 
#            url = "http://192.168.0.13/odooapi/Controllers/controller.php" #LOCAL
            url = "http://121.241.242.102/odooapi/Controllers/controller.php" #LIVE
            post_response = requests.post(url=url, data=post_data)
            print post_data
            print post_response.text
	    #import ipdb;ipdb.set_trace()
	    if post_response.json().get('error')=='No Record Found to Update' :
		return True
            assert post_response.json().get('success'),post_response.json().get('error')
        except Exception as E  : 
           raise osv.except_osv(_('Error'),_('{} ').format(E.message))
    
    @api.multi
    def partner_account_swap(self):
        
        emp_obj = self.env["hr.employee"]
        partner = self.id
        account_type = "0" if partner.prepaid else "1"
        odoo_id = partner.partner_sequence
	#import ipdb;ipdb.set_trace()
        session_user = emp_obj.sudo().search([ ("user_id","=",partner.user_id.id) ])
        if not session_user : 
            raise osv.except_osv(_("Error"),_("Employee Record Not Found\nContact HR Team"))
        account_type_vals = {
        "iAccountType" : account_type, "odoo_id" : odoo_id, "session_user" : session_user.routesms_username}
        return self.partner_account_swap_post_to_server(account_type_vals)
        
    
    @api.multi
    def error_codes(self, response_from_requested_server) : 
        '''Throw error to end user '''
        try : 
            
            if 'ERR_601' in response_from_requested_server : 
                raise osv.except_osv(_('Error !'), _('Empty Values !!')) 
           
            elif 'ERR_602' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _(' valid Username !!'))
            
            elif 'ERR_603' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Blankspace Username !!'))                
    
            elif 'ERR_604' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Duplicate Username master !!'))
            
            elif 'ERR_605' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _(' valid Email !!'))
            
            elif 'ERR_606' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('DB Connection Err !!'))
            
            elif 'SUC_607' in response_from_requested_server   :
                 
                return True
    
    
            elif 'ERR_608' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Mail Error !!'))
            
            elif 'ERR_609' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Duplicate Username slave !!'))
            
            elif 'ERR_610' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Unable to log !!'))  
            
            elif 'ERR_611' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Unable to connect db !!'))  

            elif 'ERR_612' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Invalid credit !!'))  

            elif 'ERR_613' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Invalid code !!'))  

            elif 'ERR_614' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Invalid od !!'))  

            elif 'ERR_615' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Invalid route price !!'))  

            elif 'ERR_616' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Code length !!'))  

            elif 'ERR_617' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Routetype !!'))  

            elif 'ERR_618' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Usernamelength !!'))  

            elif 'ERR_627' in response_from_requested_server   :
                raise osv.except_osv(_('Error !'), _('Price is less than lsp !!'))

            elif 'ERR_628' in response_from_requested_server   :
                raise osv.except_osv(_('Error !'), _('No Routing !!'))
    
            else : 
                raise osv.except_osv(_('Error !'), _('Error Code Not Found\Contact Technical Team'))
    
        except Exception as E : 
            if not E.message : 
                E.message=E.value   
                           
            raise osv.except_osv(_('Error'),_('{} ').format(E.message))


    @api.multi
    def subroute_error_codes(self, response_from_requested_server) : 
        '''Throw error to end user '''
        try : 
            
            if 'ERR_601' in response_from_requested_server : 
                raise osv.except_osv(_('Error !'), _('Empty Values !!')) 
           
            elif 'ERR_602' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _(' Invalid Username !!'))
            
            elif 'ERR_603' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Blankspace Username !!'))                
    
            elif 'ERR_604' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Duplicate Username master !!'))
            
            elif 'ERR_605' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _(' Invalid Email !!'))
            
            elif 'ERR_606' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('DB Connection Err !!'))
            
            elif 'SUC_607' in response_from_requested_server   :
                
                # SEND EMAIL NOTIFICATIONS
                
                return True
    
    
            elif 'ERR_608' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Mail Error !!'))
            
            elif 'ERR_609' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Duplicate Username slave !!'))
            
            elif 'ERR_610' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Unable to log !!'))  
            
            elif 'ERR_611' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Unable to connect db !!'))  

            elif 'ERR_612' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Invalid credit !!'))  

            elif 'ERR_613' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Invalid code !!'))  

            elif 'ERR_614' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Invalid od !!'))  

            elif 'ERR_615' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Invalid route price !!'))  

            elif 'ERR_616' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Code length !!'))  

            elif 'ERR_617' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Routetype !!'))  

            elif 'ERR_618' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Username_length !!'))  


            elif 'ERR_619' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('nvalid_routetype !!')) 
            
            elif 'ERR_620' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Invalid_routename !!')) 

            elif 'ERR_621' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Length_routename !!')) 

            elif 'ERR_622' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Invalid_routing_server !!')) 

            elif 'ERR_623' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Exist_Routing_err !!')) 

            elif 'ERR_624' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('Sub_routing_User_Err !!'))                                                             

            elif 'ERR_625' in response_from_requested_server   : 
                raise osv.except_osv(_('Error !'), _('User_does_not_exist !!')) 

            elif 'ERR_627' in response_from_requested_server   :
                raise osv.except_osv(_('Error !'), _('Price is less than lsp !!'))

            elif 'ERR_628' in response_from_requested_server   :
                raise osv.except_osv(_('Error !'), _('No Routing !!'))
    
            else : 
                raise osv.except_osv(_('Error !'), _('Error Code Not Found\Contact Technical Team'))
    
        except Exception as E : 
            if not E.message : 
                E.message=E.value   
                           
            raise osv.except_osv(_('Error'),_('{} ').format(E.message))
        
    
    @api.multi
    def post_to_server(self, vals, mode):
        '''Post Data To RSL Servers '''
        post_data = vals
       
        # User Creation link
        if not mode :
           # url = "http://192.168.0.243/routesms/smpp1/odoo/"
           url = "http://121.241.242.102/odoo/"			
        else  :
            
        # User Updation link
            #url = "http://192.168.0.243/routesms/smpp1/odoo/update_user/"  
	    url = "http://121.241.242.102/odoo/update_user/" 
        #import ipdb;ipdb.set_trace() 
        post_response = requests.post(url=url, data=post_data)
        print post_data
        print post_response.text
#        return True
        return self.error_codes(post_response.text )

    @api.multi
    def subroute_post_to_server(self, vals, mode):
        '''Post Data To RSL Servers for subrouting '''
        post_data = vals
        
        # User Creation link
        if not mode :
            #url = "http://192.168.0.243/routesms/smpp1/odoo/insert_sub_routing/" #LOCAL
            url = "http://121.241.242.102/odoo/insert_sub_routing/" #LIVE

        else  :
            
        # User Updation link
#            url = "http://192.168.0.243/routesms/smpp1/odoo/update_sub_routing/" #LOCAL  
            url = "http://121.241.242.102/odoo/update_sub_routing/" #LIVE
        
        post_response = requests.post(url=url, data=post_data)
        print post_data
        print post_response.text
        #return True
        return self.subroute_error_codes(post_response.text )    
    

    
    def user_account_post_data(self, server, partner_user, emp_id, mode ): 
        '''Master method to post data on RSL application based on servers type '''
        try :
            
            # COMMON DATA SHARING TO ALL NESTED METHODS
            partner_obj=self.pool.get("res.partner")
            user_active = partner_user.is_active
            if mode =="update" : 
                self.result ["bActive"] = "1" if user_active else "0"

            self.result.update( {  
                               
            'username' : partner_user.username ,'servername' : partner_user.server_domain.name ,\
            'odooid' : partner_user.partner_id.partner_sequence,\
            'businessManager' : emp_id.routesms_username , 'company_name' : partner_user.partner_id.name,\
            'contact_person' : partner_user.partner_id.child_ids[0].name \
            if partner_user.partner_id.child_ids else '', 'email': partner_user.price_notification_email  , \
            'iDefaultRoutePrice' : partner_user.local_price, 'iCreditLimit' : partner_user.credit_limit,\
            'iOverDraftLimit' : partner_user.od_limit,\
            'iAccountType' : '0' if partner_user.partner_id.prepaid else '1', 'sCompanyId' : 'RI',\
            'Commercial':partner_user.commercial_email,\
            'Account' : partner_user.account_email, 'Technical' : partner_user.technical_email,\
            'MobileNo' : partner_user.user_account_phone_number,
                            } )
            
            def server_general_international(self, partner_user, emp_id): 
                '''# CASE 1: GENERAL->  INTERNATIONAL '''
                return self.result
            
            def server_general_local(self, partner_user, emp_id): 
                '''# CASE 2: GENERAL-> LOCAL  '''
                
                if partner_user.route_type == "promotional"  :
                    routetype = self.Promotional
                     
                elif partner_user.route_type == "transactional"  :  
                    routetype = self.Transactional
                    
                elif partner_user.route_type == "both"  :  
                    routetype = self.Both

                elif partner_user.route_type == "transcrub"  :  
                    routetype = self.Transcrub

                else  : 
                    raise osv.except_osv(_('Error'), _("Invalid Route Type"))
                    
                self.result ["iRouteType"] = routetype
                return self.result 

            
            def server_reseller_international(self, partner_user, emp_id): 
                '''CASE 3: RESELLER ->  INTERNATIONAL '''
                
                self.result ["code"] = partner_user.reseller_code
                return self.result

                            
            def server_reseller_local(self, partner_user, emp_id):  
                '''CASE 4: RESELLER ->  LOCAL '''
                
                del self.result ["iDefaultRoutePrice"]
                self.result ["code"] = partner_user.reseller_code
                return self.result
            
                                         
            def server_distributor_international(self, partner_user, emp_id): 
                '''#CASE 5: DISTRIBUTOR ->  INTERNATIONAL '''
                
                self.result ["code"] = partner_user.distributor_code
                return self.result
            
            
            def server_distributor_local(self, partner_user, emp_id): 
                '''#CASE 6: DISTRIBUTOR ->  LOCAL '''
                
                del self.result ["iDefaultRoutePrice"]
                self.result ["code"] = partner_user.distributor_code
                return self.result
            
#             def manage_subrouting_old(self, partner_user, emp_id): 
#                 ''' Manage subrouting for india reseller and india distributor server'''
#                 import ipdb;ipdb.set_trace()
#                 subrouting = partner_user.manage_subroute
#                 if subrouting.route_type == "promotional" : 
#                     routetype = self.Promotional
#                     
#                 else : 
#                     routetype = self.Transactional
#                     
#                 subroute_vals = {"servername" : partner_user.manage_subroute.server.name,\
#                 "username" : subrouting.username, "sRouteName" : subrouting.routename,\
#                 "sDefaultRoute" : "","iDefaultPrice" : subrouting.local_price,\
#                 "iRouteType" : routetype, "sUpdatedBy" : emp_id.routesms_username, 
#                 }
#                 if partner_user.manage_subroute.confirm : 
#                     mode = True
#                 else : 
#                     mode = False
#                     
#                 self.subroute_post_to_server(subroute_vals, mode)
#                 # CONFIRM SUBROUTE DETAILS AND USER THEN CANNOT MODIFY AGAIN
#                 import ipdb;ipdb.set_trace()
#                 return partner_user.manage_subroute.write({"confirm" : True})
            @api.multi
            def manage_subrouting(self, partner_user, emp_id): 
                ''' Manage subrouting for india reseller and india distributor server'''
                
                subroute_line_obj = self.env["subroute.line"]
                subrouting = partner_user.manage_subroute
                if subrouting : 
                    # GETTING PROMOTIONAL DATA
                    
                    subroute_line_promotional = subroute_line_obj.search([("subroute_id_promotional","=",subrouting.id), ("status","=","pending")])
                
                    for promotional_line in  subroute_line_promotional : 
                        subroute_vals = {"servername" : promotional_line.server.name,\
                        "username" : promotional_line.username, "sRouteName" : promotional_line.routename,\
                        "sDefaultRoute" : "","iDefaultPrice" : promotional_line.local_price,\
                        "iRouteType" : promotional_line.route_type, "sUpdatedBy" : emp_id.routesms_username, 
                        }
                        # POST PROMOTIONAL DATA
                        self.subroute_post_to_server(subroute_vals, promotional_line.mode)
                        promotional_line.write({"status" : "approved"})
                        
                    # GETTING TRANSACTIONAL DATA
                    subroute_line_transactional = subroute_line_obj.search([("subroute_id_transactional","=",subrouting.id), ("status","=","pending")])
                    
                    for transactional_line in  subroute_line_transactional : 
                        subroute_vals = {"servername" : transactional_line.server.name,\
                        "username" : transactional_line.username, "sRouteName" : transactional_line.routename,\
                        "sDefaultRoute" : "","iDefaultPrice" : transactional_line.local_price,\
                        "iRouteType" : transactional_line.route_type, "sUpdatedBy" : emp_id.routesms_username, 
                        }
                        # POST PROMOTIONAL DATA
                        self.subroute_post_to_server(subroute_vals, transactional_line.mode)
                        transactional_line.write({"status" : "approved"})
                
                
                return subrouting  

            
            if server.type == 'general' and server.locality == 'international' : 
                post_data =  server_general_international(self, partner_user, emp_id)
            
            elif server.type == 'general' and server.locality == 'local' :
                post_data = server_general_local(self, partner_user, emp_id)

            elif server.type == 'reseller' and server.locality == 'international' :
                post_data = server_reseller_international(self, partner_user, emp_id) 

            elif server.type== 'reseller' and server.locality == 'local' :
                post_data = server_reseller_local(self, partner_user, emp_id)
            
            elif server.type == 'distributor' and server.locality == 'international' :
                post_data = server_distributor_international(self, partner_user, emp_id)  
                  
            elif server.type == 'distributor' and server.locality == 'local' :
                post_data = server_distributor_local(self, partner_user, emp_id)   
            
            else :
                raise osv.except_osv(
                    _('Error'), _('Technical Issue\nInvalid Server\nContact Odoo Team'))

        except Exception as E : 
            if not E.message : 
                E.message=E.value              
            raise osv.except_osv(_('Error'),
                            _('{} ').format(E.message))    

        
        self.post_to_server(post_data,True if mode == "update" else False)
        if partner_user.manage_subroute : 
            # POST SUBROUTE DATA
            subroute_post_data = manage_subrouting(self, partner_user, emp_id)


        # SEND EMAIL NOTIFICATIONS
        return partner_obj.user_account_email_notifications (self.env.cr, SUPERUSER, partner_user, "user_creation"  )
                 
    
    


        
    
