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
SUPERID=1
SUPERUSERID=1
import requests
count=0
class routesms_api(osv.osv):
    _name = 'routesms.api'
    _description='API to integrate with Odoo application'


    count=0


    def upload_subroute_data(self,cr,uid,vals):
        ''' upload subroute data from csv'''
        subroute_obj=self.pool.get('subroute')
        subroute_line_obj=self.pool.get('subroute.line')
        res={}
        
        def indiareseller_create_manage_subroute(self,cr,uid): 

            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/subroute/indiareseller/subroutereseller.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        
                        # SEARCH USERNAME IN ODOO
                        add_user_id = add_user_obj.search(cr,uid,[("username",'=',val[0])])
                        if not add_user_id :
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/subroute/indiareseller/logs/no_user_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+'\n') 
                            continue    
                             
                            
                        if len(add_user_id) > 1 : 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/subroute/indiareseller/logs/multiple_user_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+'\n') 
                            continue                                
                        name="Manage subroute "+val[0]
                        username =val[0]
                        routename=val[1]
                        local_price=val[2]
                        #res_partner_add_user_id =                        
                        user_browse=add_user_obj.browse(cr,uid,add_user_id[0])
                        #import ipdb;ipdb.set_trace()
                        if not  user_browse.manage_subroute :
                            #import ipdb;ipdb.set_trace() 
                            # CREATE SUBROUTE DATA
                            subroute_vals={"name" : name,"routename":routename,"username":user_browse.username,\
                        "server":user_browse.server_domain.id,"res_partner_add_user_id":user_browse.id}
                            
                            subroute_id=subroute_obj.create(cr,uid,subroute_vals)
                            print "--------SUBROUTE  RECORD CREATED----------"
                            user_browse.write({"manage_subroute":subroute_id})
                        else : 
                            print "--------EXIST----------"
                            
            except Exception as E : 
                print E
                import ipdb;ipdb.set_trace()

        def indiareseller_create_manage_subroute_line(self,cr,uid): 

            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/subroute/indiareseller/subroutereseller.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        
                        # SEARCH USERNAME IN ODOO
                        add_user_id = add_user_obj.search(cr,uid,[("username",'=',val[0])])
                        if not add_user_id :
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/subroute/indiareseller/logs/no_user_loine_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+'\n') 
                            continue    
                             
                            
                        if len(add_user_id) > 1 : 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/subroute/indiareseller/logs/multiple_user_line_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+'\n') 
                            continue                                

                        #res_partner_add_user_id =                        
                        user_browse=add_user_obj.browse(cr,uid,add_user_id[0]) 
                        
                        if not  user_browse.manage_subroute : 
                            # CREATE SUBROUTE DATA
                            import ipdb;ipdb.set_trace()

                            

                            print "--------SUBROUTE  RECORD CREATED----------"
                        else : 
                            # ASSIGN ROUTENAME TO SUBROUTE
                            print "--------EXIST----------"
                            subroute_line_vals={"routename":val[1],"username":user_browse.username,\
                        "server":user_browse.server_domain.id,"local_price":val[2],"status":"approved"} 
                            if val[3]=="0" : 
                                subroute_line_vals["subroute_id_promotional"]= user_browse.manage_subroute.id
                                subroute_line_vals["route_type"]="promotional"
                            else : 
                                subroute_line_vals["subroute_id_transactional"]= user_browse.manage_subroute.id
                                subroute_line_vals["route_type"]="transactional"
                            subroute_line_obj.create(cr,uid,subroute_line_vals)
                            print "--------SUBROUTE  LINE RECORD CREATED----------"
                                                           
                            
                            
                            
            except Exception as E : 
                print E
                import ipdb;ipdb.set_trace()


        def indiadistributor_create_manage_subroute(self,cr,uid): 

            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/subroute/indiadistributor/subroutedis.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        
                        # SEARCH USERNAME IN ODOO
                        add_user_id = add_user_obj.search(cr,uid,[("username",'=',val[0])])
                        if not add_user_id :
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/subroute/indiadistributor/logs/no_user_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+'\n') 
                            continue    
                             
                            
                        if len(add_user_id) > 1 : 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/subroute/indiadistributor/logs/multiple_user_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+'\n') 
                            continue                                
                        name="Manage subroute "+val[0]
                        username =val[0]
                        routename=val[1]
                        local_price=val[2]
                        #res_partner_add_user_id =                        
                        user_browse=add_user_obj.browse(cr,uid,add_user_id[0])
                        #import ipdb;ipdb.set_trace()
                        if not  user_browse.manage_subroute :
                            # CREATE SUBROUTE DATA
                            subroute_vals={"name" : name,"routename":routename,"username":user_browse.username,\
                        "server":user_browse.server_domain.id,"res_partner_add_user_id":user_browse.id}
                            
                            subroute_id=subroute_obj.create(cr,uid,subroute_vals)
                            print "--------SUBROUTE  RECORD CREATED----------"
                            user_browse.write({"manage_subroute":subroute_id})
                        else : 
                            #import ipdb;ipdb.set_trace() 
                            print "--------EXIST----------"
            except Exception as E : 
                print E
                import ipdb;ipdb.set_trace()

        def indiadistributor_create_manage_subroute_line(self,cr,uid): 

            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/subroute/indiadistributor/subroutedis.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        
                        # SEARCH USERNAME IN ODOO
                        add_user_id = add_user_obj.search(cr,uid,[("username",'=',val[0])])
                        if not add_user_id :
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/subroute/indiadistributor/logs/no_user_loine_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+'\n') 
                            continue    
                             
                            
                        if len(add_user_id) > 1 : 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/subroute/indiareseller/logs/multiple_user_line_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+'\n') 
                            continue                                

                        #res_partner_add_user_id =                        
                        user_browse=add_user_obj.browse(cr,uid,add_user_id[0]) 
                        
                        if not  user_browse.manage_subroute : 
                            # CREATE SUBROUTE DATA
                            import ipdb;ipdb.set_trace()

                            

                            print "--------SUBROUTE  RECORD CREATED----------"
                        else : 
                            # ASSIGN ROUTENAME TO SUBROUTE
                            print "--------EXIST----------"
                            subroute_line_vals={"routename":val[1],"username":user_browse.username,\
                        "server":user_browse.server_domain.id,"local_price":val[2],"status":"approved"} 
                            if val[3]=="0" : 
                                subroute_line_vals["subroute_id_promotional"]= user_browse.manage_subroute.id
                                subroute_line_vals["route_type"]="promotional"
                            else : 
                                subroute_line_vals["subroute_id_transactional"]= user_browse.manage_subroute.id
                                subroute_line_vals["route_type"]="transactional"
                            subroute_line_obj.create(cr,uid,subroute_line_vals)
                            print "--------SUBROUTE  LINE RECORD CREATED----------"
                                                           
                            
                            
                            
            except Exception as E : 
                print E
                import ipdb;ipdb.set_trace()

                
        #fun = indiareseller_create_manage_subroute(self,cr,uid)            
        #fun1 = indiareseller_create_manage_subroute_line(self,cr,uid)
        #fun2 = indiadistributor_create_manage_subroute(self,cr,uid)            
        fun3 = indiadistributor_create_manage_subroute_line(self,cr,uid)

        return True                 




    def upload_user_account_data_for_missing_odoo_id(self,cr,uid,vals): 
        '''upload user data from RSL servers whose odoo id was missing in 1st sheet'''
        
        partner_obj=self.pool.get('res.partner')
        server_obj=self.pool.get('server')
        res={}
        
        
        def server_distributor_local(self,cr,uid ):
            '''#CASE 6: DISTRIBUTOR ->  LOCAL '''


            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/displusindiauserss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        #import ipdb;ipdb.set_trace()
                            
                            
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[3] or not val[3]:
                            continue
                        
                        bactive=True if val[11]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :
                                #import ipdb;ipdb.set_trace()
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_local/logs/no_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[3])+'\n') 
                                continue    
                                         
                                
                        if len(partner_id)>1: 
                            
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_local/logs/multiple_odoo_id_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[3])+'\n') 
                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
                        #SEARCH SERVER
                        server_id=server_obj.search(cr,uid,[("name","=",val[2])])
                        if not server_id  :
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_local/logs/no_server_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue                      
                                
                        if len(server_id)>1: 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_local/logs/multiple_serverfound.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue          
                        
                        #GET SERVER
                        server=server_obj.browse(cr,uid,server_id[0])   
    
                        
                        res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                        "od_limit":float(val[8]),"credit_limit":float(val[7]),"status":"approved",\
                        "is_live":True,"routesms_notes":"FROM LEGACY","is_active":bactive,"reseller_code":val[1]}
    
                        add_user_obj.create(cr,uid,res)
                        print "----USER CREATED FROM LEGACY----"
                        
                        
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True                    

        def server_distributor_international(self, partner_user, emp_id): 
            '''#CASE 5: DISTRIBUTOR ->  INTERNATIONAL '''        

            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/displususerss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        #import ipdb;ipdb.set_trace()
                            
                            
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[3] or not val[3]:
                            continue
                        
                        bactive=True if val[11]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :
                                #import ipdb;ipdb.set_trace()
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_international/logs/no_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[3])+'\n') 
                                continue    
                                         
                                
                        if len(partner_id)>1: 
                            
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_international/logs/multiple_odoo_id_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[3])+'\n') 
                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
                        #SEARCH SERVER
                        server_id=server_obj.search(cr,uid,[("name","=",val[2])])
                        if not server_id  :
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_international/logs/no_server_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue                      
                                
                        if len(server_id)>1: 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_international/logs/multiple_serverfound.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue          
                        
                        #GET SERVER
                        server=server_obj.browse(cr,uid,server_id[0])   
    
                        
                        res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                        "local_price":float(val[7]),"od_limit":float(val[9]),"credit_limit":float(val[8]),"status":"approved",\
                        "is_live":True,"routesms_notes":"FROM LEGACY","is_active":bactive,"reseller_code":val[1]}
    
                        add_user_obj.create(cr,uid,res)
                        print "----USER CREATED FROM LEGACY----"
                        
                        
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True             



        def server_reseller_local(self, cr,uid):  
            '''CASE 4: RESELLER ->  LOCAL '''   

            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/missing_odoo_id/server_reseller_local/resplusindiauserss_29april.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        #import ipdb;ipdb.set_trace()
                            
                            
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[3] or not val[3]:
                            continue
                        
                        bactive=True if val[10]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[3])])
                            if not partner_id :
                                #import ipdb;ipdb.set_trace()
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/missing_odoo_id/server_reseller_local/logs/no_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[3])+'\n') 
                                continue    
                                         
                                
                        if len(partner_id)>1: 
                            
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/missing_odoo_id/server_reseller_local/logs/multiple_odoo_id_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[3])+'\n') 
                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
                        #SEARCH SERVER
                        server_id=server_obj.search(cr,uid,[("name","=",val[2])])
                        if not server_id  :
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/missing_odoo_id/server_reseller_local/logs/no_server_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue                      
                                
                        if len(server_id)>1: 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/missing_odoo_id/server_reseller_local/logs/multiple_serverfound.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue          
                        
                        #GET SERVER
                        server=server_obj.browse(cr,uid,server_id[0])   
                        is_live =True if val[11] =="LIVE USER" else False
                        
                        res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                        "od_limit":float(val[8]),"credit_limit":float(val[7]),"status":"approved",\
                        "is_live":is_live,"routesms_notes":"FROM LEGACY_29/04/2016","is_active":bactive,"reseller_code":val[1]}
    
                        add_user_obj.create(cr,uid,res)
                        print "----USER CREATED FROM LEGACY----"
                        
                        
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True             


                 

        def server_reseller_international(self, cr,uid): 
            
            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/missing_odoo_id/server_reseller_international/resellerplususerss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        #import ipdb;ipdb.set_trace()
                            
                            
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[3] or not val[3]:
                            continue
                        
                        bactive=True if val[11]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[3])])
                            if not partner_id :
                                #import ipdb;ipdb.set_trace()
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/missing_odoo_id/server_reseller_international/logs/no_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[3])+'\n') 
                                continue    
                                         
                                
                        if len(partner_id)>1: 
                            
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/missing_odoo_id/server_reseller_international/logs/multiple_odoo_id_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[3])+'\n') 
                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
                        #SEARCH SERVER
                        server_id=server_obj.search(cr,uid,[("name","=",val[2])])
                        if not server_id  :
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/missing_odoo_id/server_reseller_international/logs/no_server_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue                      
                                
                        if len(server_id)>1: 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/missing_odoo_id/server_reseller_international/logs/multiple_serverfound.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue          
                        
                        #GET SERVER
                        server=server_obj.browse(cr,uid,server_id[0])   
                        is_live =True if val[11] =="LIVE USER" else False
                        
                        res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                        "local_price":float(val[7]),"od_limit":float(val[9]),"credit_limit":float(val[8]),"status":"approved",\
                        "is_live":is_live,"routesms_notes":"FROM LEGACY_13/05/2016","is_active":bactive,"reseller_code":val[1]}
    
                        add_user_obj.create(cr,uid,res)
                        print "----USER CREATED FROM LEGACY----"                        
                        
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True             
            

        
        def server_general_international(self, cr,uid): 
            '''# CASE 1: GENERAL->  INTERNATIONAL '''
            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/missing_odoo_id/server_general_international/smsplususerss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        #import ipdb;ipdb.set_trace()
                            
                            
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[2] or not val[2]:
                            continue
                        
                        bactive=True if val[10]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        import ipdb;ipdb.set_trace()
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[2])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :
                                #import ipdb;ipdb.set_trace()
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/missing_odoo_id/server_general_international/logs/no_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[2])+'\n') 
                                continue    
                                         
                                
                        if len(partner_id)>1: 
                            
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/missing_odoo_id/server_general_international/logs/multiple_odoo_id_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[2])+'\n') 
                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
                        #SEARCH SERVER
                        server_id=server_obj.search(cr,uid,[("name","=",val[1])])
                        if not server_id  :
                            server_id=server_obj.search(cr,uid,[("active",'=',False),("name","=",val[1])])
                            if not server_id : 
                                
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/missing_odoo_id/server_general_international/logs/no_server_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[0])+ "{}" +  str(val[1]) +  '\n') 
                                continue                      
                                
                        if len(server_id)>1: 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/missing_odoo_id/server_general_international/logs/multiple_serverfound.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[2]) +  '\n') 
                            continue          
                        
                        #GET SERVER
                        server=server_obj.browse(cr,uid,server_id[0])   
                        is_live =True if val[11] =="LIVE USER" else False
                        
                        res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                        "local_price":float(val[6]),"od_limit":float(val[8]),"credit_limit":float(val[7]),"status":"approved",\
                        "is_live":is_live,"routesms_notes":"FROM LEGACY_3/05/2016","is_active":bactive}
    
                        add_user_obj.create(cr,uid,res)
                        print "----USER CREATED FROM LEGACY----"                        
                        
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True             
            
        def server_general_local(self,cr,uid): 
            '''# CASE 2: GENERAL-> LOCAL  '''
            
            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/indiaplususerss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[2] or not val[2]:
                            continue
                        
                        bactive=True if val[10]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[2])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/no_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[2])+'\n') 
                                continue    
                                         
                                
                        if len(partner_id)>1: 
                            import ipdb;ipdb.set_trace()
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/multiple_odoo_id_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[2])+'\n') 
                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
                        #SEARCH SERVER
                        server_id=server_obj.search(cr,uid,[("name","=",val[1])])
                        if not server_id  :
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/no_server_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+'\n') 
                            continue                      
                                
                        if len(server_id)>1: 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/multiple_serverfound.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+'\n') 
                            continue          
                        
                        #GET SERVER
                        server=server_obj.browse(cr,uid,server_id[0])   
    
                        if val[12] == "PROMOTIONAL"  :
                            routetype = "promotional"
                             
                        elif val[12] == "TRANSACTIONAL"  :  
                            routetype = "transactional"
                            
                        elif val[12] == "BOTH"  :  
                            routetype = "both"
        
                        elif val[12] ==  "TRANSCRUB" :  
                            routetype = "transcrub"
        
                        else  : 
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/routetype_not_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[0])+'\n') 
                                continue                      
                        
                        
                        res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                        "local_price":float(val[6]),"od_limit":float(val[8]),"credit_limit":float(val[7]),"status":"approved",\
                        "is_live":True,"routesms_notes":"FROM LEGACY","is_active":bactive,"route_type":routetype}
    
                        add_user_obj.create(cr,uid,res)
                        print "----USER CREATED FROM LEGACY----"
                        
                
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True
        #fun = server_general_international(self,cr,uid)    
#         fun1=server_general_local(self,cr,uid)
        fun2 =server_reseller_international(self,cr,uid)
#        fun3 =server_reseller_local(self,cr,uid)
#         fun4 = server_distributor_international (self,cr,uid)
#         fun5 = server_distributor_local (self,cr,uid)
        print "------------OVER--------------"
        return True



    def correct_live_to_test_user(self,cr,uid,vals):
        '''update live to test  '''
        
        
        def server_distributor_local(self,cr,uid):
            self.count=0
            correction_count=0
            missing_odoo_ids =[]
            partner_obj=self.pool.get('res.partner')
            server_obj=self.pool.get('server')
            add_user_obj=self.pool.get("res.partner.add.user")
            import ipdb;ipdb.set_trace()
            try : 
                
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/displusindiauserss.csv','r') as e: 
                    reader = csv.reader(e)            
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        
                        val=[x.strip() for x in val]
                            
                        #if "\\N" in val[3] or not val[3]:
                        #import ipdb;ipdb.set_trace()
                        if val [11] =="TEST USER" : 
                             
                            # SWAP RESLER CODE TO DITRIBUTIR
                            #SEARCH PARTNER
                            partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                            if not partner_id  :
                                partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[3])])
                            if not partner_id  : 
                                print '----------PARTNER NOT FOUND'
                                continue    
                            partner=partner_obj.browse(cr,uid,partner_id[0])
                            for add_user in partner.user_line : 
                                if add_user.id in [5872,5761] : 
                                    continue 
                                correction_count+=1;print correction_count
                                if add_user.username == val[0] : 
                                    add_user_obj.write(cr,uid,[add_user.id],{"is_live":False})
                                    print '---------CORRECTION MADE-----------'                         
                              
                    
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True                        


        def reseller_india(self,cr,uid):
            self.count=0
            correction_count=0
            missing_odoo_ids =[]
            partner_obj=self.pool.get('res.partner')
            server_obj=self.pool.get('server')
            add_user_obj=self.pool.get("res.partner.add.user")
            import ipdb;ipdb.set_trace()
            try : 
                
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/resplusindiauserss.csv','r') as e: 
                    reader = csv.reader(e)            
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        
                        val=[x.strip() for x in val]
                            
                        #if "\\N" in val[3] or not val[3]:
                        #import ipdb;ipdb.set_trace()
                        if val [11] =="TEST USER" : 
                             
                            # SWAP RESLER CODE TO DITRIBUTIR
                            #SEARCH PARTNER
                            partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                            if not partner_id  :
                                partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[3])])
                            if not partner_id  : 
                                print '----------PARTNER NOT FOUND'
                                continue    
                            partner=partner_obj.browse(cr,uid,partner_id[0])
                            for add_user in partner.user_line : 
                                if add_user.id in [5872,5761] : 
                                    continue 
                                correction_count+=1;print correction_count
                                if add_user.username == val[0] : 
                                    add_user_obj.write(cr,uid,[add_user.id],{"is_live":False})
                                    print '---------CORRECTION MADE-----------'                         
                              
                    
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True                        
        

        def indiaplus(self,cr,uid):
            self.count=0
            correction_count=0
            missing_odoo_ids =[]
            partner_obj=self.pool.get('res.partner')
            server_obj=self.pool.get('server')
            add_user_obj=self.pool.get("res.partner.add.user")
            import ipdb;ipdb.set_trace()
            try : 
                
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/indiaplususerss.csv','r') as e: 
                    reader = csv.reader(e)            
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        
                        val=[x.strip() for x in val]
                            
                        #if "\\N" in val[3] or not val[3]:
                        #import ipdb;ipdb.set_trace()
                        if val [11] =="TEST USER" : 
                             
                            # SWAP RESLER CODE TO DITRIBUTIR
                            #SEARCH PARTNER
                            partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[2])])
                            if not partner_id  :
                                partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id  : 
                                print '----------PARTNER NOT FOUND'
                                continue    
                            partner=partner_obj.browse(cr,uid,partner_id[0])
                            for add_user in partner.user_line : 
                                if add_user.id in [5872,5761] : 
                                    continue 
                                correction_count+=1;print correction_count
                                if add_user.username == val[0] : 
                                    add_user_obj.write(cr,uid,[add_user.id],{"is_live":False})
                                    print '---------CORRECTION MADE-----------'                         
                              
                    
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True                        



        def smsplus(self,cr,uid):
            self.count=0
            correction_count=0
            missing_odoo_ids =[]
            partner_obj=self.pool.get('res.partner')
            server_obj=self.pool.get('server')
            add_user_obj=self.pool.get("res.partner.add.user")
            import ipdb;ipdb.set_trace()
            try : 
                
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/smsplususerss.csv','r') as e: 
                    reader = csv.reader(e)            
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        
                        val=[x.strip() for x in val]
                            
                        #if "\\N" in val[3] or not val[3]:
                        #import ipdb;ipdb.set_trace()
                        if val [11] =="TEST USER" : 
                             
                            # SWAP RESLER CODE TO DITRIBUTIR
                            #SEARCH PARTNER
                            partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[2])])
                            if not partner_id  :
                                partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id  : 
                                print '----------PARTNER NOT FOUND'
                                continue    
                            partner=partner_obj.browse(cr,uid,partner_id[0])
                            for add_user in partner.user_line : 
                                if add_user.id in [5872,5761] : 
                                    continue 
                                correction_count+=1;print correction_count
                                if add_user.username == val[0] : 
                                    add_user_obj.write(cr,uid,[add_user.id],{"is_live":False})
                                    print '---------CORRECTION MADE-----------'                         
                              
                    
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True                        

        fun =server_distributor_local(self,cr,uid)
        fun1 =reseller_india(self,cr,uid)
        fun2 =indiaplus(self,cr,uid)
        fun3 =smsplus(self,cr,uid)
        
        return True



    def import_missing_user_during_import_users_account (self,cr,uid,vals): 
        '''import those user account which failed to import '''
        partner_obj=self.pool.get('res.partner')
        server_obj=self.pool.get('server')
        add_user_obj=self.pool.get("res.partner.add.user")
                
        def server_distributor_local(self,cr,uid):
            self.count=0
            correction_count=0
            missing_odoo_ids =[]
            import ipdb;ipdb.set_trace()
            try : 
                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_local/logs/no_odoo_id_found.txt","r") as f : 
                    
                    missing_odoo_ids = [ odoo_id.replace("\n","") for odoo_id in f.readlines()  ]
                print 'total missing odoo id',len(missing_odoo_ids)
                if not missing_odoo_ids : 
                    return "NO MISSING ODOO ID FOUND"
                
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/displusindiauserss.csv','r') as e: 
                    reader = csv.reader(e)            
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        
                        val=[x.strip() for x in val]
                            
                        #if "\\N" in val[3] or not val[3]:
                        #import ipdb;ipdb.set_trace()
                        bactive=True if val[10]=="ACTIVE" else False
                        if val [3] not in missing_odoo_ids : 
                            # SWAP RESLER CODE TO DITRIBUTIR
                            #SEARCH PARTNER
                            partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                            if not partner_id  :
                                partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[3])])
                            if not partner_id  : 
                                print '----------PARTNER NOT FOUND'
                                continue    
                            partner=partner_obj.browse(cr,uid,partner_id[0])
                            for add_user in partner.user_line : 
                                correction_count+=1;print correction_count
                                if add_user.username == val[0] : 
                                    add_user_obj.write(cr,uid,[add_user.id],{'reseller_code':'','distributor_code':val[0],\
                                                "routesms_notes":"FROM LEGACY-distributorindia","is_active":bactive })
                                    print '---------CORRECTION MADE-----------'                         
                              
                        else : 
                             
                                
                            
                            bactive=True if val[10]=="ACTIVE" else False
                            
                            #SEARCH PARTNER
                            partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                            if not partner_id  :
                                partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[3])])
                                
                                if not partner_id :
                                    #import ipdb;ipdb.set_trace()
                                    with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_local/logs/logs_after_correction/no_odoo_id_found.txt", "a") as donefile_new:
                                        donefile_new.write(str(val[3])+'\n') 
                                    continue    
                                             
                                    
                            if len(partner_id)>1: 
                                
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_local/logs/logs_after_correction/multiple_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[3])+'\n') 
                                continue      
                            
                            #GET PARTNER
                            partner=partner_obj.browse(cr,uid,partner_id[0])        
                            
                            #SEARCH SERVER
                            server_id=server_obj.search(cr,uid,[("name","=",val[2])])
                            if not server_id  : 
                                server_id=server_obj.search(cr,uid,[("active","=",False),("name","=",val[2])])
                                if not server_id  :
                                    with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_local/logs/logs_after_correction/no_server_found.txt", "a") as donefile_new:
                                        donefile_new.write(str(val[0])+ "{}" +  str(val[2]) +  '\n') 
                                    continue                      
                                    
                            if len(server_id)>1: 
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_local/logs/logs_after_correction/multiple_serverfound.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                                continue          
                            
                            #GET SERVER
                            server=server_obj.browse(cr,uid,server_id[0])   
                            # Check user in odoo
                            cr.execute('''select id from res_partner_add_user where username=%s ''',(val[0],))
                            user_list=map(lambda x:x[0],cr.fetchall()) 
                                    
                            
                            if user_list : 
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_local/logs/logs_after_correction/user_already_exist.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                                continue                              
                            self.count+=1;print self.count
                            res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                            "od_limit":float(val[8]),"credit_limit":float(val[7]),"status":"approved",\
                            "is_live":True,"routesms_notes":"FROM LEGACY-distributorindia","is_active":bactive,"distributor_code":val[1]}
        
                            add_user_obj.create(cr,uid,res)
                            print "----USER CREATED FROM LEGACY----"
                        
                    
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True                        
                    
        def distributor_int(self,cr,uid):
            self.count=0
            correction_count=0
            missing_odoo_ids =[]
            import ipdb;ipdb.set_trace()
            try : 
                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_international/logs/no_odoo_id_found.txt","r") as f : 
                    
                    missing_odoo_ids = [ odoo_id.replace("\n","") for odoo_id in f.readlines()  ]
                print 'total missing odoo id',len(missing_odoo_ids)
                if not missing_odoo_ids : 
                    return "NO MISSING ODOO ID FOUND"
                
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/displususerss.csv','r') as e: 
                    reader = csv.reader(e)            
                    
                    vals=[row for row in reader] 
                    
                    for val in vals :
                        
                        val=[x.strip() for x in val]
                        bactive=True if val[11]=="ACTIVE" else False
                        #if "\\N" in val[3] or not val[3]:
                        #import ipdb;ipdb.set_trace()
                        if val [3] not in missing_odoo_ids :
                             
                            # SWAP RESLER CODE TO DITRIBUTIR
                            #SEARCH PARTNER
                            partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                            if not partner_id  :
                                partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[3])])
                            if not partner_id  : 
                                print '----------PARTNER NOT FOUND'
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_international/logs/logs_after_correction/no_odoo_id_found_2.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[3])+'\n') 
                                continue    
                            partner=partner_obj.browse(cr,uid,partner_id[0])
                            for add_user in partner.user_line : 
                                correction_count+=1;print correction_count
                                if add_user.username == val[0] : 
                                    add_user_obj.write(cr,uid,[add_user.id],{'reseller_code':'','distributor_code':val[0],\
                                                                "routesms_notes":"FROM LEGACY-displusint","is_active":bactive})
                                    print '---------CORRECTION MADE-----------'                         
                              
                        else : 
                             
                                
                            
                            bactive=True if val[11]=="ACTIVE" else False
                            
                            #SEARCH PARTNER
                            
                            partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                            if not partner_id  : 
                                partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[3])])
                                
                                if not partner_id :
                                    #import ipdb;ipdb.set_trace()
                                    with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_international/logs/logs_after_correction/no_odoo_id_found.txt", "a") as donefile_new: 
                                        donefile_new.write(str(val[3])+'\n') 
                                    continue    
                                             
                                    
                            if len(partner_id)>1: 
                                
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_international/logs/logs_after_correction/multiple_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[3])+'\n') 
                                continue      
                            
                            #GET PARTNER
                            partner=partner_obj.browse(cr,uid,partner_id[0])        
                            
                            #SEARCH SERVER
                            server_id=server_obj.search(cr,uid,[("name","=",val[2])])
                            if not server_id  :
                                server_id=server_obj.search(cr,uid,[("active","=",False),("name","=",val[2])])
                                if not server_id  :
                                    with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_international/logs/logs_after_correction/no_server_found.txt", "a") as donefile_new:
                                        donefile_new.write(str(val[0])+ "{}" +  str(val[2]) +  '\n') 
                                    continue                      
                                    
                            if len(server_id)>1: 
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_international/logs/logs_after_correction/multiple_serverfound.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                                continue          
                            
                            #GET SERVER
                            server=server_obj.browse(cr,uid,server_id[0])   
                            # Check user in odoo
                            
                            self.count+=1;print self.count
                            cr.execute('''select id from res_partner_add_user where username=%s ''',(val[0],))
                            user_list=map(lambda x:x[0],cr.fetchall()) 
                                    
                            
                            if user_list : 
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_international/logs/logs_after_correction/user_already_exist.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                                continue                                  
                                
                                                  
                            res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                            "local_price":float(val[7]),"od_limit":float(val[9]),"credit_limit":float(val[8]),"status":"approved",\
                            "is_live":True,"routesms_notes":"FROM LEGACY-displusint","is_active":bactive,"distributor_code":val[1]}
                
                            add_user_obj.create(cr,uid,res)
                            print "----USER CREATED FROM LEGACY----"
                    
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True                      


        def reseller_local(self,cr,uid):
            self.count=0
            correction_count=0
            missing_odoo_ids =[]
            import ipdb;ipdb.set_trace()
            try : 
                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_local/logs/no_odoo_id_found.txt","r") as f :   
                    
                    missing_odoo_ids = [ odoo_id.replace("\n","") for odoo_id in f.readlines()  ]
                print 'total missing odoo id',len(missing_odoo_ids)
                if not missing_odoo_ids : 
                    return "NO MISSING ODOO ID FOUND"
                
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/resplusindiauserss.csv','r') as e: 
                    reader = csv.reader(e)            
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        
                        val=[x.strip() for x in val]
                            
                        #if "\\N" in val[3] or not val[3]:
                        #import ipdb;ipdb.set_trace()
                        if val [3] not in missing_odoo_ids : 
                            bactive=True if val[10]=="ACTIVE" else False
                            partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                            if not partner_id  :
                                partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[3])])
                            if not partner_id  : 
                                print '----------PARTNER NOT FOUND'
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_local/logs/logs_after_correction/no_odoo_id_found_2.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[3])+'\n') 
                                continue    
                            partner=partner_obj.browse(cr,uid,partner_id[0])
                            for add_user in partner.user_line : 
                                correction_count+=1;print correction_count
                                if add_user.username == val[0] : 
                                    add_user_obj.write(cr,uid,[add_user.id],{
                                                                "routesms_notes":"FROM LEGACY-resellerindia","is_active":bactive})
                                    print '---------CORRECTION MADE-----------'                         
                         
                        else : 
                            bactive=True if val[10]=="ACTIVE" else False
                            
                            #SEARCH PARTNER
                            partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                            if not partner_id  :
                                partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[3])])
                                
                                if not partner_id :
                                    #import ipdb;ipdb.set_trace()
                                    with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_local/logs/logs_after_correction/no_odoo_id_found.txt", "a") as donefile_new:
                                        donefile_new.write(str(val[3])+'\n') 
                                    continue    
                                             
                                    
                            if len(partner_id)>1: 
                                
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_local/logs/logs_after_correction/multiple_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[3])+'\n') 
                                continue      
                            
                            #GET PARTNER
                            partner=partner_obj.browse(cr,uid,partner_id[0])        
                            
                            #SEARCH SERVER
                            server_id=server_obj.search(cr,uid,[("name","=",val[2])])
                            if not server_id  :
                                server_id=server_obj.search(cr,uid,[("active","=",False),("name","=",val[2])])
                                if not server_id  :
                                    with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_local/logs/logs_after_correction/no_server_found.txt", "a") as donefile_new:
                                        donefile_new.write(str(val[0])+ "{}" +  str(val[2]) +  '\n') 
                                    continue                      
                                    
                            if len(server_id)>1: 
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_local/logs/logs_after_correction/multiple_serverfound.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[2])+ "{}" +  str(val[3]) +  '\n') 
                                continue          
                            
                            #GET SERVER
                            server=server_obj.browse(cr,uid,server_id[0])   
                            # Check user in odoo
                            cr.execute('''select id from res_partner_add_user where username=%s ''',(val[0],))
                            user_list=map(lambda x:x[0],cr.fetchall()) 
                            
                            
                            if user_list : 
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_local/logs/logs_after_correction/user_already_exist.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                                continue                              
                            self.count+=1;print self.count
                            res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                            "od_limit":float(val[8]),"credit_limit":float(val[7]),"status":"approved",\
                            "is_live":True,"routesms_notes":"FROM LEGACY-resellerindia","is_active":bactive,"reseller_code":val[1]}
        
                            add_user_obj.create(cr,uid,res)
                            print "----USER CREATED FROM LEGACY----"
                        
                    
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True   



        def reseller_int(self,cr,uid):
            self.count=0
            correction_count=0
            missing_odoo_ids =[]
            import ipdb;ipdb.set_trace()
            try : 
                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_international/logs/no_odoo_id_found.txt","r") as f :   
                    
                    missing_odoo_ids = [ odoo_id.replace("\n","") for odoo_id in f.readlines()  ]
                print 'total missing odoo id',len(missing_odoo_ids)
                if not missing_odoo_ids : 
                    return "NO MISSING ODOO ID FOUND"
                
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/resellerplususerss.csv','r') as e: 
                    reader = csv.reader(e)            
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        
                        val=[x.strip() for x in val]
                            
                        #if "\\N" in val[3] or not val[3]:
                        #import ipdb;ipdb.set_trace()
                        
                        if val [3] not in missing_odoo_ids :
                            continue 
                         
                        else : 
                            bactive=True if val[11]=="ACTIVE" else False
                            
                            #SEARCH PARTNER
                            partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                            if not partner_id  :
                                partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[3])])
                                
                                if not partner_id :
                                    #import ipdb;ipdb.set_trace()
                                    with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_international/logs/logs_after_correction/no_odoo_id_found.txt", "a") as donefile_new:
                                        donefile_new.write(str(val[3])+'\n') 
                                    continue    
                                             
                                    
                            if len(partner_id)>1: 
                                
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_international/logs/logs_after_correction/multiple_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[3])+'\n') 
                                continue      
                            
                            #GET PARTNER
                            partner=partner_obj.browse(cr,uid,partner_id[0])        
                            
                            #SEARCH SERVER
                            server_id=server_obj.search(cr,uid,[("name","=",val[2])])
                            if not server_id  :
                                server_id=server_obj.search(cr,uid,[("active","=",False),("name","=",val[2])])
                                if not server_id  :
                                    with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_international/logs/logs_after_correction/no_server_found.txt", "a") as donefile_new:
                                        donefile_new.write(str(val[0])+ "{}" +  str(val[2]) +  '\n') 
                                    continue                      
                                    
                            if len(server_id)>1: 
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_international/logs/logs_after_correction/multiple_serverfound.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[2])+ "{}" +  str(val[3]) +  '\n') 
                                continue          
                            
                            #GET SERVER
                            server=server_obj.browse(cr,uid,server_id[0])   
                            # Check user in odoo
                            cr.execute('''select id from res_partner_add_user where username=%s ''',(val[0],))
                            user_list=map(lambda x:x[0],cr.fetchall()) 
                            
                            
                            if user_list : 
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_international/logs/logs_after_correction/user_already_exist.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                                continue                              
                            self.count+=1;print self.count

                            res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                            "local_price":float(val[7]),"od_limit":float(val[9]),"credit_limit":float(val[8]),"status":"approved",\
                            "is_live":True,"routesms_notes":"FROM LEGACY-resellerintrenational","is_active":bactive,"reseller_code":val[1]}

        
                            add_user_obj.create(cr,uid,res)
                            print "----USER CREATED FROM LEGACY----"
                        
                    
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True   
                

        def indiaplus_local(self,cr,uid):
            self.count=0
            correction_count=0
            missing_odoo_ids =[]
            import ipdb;ipdb.set_trace()
            try : 
                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/no_odoo_id_found.txt","r") as f :   
                    
                    missing_odoo_ids = [ odoo_id.replace("\n","") for odoo_id in f.readlines()  ]
                print 'total missing odoo id',len(missing_odoo_ids)
                if not missing_odoo_ids : 
                    return "NO MISSING ODOO ID FOUND"
                
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/indiaplususerss.csv','r') as e: 
                    reader = csv.reader(e)            
                    
                    vals=[row for row in reader]
                    
                    for val in vals : 
                        
                        val=[x.strip() for x in val]
                            
                        #if "\\N" in val[3] or not val[3]:
                        #import ipdb;ipdb.set_trace()
                        
                        if val [2] not in missing_odoo_ids :
                            continue 
                         
                        else :
                            #import ipdb;ipdb.set_trace() 
                            bactive=True if val[10]=="ACTIVE" else False



                            if val[12] == "PROMOTIONAL"  :
                                routetype = "promotional"
                                 
                            elif val[12] == "TRANSACTIONAL"  :  
                                routetype = "transactional"
                                
                            elif val[12] == "BOTH"  :  
                                routetype = "both"
            
                            elif val[12] ==  "TRANSCRUB" :  
                                routetype = "transcrub"
            
                            else  : 
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/logs_after_correction/routetype_not_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[0])+'\n') 
                                continue                      

                            
                                                        
                            #SEARCH PARTNER
                            
                            partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[2])])
                            if not partner_id  :
                                partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                                
                                if not partner_id :
                                    
                                    with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/logs_after_correction/no_odoo_id_found.txt", "a") as donefile_new:
                                        donefile_new.write(str(val[2])+'\n') 
                                    continue    
                                             
                                    
                            if len(partner_id)>1: 
                                
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/logs_after_correction/multiple_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[2])+'\n') 
                                continue      
                            
                            #GET PARTNER
                            partner=partner_obj.browse(cr,uid,partner_id[0])        
                            
                            #SEARCH SERVER
                            server_id=server_obj.search(cr,uid,[("name","=",val[1])])
                            if not server_id  :
                                server_id=server_obj.search(cr,uid,[("active","=",False),("name","=",val[1])])
                                if not server_id  :
                                    with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/logs_after_correction/no_server_found.txt", "a") as donefile_new:
                                        donefile_new.write(str(val[0])+ "{}" +  str(val[1]) +  '\n') 
                                    continue                      
                                    
                            if len(server_id)>1: 
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/logs_after_correction/multiple_serverfound.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[1])+ "{}" +  str(val[2]) +  '\n') 
                                continue          
                            
                            #GET SERVER
                            server=server_obj.browse(cr,uid,server_id[0])   
                            # Check user in odoo
                            cr.execute('''select id from res_partner_add_user where username=%s ''',(val[0],))
                            user_list=map(lambda x:x[0],cr.fetchall()) 
                            
                            
                            if user_list : 
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/logs_after_correction/user_already_exist.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[0])+ "{}" +  str(val[2]) +  '\n') 
                                continue                              
                            self.count+=1;print self.count


                            res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                            "local_price":float(val[6]),"od_limit":float(val[8]),"credit_limit":float(val[7]),"status":"approved",\
                            "is_live":True,"routesms_notes":"FROM-LEGACY-indiaplus","is_active":bactive,"route_type":routetype}

        
                            add_user_obj.create(cr,uid,res)
                            print "----USER CREATED FROM LEGACY----"
                        
                    
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True   

        def smsplus_int(self,cr,uid):
            self.count=0
            correction_count=0
            missing_odoo_ids =[]
            import ipdb;ipdb.set_trace()
            try : 
                #with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_international/logs/no_odoo_id_found.txt","r") as f :   
                #with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_international/logs/no_server_found.txt","r") as f :
                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_international/logs/multiple_serverfound.txt","r") as f :
                    
                    missing_odoo_ids = [ odoo_id.split("{}")[1].strip() for odoo_id in f.readlines()  ]
                print 'total missing odoo id',len(missing_odoo_ids)
                import ipdb;ipdb.set_trace()
                if not missing_odoo_ids : 
                    return "NO MISSING ODOO ID FOUND"
                
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/smsplususerss.csv','r') as e: 
                    reader = csv.reader(e)            
                    
                    vals=[row for row in reader]
                    
                    for val in vals : 
                        
                        val=[x.strip() for x in val]
                            
                        #if "\\N" in val[3] or not val[3]:
#                         
#                         if val[2] in ["R129929"] : 
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             continue 
                            
                        if val [2] not in missing_odoo_ids :
                            continue 
                         
                        else :
                             
                            bactive=True if val[10]=="ACTIVE" else False

                            
                                                        
                            #SEARCH PARTNER
                            
                            partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[2])])
                            if not partner_id  :
                                partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                                
                                if not partner_id :
                                    
                                    with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_international/logs/logs_after_correction/no_odoo_id_found.txt", "a") as donefile_new:
                                        donefile_new.write(str(val[2])+'\n') 
                                    continue    
                                             
                                    
                            if len(partner_id)>1: 
                                
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_international/logs/logs_after_correction/multiple_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[2])+'\n') 
                                continue      
                            
                            #GET PARTNER
                            partner=partner_obj.browse(cr,uid,partner_id[0])        
                            
                            #SEARCH SERVER
                            server_id=server_obj.search(cr,uid,[("name","=",val[1])])
                            if not server_id  :
                                server_id=server_obj.search(cr,uid,[("active","=",False),("name","=",val[1])])
                                if not server_id  :
                                    with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_international/logs/logs_after_correction/no_server_found.txt", "a") as donefile_new:
                                        donefile_new.write(str(val[0])+ "{}" +  str(val[1]) +  '\n') 
                                    continue                      
                                    
                            if len(server_id)>1: 
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_international/logs/logs_after_correction/multiple_serverfound.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[1])+ "{}" +  str(val[2]) +  '\n') 
                                continue          
                            
                            #GET SERVER
                            server=server_obj.browse(cr,uid,server_id[0])   
                            # Check user in odoo
                            cr.execute('''select id from res_partner_add_user where username=%s ''',(val[0],))
                            user_list=map(lambda x:x[0],cr.fetchall()) 
                            
                            
                            if user_list : 
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_international/logs/logs_after_correction/user_already_exist.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[0])+ "{}" +  str(val[2]) +  '\n') 
                                continue                              
                            self.count+=1;print self.count


                            res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                            "local_price":float(val[6]),"od_limit":float(val[8]),"credit_limit":float(val[7]),"status":"approved",\
                            "is_live":True,"routesms_notes":"FROM-LEGACY-smsplus","is_active":bactive}
    

        
                            add_user_obj.create(cr,uid,res)
                            print "----USER CREATED FROM LEGACY----"
                        
                    
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True   

                
                
            
        #fun =server_distributor_local(self,cr,uid)
       # fun1 =distributor_int(self,cr,uid)
        #fun2 =reseller_local(self,cr,uid)
        #fun3 =reseller_int(self,cr,uid)
      	#fun4 =indiaplus_local(self,cr,uid)
        fun5 =smsplus_int(self,cr,uid)
        print '---------OVER----------'    
        return True


    def correct_contact_person_name_imported_via_csv_servers(self,cr,uid,vals):
        '''make corecton for contact person name whichb were imported via sheeet '''
        partner_obj=self.pool.get('res.partner')
        server_obj=self.pool.get('server')
        
        def distributor_local(self,cr,uid):
            self.count=0
            import ipdb;ipdb.set_trace()
            # DISTRIBUTOR LOCAL 
            
            with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/correct_contact_peron/distributor_local.csv','r') as e: 
                reader = csv.reader(e)
                
                parent_id_vals=[row for row in reader]
                
                parent_id=[int(x[0]) for x in parent_id_vals]
                print "---_TOTAL ID---",len(parent_id)
                
                import ipdb;ipdb.set_trace()
            
            with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/displusindiauserss.csv','r') as e: 
                reader = csv.reader(e)
                
                vals=[row for row in reader]
                
                for val in vals : 
                    
                    val=[x.strip() for x in val]
                    if "\\N" in val[3] or not val[3]:
                        continue
                    
                    
                    #SEARCH PARTNER
                    partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                    if not partner_id  :
                        partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[3])])
                        if not partner_id :
                            #import ipdb;ipdb.set_trace()
                            continue    
                                     
                            
                    if len(partner_id)>1: 
                        
                        continue      
                    
                    #GET PARTNER
                    partner=partner_obj.browse(cr,uid,partner_id[0])
                    if partner.id in parent_id :
                        
                        self.count+=1;print self.count
                        child_id=partner.child_ids[0]
                        #import ipdb;ipdb.set_trace()
                        partner_obj.write(cr,uid,[child_id.id],{"name":val[6]})
                        print '==-----------correction done----------'
            return True


        def distributor_int(self,cr,uid):
            self.count=0
            import ipdb;ipdb.set_trace()
            # DISTRIBUTOR int 
            
            with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/correct_contact_peron/distributor_int.csv','r') as e: 
                reader = csv.reader(e)
                
                parent_id_vals=[row for row in reader]
                
                parent_id=[int(x[0]) for x in parent_id_vals]
                print "---_TOTAL ID---",len(parent_id)
                
                import ipdb;ipdb.set_trace()
            
            with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/displususerss.csv','r') as e: 
                reader = csv.reader(e)
                
                vals=[row for row in reader]
                
                for val in vals : 
                    
                    val=[x.strip() for x in val]
                    if "\\N" in val[3] or not val[3]:
                        continue
                    
                    
                    #SEARCH PARTNER
                    partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                    if not partner_id  :
                        partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[3])])
                        if not partner_id :
                            #import ipdb;ipdb.set_trace()
                            continue    
                                     
                            
                    if len(partner_id)>1: 
                        
                        continue      
                    
                    #GET PARTNER
                    partner=partner_obj.browse(cr,uid,partner_id[0])
                    if partner.id in parent_id :
                        
                        self.count+=1;print self.count
                        child_id=partner.child_ids[0]
                        #import ipdb;ipdb.set_trace()
                        partner_obj.write(cr,uid,[child_id.id],{"name":val[6]})
                        print '==-----------correction done----------'
            return  True


        def reseller_local(self,cr,uid):
            self.count=0
            import ipdb;ipdb.set_trace()
            # RESELLER LOCAL 
            
            with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/correct_contact_peron/reseller_local.csv','r') as e: 
                reader = csv.reader(e)
                
                parent_id_vals=[row for row in reader]
                
                parent_id=[int(x[0]) for x in parent_id_vals]
                print "---_TOTAL ID---",len(parent_id)
                
                import ipdb;ipdb.set_trace()
            
            with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/resplusindiauserss.csv','r') as e: 
                reader = csv.reader(e)
                
                vals=[row for row in reader]
                
                for val in vals : 
                    
                    val=[x.strip() for x in val]
                    if "\\N" in val[3] or not val[3]:
                        continue
                    
                    
                    #SEARCH PARTNER
                    partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                    if not partner_id  :
                        partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[3])])
                        if not partner_id :
                            #import ipdb;ipdb.set_trace()
                            continue    
                                     
                            
                    if len(partner_id)>1: 
                        
                        continue      
                    
                    #GET PARTNER
                    partner=partner_obj.browse(cr,uid,partner_id[0])
                    if partner.id in parent_id :
                        
                        self.count+=1;print self.count
                        child_id=partner.child_ids[0]
                        #import ipdb;ipdb.set_trace()
                        partner_obj.write(cr,uid,[child_id.id],{"name":val[6]})
                        print '==-----------correction done----------'
            return  True

        def reseller_int(self,cr,uid):
            self.count=0
            import ipdb;ipdb.set_trace()
            # RESELLER int 
            
            with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/correct_contact_peron/reseller_int.csv','r') as e: 
                reader = csv.reader(e)
                
                parent_id_vals=[row for row in reader]
                
                parent_id=[int(x[0]) for x in parent_id_vals]
                print "---_TOTAL ID---",len(parent_id)
                
                import ipdb;ipdb.set_trace()
            
            with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/resellerplususerss.csv','r') as e: 
                reader = csv.reader(e)
                
                vals=[row for row in reader]
                
                for val in vals : 
                    
                    val=[x.strip() for x in val]
                    if "\\N" in val[3] or not val[3]:
                        continue
                    
                    
                    
                    #SEARCH PARTNER
                    partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                    if not partner_id  :
                        partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[3])])
                        if not partner_id :
                            #import ipdb;ipdb.set_trace()
                            continue    
                                     
                            
                    if len(partner_id)>1: 
                        
                        continue      
                    
                    #GET PARTNER
                    partner=partner_obj.browse(cr,uid,partner_id[0])
                    if partner.id in parent_id :
                        
                        self.count+=1;print self.count
                        child_id=partner.child_ids[0]
                        #import ipdb;ipdb.set_trace()
                        partner_obj.write(cr,uid,[child_id.id],{"name":val[6]})
                        print '==-----------correction done----------'
            return  True


        def indiaplus_local(self,cr,uid):
            self.count=0
            import ipdb;ipdb.set_trace()
            # indiaplus
            
            with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/correct_contact_peron/indiaplus.csv','r') as e: 
                reader = csv.reader(e)
                
                parent_id_vals=[row for row in reader]
                
                parent_id=[int(x[0]) for x in parent_id_vals]
                print "---_TOTAL ID---",len(parent_id)
                
                import ipdb;ipdb.set_trace()
            
            with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/indiaplususerss.csv','r') as e: 
                reader = csv.reader(e)
                
                vals=[row for row in reader]
                
                for val in vals : 
                    
                    val=[x.strip() for x in val]
                    if "\\N" in val[2] or not val[2]:
                        continue
                    
                    
                    
                    #SEARCH PARTNER
                    partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[2])])
                    if not partner_id  :
                        partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                        if not partner_id :
                            #import ipdb;ipdb.set_trace()
                            continue    
                                     
                            
                    if len(partner_id)>1: 
                        
                        continue      
                    
                    #GET PARTNER
                    partner=partner_obj.browse(cr,uid,partner_id[0])
                    if partner.id in parent_id :
                        
                        self.count+=1;print self.count
                        if not partner.child_ids : 
                            continue
                        
                        child_id=partner.child_ids[0]
                        #import ipdb;ipdb.set_trace()
                        partner_obj.write(cr,uid,[child_id.id],{"name":val[5]})
                        print '==-----------correction done----------'
            return  True


        def smsplus_int(self,cr,uid):
            self.count=0
            import ipdb;ipdb.set_trace()
            # smsplus
            
            with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/correct_contact_peron/smsplus.csv','r') as e: 
                reader = csv.reader(e)
                
                parent_id_vals=[row for row in reader]
                
                parent_id=[int(x[0]) for x in parent_id_vals]
                print "---_TOTAL ID---",len(parent_id)
                
                import ipdb;ipdb.set_trace()
            
            with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/smsplususerss.csv','r') as e: 
                reader = csv.reader(e)
                
                vals=[row for row in reader]
                
                for val in vals : 
                    
                    val=[x.strip() for x in val]
                    if "\\N" in val[2] or not val[2]:
                        continue
                    
                    
                    
                    #SEARCH PARTNER
                    partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[2])])
                    if not partner_id  :
                        partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                        if not partner_id :
                            #
                            continue    
                                     
                            
                    if len(partner_id)>1: 
                        
                        continue      
                    
                    #GET PARTNER
                    try :
                        
                        partner=partner_obj.browse(cr,uid,partner_id[0])
                        
                        
                        if partner.id in parent_id :
                            self.count+=1;print self.count
                            if self.count==8:
                                import ipdb;ipdb.set_trace()
                            else:
                                continue
                            if not partner.child_ids : 
                                continue
                            child_id=partner.child_ids[0]
                            #import ipdb;ipdb.set_trace()
                            partner_obj.write(cr,uid,[child_id.id],{"name":val[5]})
                            print '==-----------correction done----------'
                    except Exception as E:
                        print E,self.count
                        import ipdb;ipdb.set_trace()
                        
                        
            return  True


        
#         fun =distributor_local(self,cr,uid)
#         fun1 =distributor_int(self,cr,uid)
#         fun2 =reseller_local(self,cr,uid)
#         fun3 =reseller_int(self,cr,uid)
#         fun4 =indiaplus_local(self,cr,uid)
        fun5 =smsplus_int(self,cr,uid)
           
                
        print "=======over========"
        return True



    def update_partner_account_status(self,cr,uid,vals ): 
        '''API to set partner status from Test To Live '''
        uid=SUPERID
        partner_add_user_obj=self.pool.get('res.partner.add.user')
        server_obj=self.pool.get('server')
        partner_obj=self.pool.get("res.partner")
        
        try : 
            
            assert vals.get("username") , "Username Name Required"
            assert vals.get("servername") , "Server Name Required"
            assert vals.get("odooid") , "Odoo Id Required"
	    #import ipdb;ipdb.set_trace()
         
            #  CHECK SERVER EXIST IN ODOO
            server_id=server_obj.search(cr,uid,[ ('name' ,'=',vals.get('servername')) ])
            if not server_id : 
                server_id=server_obj.search(cr,uid,[ ('active','=',False),('name' ,'=',vals.get('servername')) ])
                
            assert server_id , "No Server Found On Odoo"
            assert len(server_id) == 1, "Multiple Server Found"
            
            #  CHECK USERNAME AND ODOO ID EXIST IN ODOO
            
            add_user_val=partner_add_user_obj.search(cr,uid,[ ('username','=', vals.get('username') ) ])
            assert add_user_val, "No User Found In Odoo"
            
                     
            add_user_ids=[ x for x in partner_add_user_obj.browse(cr, uid, add_user_val) ]
            
            assert add_user_ids, "No User Account Found"
            assert len(add_user_ids) == 1, "Multiple User Account Found"
            #[ partner_add_user_obj.write(cr,uid,[add_user.id],{'is_live':True}) for add_user in (x for x in partner_add_user_obj.browse(cr,uid,add_user_val)) if add_user   ]
            for add_user in add_user_ids :
                assert  add_user.partner_id.partner_sequence == vals.get("odooid"), "User Account Belongs \
                To Different Odoo Id"
                #assert not add_user.is_live ,"User Account Status Is Already Set To Live On Odoo"
                partner_add_user_obj.write(cr, uid, [ add_user.id ], { 'is_live' : True, 'server_domain' : server_id[0] })
                
                # SEND EMAIL NOTIFICATIONS 
                partner_obj.user_account_email_notifications (cr, SUPERUSERID, add_user, "test_to_live" )
                return "User Account Successfully Updated"

        except Exception as E:
            if not E.message : 
                E.message=E.value   

            return E.message   
           
        return "Updating User Failed"


    def create_contact_person_for_user_account(self,cr,uid,vals): 
        '''create missing contact person '''
        
        partner_obj=self.pool.get('res.partner')
        server_obj=self.pool.get('server')
        res={}
        
        
        def server_distributor_local(self,cr,uid ):
            '''#CASE 6: DISTRIBUTOR ->  LOCAL '''


            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/displusindiauserss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        #import ipdb;ipdb.set_trace()
                            
                            
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[3] or not val[3]:
                            continue
                        
                        bactive=True if val[11]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :
                                #import ipdb;ipdb.set_trace()
                                continue    
                                         
                                
                        if len(partner_id)>1: 
                            
                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])
                        if not partner.child_ids :         
                            partner_vals={}
                            partner_vals={'comment': False, 'user_id':partner.user_id.id,'function': False, 'property_account_position': False,\
                                          'notify_email': 'none', 'message_follower_ids': False, 'company_registery': False,\
                                          'image': False, 'property_stock_supplier': 8, 'use_parent_address': False, 'active': partner.active, \
                                             'property_stock_customer': 9, 'payment_next_action_date': False, 'tan': False,\
                                           'property_product_pricelist': False, 'message_ids': False, 'city': False, 'opt_out': False,\
                                             'title': False, 'property_account_receivable': 1225, 'company_id': 1, \
                                            'property_account_payable': 1117, 'parent_id': partner.id, 'last_reconciliation_date': False, 'pan': False,\
                                            'supplier': partner.supplier, 'routesms_cust_id': False,  'is_company': False, 'website': False,\
                                            'lang': 'en_US',  'bank_ids': [], 'vertical': 1, 'routesms_remark': 'PARTNER IMPORTED VIA USER ACCOUNT SHEET distributor local', 'child_ids': [],\
                                            'section_id': False, 'partner_type': False, \
                                            'property_supplier_payment_term': False, 'signatory': False, 'date': False, 'unreconciled_aml_ids': [],\
                                            'vat_subjected': False, 'payment_responsible_id': False, 'customer': partner.customer, 'ref': False, 'name': row[6],\
                                            'property_product_pricelist_purchase': 2  , 'type': 'contact', 'cin': False,\
                                            'postpaid': partner.postpaid, 'payment_next_action': False, 'vat': False,\
                                            'property_payment_term': False,  'category_id': [[6, False, []]], 'prepaid': partner.prepaid, \
                                            'payment_note': False,'use_parent_address':True}
    
                            #import ipdb;ipdb.set_trace()               
                            new_contact_partner_id=partner_obj.create(cr,uid,partner_vals)
                                #add odoo od
                                
                            odoo_id=partner_obj.validate_partner(cr,uid,[new_contact_partner_id],{})
                            print '--------contact person added---------'                        
                        

                        
                        
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True                    

        def server_distributor_international(self, partner_user, emp_id): 
            '''#CASE 5: DISTRIBUTOR ->  INTERNATIONAL '''        

            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/displususerss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        
                            
                            
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[3] or not val[3]:
                            continue
                        
                        bactive=True if val[11]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :
                                #import ipdb;ipdb.set_trace()
                                continue    
                                         
                                
                        if len(partner_id)>1: 
                            
                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
                        if not partner.child_ids :         
                            partner_vals={}
                            partner_vals={'comment': False, 'user_id':partner.user_id.id,'function': False, 'property_account_position': False,\
                                          'notify_email': 'none', 'message_follower_ids': False, 'company_registery': False,\
                                          'image': False, 'property_stock_supplier': 8, 'use_parent_address': False, 'active': partner.active, \
                                             'property_stock_customer': 9, 'payment_next_action_date': False, 'tan': False,\
                                           'property_product_pricelist': False, 'message_ids': False, 'city': False, 'opt_out': False,\
                                             'title': False, 'property_account_receivable': 1225, 'company_id': 1, \
                                            'property_account_payable': 1117, 'parent_id': partner.id, 'last_reconciliation_date': False, 'pan': False,\
                                            'supplier': partner.supplier, 'routesms_cust_id': False,  'is_company': False, 'website': False,\
                                            'lang': 'en_US',  'bank_ids': [], 'vertical': 1, 'routesms_remark': 'PARTNER IMPORTED VIA USER ACCOUNT SHEET distributor international', 'child_ids': [],\
                                            'section_id': False, 'partner_type': False, \
                                            'property_supplier_payment_term': False, 'signatory': False, 'date': False, 'unreconciled_aml_ids': [],\
                                            'vat_subjected': False, 'payment_responsible_id': False, 'customer': partner.customer, 'ref': False, 'name': row[6],\
                                            'property_product_pricelist_purchase': 2  , 'type': 'contact', 'cin': False,\
                                            'postpaid': partner.postpaid, 'payment_next_action': False, 'vat': False,\
                                            'property_payment_term': False,  'category_id': [[6, False, []]], 'prepaid': partner.prepaid, \
                                            'payment_note': False,'use_parent_address':True}
    
                            #import ipdb;ipdb.set_trace()               
                            new_contact_partner_id=partner_obj.create(cr,uid,partner_vals)
                                #add odoo od
                            
                            odoo_id=partner_obj.validate_partner(cr,uid,[new_contact_partner_id],{})
                            print '--------contact person added---------'                        
                        
                        
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True             



        def server_reseller_local(self, cr,uid):  
            '''CASE 4: RESELLER ->  LOCAL '''   

            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/resplusindiauserss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        #import ipdb;ipdb.set_trace()
                            
                            
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[3] or not val[3]:
                            continue
                        
                        bactive=True if val[11]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :
                                #import ipdb;ipdb.set_trace()
                                continue    
                                         
                                
                        if len(partner_id)>1: 
                            
                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])
                        if not partner.child_ids :         
                            partner_vals={}
                            partner_vals={'comment': False, 'user_id':partner.user_id.id,'function': False, 'property_account_position': False,\
                                          'notify_email': 'none', 'message_follower_ids': False, 'company_registery': False,\
                                          'image': False, 'property_stock_supplier': 8, 'use_parent_address': False, 'active': partner.active, \
                                             'property_stock_customer': 9, 'payment_next_action_date': False, 'tan': False,\
                                           'property_product_pricelist': False, 'message_ids': False, 'city': False, 'opt_out': False,\
                                             'title': False, 'property_account_receivable': 1225, 'company_id': 1, \
                                            'property_account_payable': 1117, 'parent_id': partner.id, 'last_reconciliation_date': False, 'pan': False,\
                                            'supplier': partner.supplier, 'routesms_cust_id': False,  'is_company': False, 'website': False,\
                                            'lang': 'en_US',  'bank_ids': [], 'vertical': 1, 'routesms_remark': 'PARTNER IMPORTED VIA USER ACCOUNT SHEET reseller local', 'child_ids': [],\
                                            'section_id': False, 'partner_type': False, \
                                            'property_supplier_payment_term': False, 'signatory': False, 'date': False, 'unreconciled_aml_ids': [],\
                                            'vat_subjected': False, 'payment_responsible_id': False, 'customer': partner.customer, 'ref': False, 'name': row[6],\
                                            'property_product_pricelist_purchase': 2  , 'type': 'contact', 'cin': False,\
                                            'postpaid': partner.postpaid, 'payment_next_action': False, 'vat': False,\
                                            'property_payment_term': False,  'category_id': [[6, False, []]], 'prepaid': partner.prepaid, \
                                            'payment_note': False,'use_parent_address':True}
    
                            #import ipdb;ipdb.set_trace()               
                            new_contact_partner_id=partner_obj.create(cr,uid,partner_vals)
                                #add odoo od
                                
                            odoo_id=partner_obj.validate_partner(cr,uid,[new_contact_partner_id],{})
                            print '--------contact person added---------'                                      
                        
                        
                        
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True             


                 

        def server_reseller_international(self, cr,uid): 
            
            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/resellerplususerss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        #import ipdb;ipdb.set_trace()
                            
                            
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[3] or not val[3]:
                            continue
                        
                        bactive=True if val[11]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :

                                continue    
                                         
                                
                        if len(partner_id)>1: 

                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
                        if not partner.child_ids :         
                            partner_vals={}
                            partner_vals={'comment': False, 'user_id':partner.user_id.id,'function': False, 'property_account_position': False,\
                                          'notify_email': 'none', 'message_follower_ids': False, 'company_registery': False,\
                                          'image': False, 'property_stock_supplier': 8, 'use_parent_address': False, 'active': partner.active, \
                                             'property_stock_customer': 9, 'payment_next_action_date': False, 'tan': False,\
                                           'property_product_pricelist': False, 'message_ids': False, 'city': False, 'opt_out': False,\
                                             'title': False, 'property_account_receivable': 1225, 'company_id': 1, \
                                            'property_account_payable': 1117, 'parent_id': partner.id, 'last_reconciliation_date': False, 'pan': False,\
                                            'supplier': partner.supplier, 'routesms_cust_id': False,  'is_company': False, 'website': False,\
                                            'lang': 'en_US',  'bank_ids': [], 'vertical': 1, 'routesms_remark': 'PARTNER IMPORTED VIA USER ACCOUNT SHEET reseller international', 'child_ids': [],\
                                            'section_id': False, 'partner_type': False, \
                                            'property_supplier_payment_term': False, 'signatory': False, 'date': False, 'unreconciled_aml_ids': [],\
                                            'vat_subjected': False, 'payment_responsible_id': False, 'customer': partner.customer, 'ref': False, 'name': row[5],\
                                            'property_product_pricelist_purchase': 2  , 'type': 'contact', 'cin': False,\
                                            'postpaid': partner.postpaid, 'payment_next_action': False, 'vat': False,\
                                            'property_payment_term': False,  'category_id': [[6, False, []]], 'prepaid': partner.prepaid, \
                                            'payment_note': False,'use_parent_address':True}
    
                            #import ipdb;ipdb.set_trace()               
                            new_contact_partner_id=partner_obj.create(cr,uid,partner_vals)
                                #add odoo od
                                
                            odoo_id=partner_obj.validate_partner(cr,uid,[new_contact_partner_id],{})
                            print '--------contact person added---------' 
                        
                        
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True             
            

        
        def server_general_international(self, cr,uid): 
            '''# CASE 1: GENERAL->  INTERNATIONAL '''
            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/smsplususerss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        #import ipdb;ipdb.set_trace()
#                         if self.count==300:
#                             import ipdb;ipdb.set_trace()
#                         else :
#                             continue
                            
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[2] or not val[2]:
                            continue
                        
                        bactive=True if val[10]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[2])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :

                                continue    
                                         
                                
                        if len(partner_id)>1: 

                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
                        if not partner.child_ids :         
                            partner_vals={}
                            partner_vals={'comment': False, 'user_id':partner.user_id.id,'function': False, 'property_account_position': False,\
                                          'notify_email': 'none', 'message_follower_ids': False, 'company_registery': False,\
                                          'image': False, 'property_stock_supplier': 8, 'use_parent_address': False, 'active': partner.active, \
                                             'property_stock_customer': 9, 'payment_next_action_date': False, 'tan': False,\
                                           'property_product_pricelist': False, 'message_ids': False, 'city': False, 'opt_out': False,\
                                             'title': False, 'property_account_receivable': 1225, 'company_id': 1, \
                                            'property_account_payable': 1117, 'parent_id': partner.id, 'last_reconciliation_date': False, 'pan': False,\
                                            'supplier': partner.supplier, 'routesms_cust_id': False,  'is_company': False, 'website': False,\
                                            'lang': 'en_US',  'bank_ids': [], 'vertical': 1, 'routesms_remark': 'PARTNER IMPORTED VIA USER ACCOUNT SHEET general international', 'child_ids': [],\
                                            'section_id': False, 'partner_type': False, \
                                            'property_supplier_payment_term': False, 'signatory': False, 'date': False, 'unreconciled_aml_ids': [],\
                                            'vat_subjected': False, 'payment_responsible_id': False, "customer": partner.customer, 'ref': False, 'name': row[5],\
                                            'property_product_pricelist_purchase': 2  , 'type': 'contact', 'cin': False,\
                                            'postpaid': partner.postpaid, 'payment_next_action': False, 'vat': False,\
                                            'property_payment_term': False,  'category_id': [[6, False, []]], 'prepaid': partner.prepaid, \
                                            'payment_note': False,'use_parent_address':True}
    
                            new_contact_partner_id=partner_obj.create(cr,uid,partner_vals)
                                #add odoo od
                                
                            odoo_id=partner_obj.validate_partner(cr,uid,[new_contact_partner_id],{})
                            print '--------contact person added---------' 
                        
                        
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True
            
            
        def server_general_local(self,cr,uid): 
            '''# CASE 2: GENERAL-> LOCAL  '''
            
            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/indiaplususerss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[2] or not val[2]:
                            continue
                        
                        bactive=True if val[10]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[2])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :

                                continue    
                                         
                                
                        if len(partner_id)>1: 

                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
 
                        
                        if not partner.child_ids :         
                            partner_vals={}
                            partner_vals={'comment': False, 'user_id':partner.user_id.id,'function': False, 'property_account_position': False,\
                                          'notify_email': 'none', 'message_follower_ids': False, 'company_registery': False,\
                                          'image': False, 'property_stock_supplier': 8, 'use_parent_address': False, 'active': partner.active, \
                                             'property_stock_customer': 9, 'payment_next_action_date': False, 'tan': False,\
                                           'property_product_pricelist': False, 'message_ids': False, 'city': False, 'opt_out': False,\
                                             'title': False, 'property_account_receivable': 1225, 'company_id': 1, \
                                            'property_account_payable': 1117, 'parent_id': partner.id, 'last_reconciliation_date': False, 'pan': False,\
                                            'supplier': partner.supplier, 'routesms_cust_id': False,  'is_company': False, 'website': False,\
                                            'lang': 'en_US',  'bank_ids': [], 'vertical': 1, 'routesms_remark': 'PARTNER IMPORTED VIA USER ACCOUNT SHEET general local', 'child_ids': [],\
                                            'section_id': False, 'partner_type': False, \
                                            'property_supplier_payment_term': False, 'signatory': False, 'date': False, 'unreconciled_aml_ids': [],\
                                            'vat_subjected': False, 'payment_responsible_id': False, 'customer': partner.customer, 'ref': False, 'name': row[5],\
                                            'property_product_pricelist_purchase': 2  , 'type': 'contact', 'cin': False,\
                                            'postpaid': partner.postpaid, 'payment_next_action': False, 'vat': False,\
                                            'property_payment_term': False,  'category_id': [[6, False, []]], 'prepaid': partner.prepaid, \
                                            'payment_note': False,'use_parent_address':True}
    
                            #import ipdb;ipdb.set_trace()               
                            new_contact_partner_id=partner_obj.create(cr,uid,partner_vals)
                                #add odoo od
                                
                            odoo_id=partner_obj.validate_partner(cr,uid,[new_contact_partner_id],{})
                            print '--------contact person added---------' 
                        
                
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True
        fun = server_general_international(self,cr,uid)    
        fun1=server_general_local(self,cr,uid)
        fun2 =server_reseller_international(self,cr,uid)
        fun3 =server_reseller_local(self,cr,uid)
        fun4 = server_distributor_international (self,cr,uid)
        fun5 = server_distributor_local (self,cr,uid)
        print "------------OVER--------------"
        return True



    def upload_user_account_data_from_legacy(self,cr,uid,vals): 
        '''upload user data from RSL servers '''
        
        partner_obj=self.pool.get('res.partner')
        server_obj=self.pool.get('server')
        res={}
        
        
        def server_distributor_local(self,cr,uid ):
            '''#CASE 6: DISTRIBUTOR ->  LOCAL '''


            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/displusindiauserss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        #import ipdb;ipdb.set_trace()
                            
                            
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[3] or not val[3]:
                            continue
                        
                        bactive=True if val[11]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :
                                #import ipdb;ipdb.set_trace()
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_local/logs/no_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[3])+'\n') 
                                continue    
                                         
                                
                        if len(partner_id)>1: 
                            
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_local/logs/multiple_odoo_id_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[3])+'\n') 
                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
                        #SEARCH SERVER
                        server_id=server_obj.search(cr,uid,[("name","=",val[2])])
                        if not server_id  :
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_local/logs/no_server_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue                      
                                
                        if len(server_id)>1: 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_local/logs/multiple_serverfound.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue          
                        
                        #GET SERVER
                        server=server_obj.browse(cr,uid,server_id[0])   
    
                        
                        res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                        "od_limit":float(val[8]),"credit_limit":float(val[7]),"status":"approved",\
                        "is_live":True,"routesms_notes":"FROM LEGACY","is_active":bactive,"reseller_code":val[1]}
    
                        add_user_obj.create(cr,uid,res)
                        print "----USER CREATED FROM LEGACY----"
                        
                        
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True                    

        def server_distributor_international(self, partner_user, emp_id): 
            '''#CASE 5: DISTRIBUTOR ->  INTERNATIONAL '''        

            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/displususerss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        #import ipdb;ipdb.set_trace()
                            
                            
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[3] or not val[3]:
                            continue
                        
                        bactive=True if val[11]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :
                                #import ipdb;ipdb.set_trace()
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_international/logs/no_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[3])+'\n') 
                                continue    
                                         
                                
                        if len(partner_id)>1: 
                            
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_international/logs/multiple_odoo_id_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[3])+'\n') 
                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
                        #SEARCH SERVER
                        server_id=server_obj.search(cr,uid,[("name","=",val[2])])
                        if not server_id  :
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_international/logs/no_server_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue                      
                                
                        if len(server_id)>1: 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_distributor_international/logs/multiple_serverfound.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue          
                        
                        #GET SERVER
                        server=server_obj.browse(cr,uid,server_id[0])   
    
                        
                        res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                        "local_price":float(val[7]),"od_limit":float(val[9]),"credit_limit":float(val[8]),"status":"approved",\
                        "is_live":True,"routesms_notes":"FROM LEGACY","is_active":bactive,"reseller_code":val[1]}
    
                        add_user_obj.create(cr,uid,res)
                        print "----USER CREATED FROM LEGACY----"
                        
                        
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True             



        def server_reseller_local(self, cr,uid):  
            '''CASE 4: RESELLER ->  LOCAL '''   

            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/resplusindiauserss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        #import ipdb;ipdb.set_trace()
                            
                            
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[3] or not val[3]:
                            continue
                        
                        bactive=True if val[11]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :
                                #import ipdb;ipdb.set_trace()
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_local/logs/no_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[3])+'\n') 
                                continue    
                                         
                                
                        if len(partner_id)>1: 
                            
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_local/logs/multiple_odoo_id_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[3])+'\n') 
                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
                        #SEARCH SERVER
                        server_id=server_obj.search(cr,uid,[("name","=",val[2])])
                        if not server_id  :
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_local/logs/no_server_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue                      
                                
                        if len(server_id)>1: 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_local/logs/multiple_serverfound.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue          
                        
                        #GET SERVER
                        server=server_obj.browse(cr,uid,server_id[0])   
    
                        
                        res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                        "od_limit":float(val[8]),"credit_limit":float(val[7]),"status":"approved",\
                        "is_live":True,"routesms_notes":"FROM LEGACY","is_active":bactive,"reseller_code":val[1]}
    
                        add_user_obj.create(cr,uid,res)
                        print "----USER CREATED FROM LEGACY----"
                        
                        
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True             


                 

        def server_reseller_international(self, cr,uid): 
            
            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/resellerplususerss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        #import ipdb;ipdb.set_trace()
                            
                            
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[3] or not val[3]:
                            continue
                        
                        bactive=True if val[11]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[3])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :
                                #import ipdb;ipdb.set_trace()
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_international/logs/no_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[3])+'\n') 
                                continue    
                                         
                                
                        if len(partner_id)>1: 
                            
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_international/logs/multiple_odoo_id_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[3])+'\n') 
                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
                        #SEARCH SERVER
                        server_id=server_obj.search(cr,uid,[("name","=",val[2])])
                        if not server_id  :
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_international/logs/no_server_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue                      
                                
                        if len(server_id)>1: 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_reseller_international/logs/multiple_serverfound.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[3]) +  '\n') 
                            continue          
                        
                        #GET SERVER
                        server=server_obj.browse(cr,uid,server_id[0])   
    
                        
                        res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                        "local_price":float(val[7]),"od_limit":float(val[9]),"credit_limit":float(val[8]),"status":"approved",\
                        "is_live":True,"routesms_notes":"FROM LEGACY","is_active":bactive,"reseller_code":val[1]}
    
                        add_user_obj.create(cr,uid,res)
                        print "----USER CREATED FROM LEGACY----"
                        
                        
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True             
            

        
        def server_general_international(self, cr,uid): 
            '''# CASE 1: GENERAL->  INTERNATIONAL '''
            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/smsplususerss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        #import ipdb;ipdb.set_trace()
                            
                            
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[2] or not val[2]:
                            continue
                        
                        bactive=True if val[10]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[2])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_international/logs/no_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[2])+'\n') 
                                continue    
                                         
                                
                        if len(partner_id)>1: 
                            import ipdb;ipdb.set_trace()
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_international/logs/multiple_odoo_id_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[2])+'\n') 
                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
                        #SEARCH SERVER
                        server_id=server_obj.search(cr,uid,[("name","=",val[1])])
                        if not server_id  :
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_international/logs/no_server_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[2]) +  '\n') 
                            continue                      
                                
                        if len(server_id)>1: 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_international/logs/multiple_serverfound.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+ "{}" +  str(val[2]) +  '\n') 
                            continue          
                        
                        #GET SERVER
                        server=server_obj.browse(cr,uid,server_id[0])   
    
                        
                        res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                        "local_price":float(val[6]),"od_limit":float(val[8]),"credit_limit":float(val[7]),"status":"approved",\
                        "is_live":True,"routesms_notes":"FROM LEGACY","is_active":bactive}
    
                        add_user_obj.create(cr,uid,res)
                        print "----USER CREATED FROM LEGACY----"
                        
                        
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True
            
            
        def server_general_local(self,cr,uid): 
            '''# CASE 2: GENERAL-> LOCAL  '''
            
            add_user_obj=self.pool.get("res.partner.add.user") 
            try : 
                import ipdb;ipdb.set_trace()
                with open('/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/indiaplususerss.csv','r') as e: 
                    reader = csv.reader(e)
                    
                    vals=[row for row in reader]
                    
                    for val in vals :
                        self.count+=1;print self.count
                        val=[x.strip() for x in val]
                        
                        # ACTIVE ACCOUNT OR NOT
#                         if val[2]=="R118553":
#                             import ipdb;ipdb.set_trace()
#                         else:
#                             
#                             continue
                            
                        if "\\N" in val[2] or not val[2]:
                            continue
                        
                        bactive=True if val[10]=="ACTIVE" else False
                        
                        #SEARCH PARTNER
                        partner_id=partner_obj.search(cr,uid,[("partner_sequence","=",val[2])])
                        if not partner_id  :
                            partner_id=partner_obj.search(cr,uid,[("active","=",False),("partner_sequence","=",val[2])])
                            if not partner_id :
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/no_odoo_id_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[2])+'\n') 
                                continue    
                                         
                                
                        if len(partner_id)>1: 
                            import ipdb;ipdb.set_trace()
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/multiple_odoo_id_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[2])+'\n') 
                            continue      
                        
                        #GET PARTNER
                        partner=partner_obj.browse(cr,uid,partner_id[0])        
                        
                        #SEARCH SERVER
                        server_id=server_obj.search(cr,uid,[("name","=",val[1])])
                        if not server_id  :
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/no_server_found.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+'\n') 
                            continue                      
                                
                        if len(server_id)>1: 
                            with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/multiple_serverfound.txt", "a") as donefile_new:
                                donefile_new.write(str(val[0])+'\n') 
                            continue          
                        
                        #GET SERVER
                        server=server_obj.browse(cr,uid,server_id[0])   
    
                        if val[12] == "PROMOTIONAL"  :
                            routetype = "promotional"
                             
                        elif val[12] == "TRANSACTIONAL"  :  
                            routetype = "transactional"
                            
                        elif val[12] == "BOTH"  :  
                            routetype = "both"
        
                        elif val[12] ==  "TRANSCRUB" :  
                            routetype = "transcrub"
        
                        else  : 
                                with open("/home/bista/Downloads/shanky/CSV_UPLOAD_SHEET/api3/final/server_general_local/logs/routetype_not_found.txt", "a") as donefile_new:
                                    donefile_new.write(str(val[0])+'\n') 
                                continue                      
                        
                        
                        res = {"partner_id":partner.id,"username":val[0],"server_domain":server.id,\
                        "local_price":float(val[6]),"od_limit":float(val[8]),"credit_limit":float(val[7]),"status":"approved",\
                        "is_live":True,"routesms_notes":"FROM LEGACY","is_active":bactive,"route_type":routetype}
    
                        add_user_obj.create(cr,uid,res)
                        print "----USER CREATED FROM LEGACY----"
                        
                
            except Exception as E :
                print E
                import ipdb;ipdb.set_trace()
            
            return True
        fun = server_general_international(self,cr,uid)    
        fun1=server_general_local(self,cr,uid)
        fun2 =server_reseller_international(self,cr,uid)
        fun3 =server_reseller_local(self,cr,uid)
        fun4 = server_distributor_international (self,cr,uid)
        fun5 = server_distributor_local (self,cr,uid)
        print "------------OVER--------------"
        return True



    def compute_assets(self,cr,uid,vals):
        '''compute old asset auto '''
        asset_obj=self.pool.get('account.asset.asset')
        asset_obj.compute_depreciation_board(cr,uid,)
        return True

    def auto_old_asset_create_move(self,cr,uid,vals): 
        '''Generate Auto Moves for Asset old records'''
        asset_obj=self.pool.get('account.asset.asset')
        asset_line_obj=self.pool.get('account.asset.depreciation.line')
        current_date=time.strftime("%Y-%m-%d")
        #start_dedicated_date="2016-04-01"
        #dedicated_date="2016-04-30"
        import ipdb;ipdb.set_trace()
        dedicated_date="2016-04-01"
        try : 
            global count
            for asset in asset_obj.browse(cr,uid,asset_obj.search(cr,uid,[('state','=','open')])) :
                #if wow>0:break 
                count+=1;print count
                if asset.depreciation_line_ids : 
                    for asset_line in asset.depreciation_line_ids :
                        
                        #if dedicated_date >=asset_line.depreciation_date ==start_dedicated_date  and asset_line.move_check ==False : 
                        if asset_line.depreciation_date <=dedicated_date and asset_line.move_check ==False : 
                            asset_line_obj.create_move(cr, uid, [asset_line.id])
                            print '-------------------ASSET  MOVE  AUTOMATICALLY  CREATED-----------------'

        except Exception as E : 
            print E                                   
                        
        print '-------------EXITING SCRIPTING---------------'
        return True    
    

    def upload_asset_data(self,cr,uid,vals):
        ''' import asset category and asset record from excel sheet'''
        
        asset_obj=self.pool.get('account.asset.asset')
        
        asset_cat_obj=self.pool.get('account.asset.category')
        count=0
        import ipdb;ipdb.set_trace()
        #with open('/home/bista/Downloads/shanky/2016/MARFCH/18march/final_asset.csv','r') as e: 
        with open('/home/bista/Downloads/shanky/2016/APRIL/final_asset.csv','r') as e:
            reader = csv.reader(e)
            
            vals=[row for row in reader]
            
            for val in vals :
                res={}
                count+=1;print count
#                 if count==597 : 
#                     import ipdb;ipdb.set_trace()
#                 else :
#                     
#                     continue    
                val=[value.strip() for value in val]
                print val
                cat=asset_cat_obj.browse(cr,uid,int(val[1]))
                name=cat.name
                try:
                    
                    category_id=int(float(val[1]))
                except Exception as E :
                    continue
                
                purchase_date='04-01-2015'
                currency_id=1064
                company_id=10
                purchase_value=float(val[6].replace(',',''))
                salvage_value=float(val[4].replace(',',''))
                value_residual=purchase_value-salvage_value
                prorata=True
                try :
                    
                    method_number=int(val[5])
                    if method_number :
                        method_number=method_number*12
                        method_period=1
                        
                except Exception as E : 
                    
                    method_number=0
                    method_period=0
                    
                    
                
                res.update({'name':name,'category_id':category_id,'purchase_date':purchase_date,\
                'currency_id':currency_id,'company_id':company_id,'purchase_value':purchase_value,\
                'salvage_value':salvage_value,'value_residual':value_residual,'prorata':prorata,\
                'method_number':method_number,'method_period':method_period})
                
                try :
                    
                    new_asset_id=asset_obj.create(cr,uid,res)
                    print '---------ASSET CREATED-------'
                    asset_obj.compute_depreciation_board(cr,uid,[new_asset_id])
                    print '---------ASSET COMPUTED-------'
                    asset_obj.validate(cr,uid,[new_asset_id])
                    print '---------ASSET CONFIRMED-------'
                    
                    
                except Exception as E : 
                    print E
                    import ipdb;ipdb.set_trace() 
                    E
                    
        print '##########OVER##################'
        return True
            
        





    def partner_auction(self,cr,uid,vals):
        '''display list of partner for auction rohan gupta clients '''
        partner_obj=self.pool.get('res.partner')
        partner_auction_obj=self.pool.get('res.partner.auction')
        
        query='''select id,name from res_partner where user_id=507 and is_company=True and active=True ORDER BY name ASC limit 500  '''
        cr.execute(query)
        partner_ids=map(lambda x:x[0],cr.fetchall())
        print '------TOTAL IDS-------',len(partner_ids)
        import ipdb;ipdb.set_trace()
        for partner in partner_obj.browse(cr,uid, partner_ids) :
            global count 
            count+=1;print count
            vals={'partner_id':partner.id, 'name':partner.name,'partner_active':'YES' if partner.active else 'NO',\
            'customer':'YES' if partner.customer else 'NO','supplier':'YES' if partner.supplier else 'NO',\
            'odoo_id':partner.partner_sequence,\
            'account_type':'prepaid' if partner.prepaid else 'postpaid','country':partner.country_id.name,\
            'lead_status':partner.crm_lead_state }
            partner_auction_obj.create(cr,uid,vals)
            print '-------AUCTION RECORD CREATED--------'
            
        print '-------over--------'
        return True

    def add_salesperson_alias_to_crm(self,cr,uid,vals):
        ''' add BM name to CRM for reporting'''
        count=0
        crm_obj=self.pool.get('crm.lead')
        crm_ids=crm_obj.search(cr,uid,[])
        print len(crm_ids)
        import ipdb;ipdb.set_trace()
        for crm in crm_obj.browse(cr,uid,crm_ids)  :
            count+=1;print count
            
            if crm.user_id : 
                cr.execute('''update crm_lead set salesperson_alias=%s where id=%s''',(crm.user_id.name,crm.id))
                print '****************UPDATED********************'
                
            else:
                print '****************NO BM  FOUND********************'
                with open("/home/bista/Downloads/shanky/no_bm.txt", "a") as donefile_new:
                    donefile_new.write(str(crm.id)+'\n')                     
                                            
        return True


    def deactivate_employee_record(self,cr,uid,vals): 
        ''' deactivate _employee_record'''
        
        dont_touch=[1,582,302,507,508]
        password='YourAccountDeactivated420'
        user_obj=self.pool.get('res.users')
        international_obj=self.pool.get('int.user')
        hr_obj=self.pool.get('hr.employee')
        data=[]
        count=0
        try:
            with open('/home/bista/Downloads/rakesh/deactivate_employee.csv','r') as e: 
                reader = csv.reader(e)
                country_li=[]
                vals1=[int(row[0]) for row in reader if row[2]=='1']
                import ipdb;ipdb.set_trace()
                
                for hr_id in vals1 :
                       
                    hr_obj.write(cr,uid,[hr_id],{'active':False})
                    print 'EMployye disabled'

        except Exception as E  :
            print E   


    def bmxpin_to_odoo_employee_structure(self,cr,uid,vals):
        '''copy bmxpin employee details to odoo '''
        count=0
        user_obj=self.pool.get('res.users')
        hr_obj=self.pool.get('hr.employee')
        partner_obj=self.pool.get('res.partner')
        hr_job_obj=self.pool.get('hr.job')
        import ipdb;ipdb.set_trace()
        emp_ids=hr_obj.search(cr,uid,[])
        emp_users_ids=[x.user_id.id for x in hr_obj.browse(cr,uid,emp_ids) ]
        user_id_not_found=[]
        try :
            
            data=[]
            with open('/home/bista/Downloads/shanky/2016/MARFCH/8march/employee_structure.csv','r') as e:  
                reader = csv.reader(e)
                country_li=[]
                count=0
    
                
                
                vals=[ row for row in reader]
                for val in vals :
                    #import ipdb;ipdb.set_trace()
                    res={}
                    count+=1;print count
                    if val[2] :
                        user_id=int(val[2])
                    else:
                        val.append('user_id not found in this record')
                        user_id_not_found.append(val)
                        #import ipdb;ipdb.set_trace()
                        continue
                        
                         
                    
                    hr_id=hr_obj.search(cr,uid,[('user_id','=',user_id)])
                    if not hr_id:
                        val.append('Employee record not found on LIVE')
                        user_id_not_found.append(val)
                        #import ipdb;ipdb.set_trace()
                        continue
                    if len(hr_id)>1 :
                        val.append('Multiple user assigned on  LIVE')
                        user_id_not_found.append(val)
                        #import ipdb;ipdb.set_trace()
                        continue
                        
                     
                    hr_id=hr_id[0]     
                        
#                     if user_id not in emp_users_ids:
#                         user_id_not_found.append(vals)
#                         continue
                    job_id=hr_job_obj.search(cr,uid,[('name','=',val[3])])

                    if not job_id :
                        pass
                        
                    elif len(job_id)>1 : 
                        import ipdb;ipdb.set_trace()
                        pass
                    else:
                        res.update({'job_id':job_id[0]})
                        
                    
                    if val[4]=='SuperAdmin':
                        role='SA'
                    elif val[4]=='Admin':
                        role='AD'
    
                    elif val[4]=='Enterprise':
                        role='ENT'
    
                    elif val[4]=='Support':
                        role='SUP'
    
                    elif val[4]=='Technical':
                        role='TECH'
    
                    elif val[4]=='Accounts':
                        role='ACC'
    
                    elif val[4]=='Independent':
                        role='IND'
    
                    elif val[4]=='Super Account':
                        role='SACC'
                        
                    else :
                        role=''
                    
                    res.update({'role':role})
                    res.update({'routesms_username':val[5]})
                    
                    #import ipdb;ipdb.set_trace()
                    #res.update({'job_id':job_ids,'role':role,'routesms_username':routesms_username})
                    hr_obj.write(cr,uid,[hr_id],res)
                    print '--RECORD UPDATED---'

            
            print len(user_id_not_found)
            import ipdb;ipdb.set_trace()
            with open('/home/bista/Downloads/shanky/2016/MARFCH/8march/no_emp_found.csv','wb') as csvfile:
            #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
                spamwriter = csv.writer(csvfile, delimiter=',')  
                         
                for write_rows in user_id_not_found:
                    try :
                    
                        spamwriter.writerow(write_rows)
                    except Exception as E :
                        print E

                    
        except Exception as E :
            import ipdb;ipdb.set_trace()
            print E
                    
                    

        print '-----over'
        
        return True



    def deactivate_partners_issue_no3_open_email_field(self,cr,uid,vals):
        ''' deactive partners who not rectified for issue no.3 '''

        partner_obj=self.pool.get('res.partner')
        hr_obj=self.pool.get('hr.employee')
        multi_emp=[]
        no_parent=[]
        no_user=[]
        contact_crm_id=[]
        count=0
        partners_ids=partner_obj.search(cr,uid,[('state','=','confirm'),('email','=',False),('is_company','=',True),\
                                                                            ('customer','=',True),('active','=',True)])

#         partners_ids=partner_obj.search(cr,uid,[('state','=','confirm'),('email','=',False),('is_company','=',True),\
#                                                                             ('active','=',True)])

        print '-----total partner = {}'.format(partners_ids)   
        import ipdb;ipdb.set_trace()   
        for partner in partner_obj.browse(cr,uid,partners_ids):
            count+=1;print count
            if partner :
                if partner.id==6:
                    continue
                else :
                    
                    cr.execute(''' select id from res_partner where parent_id=%s''',(partner.id,))
                    record_ids=[partner.id]+map(lambda x:x[0],cr.fetchall())
                    
                    cr.execute(''' update res_partner set active=False where id in %s''',(tuple(record_ids),))
                    
                    print '-----PARTNER DEACTIVATED---------------'

        import ipdb;ipdb.set_trace() 
        return True


    def issue_no1_1_genearte_odoo_id_to_contact_person(self,cr,uid,vals):
        ''' generate odoo id and confirm contact persons'''
        partner_obj=self.pool.get('res.partner')
        hr_obj=self.pool.get('hr.employee')
        contact_p=[]
        no_parent=[]
        not_applicable=[]
        count=0
        import ipdb;ipdb.set_trace()
        for partner in partner_obj.browse(cr,uid,partner_obj.search(cr,uid,[('state','!=','confirm'),('partner_sequence','=',False),('user_id','!=',False),('parent_id','!=',False),('is_company','=',False)])  ) :
            count+=1;print count
            if partner.parent_id :
                if partner.parent_id.partner_sequence and partner.parent_id.state=='confirm':
                    partner_obj.validate_contact_person(cr,uid,[partner.id],{})
                    contact_p.append(partner.id)
                    #print 'odoo id generate'

                else:
                    not_applicable.append(partner.id)
            else:
                no_parent.append([partner.id])
        import ipdb;ipdb.set_trace()        
        return True   	

    def issue_no3_open_email_field(self,cr,uid,vals):
        ''' set flag=True if email=False'''

        partner_obj=self.pool.get('res.partner')
        hr_obj=self.pool.get('hr.employee')
        multi_emp=[]
        no_parent=[]
        no_user=[]
        contact_crm_id=[]
        count=0
         
        import ipdb;ipdb.set_trace()   
        for partner in partner_obj.browse(cr,uid,partner_obj.search(cr,uid,[('state','=','confirm'),('email','=',False),('is_company','=',True)])  ) :
            count+=1;print count
            if partner :
                    cr.execute(''' update res_partner set check_primary_email=True where id =%s''',(partner.id,))
                    print 'rectified'
                    contact_crm_id.append(partner.id)
            else:
                 
                no_parent.append([partner.id])
#         import ipdb;ipdb.set_trace()      
#         vals=tuple(contact_crm_id)
#         cr.execute('''select count(id) from crm_lead where partner_id in %s ''',(vals,))
#         crm_vals=map(lambda x:x,cr.fetchall())
        import ipdb;ipdb.set_trace() 
        return True

    def sale_issue_no2_bm_not_found(self,cr,uid,vals):
        ''' assign rohan gupta to such records'''
        bm_id=507#Anand Tawari
        #bm_id=[410,460,405]#Anand Tawari
        partner_obj=self.pool.get('res.partner')
        hr_obj=self.pool.get('hr.employee')
        multi_emp=[]
        no_parent=[]
        no_contact=[]
        contact_crm_id=[]
        count=0
         
        
        idss=partner_obj.search(cr,uid,[('user_id','=',False),('is_company','=',True)])
        import ipdb;ipdb.set_trace()
        print len(idss)   
        for partner in partner_obj.browse(cr,uid,idss  ) :
            count+=1;print count
            if partner :
                    cr.execute(''' update res_partner set user_id=%s where id =%s''',(bm_id,partner.id))
                    print 'partner rectified'
                    if partner.child_ids : 
                        contact_ids=[contact.id for contact in partner.child_ids]
                        if contact_ids  :
                            
                            cr.execute(''' update res_partner set user_id=%s where id =%s''',(bm_id,partner.id))
                            print 'partner rectified'   
                        
                              
                        
                    else:
                            
                        no_contact.append(partner.id)

        import ipdb;ipdb.set_trace() 
        return True


    def remove_company_equal_true_from_contact_person(self,cr,uid,vals):
        ''' rectify contact person who are companies'''
        bm_id=[405]#Anand Tawari
        #bm_id=[410,460,405]#Anand Tawari
        partner_obj=self.pool.get('res.partner')
        hr_obj=self.pool.get('hr.employee')
        multi_emp=[]
        no_parent=[]
        no_user=[]
        contact_crm_id=[]
        count=0
         
        import ipdb;ipdb.set_trace()   
        for partner in partner_obj.browse(cr,uid,partner_obj.search(cr,uid,[('parent_id','!=',False),('is_company','=',True),('user_id','in',bm_id)])  ) :
            count+=1;print count
            if partner.parent_id :
                    cr.execute(''' update res_partner set is_company=False where id =%s''',(partner.id,))
                    print 'rectified'
                    contact_crm_id.append(partner.id)
            else:
                 
                no_parent.append([partner.id])
#         import ipdb;ipdb.set_trace()      
#         vals=tuple(contact_crm_id)
#         cr.execute('''select count(id) from crm_lead where partner_id in %s ''',(vals,))
#         crm_vals=map(lambda x:x,cr.fetchall())
        import ipdb;ipdb.set_trace() 
        return True


    def assign_account_type_to_contact_person(self,cr,uid,vals):
        ''' rectify contact person who are companies for account type'''
        partner_obj=self.pool.get('res.partner')
        hr_obj=self.pool.get('hr.employee')
        multi_emp=[]
        no_parent=[]
        no_account_type=[]
        both_account_type=[]
        count=0
        import ipdb;ipdb.set_trace()
        #for partner in partner_obj.browse(cr,uid,partner_obj.search(cr,uid,[('user_id','=',False),('parent_id','!=',False),('is_company','=',False)])  ) :
        for partner in partner_obj.browse(cr,uid,partner_obj.search(cr,uid,[('prepaid','=',False),('postpaid','=',False),('parent_id','!=',False),('is_company','=',True)])  ) :
            count+=1;print count
            if partner.parent_id :
                if partner.parent_id.prepaid and not partner.parent_id.postpaid:
                        cr.execute(''' update res_partner set prepaid=True where id =%s''',(partner.id,))
                        print 'prepaid'
                elif partner.parent_id.postpaid and not partner.parent_id.prepaid:
                        cr.execute(''' update res_partner set postpaid=True where id =%s''',(partner.id,))
                        print 'psotpaid'                
                
                elif partner.parent_id.postpaid and partner.parent_id.prepaid:
                    both_account_type.append([partner.id])
                
                elif not  partner.parent_id.postpaid and not partner.parent_id.prepaid:
                    no_account_type.append([partner.id])
                    
            else:
                no_parent.append([partner.id])
        import ipdb;ipdb.set_trace()        
        return True



    def assign_user_id_to_contact_person(self,cr,uid,vals):
        ''' rectify contact person who are companies'''
        partner_obj=self.pool.get('res.partner')
        hr_obj=self.pool.get('hr.employee')
        multi_emp=[]
        no_parent=[]
        no_user=[]
        count=0
        import ipdb;ipdb.set_trace()
        #for partner in partner_obj.browse(cr,uid,partner_obj.search(cr,uid,[('user_id','=',False),('parent_id','!=',False),('is_company','=',False)])  ) :
        for partner in partner_obj.browse(cr,uid,partner_obj.search(cr,uid,[('user_id','=',False),('parent_id','!=',False)])  ) :
            count+=1;print count
            if partner.parent_id :
                if partner.parent_id.user_id:
                        cr.execute(''' update res_partner set user_id=%s where id =%s''',(partner.parent_id.user_id.id,partner.id))
                        print 'rectified'
                else:
                    no_user.append([partner.id])
            else:
                no_parent.append([partner.id])
        import ipdb;ipdb.set_trace()        
        return True

    def check_crm_replica(self,cr,uid,vals):
        '''find partner of european countries '''
        count=0
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        data=[]
        with open('/home/bista/Downloads/shanky/2016/feb/replica_leads_client.csv','r') as e: 
            reader = csv.reader(e)
            country_li=[]
            
            partner_ids=[int(row[0]) for row in reader]
            
            for partner in partner_obj.browse(cr,uid,partner_ids) : 
                
                    
                crm_ids=crm_obj.search(cr,uid,[('partner_id','=',partner.id),('stage_id','!=',1)])
                if not crm_ids  :
                    #import ipdb;ipdb.set_trace()
                    cr.execute('''update res_partner set crm_lead_state=%s where id=%s ''',('New Lead / Query',partner.id))
                    print '------PARTNER   LEAD  STATUS  UPDATED-----------------'                    
                    
                if len(crm_ids)>1 : 
                    data.append([partner.id,partner.name,partner.partner_sequence,\
                                 partner.user_id.name,partner.user_id.login,partner.email])
                else : 
                    for crm in crm_obj.browse(cr,uid,crm_ids) : 
                        if crm.stage_id : 
                            cr.execute('''update res_partner set crm_lead_state=%s where id=%s ''',(crm.stage_id.name,partner.id))
                            print '------PARTNER   LEAD  STATUS  UPDATED-----------------'
        import ipdb;ipdb.set_trace()
        with open('/home/bista/Downloads/shanky/2016/feb/testrest.csv','wb') as csvfile:
        #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
            spamwriter = csv.writer(csvfile, delimiter=',')  
                     
            for write_rows in data:
                try :
                
                    spamwriter.writerow(write_rows)
                except Exception as E :
                    with open("/home/bista/Downloads/shanky/2016/feb/error_after_write.txt", "a") as donefile_new:
                        donefile_new.write(str(count)+'\n')                     
                        print '---------WRITE ERROR-----',count                        
                        
                                    
                

        return True


    def deactivate_login_account(self,cr,uid,vals):
        ''' deactivate login account'''
        
        dont_touch=[1,582,302,507,508]
        password='YourAccountDeactivated420'
        user_obj=self.pool.get('res.users')
        international_obj=self.pool.get('int.user')
        ind_obj=self.pool.get('ind.user')
        data=[]
        count=0
        
        for user in user_obj.browse(cr,uid,user_obj.search(cr,uid,[('id','not in',dont_touch)])) :
            count+=1
            print count 
            int_user=[x.name for x in international_obj.\
                      browse(cr,uid,international_obj.search(cr,uid,[('name','=',user.id)]) )  \
                             if x.password_reset==False]
              
            ind_user=[x.name for x in ind_obj.\
                      browse(cr,uid,ind_obj.search(cr,uid,[('name','=',user.id)] ))  if x.password_reset==False]
            
            
            for user_int in int_user : 
                user_obj.write(cr,uid,[user_int.id],{'password':password},{})
                print '{}  HAS BEEN DEACTIVATED   '.format(user_int.login)
                data.append([user_int.id,user_int.name,user_int.login,user_int.partner_type]) 
                 
            for user_ind in  ind_user : 
                user_obj.write(cr,uid,[user_ind.id],{'password':password},{})
                print '{}  HAS BEEN DEACTIVATED   '.format(user_ind.login) 
                data.append([user_ind.id,user_ind.name,user_ind.login,user_ind.partner_type])
        
        print data
        import ipdb;ipdb.set_trace()
        with open('/home/bista/Downloads/shanky/2016/feb/USER_ACCOUNT_DEACTIVATED.csv','wb') as csvfile:
        #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
            spamwriter = csv.writer(csvfile, delimiter=',')  
                     
            for write_rows in data:
                try :
                
                    spamwriter.writerow(write_rows)
                except Exception as E :
		    import ipdb;ipdb.set_trace()
                    with open("/home/bista/Downloads/shanky/2016/feb/error_after_write.txt", "a") as donefile_new:
                        donefile_new.write(str(count)+'\n')                     
                        print '---------WRITE ERROR-----',count                        
                        
                
                
        return True

    def update_account_period_name_use_company_convention(self,cr,uid,vals): 
        '''update period name wid company convention '''
        acc_period=self.pool.get('account.period')
        
        total= len(acc_period.browse(cr,uid,acc_period.search(cr,uid,[("date_start",">=",'2016-04-01')])))
        print "total period",total
        import ipdb;ipdb.set_trace()
        for period in  acc_period.browse(cr,uid,acc_period.search(cr,uid,[("date_start",">=",'2016-04-01')])) : 
            if period.name:
                conv_name=period.company_id.name_convention
                if conv_name : 
                    final_name=period.name +' ' +conv_name
                    acc_period.write(cr,uid,[period.id],{'name':final_name})
                    print '----period updatd----'
                    
        print '--over-----'
        return True


    def bm_swapping(self,cr,uid,ids) :
         
        '''Migrate BM and its other documents '''
        context={}
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead') 
        sale_obj=self.pool.get('sale.order')
        inv_obj=self.pool.get('account.invoice')
        voucher_obj=self.pool.get('account.voucher')
        swap_history_obj=self.pool.get('partner.swap.history')
        ids=partner_obj.search(cr,uid,[('state','=','confirm'),('is_company','=',True)])
        count=0;print 'len',len(ids)
        import ipdb;ipdb.set_trace()
        try :
             
            for partner in partner_obj.browse(cr,uid,ids) : 
                count+=1;print count
                if not partner.user_id:
                    continue
                
                bm_id=partner.user_id.id
                if partner.state !='confirm' : 
                    continue
             
                if partner.is_company ==False : 
                    continue
               
                
                crm_id=crm_obj.search(cr,SUPERUSERID,[('partner_id','=',partner.id)])
            #                 cr.execute('''select id from crm_lead where partner_id=%s ''',(partner.id,))
            #                 crm_id=map(lambda x:x[0],cr.fetchall())
                if crm_id : 
                    #print '*********import ipdb;ipdb.set_trace()*********TOTAL CRM *************',len(crm_id)
                       
                          
                    for crm in crm_obj.browse(cr,SUPERUSERID,crm_id) : 
                        if not crm.user_id or crm.user_id.id !=bm_id : 
                              
                            user_id_onchange=crm_obj.on_change_user(cr,bm_id,[crm],bm_id)
                             
                            if user_id_onchange.get('value').get('employee_id') :
                                #
                                crm_obj.write(cr,SUPERUSERID,[crm.id],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                            ,'user_id':bm_id})
                                  
                                print '*****************CRM UPDATED******************'
                            else : 
                                return 'Employee Not Found.\nContact HR xDepartment TO Create Employee For Odoo User'
                                        
             
             
                   
                ######assigne to Sale order#import ipdb;ipdb.set_trace()#########
                sale_id=sale_obj.search(cr,SUPERUSERID,[('partner_id','=',partner.id)])
                #import ipdb;ipdb.set_trace()
            #                 cr.execute('''select id from sale_order where partner_id=%s ''',(partner.id,))
            #                 sale_id=map(lambda x:x[0],cr.fetchall())                
                if sale_id : 
                    for sale in sale_obj.browse(cr,SUPERUSERID,sale_id)  :
                        if not sale.user_id or sale.user_id.id !=bm_id :
                             
                            user_id_onchange=sale_obj.sale_onchange_user(cr, bm_id, [sale_id], bm_id)
                            if user_id_onchange.get('value').get('employee_id') :
                                #import ipdb;ipdb.set_trace() 
                                sale_obj.write(cr,SUPERUSERID,[sale.id],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                                 ,'user_id':bm_id})
                  
                                print '*****************SALE UPDATED******************'
                           
             
                #############assign to invoices##########
                #import ipdb;ipdb.set_trace()
                for invoice in inv_obj.browse(cr,SUPERUSERID,inv_obj.search(cr,SUPERUSERID,[('partner_id','=',partner.id)])) : 
                    if not invoice.user_id or invoice.user_id.id !=bm_id :
                             
                        inv_obj.write(cr,SUPERUSERID,[invoice.id],{'user_id':bm_id})
                        print '*****************INVOICE UPDATED******************'
                                 
                 
                #############assign to payments invoices##########        
                for voucher in voucher_obj.browse(cr,SUPERUSERID,voucher_obj.search(cr,SUPERUSERID,[('partner_id','=',partner.id)])) : 
                    if not voucher.user_id or voucher.user_id.id !=bm_id :
                        #import ipdb;ipdb.set_trace()    
                         
                        voucher_obj.write(cr,SUPERUSERID,[voucher.id],{'user_id':bm_id})
                        print '*****************PAYMENT  UPDATED******************'
                        
                         
                 
                #import ipdb;ipdb.set_trace()
#                 context.update({'from_bm_id':old_bm_id,'to_bm_id':bm_id,\
#                                                                      'partner':partner})
#                 ##send email to notify BM for swap
#                 self.send_swap_mail_to_bm(cr,uid,ids,context)
#                 
#                 ###maintain history of swap
#                 swap_history_obj.create(cr,SUPERUSERID,{'from_bm_id':old_bm_id,'to_bm_id':bm_id,'partner_id':partner.id})
#                                 
        except Exception as E :
            import ipdb;ipdb.set_trace()
            raise osv.except_osv(_('Error'),
                                        _('{}').format(E))
 
         
        print '------------UPDATE SUCCCESSFULLLY--------'
        return True


    def create_users_for_swap1(self,cr,uid,vals): 
        '''create users for swap '''
        int_obj = self.pool.get('int.user')
        ind_obj= self.pool.get('ind.user')
        user_obj= self.pool.get('res.users')
        ind_users=user_obj.search(cr,uid,[('partner_type','=','india')])
        int_users=user_obj.search(cr,uid,[('partner_type','=','international')])
        import ipdb;ipdb.set_trace()
        for ind in user_obj.browse(cr,uid,ind_users) : 
            ind_obj.create(cr,uid,{'username':ind.name,'name':ind.id,'active':ind.active})
            print '-------INDIA USER CRAETED-------'
            
        for int in user_obj.browse(cr,uid,int_users) : 
            int_obj.create(cr,uid,{'username':int.name,'name':int.id,'active':int.active})
            print '-------INTERNATIONAL USER CRAETED-------'
            
            
        print '-----OVER'
        
        
        return True
    def assign_responsible_user_to_invoices(self,cr,uid,vals):
        '''Remove CEO desk and assign acccount user to invoices '''
         
        invoice_obj=self.pool.get('account.invoice')
        invoice_ids=invoice_obj.search(cr,uid,[('state','not in',['draft','cancel'])])
        count=0
        no_bm=[]
        no_move=[]
        print 'Total invoices',len(invoice_ids)
        
        for invoice in invoice_obj.browse(cr,uid,invoice_ids) : 
            
            if invoice.state not in ('draft','cancel')   :
                count+=1;print count
                if invoice.move_id: 
                    cr.execute('''select write_uid from account_move where id=%s ''',(invoice.move_id.id,))
                    account_user=map(lambda x:x[0],cr.fetchall())
                    if account_user : 
                        invoice_obj.write(cr,uid,[invoice.id],{'responsible':account_user[0]})
                        print '------invoice updated------'
                        
                    else:
                        print '-------NO salesuser found------'
                        no_bm.append(invoice.id)

                else : 
                    print '-------NO Move  found------'
                    no_move.append(invoice.id)
        import ipdb;ipdb.set_trace()
        if no_bm:
            with open("/home/bista/Downloads/account_logs/responsible_user_no_move.txt", "a") as donefile_new:
                donefile_new.write(str(invoice.id)+'\n')   
        if no_move : 
            
            with open("/home/bista/Downloads/account_logs/responsible_user_no_BM.txt", "a") as donefile_new:
                donefile_new.write(str(invoice.id))                             
        print '---over--'
        return True
    def remove_spaces_from_email(self,cr,uid,vals):
        ''' remove white spaces from partner email'''
        partner_obj=self.pool.get('res.partner')
        try : 
            
            ids=partner_obj.search(cr,uid,[('is_company','=',True)])
            print 'len',len(ids)
            import ipdb;ipdb.set_trace()
            count=0
            for partner in partner_obj.browse(cr,uid,ids):
                count+=1;print count
                if not partner.email : 
                    continue
                #email=partner.email.lstrip(' ').rstrip(' ')

                email=partner.email.replace(" ","")
                cr.execute('''update res_partner set email=%s where id=%s''',(email,partner.id))
                print '------email updated'
            
        except Exception as E:
            import ipdb;ipdb.set_trace()
            print E
        print '----over-------'
        return True

    def assign_manager_to_employee(self,cr,uid,vals): 
        '''assign manager to employee so that manager can see records of its suborindaies '''
        employee_obj = self.pool.get('hr.employee')
        user_obj= self.pool.get('res.users')
        try:
            user_ids=user_obj.search(cr,uid,[('partner_type','=','international')])
            
            print '---total retail users---',len(user_ids)
            import ipdb;ipdb.set_trace()
            for user in user_obj.browse(cr,uid,user_ids) : 
                employee_id=employee_obj.search(cr,uid,[('user_id','=',user.id)])
                if not employee_id :

                    with open("/home/bista/Downloads/sandhya/logs/assign_manager_to_emp/no_employee.txt", "a") as donefile_new:
                        donefile_new.write(str(user.id))
 
                
                else : 
                    
                    sandhya_uid=350
                    if len(employee_id)>1 : 
                        with open("/home/bista/Downloads/sandhya/logs/assign_manager_to_emp/multi_employee.txt", "a") as donefile_new:
                            donefile_new.write(str(user.id))
                    lester=178
                    employee_obj.write(cr,sandhya_uid,employee_id,{'parent_id':lester})
                    print '-------LESTER AS MANAGER ASSIGNED TO EMPLOYEE'
                    
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E
                                
                
        print '-----OVER-----'
        return True

    def create_users_for_swap(self,cr,uid,vals): 
        '''create users for swap '''
        int_obj = self.pool.get('int.user')
        ind_obj= self.pool.get('ind.user')
        user_obj= self.pool.get('res.users')
        ind_users=user_obj.search(cr,uid,[('partner_type','=','india')])
        int_users=user_obj.search(cr,uid,[('partner_type','=','international')])
        import ipdb;ipdb.set_trace()
        for ind in user_obj.browse(cr,uid,ind_users) : 
            ind_obj.create(cr,uid,{'username':ind.name,'name':ind.id,'active':ind.active})
            print '-------INDIA USER CRAETED-------'
            
        for int in user_obj.browse(cr,uid,int_users) : 
            int_obj.create(cr,uid,{'username':int.name,'name':int.id,'active':int.active})
            print '-------INTERNATIONAL USER CRAETED-------'
            
            
        print '-----OVER'
        
        
        return True

    
    def create_user_setting_for_count(self,cr,uid,assign_users_for_count): 
        user_settings_obj=self.pool.get('user.settings')
        import time;start_time = time.time()
        user_obj=self.pool.get('res.users')
        try : 
            import ipdb;ipdb.set_trace()
            user_val= (   user for user in user_obj.browse(cr,uid,user_obj.search(cr,uid,[]))    )
            print user_val
            import ipdb;ipdb.set_trace()
            for user in user_val : 
                user_settings_obj.create(cr,uid,{'name':user.name,'user_id':user.id,'active':True,\
                'rule':[(6, 0, [1])],'count_flag':True,'count':5,'readonly_flag':False})
                print 'USer comnfiguration created'
        except Exception  as E : 
            import ipdb;ipdb.set_trace()
            print E 
        #import ipdb;ipdb.set_trace()
        print time.time() - start_time   
        print '-------OVER-----------'
        return True

    def update_line_count_for_report(self,cr,uid,vals):
       
        inv_obj=self.pool.get('account.invoice')
        inv_ids =inv_obj.search(cr,uid,[])
        count=0
        import ipdb;ipdb.set_trace()
        for inv_id in inv_ids :
            name='total_invoice_line'
            count+=1;print count
            count_len=inv_obj._count_total_invoice_line(cr, uid, [inv_id], name, None, {})
	    cr.execute(''' update account_invoice set total_invoice_line=%s where id=%s''',(count_len.values()[0],inv_id))
#            inv_obj.write(cr,uid,inv_id,{'total_invoice_line':count_len})
        print '----over---'
        return True 



    def migrate_salesperson_Lester(self,cr,uid,vals) :
        ''' Migrate BM'''
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        sale_obj=self.pool.get('sale.order')
        inv_obj=self.pool.get('account.invoice')
        vals={}
        count=0
        bm_id=365
        data=[]
        #import ipdb;ipdb.set_trace()
        try: 
            

            #import ipdb;ipdb.set_trace()
            partner_id=partner_obj.search(cr,uid,[('partner_sequence','=','R404184')])
            if partner_id : 
                ###assigned BM to partner
                #partner=partner_obj.browse(cr,uid,partner_id[0])
                #data.append([partner.name,partner.email,partner.partner_sequence,partner.user_id.name])
                partner_obj.write(cr,uid,partner_id,{'user_id':bm_id})
                 
                ###assigned to CRM#####
                crm_id=crm_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                if crm_id : 
                    print '******************TOTAL CRM *************',len(crm_id)
                     
                         
                    for crm in crm_id : 
                        user_id_onchange=crm_obj.on_change_user(cr,uid,[crm],bm_id)
                        if user_id_onchange.get('value').get('employee_id') : 
                            crm_obj.write(cr,uid,[crm],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                        ,'user_id':bm_id})
                             
                            print '*****************CRM UPDATED******************'
                             
                 
                ######assigne to Sale order##########
                sale_id=sale_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                if sale_id : 
                    for sale in sale_id  :
                        user_id_onchange=sale_obj.sale_onchange_user(cr, uid, [sale_id], bm_id)
                        if user_id_onchange.get('value').get('employee_id') : 
                            sale_obj.write(cr,uid,[sale],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                             ,'user_id':bm_id})
            
                            print '*****************SALE UPDATED******************'
                         
                         
                #############assign invoices##########
                inv_id=inv_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                if inv_id : 
                    for inv in inv_id :
                            inv_obj.write(cr,uid,[inv],{'user_id':bm_id})
                            print '*****************INVOICE UPDATED******************'
                            
            else:
                print '*****************N O !!! P A R T N E R FOUND!!!!!******************'
                           
                        
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E

                        
             
        print '-------------O V E R------------'                                                
        return True


    def update_country_on_invoices(self,cr,uid,vals):
        '''update country on invoices '''
        inv_obj=self.pool.get('account.invoice')
        inv_ids =inv_obj.search(cr,uid,[])
        count=0
        import ipdb;ipdb.set_trace()
        for inv_id in inv_obj.browse(cr,uid,inv_ids) :

            count+=1;print count
            if inv_id.partner_id.country_id : 
                cr.execute('''update account_invoice set partner_country =%s where id=%s''',(inv_id.partner_id.country_id.name,\
                                                                                             inv_id.id))
                print '-------INVOICE UPDATED--------'
                
            else : 
                print '----------NO COUNTRY FOUND----------'
                
            #    inv_obj.write(cr,uid,[inv_id.id],{'partner_country':inv_id.partner_id.country_id.name})
            
        print '----over---'
        return True 



    def add_qms_country(self,cr,uid,vals): 
        
        country_obj=self.pool.get('res.country')
        
        count=0
#        from numpy import loadtxt
        data=[]
        
        #lines = loadtxt("/home/bista/Downloads/jignesh/country_list.txt'", comments="#", delimiter=">", unpack=False)
        import ipdb;ipdb.set_trace()
        with open('/home/bista/Downloads/jignesh/cou.txt','r') as text_file:
            #import ipdb;ipdb.set_trace()
            linelist = text_file.readlines()
            for i in linelist : 
                country=i.split('>')[1].split('<')[0]
                cr.execute('''select id from res_country where name like %s ''',('%'+country+'%',))
                odoo_co_name=map(lambda x:x[0],cr.fetchall()) 
                if odoo_co_name : 
                    pass
                else : 
                    data.append([country])
                    country_obj.create(cr,uid,{'name':country})
                    print 'NOT foudn'


#         with open('/home/bista/Downloads/jignesh/data_not_found.csv','wb') as csvfile: 
#         #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
#             spamwriter = csv.writer(csvfile, delimiter=',')  
#             #import ipdb;ipdb.set_trace()     
#             for write_rows in data:
#                 spamwriter.writerow(write_rows)                      
#                     
#                 
#             
#         
       
        print '----------------over-------------------'
        return True




    def resolve_tax_jv_issue(self,cr,uid,vals): 
        
        jv_obj=self.pool.get('account.move.line')
        
        count=0
        
######################ROUTESMS SOLUTIONS LIMITED########      
       #### #############sales  tax########################  
        ####get JV line ids of tax amount

###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##########################         
          
#         cr.execute('''select id from account_move_line where account_id=4220 and journal_id in (34)''')
#         output_tax__jv_line_ids=map(lambda x:x[0],cr.fetchall())
#         print 'TOTAL OUTPUT TAX JV',len(output_tax__jv_line_ids)
#         import ipdb;ipdb.set_trace()
#         for jv_line in jv_obj.browse(cr,uid,output_tax__jv_line_ids) : 
#             ###updating tax applied line##
#              
#                
#             cr.execute('''update account_move_line set tax_code_id=1827,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#             print '-----------tax code and amount updated for tax line------'
#              
#                
#             cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#             jv_line_ids=map(lambda x:x[0],cr.fetchall())
#             ##get jv line ids of product
#             cr.execute('''select id from account_move_line where account_id=1269 and journal_id in (34) and id in %s''',(tuple(jv_line_ids),))
#             product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                
#    
#    
#                
#             for jv_line in jv_obj.browse(cr,uid,product__jv_line_ids) :     
#                 count+=1;print count      
#                 ##updating product line##
#                 cr.execute('''update account_move_line set tax_code_id=1826,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'    
# #             ###sale tax  ends####
# # 
# # #         #### #############sale refund  tax########################  
# # #         ####get JV line ids of tax amount
# # #         
#         print '---sale refund tax---'
#         cr.execute('''select id from account_move_line where account_id=4220 and journal_id in (36)''')
#         output_tax__jv_line_ids=map(lambda x:x[0],cr.fetchall())
#         print 'TOTAL OUTPUT TAX JV',len(output_tax__jv_line_ids)
#         import ipdb;ipdb.set_trace()
#         for jv_line in jv_obj.browse(cr,uid,output_tax__jv_line_ids) : 
#             ###updating tax applied line##
#   
#             cr.execute('''update account_move_line set tax_code_id=1827,tax_amount=%s where id=%s''',(-(jv_line.debit),jv_line.id))
#             print '-----------tax code and amount updated for tax line------'
#                
#             cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#             jv_line_ids=map(lambda x:x[0],cr.fetchall())
#             ##get jv line ids of product
#             cr.execute('''select id from account_move_line where account_id=1269 and journal_id in (36) and id in %s''',(tuple(jv_line_ids),))
#             product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#              
#    
#                
#             for jv_line in jv_obj.browse(cr,uid,product__jv_line_ids) :     
#                 count+=1;print count      
#                 ##updating product line##
#                 cr.execute('''update account_move_line set tax_code_id=1826,tax_amount=%s where id=%s''',(-(jv_line.debit),jv_line.id))
#                 print '-----------tax code and amount updated for product line------'  
# # # # 
# # # #             
# # # #             ####sale refund  tax ends#####
# #             
# #             
# # #         #### #############purchase  tax########################  
# # #         ####get JV line ids of tax amount
# # #         
#         print '---purchase tax---'
#         cr.execute('''select id from account_move_line where account_id=4221 and journal_id in (35)''')
#         output_tax__jv_line_ids=map(lambda x:x[0],cr.fetchall())
#         print 'TOTAL OUTPUT TAX JV',len(output_tax__jv_line_ids)
#         import ipdb;ipdb.set_trace()
#         for jv_line in jv_obj.browse(cr,uEXJid,output_tax__jv_line_ids) : 
#             ###updating tax applied line##
#    
#             cr.execute('''update account_move_line set tax_code_id=1829,tax_amount=%s where id=%s''',(-(jv_line.debit),jv_line.id))
#             print '-----------tax code and amount updated for tax line------'
#                
#             cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#             jv_line_ids=map(lambda x:x[0],cr.fetchall())
#             ##get jv line ids of product
#             cr.execute('''select id from account_move_line where account_id=1279 and journal_id in (35) and id in %s''',(tuple(jv_line_ids),))
#             product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                
#    
#    
#                
#             for jv_line in jv_obj.browse(cr,uid,product__jv_line_ids) :     
#                 count+=1;print count      
#                 ##updating product line##
#                 cr.execute('''update account_move_line set tax_code_id=1828,tax_amount=%s where id=%s''',(-(jv_line.debit),jv_line.id))
#                 print '-----------tax code and amount updated for product line------'              
# # # 
# # #             #############purchase  tax  ends #########
# # 
# # #         #### #############purchase refund tax########################  
# # #         ####get JV line ids of tax amount
# # #          
#         print '---purchase  refund tax---'
#         cr.execute('''select id from account_move_line where account_id=4221 and journal_id in (37)''')
#         output_tax__jv_line_ids=map(lambda x:x[0],cr.fetchall())
#         print 'TOTAL input TAX JV',len(output_tax__jv_line_ids)
#         import ipdb;ipdb.set_trace()
#         for jv_line in jv_obj.browse(cr,uid,output_tax__jv_line_ids) : 
#             ###updating tax applied line##
#    
#             cr.execute('''update account_move_line set tax_code_id=1829,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#             print '-----------tax code and amount updated for tax line------'
#                
#             cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#             jv_line_ids=map(lambda x:x[0],cr.fetchall())
#             ##get jv line ids of product
#             cr.execute('''select id from account_move_line where account_id=1279 and journal_id in (37) and id in %s''',(tuple(jv_line_ids),))
#             product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                
#    
#    
#                
#             for jv_line in jv_obj.browse(cr,uid,product__jv_line_ids) :     
#                 count+=1;print count      
#                 ##updating product line##
#                 cr.execute('''update account_move_line set tax_code_id=1828,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'              

###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##########################
# #  
# #             #############purchase  refund tax  ends #########
# 
# 
#                         
#         
#         ######################ROUTESMS SOLUTIONS LIMITED  ENDS ##########  
#         
#         
######@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#####        
        
# ######################ROUTESMS SOLUTIONS NIGERIA LIMITED########      
#        #### #############sales  tax########################
#        ####fetch JV records frm file
# ###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##########################       
#         jv_obj=self.pool.get('account.move')
#         jv_line_obj=self.pool.get('account.move.line')
#         print '---------------ROUTESMS SOLUTIONS NIGERIA LIMITED-----------------'
#         with open('/home/bista/Downloads/rakesh/issues/JV/NOV/17NOV/NGN/Input VAT Tax 5% NGN_JV_list.csv','r') as e: 
#         #with open('/home/bista/Downloads/rakesh/issues/JV/NOV/17NOV/NGN/Output VAT Tax 5% NGN_JV_list.csv','r') as e:
#             ng_data_sale=[]
#             ng_data_purchase=[]
#             reader = csv.reader(e)
#             import ipdb;ipdb.set_trace()
#             for row in reader:
#                 count+=1;print count 
#                 jv=jv_obj.browse(cr,uid,int(row[0]))
#                 for line in jv.line_id : 
#                     ###check sale tax###
#                     if line.name=='Output VAT Tax 5% NGN' or line.name=='VAT Tax 5%_Routesms Nigeria Limited' : 
#                         ##if sale invoice
#                         if line.journal_id.id==82 : 
#                             #import ipdb;ipdb.set_trace()
#                                   
#                             cr.execute('''update account_move_line set account_id=%s,tax_code_id=%s,tax_amount=%s where id=%s ''',\
#                                        (2751,918,line.credit,line.id))
#                             print '-----sale tax line updated------' 
#                             cr.commit()
#   
#                             ##get jv line ids of product
#                             cr.execute('''select id from account_move_line where move_id=%s ''',(line.move_id.id,))
#                             jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                               
#                             cr.execute('''select id from account_move_line where account_id=2889 and journal_id in (82) and id in %s''',(tuple(jv_line_ids),))
#                             product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                                 
#                     
#                   
#                             for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                                 count+=1;print count      
#                                 ##updating product line##
#                                 cr.execute('''update account_move_line set tax_code_id=967,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                                 print '-----------tax code and amount updated for product line------'                             
#                                 cr.commit()
# #                         
# #                         ##if sale refund invoice
#                         elif line.journal_id.id==84 : 
#                             #import ipdb;ipdb.set_trace()
#                             cr.execute('''update account_move_line set account_id=%s,tax_code_id=%s,tax_amount=%s where id=%s ''',\
#                                        (2751,918,-(line.debit),line.id))
#                             cr.commit()
#                             print '-----sale @@@@@refund@@@@@@@@@tax line updated------' 
#   
#                             ##get jv line ids of product
#                             cr.execute('''select id from account_move_line where move_id=%s ''',(line.move_id.id,))
#                             jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                               
#                             cr.execute('''select id from account_move_line where account_id=2889 and journal_id in (84) and id in %s''',(tuple(jv_line_ids),))
#                             product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                                 
#                     
#                   
#                             for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                                 count+=1;print count      
#                                 ##updating product line##
#                                 cr.execute('''update account_move_line set tax_code_id=967,tax_amount=%s where id=%s''',(-(jv_line.debit),jv_line.id))
#                                 print '-----------tax code and amount updated for product line------'  
#                                 cr.commit() 
#                               
#                               
#                         else :
#                               
#                             print '-----INVALID SALE RECORD-----------' 
#                             ng_data_sale.append([int(row[0])])
#                       
#                     ###check purchase tax###
#                     elif line.name=='Input VAT Tax 5% NGN' : 
#                         ##if purchase invoice
#                         if line.journal_id.id==83 : 
#                             #import ipdb;ipdb.set_trace()
#                                   
#                             cr.execute('''update account_move_line set account_id=%s,tax_code_id=%s,tax_amount=%s where id=%s ''',\
#                                        (2870,939,-(line.debit),line.id))
#                             print '-----purchase tax line updated------' 
#                             cr.commit()
#   
#                             ##get jv line ids of product
#                             cr.execute('''select id from account_move_line where move_id=%s ''',(line.move_id.id,))
#                             jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                               
#                             cr.execute('''select id from account_move_line where account_id=2899 and journal_id in (83) and id in %s''',(tuple(jv_line_ids),))
#                             product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                                 
#                     
#                   
#                             for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                                 count+=1;print count      
#                                 ##updating product line##
#                                 cr.execute('''update account_move_line set tax_code_id=982,tax_amount=%s where id=%s''',(-(jv_line.debit),jv_line.id))
#                                 print '-----------tax code and amount updated for product line------'     
#                                 cr.commit()                        
#   
#   
#                               
#                               
#                         ##if purchase refund invoice
#                         elif line.journal_id.id==85 : 
#                            # import ipdb;ipdb.set_trace()
#                             cr.execute('''update account_move_line set account_id=%s,tax_code_id=%s,tax_amount=%s where id=%s ''',\
#                                        (2870,939,line.credit,line.id))
#                             print '-----purchase tax line updated------' 
#                             cr.commit()
#   
#                             ##get jv line ids of product
#                             cr.execute('''select id from account_move_line where move_id=%s ''',(line.move_id.id,))
#                             jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                               
#                             cr.execute('''select id from account_move_line where account_id=2899 and journal_id in (85) and id in %s''',(tuple(jv_line_ids),))
#                             product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                                 
#                     
#                   
#                             for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                                 count+=1;print count      
#                                 ##updating product line##
#                                 cr.execute('''update account_move_line set tax_code_id=982,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                                 print '-----------tax code and amount updated for product line------'  
#                                 cr.commit()
#                               
#                               
#                         else :
#                               
#                             print '-----INVALID PURCHASE RECORD-----------' 
#                             ng_data_purchase.append([int(row[0])])                        
# #                       
# #        #####make errror file for sale record                        
#         with open('/home/bista/Downloads/rakesh/issues/JV/NOV/17NOV/NGN/error/sale_error_records.csv ','wb') as csvfile:
#         #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
#             spamwriter = csv.writer(csvfile, delimiter=',')  
#             #import ipdb;ipdb.set_trace()     
#             for write_rows in ng_data_sale:
#                 spamwriter.writerow(write_rows)            
# #  
# # #####make errror file for purchase record                     
#         with open('/home/bista/Downloads/rakesh/issues/JV/NOV/17NOV/NGN/error/purchase_error_records.csv ','wb') as csvfile:
#         #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
#             spamwriter = csv.writer(csvfile, delimiter=',')  
#             #import ipdb;ipdb.set_trace()     
#             for write_rows in ng_data_purchase:
#                 spamwriter.writerow(write_rows)                             
                                           
  
# 
#         
# #         ######################ROUTESMS SOLUTIONS NIGERIA LIMITED  ENDS ##########  

###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##########################

######################SPHERE EDGE CONSULTING INDIA PVT. LTD########      
       #### #############sales  tax########################  
        ####get JV line ids of tax amount
           
#           
#         cr.execute('''select id from account_move_line where account_id=4223 and journal_id in (58)''')
#         output_tax__jv_line_ids=map(lambda x:x[0],cr.fetchall())
#         print 'TOTAL OUTPUT TAX JV',len(output_tax__jv_line_ids)
#         import ipdb;ipdb.set_trace()
#         for jv_line in jv_line_obj.browse(cr,uid,output_tax__jv_line_ids) : 
#             ###updating tax applied line##
#              
#                
#             cr.execute('''update account_move_line set tax_code_id=1832,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#             print '-----------tax code and amount updated for tax line------'
#              
#                
#             cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#             jv_line_ids=map(lambda x:x[0],cr.fetchall())
#             ##get jv line ids of product
#             cr.execute('''select id from account_move_line where account_id=2079 and journal_id in (58) and id in %s''',(tuple(jv_line_ids),))
#             product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                
#    
#    
#                
#             for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                 count+=1;print count      
#                 ##updating product line##
#                 cr.execute('''update account_move_line set tax_code_id=1834,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'    
# #             ###sale tax  ends####
# # 
# # #         #### #############sale refund  tax########################  
# # #         ####get JV line ids of tax amount
# # #         
#         print '---sale refund tax---'
#         cr.execute('''select id from account_move_line where account_id=4223 and journal_id in (60)''')
#         output_tax__jv_line_ids=map(lambda x:x[0],cr.fetchall())
#         print 'TOTAL OUTPUT TAX JV',len(output_tax__jv_line_ids)
#         import ipdb;ipdb.set_trace()
#         for jv_line in jv_line_obj.browse(cr,uid,output_tax__jv_line_ids) : 
#             ###updating tax applied line##
#   
#             cr.execute('''update account_move_line set tax_code_id=1832,tax_amount=%s where id=%s''',(-(jv_line.debit),jv_line.id))
#             print '-----------tax code and amount updated for tax line------'
#                
#             cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#             jv_line_ids=map(lambda x:x[0],cr.fetchall())
#             ##get jv line ids of product
#             cr.execute('''select id from account_move_line where account_id=2079 and journal_id in (60) and id in %s''',(tuple(jv_line_ids),))
#             product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#              
#    
#                
#             for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                 count+=1;print count      
#                 ##updating product line##
#                 cr.execute('''update account_move_line set tax_code_id=1834,tax_amount=%s where id=%s''',(-(jv_line.debit),jv_line.id))
#                 print '-----------tax code and amount updated for product line------'  
# # # # 
# # # #             
# # # #             ####sale refund  tax ends#####
# #             
# #             
# # #         #### #############purchase  tax########################  
# # #         ####get JV line ids of tax amount
# # #         
#         print '---purchase tax---'
#         cr.execute('''select id from account_move_line where account_id=4222 and journal_id in (59)''')
#         output_tax__jv_line_ids=map(lambda x:x[0],cr.fetchall())
#         print 'TOTAL OUTPUT TAX JV',len(output_tax__jv_line_ids)
#         import ipdb;ipdb.set_trace()
#         for jv_line in jv_line_obj.browse(cr,uid,output_tax__jv_line_ids) : 
#             ###updating tax applied line##
#    
#             cr.execute('''update account_move_line set tax_code_id=1836,tax_amount=%s where id=%s''',(-(jv_line.debit),jv_line.id))
#             print '-----------tax code and amount updated for tax line------'
#                
#             cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#             jv_line_ids=map(lambda x:x[0],cr.fetchall())
#             ##get jv line ids of product
#             cr.execute('''select id from account_move_line where account_id=2089 and journal_id in (59) and id in %s''',(tuple(jv_line_ids),))
#             product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                
#    
#    
#                
#             for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                 count+=1;print count      
#                 ##updating product line##
#                 cr.execute('''update account_move_line set tax_code_id=1835,tax_amount=%s where id=%s''',(-(jv_line.debit),jv_line.id))
#                 print '-----------tax code and amount updated for product line------'    
# 
#             ##get jv line ids of product2
#             cr.execute('''select id from account_move_line where account_id=4144 and journal_id in (59) and id in %s''',(tuple(jv_line_ids),))
#             product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                
#    
#    
#                
#             for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                 count+=1;print count      
#                 ##updating product line##
#                 cr.execute('''update account_move_line set tax_code_id=1835,tax_amount=%s where id=%s''',(-(jv_line.debit),jv_line.id))
#                 print '-----------tax code and amount updated for product line------'                 
# 
# 
# 
#                           
# # # 
# #
# # #             #############purchase  tax  ends #########
# # 
# # #         #### #############purchase refund tax########################  
# # #         ####get JV line ids of tax amount
# # #          
#         print '---purchase  refund tax---'
#         cr.execute('''select id from account_move_line where account_id=4222 and journal_id in (61)''')
#         output_tax__jv_line_ids=map(lambda x:x[0],cr.fetchall())
#         print 'TOTAL input TAX JV',len(output_tax__jv_line_ids)
#         import ipdb;ipdb.set_trace()
#         for jv_line in jv_line_obj.browse(cr,uid,output_tax__jv_line_ids) : 
#             ###updating tax applied line##
#    
#             cr.execute('''update account_move_line set tax_code_id=1836,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#             print '-----------tax code and amount updated for tax line------'
#                
#             cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#             jv_line_ids=map(lambda x:x[0],cr.fetchall())
#             ##get jv line ids of product
#             cr.execute('''select id from account_move_line where account_id=2089 and journal_id in (61) and id in %s''',(tuple(jv_line_ids),))
#             product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                
#    
#    
#                
#             for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                 count+=1;print count      
#                 ##updating product line##
#                 cr.execute('''update account_move_line set tax_code_id=1835,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
# 
#             ##get jv line ids of product2
#             cr.execute('''select id from account_move_line where account_id=4144 and journal_id in (59) and id in %s''',(tuple(jv_line_ids),))
#             product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                
#    
#    
#                
#             for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                 count+=1;print count      
#                 ##updating product line##
#                 cr.execute('''update account_move_line set tax_code_id=1835,tax_amount=%s where id=%s''',(-(jv_line.debit),jv_line.id))
#                 print '-----------tax code and amount updated for product line------'  
# 
#                               
# #  
# #             #############purchase  refund tax  ends #########
# 
# 
#                         
#         
#         ######################SPHERE EDGE CONSULTING INDIA PVT. LTD  ENDS ##########  
        
###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@########################## 


# ######################ROUTESMS SOLUTIONS (UK) LIMITED########      
#        #### #############sales  tax########################
#        ####fetch JV records frm file
# ###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##########################       
        jv_obj=self.pool.get('account.move')
        jv_line_obj=self.pool.get('account.move.line')
        print '---------------ROUTESMS SOLUTIONS (UK) LIMITED-----------------'
        with open('/home/bista/Downloads/rakesh/issues/JV/DEC/22dec/VAT Tax 20%_RSLUK_JV_list.csv','r') as e: 
        #with open('/home/bista/Downloads/rakesh/issues/JV/NOV/17NOV/NGN/Output VAT Tax 5% NGN_JV_list.csv','r') as e:
            ng_data_sale=[]
            ng_data_purchase=[]
            reader = csv.reader(e)
             
            for row in reader:
                count+=1;print count 
                jv=jv_obj.browse(cr,uid,int(row[0]))
                for line in jv.line_id : 
                    ###check sale tax###
                    if line.name=='VAT Tax 20%' : 
                        ##if sale invoice
                        if line.journal_id.id in [98,210,211] : 
                            #import ipdb;ipdb.set_trace()
                                  
                            cr.execute('''update account_move_line set account_id=%s,tax_code_id=%s,tax_amount=%s where id=%s ''',\
                                       (3291,1840,line.credit,line.id))
                            print '-----sale tax line updated------' 
                            cr.commit()
  
                            ##get jv line ids of product
                            cr.execute('''select id from account_move_line where move_id=%s ''',(line.move_id.id,))
                            jv_line_ids=map(lambda x:x[0],cr.fetchall())
                              
                            cr.execute('''select id from account_move_line where account_id=3429 and journal_id in (98,210,211) and id in %s''',(tuple(jv_line_ids),))
                            product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
                                
                    
                  
                            for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
                                count+=1;print count      
                                ##updating product line##
                                cr.execute('''update account_move_line set tax_code_id=1838,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
                                print '-----------tax code and amount updated for product line------'                             
                                cr.commit()
#                         
#                         ##if sale refund invoice
                        elif line.journal_id.id==100 : 
                            #import ipdb;ipdb.set_trace()
                            cr.execute('''update account_move_line set account_id=%s,tax_code_id=%s,tax_amount=%s where id=%s ''',\
                                       (3291,1840,-(line.debit),line.id))
                            cr.commit()
                            print '-----sale @@@@@refund@@@@@@@@@tax line updated------' 
  
                            ##get jv line ids of product
                            cr.execute('''select id from account_move_line where move_id=%s ''',(line.move_id.id,))
                            jv_line_ids=map(lambda x:x[0],cr.fetchall())
                              
                            cr.execute('''select id from account_move_line where account_id=3429 and journal_id in (100) and id in %s''',(tuple(jv_line_ids),))
                            product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
                                
                    
                  
                            for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
                                count+=1;print count      
                                ##updating product line##
                                cr.execute('''update account_move_line set tax_code_id=1838,tax_amount=%s where id=%s''',(-(jv_line.debit),jv_line.id))
                                print '-----------tax code and amount updated for product line------'  
                                cr.commit() 
                              
                              
                        else :
                              
                            print '-----INVALID SALE RECORD-----------' 
                            ng_data_sale.append([int(row[0])])


                      
      ####make errror file for sale record                        
        with open('/home/bista/Downloads/rakesh/issues/JV/DEC/22dec/issues/sale_error_records_rsluk.csv ','wb') as csvfile:
        #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
            spamwriter = csv.writer(csvfile, delimiter=',')  
            #import ipdb;ipdb.set_trace()     
            for write_rows in ng_data_sale:
                spamwriter.writerow(write_rows)            
 
#         
#         ######################ROUTESMS SOLUTIONS (UK) LIMITED  ENDS ########## 


######################29 THREE HOLIDAYS PVT. LTD########      
       #### #############sales  tax########################
       ####fetch JV records frm file
###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##########################       
#         jv_obj=self.pool.get('account.move')
#         jv_line_obj=self.pool.get('account.move.line')
#         print '---------------29 THREE HOLIDAYS PVT. LTD----------------'
#         with open('/home/bista/Downloads/rakesh/issues/JV/NOV/24NOV/travel/final.csv','r') as e: 
#         #with open('/home/bista/Downloads/rakesh/issues/JV/NOV/17NOV/NGN/Output VAT Tax 5% NGN_JV_list.csv','r') as e:
#             ng_data_sale=[]
#             ng_data_purchase=[]
#             reader = csv.reader(e)
#             import ipdb;ipdb.set_trace()
#             for row in reader:
#                 count+=1;print count 
#                 jv=jv_obj.browse(cr,uid,int(row[0]))
#                 for line in jv.line_id : 
#                     ###check sale tax###
#                     if line.name in ['Service Tax Rate on Domestic Air Ticket 0.62%','Service Tax Rate on International Air Ticket 1.24%',\
#                         'Service Tax Rate on Tour & Package  Service 3.09%',\
#                         'Service Tax Rate on Domestic Air Ticket 0.7%',\
#                         'Service Tax Rate on International Air Ticket 1.4% ',\
#                         ] : 
#                         ##if sale invoice
#                         
#                         if line.name=='Service Tax Rate on Domestic Air Ticket 0.62%' : 
#                             
# 
#     #                         
#     #                         ##if sale refund invoice
#                             if line.journal_id.id==12 : 
#                                 #import ipdb;ipdb.set_trace()
#                                 if line.name=='Service Tax Rate on Domestic Air Ticket 0.62%' : 
#                                     if line.debit==0.0000 : 
#                                         tax_amount=line.debit
#                                     else : 
#                                         tax_amount=-(line.debit)
#                                         
#                                     cr.execute('''update account_move_line set account_id=%s,tax_code_id=%s,tax_amount=%s where id=%s ''',\
#                                                (317,1870,tax_amount,line.id))
#                                     cr.commit()
#                                     print '-----sale @@@@@refund@@@@@@@@@tax line updated------' 
#      
# #                                 ##get jv line ids of product
# #                                 cr.execute('''select id from account_move_line where move_id=%s ''',(line.move_id.id,))
# #                                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
# #                                  
# #                                 cr.execute('''select id from account_move_line where account_id=3429 and journal_id in (100) and id in %s''',(tuple(jv_line_ids),))
# #                                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
# #                                    
# #                        
# #                      
# #                                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
# #                                     count+=1;print count      
# #                                     ##updating product line##
# #                                     cr.execute('''update account_move_line set tax_code_id=1838,tax_amount=%s where id=%s''',(-(jv_line.debit),jv_line.id))
# #                                     print '-----------tax code and amount updated for product line------'  
# #                                     cr.commit() 
#                                  
#                                  
#                             else :
#                                  
#                                 print '-----INVALID SALE RECORD-----------' 
#                                 ng_data_sale.append([int(row[0])])
#                                 
#                                 
#                         elif line.name=='Service Tax Rate on International Air Ticket 1.24%' : 
# 
#                             if line.journal_id.id==12 : 
#                                 #import ipdb;ipdb.set_trace()
#                                 if line.name=='Service Tax Rate on International Air Ticket 1.24%' : 
#                                     if line.debit==0.0000 : 
#                                         tax_amount=line.debit
#                                     else : 
#                                         tax_amount=-(line.debit)
#                                         
#                                     cr.execute('''update account_move_line set account_id=%s,tax_code_id=%s,tax_amount=%s where id=%s ''',\
#                                                (4118,1858,tax_amount,line.id))
#                                     cr.commit()
#                                     print '-----sale @@@@@refund@@@@@@@@@tax line updated------'
# 
#                             else :
#                                  
#                                 print '-----INVALID SALE RECORD-----------' 
#                                 ng_data_sale.append([int(row[0])])                                        
# 
#                         elif line.name=='Service Tax Rate on Tour & Package  Service 3.09%' : 
# 
#                             if line.journal_id.id==12 : 
#                                 #import ipdb;ipdb.set_trace()
#                                 if line.name=='Service Tax Rate on Tour & Package  Service 3.09%' : 
#                                     if line.debit==0.0000 : 
#                                         tax_amount=line.debit
#                                     else : 
#                                         tax_amount=-(line.debit)
#                                         
#                                     cr.execute('''update account_move_line set account_id=%s,tax_code_id=%s,tax_amount=%s where id=%s ''',\
#                                                (318,1830,tax_amount,line.id))
#                                     cr.commit()
#                                     print '-----sale @@@@@refund@@@@@@@@@tax line updated------'    
#                                                                                                
#                             else :
#                                  
#                                 print '-----INVALID SALE RECORD-----------' 
#                                 ng_data_sale.append([int(row[0])])                                                                                               
#                             
# 
#                         elif line.name=='Service Tax Rate on Domestic Air Ticket 0.7%' : 
# 
#                             if line.journal_id.id==12 : 
#                                 #import ipdb;ipdb.set_trace()
#                                 if line.name=='Service Tax Rate on Domestic Air Ticket 0.7%' : 
#                                     if line.debit==0.0000 : 
#                                         tax_amount=line.debit
#                                     else : 
#                                         tax_amount=-(line.debit)
#                                         
#                                     cr.execute('''update account_move_line set account_id=%s,tax_code_id=%s,tax_amount=%s where id=%s ''',\
#                                                (4229,1838,tax_amount,line.id))
#                                     cr.commit()
#                                     print '-----sale @@@@@refund@@@@@@@@@tax line updated------'     
# 
#                             else :
#                                  
#                                 print '-----INVALID SALE RECORD-----------' 
#                                 ng_data_sale.append([int(row[0])])                                    
# 
#                         elif line.name=='Service Tax Rate on International Air Ticket 1.4% ' : 
# 
#                             if line.journal_id.id==12 : 
#                                 #import ipdb;ipdb.set_trace()
#                                 if line.name=='Service Tax Rate on International Air Ticket 1.4% ' : 
#                                     if line.debit==0.0000 : 
#                                         tax_amount=line.debit
#                                     else : 
#                                         tax_amount=-(line.debit)
#                                         
#                                     cr.execute('''update account_move_line set account_id=%s,tax_code_id=%s,tax_amount=%s where id=%s ''',\
#                                                (4231,1842,tax_amount,line.id))
#                                     cr.commit()
#                                     print '-----sale @@@@@refund@@@@@@@@@tax line updated------'
#                                                                                                  
#                             else :
#                                  
#                                 print '-----INVALID SALE RECORD-----------' 
#                                 ng_data_sale.append([int(row[0])])                                                                                                 
# 
# 
# 
# 
#         with open('/home/bista/Downloads/rakesh/issues/JV/NOV/24NOV/travel/error.csv','wb') as csvfile:
#         #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
#             spamwriter = csv.writer(csvfile, delimiter=',')  
#             #import ipdb;ipdb.set_trace()     
#             for write_rows in ng_data_sale:
#                 spamwriter.writerow(write_rows)   
# 
# 
#         ######## CORRECT CHART OF ACCOUNTS
#         
#         
#         jv_ids=jv_line_obj.search(cr,uid,[('name','in',['Service Tax Rate on Domestic Air Ticket 0.62%'])])
#         print 'sale invoice jv line for Service Tax Rate on Domestic Air Ticket 0.62%',len(jv_ids)
#         for jv_line in jv_line_obj.browse(cr,uid,jv_ids) :
#             #for sale invoice 
#             if jv_line.journal_id.id in [10,158,156,154,152,150,148]:  
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
# 
#                 cr.execute('''update account_move_line set tax_code_id=1870,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (10,158,156,154,152,150,148) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
#                     cr.execute('''update account_move_line set tax_code_id=1868,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()     
#                     
#                     
#             elif jv_line.journal_id.id in [12]: 
#                 ###sale refund
# 
#             
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
#                 if jv_line.debit==0.0000 : 
#                     tax_amount=jv_line.debit
#                 else : 
#                     tax_amount=-(jv_line.debit)
# 
#                 cr.execute('''update account_move_line set tax_code_id=1870,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (12) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
# 
# 
#                     if jv_line.debit==0.0000 : 
#                         tax_amount=jv_line.debit
#                     else : 
#                         tax_amount=-(jv_line.debit)         
#                                    
#                     cr.execute('''update account_move_line set tax_code_id=1868,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()                     
#                            
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#####            
#         
#         jv_ids=jv_line_obj.search(cr,uid,[('name','in',['Service Tax Rate on International Air Ticket 1.24%'])])
#         print 'sale invoice jv line for Service Tax Rate on International Air Ticket 1.24%',len(jv_ids)
#         for jv_line in jv_line_obj.browse(cr,uid,jv_ids) :
#             #for sale invoice 
#             if jv_line.journal_id.id in [10,158,156,154,152,150,148]:  
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
# 
#                 cr.execute('''update account_move_line set tax_code_id=1858,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (10,158,156,154,152,150,148) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
#                     cr.execute('''update account_move_line set tax_code_id=1856,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()     
#                     
#                     
#             elif jv_line.journal_id.id in [12]: 
#                 ###sale refund
# 
#             
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
#                 if jv_line.debit==0.0000 : 
#                     tax_amount=jv_line.debit
#                 else : 
#                     tax_amount=-(jv_line.debit)
# 
#                 cr.execute('''update account_move_line set tax_code_id=1858,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (12) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
# 
# 
#                     if jv_line.debit==0.0000 : 
#                         tax_amount=jv_line.debit
#                     else : 
#                         tax_amount=-(jv_line.debit)         
#                                    
#                     cr.execute('''update account_move_line set tax_code_id=1856,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()   
#                     
# #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#################3###############
# 
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#####            
#         
#         jv_ids=jv_line_obj.search(cr,uid,[('name','in',['Service Tax Rate on Tour & Package  Service 3.09%'])])
#         print 'sale invoice jv line for Service Tax Rate on Tour & Package  Service 3.09%',len(jv_ids)
#         for jv_line in jv_line_obj.browse(cr,uid,jv_ids) :
#             #for sale invoice 
#             if jv_line.journal_id.id in [10,158,156,154,152,150,148]:  
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
# 
#                 cr.execute('''update account_move_line set tax_code_id=1830,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (10,158,156,154,152,150,148) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
#                     cr.execute('''update account_move_line set tax_code_id=1822,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()     
#                     
#                     
#             elif jv_line.journal_id.id in [12]: 
#                 ###sale refund
# 
#             
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
#                 if jv_line.debit==0.0000 : 
#                     tax_amount=jv_line.debit
#                 else : 
#                     tax_amount=-(jv_line.debit)
# 
#                 cr.execute('''update account_move_line set tax_code_id=1830,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (12) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
# 
# 
#                     if jv_line.debit==0.0000 : 
#                         tax_amount=jv_line.debit
#                     else : 
#                         tax_amount=-(jv_line.debit)         
#                                    
#                     cr.execute('''update account_move_line set tax_code_id=1822,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()   
#                     
# #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#################3###############
#         
# 
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#####            
#         
#         jv_ids=jv_line_obj.search(cr,uid,[('name','in',['Service Tax Rate on Domestic Air Ticket 0.7%'])])
#         print 'sale invoice jv line for Service Tax Rate on Domestic Air Ticket 0.7%',len(jv_ids)
#         for jv_line in jv_line_obj.browse(cr,uid,jv_ids) :
#             #for sale invoice 
#             if jv_line.journal_id.id in [10,158,156,154,152,150,148]:  
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
# 
#                 cr.execute('''update account_move_line set tax_code_id=1838,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (10,158,156,154,152,150,148) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
#                     cr.execute('''update account_move_line set tax_code_id=1836,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()     
#                     
#                     
#             elif jv_line.journal_id.id in [12]: 
#                 ###sale refund
# 
#             
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
#                 if jv_line.debit==0.0000 : 
#                     tax_amount=jv_line.debit
#                 else : 
#                     tax_amount=-(jv_line.debit)
# 
#                 cr.execute('''update account_move_line set tax_code_id=1838,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (12) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
# 
# 
#                     if jv_line.debit==0.0000 : 
#                         tax_amount=jv_line.debit
#                     else : 
#                         tax_amount=-(jv_line.debit)         
#                                    
#                     cr.execute('''update account_move_line set tax_code_id=1836,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()   
#                     
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@###############          
# 
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#####            
#         
#         jv_ids=jv_line_obj.search(cr,uid,[('name','in',['Service Tax Rate on International Air Ticket 1.4% '])])
#         print 'sale invoice jv line for Service Tax Rate on International Air Ticket 1.4% ',len(jv_ids)
#         for jv_line in jv_line_obj.browse(cr,uid,jv_ids) :
#             #for sale invoice 
#             if jv_line.journal_id.id in [10,158,156,154,152,150,148]:  
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
# 
#                 cr.execute('''update account_move_line set tax_code_id=1858,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (10,158,156,154,152,150,148) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
#                     cr.execute('''update account_move_line set tax_code_id=1856,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()     
#                     
#                     
#             elif jv_line.journal_id.id in [12]: 
#                 ###sale refund
# 
#             
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
#                 if jv_line.debit==0.0000 : 
#                     tax_amount=jv_line.debit
#                 else : 
#                     tax_amount=-(jv_line.debit)
# 
#                 cr.execute('''update account_move_line set tax_code_id=1858,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (12) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
# 
# 
#                     if jv_line.debit==0.0000 : 
#                         tax_amount=jv_line.debit
#                     else : 
#                         tax_amount=-(jv_line.debit)         
#                                    
#                     cr.execute('''update account_move_line set tax_code_id=1856,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()   
#                     
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@###############               
# 
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#####            
#         
#         jv_ids=jv_line_obj.search(cr,uid,[('name','in',['Service Tax Rate on Car Service 4.95%'])])
#         print 'sale invoice jv line for Service Tax Rate on Car Service 4.95%',len(jv_ids)
#         for jv_line in jv_line_obj.browse(cr,uid,jv_ids) :
#             #for sale invoice 
#             if jv_line.journal_id.id in [10,158,156,154,152,150,148]:  
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
# 
#                 cr.execute('''update account_move_line set tax_code_id=1862,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (10,158,156,154,152,150,148) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
#                     cr.execute('''update account_move_line set tax_code_id=1860,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()     
#                     
#                     
#             elif jv_line.journal_id.id in [12]: 
#                 ###sale refund
# 
#             
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
#                 if jv_line.debit==0.0000 : 
#                     tax_amount=jv_line.debit
#                 else : 
#                     tax_amount=-(jv_line.debit)
# 
#                 cr.execute('''update account_move_line set tax_code_id=1862,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (12) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
# 
# 
#                     if jv_line.debit==0.0000 : 
#                         tax_amount=jv_line.debit
#                     else : 
#                         tax_amount=-(jv_line.debit)         
#                                    
#                     cr.execute('''update account_move_line set tax_code_id=1860,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()   
#                     
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@###############  
# 
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#####            
#         
#         jv_ids=jv_line_obj.search(cr,uid,[('name','in',['Service Tax Rate on Tour & Package  Service 3.5%'])])
#         print 'sale invoice jv line for Service Tax Rate on Tour & Package  Service 3.5%',len(jv_ids)
#         for jv_line in jv_line_obj.browse(cr,uid,jv_ids) :
#             #for sale invoice 
#             if jv_line.journal_id.id in [10,158,156,154,152,150,148]:  
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
# 
#                 cr.execute('''update account_move_line set tax_code_id=1846,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (10,158,156,154,152,150,148) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
#                     cr.execute('''update account_move_line set tax_code_id=1844,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()     
#                     
#                     
#             elif jv_line.journal_id.id in [12]: 
#                 ###sale refund
# 
#             
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
#                 if jv_line.debit==0.0000 : 
#                     tax_amount=jv_line.debit
#                 else : 
#                     tax_amount=-(jv_line.debit)
# 
#                 cr.execute('''update account_move_line set tax_code_id=1846,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (12) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
# 
# 
#                     if jv_line.debit==0.0000 : 
#                         tax_amount=jv_line.debit
#                     else : 
#                         tax_amount=-(jv_line.debit)         
#                                    
#                     cr.execute('''update account_move_line set tax_code_id=1844,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()   
#                     
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@############### 
# 
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#####            
#         
#         jv_ids=jv_line_obj.search(cr,uid,[('name','in',['Service Tax Rate on Hotel Service 1.4%'])])
#         print 'sale invoice jv line for Service Tax Rate on Hotel Service 1.4%',len(jv_ids)
#         for jv_line in jv_line_obj.browse(cr,uid,jv_ids) :
#             #for sale invoice 
#             if jv_line.journal_id.id in [10,158,156,154,152,150,148]:  
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
# 
#                 cr.execute('''update account_move_line set tax_code_id=1854,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (10,158,156,154,152,150,148) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
#                     cr.execute('''update account_move_line set tax_code_id=1852,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()     
#                     
#                     
#             elif jv_line.journal_id.id in [12]: 
#                 ###sale refund
# 
#             
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
#                 if jv_line.debit==0.0000 : 
#                     tax_amount=jv_line.debit
#                 else : 
#                     tax_amount=-(jv_line.debit)
# 
#                 cr.execute('''update account_move_line set tax_code_id=1854,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (12) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
# 
# 
#                     if jv_line.debit==0.0000 : 
#                         tax_amount=jv_line.debit
#                     else : 
#                         tax_amount=-(jv_line.debit)         
#                                    
#                     cr.execute('''update account_move_line set tax_code_id=1852,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()   
#                     
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@############### 
# 
# 
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#####            
#         
#         jv_ids=jv_line_obj.search(cr,uid,[('name','in',['Service Tax Rate on Car Service 5.6%'])])
#         print 'sale invoice jv line for Service Tax Rate on Car Service 5.6%',len(jv_ids)
#         for jv_line in jv_line_obj.browse(cr,uid,jv_ids) :
#             #for sale invoice 
#             if jv_line.journal_id.id in [10,158,156,154,152,150,148]:  
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
# 
#                 cr.execute('''update account_move_line set tax_code_id=1850,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (10,158,156,154,152,150,148) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
#                     cr.execute('''update account_move_line set tax_code_id=1848,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()     
#                     
#                     
#             elif jv_line.journal_id.id in [12]: 
#                 ###sale refund
# 
#             
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
#                 if jv_line.debit==0.0000 : 
#                     tax_amount=jv_line.debit
#                 else : 
#                     tax_amount=-(jv_line.debit)
# 
#                 cr.execute('''update account_move_line set tax_code_id=1850,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (12) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
# 
# 
#                     if jv_line.debit==0.0000 : 
#                         tax_amount=jv_line.debit
#                     else : 
#                         tax_amount=-(jv_line.debit)         
#                                    
#                     cr.execute('''update account_move_line set tax_code_id=1848,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()   
#                     
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@############### 
# 
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#####            
#         
#         jv_ids=jv_line_obj.search(cr,uid,[('name','in',['Output Service Tax @ 14% 29T'])])
#         print 'sale invoice jv line for Output Service Tax @ 14% 29T',len(jv_ids)
#         for jv_line in jv_line_obj.browse(cr,uid,jv_ids) :
#             #for sale invoice 
#             if jv_line.journal_id.id in [10,158,156,154,152,150,148]:  
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
# 
#                 cr.execute('''update account_move_line set tax_code_id=1902,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (10,158,156,154,152,150,148) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
#                     cr.execute('''update account_move_line set tax_code_id=1900,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()     
#                     
#                     
#             elif jv_line.journal_id.id in [12]: 
#                 ###sale refund
# 
#             
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
#                 if jv_line.debit==0.0000 : 
#                     tax_amount=jv_line.debit
#                 else : 
#                     tax_amount=-(jv_line.debit)
# 
#                 cr.execute('''update account_move_line set tax_code_id=1902 ,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (12) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
# 
# 
#                     if jv_line.debit==0.0000 : 
#                         tax_amount=jv_line.debit
#                     else : 
#                         tax_amount=-(jv_line.debit)         
#                                    
#                     cr.execute('''update account_move_line set tax_code_id=162,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()   
#                     
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@############### 
# 
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#####            
#         
#         jv_ids=jv_line_obj.search(cr,uid,[('name','in',['Output Service Tax @ 12.36%'])])
#         print 'sale invoice jv line for Output Service Tax @ 12.36%',len(jv_ids)
#         for jv_line in jv_line_obj.browse(cr,uid,jv_ids) :
#             #for sale invoice 
#             if jv_line.journal_id.id in [10,158,156,154,152,150,148]:  
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
# 
#                 cr.execute('''update account_move_line set tax_code_id=117,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (10,158,156,154,152,150,148) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
#                     cr.execute('''update account_move_line set tax_code_id=1900,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()     
#                     
#                     
#             elif jv_line.journal_id.id in [12]: 
#                 ###sale refund
# 
#             
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
#                 if jv_line.debit==0.0000 : 
#                     tax_amount=jv_line.debit
#                 else : 
#                     tax_amount=-(jv_line.debit)
# 
#                 cr.execute('''update account_move_line set tax_code_id=117 ,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (12) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
# 
# 
#                     if jv_line.debit==0.0000 : 
#                         tax_amount=jv_line.debit
#                     else : 
#                         tax_amount=-(jv_line.debit)         
#                                    
#                     cr.execute('''update account_move_line set tax_code_id=162,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()   
#                     
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@############### 
# 
# ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#####            
#         
#         jv_ids=jv_line_obj.search(cr,uid,[('name','in',['Output Service Tax @ 12.36%'])])
#         print 'sale invoice jv line for Output Service Tax @ 12.36%',len(jv_ids)
#         for jv_line in jv_line_obj.browse(cr,uid,jv_ids) :
#             #for sale invoice 
#             if jv_line.journal_id.id in [10,158,156,154,152,150,148]:  
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
# 
#                 cr.execute('''update account_move_line set tax_code_id=117,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (10,158,156,154,152,150,148) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
#                     cr.execute('''update account_move_line set tax_code_id=1900,tax_amount=%s where id=%s''',(jv_line.credit,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()     
#                     
#                     
#             elif jv_line.journal_id.id in [12]: 
#                 ###sale refund
# 
#             
# 
#                 ##get jv line ids of product
#                 #
# 
# ##
#                 if jv_line.debit==0.0000 : 
#                     tax_amount=jv_line.debit
#                 else : 
#                     tax_amount=-(jv_line.debit)
# 
#                 cr.execute('''update account_move_line set tax_code_id=117 ,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                 print '-----------tax code and amount updated for product line------'
#                 
#                     
#                 cr.execute('''select id from account_move_line where move_id=%s ''',(jv_line.move_id.id,))
#                 jv_line_ids=map(lambda x:x[0],cr.fetchall())
#                   
#                 cr.execute('''select id from account_move_line where account_id in (460,4187,456,457,4212,5656,458,459) and journal_id in (12) and id in %s''',(tuple(jv_line_ids),))
#                 product__jv_line_ids=map(lambda x:x[0],cr.fetchall())             
#                     
#         
#       
#                 for jv_line in jv_line_obj.browse(cr,uid,product__jv_line_ids) :     
#                     count+=1;print count      
#                     ##updating product line##
# 
# 
#                     if jv_line.debit==0.0000 : 
#                         tax_amount=jv_line.debit
#                     else : 
#                         tax_amount=-(jv_line.debit)         
#                                    
#                     cr.execute('''update account_move_line set tax_code_id=162,tax_amount=%s where id=%s''',(tax_amount,jv_line.id))
#                     print '-----------tax code and amount updated for product line------'                             
#                     cr.commit()   
                    
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@############### 

  ##@@@@@@@@@@@@@@@@29 THREE HOLIDAYS PVT. LTD  ENDS@@@@@@@@@@@@@@@@@@@@22

        print '-----OVER-----'
        
        return True




    def get_sale_journal_for_issues(self,cr,uid,vals) :
        move_obj=self.pool.get('account.move')
        


#         #####################29 THREE HOLIDAYS PVT. LTD#############################
       
#         ############for sale and sale refund
#         data=[]
#         cr.execute('''select id from account_move_line where name='Service Tax Rate on Domestic Air Ticket 0.62%' and account_id=459  ''')
#         move_line_id=map(lambda x:x[0],cr.fetchall())
#   
#         cr.execute('''select id from account_move_line where name='Service Tax Rate on International Air Ticket 1.24%' and account_id=4212  ''')
#         move_line_id.extend(map(lambda x:x[0],cr.fetchall()))
#   
#         cr.execute('''select id from account_move_line where name='Service Tax Rate on Tour & Package  Service 3.09%' and account_id=460  ''')
#         move_line_id.extend(map(lambda x:x[0],cr.fetchall()))
#   
#         cr.execute('''select id from account_move_line where name='Service Tax Rate on Domestic Air Ticket 0.7%' and account_id=459  ''')
#         move_line_id.extend(map(lambda x:x[0],cr.fetchall()))     
# 
#         cr.execute('''select id from account_move_line where name='Service Tax Rate on International Air Ticket 1.4% ' and account_id=4212  ''')
#         move_line_id.extend(map(lambda x:x[0],cr.fetchall()))
# 
# 
#         
#          
#           
#         cr.execute('''select move_id from account_move_line where id in %s''',(tuple(move_line_id),))
#         move_id=map(lambda x:x[0],cr.fetchall())
#         print '------------SALE INVOICE--------',len(move_id)
#         import ipdb;ipdb.set_trace()   
#         for move in move_obj.browse(cr,uid,move_id) : 
#             data.append([move.id,move.name,move.company_id.name,move.journal_id.id])
#          
#  
 
#        with open('/home/bista/Downloads/rakesh/issues/JV/NOV/24NOV/travel/Service Tax Rate on Domestic Air Ticket 0.62%.csv','wb') as csvfile:
#        with open('/home/bista/Downloads/rakesh/issues/JV/NOV/24NOV/travel/Service Tax Rate on International Air Ticket 1.24%.csv','wb') as csvfile:
#        with open('/home/bista/Downloads/rakesh/issues/JV/NOV/24NOV/travel/Service Tax Rate on Tour & Package  Service 3.09%.csv','wb') as csvfile:
#        with open('/home/bista/Downloads/rakesh/issues/JV/NOV/24NOV/travel/Service Tax Rate on Domestic Air Ticket 0.7%.csv','wb') as csvfile:
#        with open('/home/bista/Downloads/rakesh/issues/JV/NOV/24NOV/travel/Service Tax Rate on International Air Ticket 1.4% .csv','wb') as csvfile:
#         with open('/home/bista/Downloads/rakesh/issues/JV/NOV/24NOV/travel/final.csv','wb') as csvfile:
#             spamwriter = csv.writer(csvfile, delimiter=',')  
#             #import ipdb;ipdb.set_trace()     
#             for write_rows in data:
#                 spamwriter.writerow(write_rows) 

# ################################29 THREE HOLIDAYS PVT. LTD  ENDS########################



#         
# #         #####################ROUTESMS SOLUTIONS (UK) LIMITED#############################
# #         
#         ############for sale and sale refund
        data=[]
        cr.execute('''select id from account_move_line where name='VAT Tax 20%' and account_id=3429  ''')
        move_line_id=map(lambda x:x[0],cr.fetchall())
        import ipdb;ipdb.set_trace() 
          
        cr.execute('''select move_id from account_move_line where id in %s''',(tuple(move_line_id),))
        move_id=map(lambda x:x[0],cr.fetchall())
        print '------------SALE INVOICE--------',len(move_id)
          
        for move in move_obj.browse(cr,uid,move_id) : 
            data.append([move.id,move.name,move.company_id.name])
          
  
  
        with open('/home/bista/Downloads/rakesh/issues/JV/DEC/22dec/VAT Tax 20%_RSLUK_JV_list.csv','wb') as csvfile:
        #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
            spamwriter = csv.writer(csvfile, delimiter=',')  
            #import ipdb;ipdb.set_trace()     
            for write_rows in data:
                spamwriter.writerow(write_rows) 
# #                 
# # ################################ROUTESMS SOLUTIONS (UK) LIMITED  ENDS########################
# 
# 
# 
# #####################################ROUTESMS SOLUTIONS NIGERIA LIMITED#########################
# 
#             ##############for sale and sale refund######
#         data=[]
#         cr.execute('''select id from account_move_line where name='Output VAT Tax 5% NGN' and account_id=2889  ''')
#         move_line_id=map(lambda x:x[0],cr.fetchall())
#         print move_line_id
#         #import ipdb;ipdb.set_trace()   
#         cr.execute('''select move_id from account_move_line where id in %s''',(tuple(move_line_id),))
#         move_id=map(lambda x:x[0],cr.fetchall())
#          
#         
#         cr.execute('''select id from account_move_line where name='VAT Tax 5%_Routesms Nigeria Limited' and account_id=2889  ''')
#         move_line_id1=map(lambda x:x[0],cr.fetchall())
#         print move_line_id1
#         #import ipdb;ipdb.set_trace()   
#         cr.execute('''select move_id from account_move_line where id in %s''',(tuple(move_line_id1),))
#         move_id.extend(map(lambda x:x[0],cr.fetchall()))      
#         print '------------SALE INVOICE--------',len(move_id)
#          
#  
#  
#          
#         for move in move_obj.browse(cr,uid,move_id) : 
#             data.append([move.id,move.name,move.company_id.name])
#          
#  
#  
#         with open('/home/bista/Downloads/rakesh/issues/JV/DEC/22dec/Output VAT Tax 5% NGN_JV_list.csv','wb') as csvfile:
#         #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
#             spamwriter = csv.writer(csvfile, delimiter=',')  
#              
#             for write_rows in data:
#                 spamwriter.writerow(write_rows) 
#                  
#  
#  
#         #######for purchase and purchase refund############
#                  
#         data=[]
#         cr.execute('''select id from account_move_line where name='Input VAT Tax 5% NGN' and account_id=2899 ''')
#         move_line_id=map(lambda x:x[0],cr.fetchall())
#         print move_line_id
#         #import ipdb;ipdb.set_trace()   
#         cr.execute('''select move_id from account_move_line where id in %s''',(tuple(move_line_id),))
#         move_id=map(lambda x:x[0],cr.fetchall())
#         print '------------PURCHASE INVOICE--------',len(move_id)
#         import ipdb;ipdb.set_trace()        
#          
#         for move in move_obj.browse(cr,uid,move_id) : 
#             data.append([move.id,move.name,move.company_id.name])
#          
#  
#  
#         with open('/home/bista/Downloads/rakesh/issues/JV/DEC/22dec/Input VAT Tax 5% NGN_JV_list.csv','wb') as csvfile:
#         #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
#             spamwriter = csv.writer(csvfile, delimiter=',')  
#             #import ipdb;ipdb.set_trace()     
#             for write_rows in data:
#                 spamwriter.writerow(write_rows)                 
#####################################ROUTESMS SOLUTIONS NIGERIA LIMITED  ENDS #####################         

###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@############################

#####################################SPHERE EDGE CONSULTING INDIA PVT. LTD#########################


            ##############for sale and sale refund######
#         data=[]
#         cr.execute('''select id from account_move_line where name='Output Service Tax @14% SPC' and account_id=2079  ''')
#         move_line_id=map(lambda x:x[0],cr.fetchall())
#         print move_line_id
#         #import ipdb;ipdb.set_trace()   
#         cr.execute('''select move_id from account_move_line where id in %s''',(tuple(move_line_id),))
#         move_id=map(lambda x:x[0],cr.fetchall())
#         
#     
#         print '------------SALE INVOICE--------',len(move_id)
#         import ipdb;ipdb.set_trace() 
# 
#         for move in move_obj.browse(cr,uid,move_id) : 
#             data.append([move.id,move.name,move.company_id.name])
#         
# 
# 
#         with open('/home/bista/Downloads/rakesh/issues/JV/NOV/17NOV/Output Service Tax @14% SPC.csv','wb') as csvfile:
#         #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
#             spamwriter = csv.writer(csvfile, delimiter=',')  
#             
#             for write_rows in data:
#                 spamwriter.writerow(write_rows) 
#                 
# 
# 
#         #######for purchase and purchase refund############
#                 
#         data=[]
#         cr.execute('''select id from account_move_line where name='Input Service Tax @14% SPC' and account_id=2089 ''')
#         move_line_id=map(lambda x:x[0],cr.fetchall())
#         print move_line_id
#         #import ipdb;ipdb.set_trace()   
#         if move_line_id : 
#             
#             cr.execute('''select move_id from account_move_line where id in %s''',(tuple(move_line_id),))
#             move_id=map(lambda x:x[0],cr.fetchall())
#             print '------------PURCHASE INVOICE--------',len(move_id)
#             import ipdb;ipdb.set_trace()        
#             
#             for move in move_obj.browse(cr,uid,move_id) : 
#                 data.append([move.id,move.name,move.company_id.name])
#             
#         else : 
#             print '-----------NO PURCHASE REOCORD FOUND-------'
#             
# 
#         with open('/home/bista/Downloads/rakesh/issues/JV/NOV/17NOV/Input Service Tax @14% SPC.csv','wb') as csvfile:
#         #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
#             spamwriter = csv.writer(csvfile, delimiter=',')  
#             #import ipdb;ipdb.set_trace()     
#             for write_rows in data:
#                 spamwriter.writerow(write_rows)                 
#####################################SPHERE EDGE CONSULTING INDIA PVT. LTD  ENDS #####################       
        
        print '-------over----------'
        return True



    def migrate_salesperson_mayank(self,cr,uid,vals) :
        ''' Migrate BM'''
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        sale_obj=self.pool.get('sale.order')
        inv_obj=self.pool.get('account.invoice')
        vals={}
        count=0
        bm_id=450
        data=[]
        #import ipdb;ipdb.set_trace()
        try: 
            
            with open('/home/bista/Downloads/mayank/bm_transfer.csv','r') as e: 
    
                reader = csv.reader(e)
                import ipdb;ipdb.set_trace()
                for row in reader:
                    count+=1
                    if row[0] : 
                        #import ipdb;ipdb.set_trace()
                        partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',row[0].rsplit()[0].lstrip())])
                        if partner_id : 
                            ###assigned BM to partner
                            #partner=partner_obj.browse(cr,uid,partner_id[0])
                            #data.append([partner.name,partner.email,partner.partner_sequence,partner.user_id.name])
                            partner_obj.write(cr,uid,partner_id,{'user_id':bm_id})
                             
                            ###assigned to CRM#####
                            crm_id=crm_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                            if crm_id : 
                                print '******************TOTAL CRM *************',len(crm_id)
                                 
                                     
                                for crm in crm_id : 
                                    user_id_onchange=crm_obj.on_change_user(cr,uid,[crm],bm_id)
                                    if user_id_onchange.get('value').get('employee_id') : 
                                        crm_obj.write(cr,uid,[crm],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                                    ,'user_id':bm_id})
                                         
                                        print '*****************CRM UPDATED******************'
                                         
                             
                            ######assigne to Sale order##########
                            sale_id=sale_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                            if sale_id : 
                                for sale in sale_id  :
                                    user_id_onchange=sale_obj.sale_onchange_user(cr, uid, [sale_id], bm_id)
                                    if user_id_onchange.get('value').get('employee_id') : 
                                        sale_obj.write(cr,uid,[sale],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                                         ,'user_id':bm_id})
     
                                        print '*****************SALE UPDATED******************'
                                     
                                     
                            #############assign invoices##########
                            inv_id=inv_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                            if inv_id : 
                                for inv in inv_id :
                                        inv_obj.write(cr,uid,[inv],{'user_id':bm_id})
                                        print '*****************INVOICE UPDATED******************'
                                        
                        else:
                            print '*****************N O !!! P A R T N E R FOUND!!!!!******************'
                            data.append([row[7]])
                        
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E
            
        with open('/home/bista/Downloads/mayank/logs/mayank_logs.csv','wb') as csvfile:
        #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
            spamwriter = csv.writer(csvfile, delimiter=',')  
            #import ipdb;ipdb.set_trace()     
            for write_rows in data:
                spamwriter.writerow(write_rows)  
                        
             
        print '-------------O V E R------------'                                                
        return True

    def create_crm_lead_fresh_for_existing_partner(self,cr,uid,vals):
        '''create leads  for partners whose lead doesnt exist '''
        
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        user_obj=self.pool.get('res.users')
        hr_obj=self.pool.get('hr.employee')
        crm_opp_obj=self.pool.get('crm.lead2opportunity.partner')
        count=0
      #  
        import ipdb;ipdb.set_trace()
        try : 
            master_partner_ids=partner_obj.search(cr,uid,[('customer','=',True),('is_company','=',True),('state','=','draft')])
            print '-------TOTAL MASTER PARTNERS ----',len(master_partner_ids)
            cr.execute('''select partner_id from crm_lead ''')
            crm_partner_ids=map(lambda x:x[0],cr.fetchall())
            print '-------TOTAL CRM ----',len(crm_partner_ids)
            for partner_id in master_partner_ids : 
                count+=1;print count
                if partner_id in crm_partner_ids  :
                    print '@@@@@@@@@@@@@@@@@@@@LEAD ALREADY  EXIST-------@@@@@@@@@@@@@@@'
                    
                else : 
                    partner_val=partner_obj.browse(cr,uid,partner_id)
                    if partner_val.user_id : 
                        bm_id=partner_val.user_id.id
                        
                    else : 
                        print '------NO BM FOUND-----'

                        with open("/home/bista/Downloads/sandip_sir/no_bm_found_fresh_lead.txt", "a") as donefile_new:
                            try : 
                                
                                donefile_new.write(str(partner_val.id)+'{}'+'odoo_id' +'{}' + str(partner_val.name)+' {}'+ str(partner_val.partner_sequence)+'\n')
                            except Exception as E : 
                                donefile_new.write(str(partner_val.id)+'{}'+'odoo_id' +'{}' +'UNICODE CHARATCER'+' {}'+ str(partner_val.partner_sequence)+'\n')
                                
                        #continue
                        bm_id=507 #rohan gupta
                    
                    employee_id=hr_obj.search(cr,uid,[('user_id','=',bm_id)])
                    if employee_id : 
                        if len(employee_id) >1 : 
                            print '--------MULITPLE EMPLOYEE IDS FOUND---'
    
                            with open("/home/bista/Downloads/sandip_sir/multi_employee_found_fresh_lead.txt", "a") as donefile_new:
                                try : 
                                
                                    donefile_new.write(str(partner_val.id)+'{}'+'odoo_id' +'{}' + str(partner_val.name)+' {}'+ str(partner_val.partner_sequence)+'\n')
                                except Exception as E : 
                                    donefile_new.write(str(partner_val.id)+'{}'+'odoo_id' +'{}' +'UNICODE CHARATCER'+' {}'+ str(partner_val.partner_sequence)+'\n')
                            continue        
                        
                        emp_id=employee_id[0]
                        
                    else:
                        print '------NO EMPLOYEE FOUND-----'
                        with open("/home/bista/Downloads/sandip_sir/no_employee_found_fresh_lead.txt", "a") as donefile_new:
                            try : 
                                
                                donefile_new.write(str(partner_val.id)+'{}'+'odoo_id' +'{}' + str(partner_val.name)+' {}'+ str(partner_val.partner_sequence)+'\n')
                            except Exception as E : 
                                donefile_new.write(str(partner_val.id)+'{}'+'odoo_id' +'{}' +'UNICODE CHARATCER'+' {}'+ str(partner_val.partner_sequence)+'\n')

                        continue                              
                            


                        
                    crm_vals={'partner_id':partner_id,'name':'Messaging Enterprise','description':'Messaging Enterprise',\
                                  'user_id':bm_id,'employee_id':emp_id,\
                                  'qms_crm':False,'odoo_script_new_crm_fresh_existing_partner':True,'stage_id':1}
                        
                    onchange_vals=crm_obj.on_change_partner_id(cr, uid, [], partner_id, context=None)
                    crm_vals.update(onchange_vals['value'])                            
                           
                    crm_id=crm_obj.create(cr,uid,crm_vals)
                    print '--------------LEAD CREATED---------------'

            
                                               
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E,count
        
        print '---------------O V  E   R ------------'
        return True




    def create_crm_lead_CC_for_existing_partner(self,cr,uid,vals):
        '''create leads and then convered client status for partners whose lead doesnt exist '''
        
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        user_obj=self.pool.get('res.users')
        hr_obj=self.pool.get('hr.employee')
        crm_opp_obj=self.pool.get('crm.lead2opportunity.partner')
        count=0
      #  
        import ipdb;ipdb.set_trace()
        try : 
            master_partner_ids=partner_obj.search(cr,uid,[('customer','=',True),('is_company','=',True),('state','=','confirm')])
            print '-------TOTAL MASTER PARTNERS ----',len(master_partner_ids)
            cr.execute('''select partner_id from crm_lead ''')
            crm_partner_ids=map(lambda x:x[0],cr.fetchall())
            print '-------TOTAL CRM ----',len(crm_partner_ids)
            for partner_id in master_partner_ids : 
                count+=1;print count
                if partner_id in crm_partner_ids  :
                    print '@@@@@@@@@@@@@@@@@@@@LEAD ALREADY  EXIST-------@@@@@@@@@@@@@@@'
                    
                else : 
                    partner_val=partner_obj.browse(cr,uid,partner_id)
                    if partner_val.user_id : 
                        bm_id=partner_val.user_id.id
                        
                    else : 
                        print '------NO BM FOUND-----'

                        with open("/home/bista/Downloads/sandip_sir/no_bm_found.txt", "a") as donefile_new:
                            donefile_new.write(str(partner_val.id)+'{}'+'odoo_id' +'{}' + str(partner_val.partner_sequence)+'\n')
                        #continue 
                    bm_id=507 #rohan gupta 
                    
                    employee_id=hr_obj.search(cr,uid,[('user_id','=',bm_id)])
                    if employee_id : 
                        if len(employee_id) >1 : 
                            print '--------MULITPLE EMPLOYEE IDS FOUND---'
    
                            with open("/home/bista/Downloads/sandip_sir/multi_employee_found.txt", "a") as donefile_new:
                                donefile_new.write(str(partner_val.id)+'{}'+'odoo_id' +' {}'+ str(partner_val.partner_sequence)+'\n')
                            continue        
                        
                        emp_id=employee_id[0]
                        
                    else:
                        print '------NO EMPLOYEE FOUND-----'
                        with open("/home/bista/Downloads/sandip_sir/no_employee_found.txt", "a") as donefile_new:
                            donefile_new.write(str(partner_val.id)+'{}'+'odoo_id' +'{}' + str(partner_val.partner_sequence)+'\n')
                        continue                              
                            


                        
                    crm_vals={'partner_id':partner_id,'name':'Messaging Enterprise','description':'Messaging Enterprise',\
                                  'user_id':bm_id,'employee_id':emp_id,\
                                  'qms_crm':False,'odoo_script_new_crm_opportunity_existing_partner':True,}
                        
                    onchange_vals=crm_obj.on_change_partner_id(cr, uid, [], partner_id, context=None)
                    crm_vals.update(onchange_vals['value'])                            
                           
                    crm_id=crm_obj.create(cr,uid,crm_vals)
                    print '--------------LEAD CREATED---------------'
                    ##################create wizard id################################
                    cr.execute(''' insert into crm_lead2opportunity_partner(name,action,user_id,partner_id) VALUES('convert','exist',%s,%s)''',(bm_id,partner_id))
                    
                    cr.execute(''' select id from crm_lead2opportunity_partner where partner_id=%s''',(partner_id,))
                    wizard_id=map(lambda x:x[0],cr.fetchall())
                    if wizard_id :
                        
         ###############convert to opportuntity###############
                        opp_context={'lang': 'en_US', 'tz': 'Asia/Calcutta', 'uid': bm_id, 'active_model': 'crm.lead', 'empty_list_help_model': 'crm.case.section', \
                                     'stage_type': 'lead', 'search_disable_custom_filters': True, \
                                     'needaction_menu_ref': 'crm.menu_crm_opportunities', 'active_ids': [crm_id], 'active_id': crm_id}
                        
                        crm_opp_obj.action_apply(cr, uid, [wizard_id[0]],opp_context)
                        
                        cr.execute('''update crm_lead set stage_id=6 where id=%s ''',(crm_id,))
                        print '-----------converted client------------'
                                                        
                    else : 
                        print 'No wizard id found'
                        with open("/home/bista/Downloads/sandip_sir/crm_no_wizard.txt", "a") as donefile_new:
                            donefile_new.write(str(partner_val.id)+'{}'+'odoo_id' +' {}'+ str(partner_val.partner_sequence)+'\n')
                                     
            
                                               
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E,count
        
        print '---------------O V  E   R ------------'
        return True


    def mehrunisha_bm_detail(self,cr,uid,vals):
        partner_obj=self.pool.get('res.partner')
        user_obj=self.pool.get('res.users')
        count=0;data=[]
        try:
            
            with open('/home/bista/Downloads/mehrunisha/bm_sheet.csv','r') as e: 
    
                reader = csv.reader(e)
                
                for row in reader:
                    count+=1;print count 
                            
                
                    user_id=user_obj.search(cr,uid,[('login','=',row[0])])
                    if user_id : 
                        print 'BM************found*************'
#                         partner_id=partner_obj.search(cr,uid,[('user_id','=',user_id[0]),('prepaid','=',True),('postpaid','=',False),\
#                                                               ('country_id','=',False),('is_company','=',True)])

                        partner_id=partner_obj.search(cr,uid,[('user_id','=',user_id[0])\
                                                              ,('is_company','=',True)])                        
                        print '----Total Partner---------------',len(partner_id)
#                        import ipdb;ipdb.set_trace()
                        for partner in partner_obj.browse(cr,uid,partner_id) : 
                            if partner.prepaid and partner.postpaid : 
                                type='BOTH'
                            elif partner.prepaid : 
                                type='PREPAID'

                            elif partner.postpaid : 
                                type='POSTPAID'
                            
                            else:
                                type='NOT DEFINED'
                            
                            if partner.country_id:
                                country=partner.country_id.name
                                
                            else:
                                country='NO COUNTRY ASSIGNED'
                                                             
                                
                            
                            data.append([partner.id,partner.user_id.name,partner.name,type,partner.partner_sequence,country])
                            print '----data appended---------------'
                    else:
                        import ipdb;ipdb.set_trace()
                        print '---NO BM FOUND-----'
                        
                            
                        
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E
            

        with open('/home/bista/Downloads/mehrunisha/updated_FINAL_SHEET1.csv','wb') as csvfile:
        #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
            spamwriter = csv.writer(csvfile, delimiter=',')  
            #import ipdb;ipdb.set_trace()     
            for write_rows in data:
                try :
                    spamwriter.writerow(write_rows)
                      
                except Exception as E : 
#                    import ipdb;ipdb.set_trace()
                    write_rows[2]='UNICODE CHARATCER'
                    spamwriter.writerow(write_rows)
                    print '----UNICODE  CHARATCER---'                
        print '-------------O V E R------------'  
        return True      

    def correct_indian_country_partner(self,cr,uid,vals):
        ''' rectifiy partner for country id=254'''
        
        partner_obj=self.pool.get('res.partner')
        count=0
        partner_ids=partner_obj.search(cr,uid,[('country_id','in',[254,255])])
        print 'Total partner------------',len(partner_ids)
        import ipdb;ipdb.set_trace()
        for partner in partner_obj.browse(cr,uid,partner_ids) : 
            count+=1;print count
            cr.execute(''' update res_partner set country_id=105 where id=%s''',(partner.id,))
           # partner_obj.write(cr,uid,[partner.id],{'country_id':105})
            print '----updated----'
            
        print '---------OVER-----------'
        return True

    def correct_indian_state_partner(self,cr,uid,vals):
        ''' rectifiy partner for country id=254,255'''
        
        state_obj=self.pool.get('res.country.state')
        count=0
        try:
                
            state_ids=state_obj.search(cr,uid,[('country_id','in',[255,254])])
            print 'Total state------------',len(state_ids)
            import ipdb;ipdb.set_trace()
            for state_id in state_ids : 
                count+=1;print count
                state_obj.write(cr,uid,state_id,{'country_id':105}) 

            print '----updated----'
        except Exception as E:
            import ipdb;ipdb.set_trace()
            print 'EROR'
        print '---------OVER-----------'
        return True    
            


    def migrate_salesperson_Shivangi_Soni(self,cr,uid,vals) :
        ''' Migrate BM'''
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        sale_obj=self.pool.get('sale.order')
        inv_obj=self.pool.get('account.invoice')
        vals={}
        count=0
        bm_id=353
        data=[]
        #import ipdb;ipdb.set_trace()
        try: 
            
            with open('/home/bista/Downloads/shivangi/QMS to Odoo-1.csv','r') as e: 
    
                reader = csv.reader(e)
                import ipdb;ipdb.set_trace()
                for row in reader:
                    count+=1
                    if row[7] : 
                        #import ipdb;ipdb.set_trace()
                        partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',row[7].rsplit()[0].lstrip())])
                        if partner_id : 
                            ###assigned BM to partner
                            #partner=partner_obj.browse(cr,uid,partner_id[0])
                            #data.append([partner.name,partner.email,partner.partner_sequence,partner.user_id.name])
                            partner_obj.write(cr,uid,partner_id,{'user_id':bm_id})
                             
                            ###assigned to CRM#####
                            crm_id=crm_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                            if crm_id : 
                                print '******************TOTAL CRM *************',len(crm_id)
                                 
                                     
                                for crm in crm_id : 
                                    user_id_onchange=crm_obj.on_change_user(cr,uid,[crm],bm_id)
                                    if user_id_onchange.get('value').get('employee_id') : 
                                        crm_obj.write(cr,uid,[crm],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                                    ,'user_id':bm_id})
                                         
                                        print '*****************CRM UPDATED******************'
                                         
                             
                            ######assigne to Sale order##########
                            sale_id=sale_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                            if sale_id : 
                                for sale in sale_id  :
                                    user_id_onchange=sale_obj.sale_onchange_user(cr, uid, [sale_id], bm_id)
                                    if user_id_onchange.get('value').get('employee_id') : 
                                        sale_obj.write(cr,uid,[sale],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                                         ,'user_id':bm_id})
     
                                        print '*****************SALE UPDATED******************'
                                     
                                     
                            #############assign invoices##########
                            inv_id=inv_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                            if inv_id : 
                                for inv in inv_id :
                                        inv_obj.write(cr,uid,[inv],{'user_id':bm_id})
                                        print '*****************INVOICE UPDATED******************'
                                        
                        else:
                            print '*****************N O !!! P A R T N E R FOUND!!!!!******************'
                            data.append([row[7]])
                        
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E
            
        with open('/home/bista/Downloads/shivangi/logs/log_Shivangi_Soni.csv','wb') as csvfile:
        #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
            spamwriter = csv.writer(csvfile, delimiter=',')  
            #import ipdb;ipdb.set_trace()     
            for write_rows in data:
                spamwriter.writerow(write_rows)  
                        
             
        print '-------------O V E R------------'                                                
        return True






    def prepare_prepaid_postpaid_sheet(self,cr,uid,vals):
        '''prepare csv sheet for prepaid and postpaid client'''
        count=0
        partner_obj=self.pool.get('res.partner')
        data=[]
        
####################################prepare partner list##################3
        try:
                                
           # cr.execute(''' select id from  res_partner where is_company=True and prepaid=True and country_id in (105,255)''')
            cr.execute(''' select id from  res_partner where is_company=True and postpaid=True and  country_id in (105,255) ''')
            partner_ids=map(lambda x:x[0],cr.fetchall())
            print '----------------total partner---------------',len(partner_ids)
            import ipdb;ipdb.set_trace()
            for partner in partner_obj.browse(cr,uid,partner_ids) :
                count+=1;print count
                
                data.append([partner.name,partner.vertical.name,partner.partner_sequence,partner.prepaid,partner.user_id.name,partner.state]) 
                                 
        except Exception as E : 
            import ipdb;ipdb.set_trace()
                    
            print '---------ERROR-----',count

                    
                  
        with open('/home/bista/Downloads/rakesh/postpaid_sheet.csv','wb') as csvfile:
        #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
            spamwriter = csv.writer(csvfile)  
                 
            for write_rows in data:
                try :
                
                    spamwriter.writerow(write_rows)
                except Exception as E :
                   
                        print '---------WRITE ERROR-----',count                        
                    
            
        print '--------------------GAME OVER --------------------'        
        return True 





    def amount_to_zero_cancel_invoice(self,cr,uid,vals) :
        ''' Assign 0 amount to cancel invoice'''

        inv_obj=self.pool.get('account.invoice')

        vals={}
        count=0

        
        inv_ids=inv_obj.search(cr,uid,[('state','=','cancel')])
        #inv_ids=inv_obj.search(cr,uid,[('state','=','cancel'),('type','=','out_refund')])
        print '----------TOTAL INVOICES =',len(inv_ids)
        import ipdb;ipdb.set_trace()
        try : 
            for inv in inv_ids : 
                count+=1;print count
                cr.execute(''' update account_invoice_line set price_unit=0.00 where invoice_id=%s''',(inv,))
                print '-------INVOICES PRICE AMOUNT SET TO ZERO------------'
                inv_obj.button_reset_taxes (cr,uid,[inv])
                print '-------INVOICES UPDATED SUCESSFULLLY------------'
                
        except Exception as E :
            print count,E      
            import ipdb;ipdb.set_trace()
            
                      
        print '----------GAME -----OVER-----'
        return True
                    




    def remove_draft_customer_payment(self,cr,uid,vals):
        '''remove draft customer payment'''
        account_obj=self.pool.get('account.voucher')
        
        count=0
        vals={}
        
        #comp_li=(10,16,15)
#        cr.execute(''' select id  from account_invoice where create_date <='2015-08-31 17:30:16.887726'and type='out_invoice' and state='draft' ''',)
        cr.execute(''' select id  from account_voucher where type='receipt' and state='draft' and company_id=15 ''')
        invoice_ids=map(lambda x:x[0],cr.fetchall())        
        #invoice_ids=account_obj.search(cr,uid,[('company_id','=',10),('type','=','out_invoice'),('state','=','draft')])
        print len(invoice_ids)
        import ipdb;ipdb.set_trace()
        for inv_id in invoice_ids :
            count+=1 
            try : 
                account_obj.unlink(cr,uid,[inv_id],{})
                print 'Sucesfully deleted',count
                
            except Exception as E : 
                import ipdb;ipdb.set_trace()
                print '------------------ERROR-------------------',E
#                 with open("/home/bista/shanky/routesms/logs/delete_draft_invoice/delete_invoice.txt", "a") as donefile_new:
#                     donefile_new.write(str(count)+'\n')            

        print '---------------GAME OVER-----------'
        return True  


    def auto_asset_create_move(self,cr,uid,vals): 
	uid=1
        '''Generate Auto Moves for Asset depend on current date'''
        asset_obj=self.pool.get('account.asset.asset')
        asset_line_obj=self.pool.get('account.asset.depreciation.line')
        current_date=time.strftime("%Y-%m-%d")
        try : 
            
            for asset in asset_obj.browse(cr,uid,asset_obj.search(cr,uid,[('state','=','open')])) : 
                if asset.depreciation_line_ids : 
                    for asset_line in asset.depreciation_line_ids : 
                        if asset_line.depreciation_date ==current_date and asset_line.move_check ==False : 
                            asset_line_obj.create_move(cr, uid, [asset_line.id])
                            print '-------------------ASSET  MOVE  AUTOMATICALLY  CREATED-----------------'
        
        

        except Exception as E : 
            
            print E                                   
                        
        print '-------------EXITING SCRIPTING---------------'
        return True


    @api.cr_uid
    def asset_management_sceduler(self, cr, uid, ids=None, context=None):
	uid=1
        """scheduler for  Asset Management."""
         
        if context is None:
            context = {}
        res=None
        
        try:
            # Force auto-commit - this is meant to be called by
            # the scheduler, and we can't allow rolling back the status
            # of previously sent emails!
            res = self.auto_asset_create_move(cr, uid, [])
        except Exception:
            print '-------------QMS SCHEDULER FAILED----------'
        return res





    def update_account_type_in_invoice(self,cr,uid,vals):
        ''' update accounttype-prepaid postpaid on invoices depend on partners'''
        partner_obj=self.pool.get('res.partner')
        invoice_obj=self.pool.get('account.invoice')
        inv_ids=invoice_obj.search(cr,uid,[])
        import ipdb;ipdb.set_trace()
        count=0
        try: 
            
            for invoice in invoice_obj.browse(cr,uid,inv_ids) : 
                count+=1;print count
                
                
                if invoice.partner_id : 
                    
                    if invoice.partner_id.prepaid : 
                        account_type='prepaid'
                    elif invoice.partner_id.postpaid : 
                        account_type='postpaid'
                        
                    else : 
                        account_type=''
                        
                        
                        
                    invoice_obj.write(cr,uid,[invoice.id],{'partner_account_type':account_type})
                    print '******************************INVOICE UPDATED******************************'
                    
                else : 
                    
                    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@NO PARTNER FOUND@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
                    
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E                    
                
                
        print '-------------------OVER------------------'
        return True




    def updating_crm_partner_bm(self,cr,uid,vals) : 
        
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')

        vals={}
        count=0
        try: 
            
            
            with open('/home/bista/Downloads/amrita_jadhav/Not my client-1.csv','r') as e: 
    
                reader = csv.reader(e)
                import ipdb;ipdb.set_trace()
                for row in reader:
                    count+=1;print count
                    if row[0] and row[1] : 
                        crm=crm_obj.browse(cr,uid,int(row[0]))
                        if crm.partner_id : 
                            if crm.partner_id.id ==int(row[1]) : 
                                print '----------------MATCHED--------'
                                if crm.partner_id.user_id: 
                                    print '----------------SALESPERSON FOUND--------'
                                    crm_obj.write(cr,uid,[crm.id],{'user_id':crm.partner_id.user_id.id})
                                    print '----------------UPDATED--------'
                                    
                                else : 
                                    print '----------------SALESPERSON----NOT----- FOUND--------'
                                    
                            
                            else : 
                                print '------------NOT----MATCHED--------'
                               
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E                         
                    
                
        print '-------------------OVER------------------'
        return True          


    def delete_fiscal_yr_jv(self,cr,uid,vals) :
        ''' delete_jv '''
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        sale_obj=self.pool.get('sale.order')
        acc_move=self.pool.get('account.move')
        vals={}
        count=0
        
        
        try: 
            

            move_ids=acc_move.search(cr,uid,[('company_id','=',10),('period_id','=',266)])
            if move_ids : 
                print len(move_ids)
                import ipdb;ipdb.set_trace()
    
                for ids in move_ids : 
                    ids=[ids]
                    
                    if acc_move.browse(cr,uid,ids[0]).state=='draft':
                        print '--------JV in drfat state---------'
                        continue
                        
                    notify=acc_move.button_cancel(cr, uid, ids)
                    if notify : 
                        print '------------cancelled-----------'
                        acc_move.unlink(cr,uid,ids)
                    
                        print '------------DELETED-----------'
                        ###assigned to CRM#####
        
                    else:
                        print '*****************JV NOT CANCELLED!!!!!******************'
                        
                else:
                    print '*****************NO JV FOUND!!!!!******************'
                    
                        
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E
            

        print '-------------O V E R------------'                                                
        return True




    def migrate_salesperson_Mangesh_Shelar(self,cr,uid,vals) :
        ''' Migrate BM'''
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        sale_obj=self.pool.get('sale.order')
        inv_obj=self.pool.get('account.invoice')
        vals={}
        count=0
        bm_id=578
        data=[]
        
        try: 
            import ipdb;ipdb.set_trace()
            with open('/home/bista/Downloads/neha/Mangesh_Shelar.csv','r') as e: 
    
                reader = csv.reader(e)
                for row in reader:
                    count+=1
                    if row[0] : 
                        
                        partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',row[0].rsplit()[0].lstrip())])
                        if partner_id : 
                            ###assigned BM to partner
                            partner_obj.write(cr,uid,partner_id,{'user_id':bm_id})
                            
                            ###assigned to CRM#####
                            crm_id=crm_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                            if crm_id : 
                                print '******************TOTAL CRM *************',len(crm_id)
                                
                                    
                                for crm in crm_id : 
                                    user_id_onchange=crm_obj.on_change_user(cr,uid,[crm],bm_id)
                                    if user_id_onchange.get('value').get('employee_id') : 
                                        crm_obj.write(cr,uid,[crm],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                                    ,'user_id':bm_id})
                                        
                                        print '*****************CRM UPDATED******************'
                                        
                            
                            ######assigne to Sale order##########
                            sale_id=sale_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                            if sale_id : 
                                for sale in sale_id  :
                                    user_id_onchange=sale_obj.sale_onchange_user(cr, uid, [sale_id], bm_id)
                                    if user_id_onchange.get('value').get('employee_id') : 
                                        sale_obj.write(cr,uid,[sale],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                                         ,'user_id':bm_id})
    
                                        print '*****************SALE UPDATED******************'
                                    
                                    
                            #############assign invoices##########
                            inv_id=inv_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                            if inv_id : 
                                for inv in inv_id :
                                        inv_obj.write(cr,uid,[inv],{'user_id':bm_id})
                                        print '*****************INVOICE UPDATED******************'
                                        
                        else:
                            print '*****************N O !!! P A R T N E R FOUND!!!!!******************',count
                            data.append([row[0],row[1]])
                            
                            
                            
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E
            
        with open('/home/bista/Downloads/neha/logs/Mangesh_Shelar.csv','wb') as csvfile:
        #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
            spamwriter = csv.writer(csvfile, delimiter=',')  
            #import ipdb;ipdb.set_trace()     
            for write_rows in data:
                spamwriter.writerow(write_rows)  
                        
 

            
        print '-------------O V E R------------'                                                
        return True




    def migrate_salesperson_Amrita_Jadhav(self,cr,uid,vals) :
        ''' Migrate BM'''
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        sale_obj=self.pool.get('sale.order')
        inv_obj=self.pool.get('account.invoice')
        vals={}
        count=0
        bm_id=511
        rohan_gupta_id=507
        data=[]
        import ipdb;ipdb.set_trace()
        try: 
            

            partner_id=partner_obj.search(cr,uid,[('user_id','=',bm_id)])
            print '------total partner----',len(partner_id)
            for partner in partner_id : 
                count+=1;print count
                
                
                ###assigned BM to partner
                partner_obj.write(cr,uid,partner_id,{'user_id':rohan_gupta_id})
                print '*****************PArtner update******************'

        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E
            
             
        print '-------------O V E R------------'                                                
        return True



    def generate_odoo_id_employee(self,cr,uid,vals): 
        ''' genereate odoo id for employee'''
        partner_obj=self.pool.get('res.partner')
        data=[]
        count=0
        
            
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        sale_obj=self.pool.get('sale.order')
        inv_obj=self.pool.get('account.invoice')
        vals={}
        count=0
        bm_id=301
        data=[]
        
        try: 
            
            with open('/home/bista/Downloads/sandhya/Odoo Employee sheet.csv','r') as e: 
    
                reader = csv.reader(e)
                
                for row in reader:
                    count+=1;print count

                    if row[2]:
                        if row[2]=='0': 
 
                            if int(row[5])==1 :
                                
                                odoo_id=partner_obj.validate_partner(cr,uid,[int(row[0])],{})
                                print '-----------ODOO ID CREATED----------'
                                
                            
                            else : 
                                partner_obj.write(cr,uid,[int(row[0])],{'active':False})
                                print '-----------EMPLOYEE DISABLED----------'                            
                                
                        else:
                            
                            if int(row[5])==0 : 
                                partner_obj.write(cr,uid,[int(row[0])],{'active':False})
                                print '-----------EMPLOYEE DISABLED----------'

                        


        except Exception as E:
            import ipdb;ipdb.set_trace()
            print E,count
        
        print '-----------over----------'                                
        return True


    def insert_UK_country(self,cr,uid,vals): 
        ''' update country as UK in Null country'''
        partner_obj=self.pool.get('res.partner')
        data=[]
        count=0
        country_id=233 #uk
        partner_li=[]
    
        try: 
            
            with open('/home/bista/Downloads/rakesh/NULL_COUNTRY_PARTNER_SHEET.csv','r') as e: 
    
                reader = csv.reader(e)
                for row in reader:
                    count+=1;print count
                    partner_li.append(int(row[0]))
            import ipdb;ipdb.set_trace()        
            cr.execute(''' update res_partner set country_id=%s where id in %s''',(country_id,tuple(partner_li)))
            print '--------UPDATED--------------'

        except Exception as E : 
            print E,count,row
            import ipdb;ipdb.set_trace()  
                        
        print '----------------O  V   E   R--------------'
        return True
                    


    def delete_jv(self,cr,uid,vals) :
        ''' delete_jv '''
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        sale_obj=self.pool.get('sale.order')
        acc_move=self.pool.get('account.move')
        vals={}
        count=0
        import ipdb;ipdb.set_trace()
        
        try: 
            
            with open('/home/bista/Downloads/rency/jv_delete.csv','r') as e: 
    
                reader = csv.reader(e)
                for row in reader:
                    count+=1;print count
                    if row[0] : 
                        ids=acc_move.search(cr,uid,[('name','=',row[0]),('company_id','=',15)])
                        if ids : 

                                
                            if acc_move.browse(cr,uid,ids[0]).state=='draft':
                                print '--------JV in drfat state---------'
                                continue
                                
                            notify=acc_move.button_cancel(cr, uid, ids)
                            if notify : 
                                print '------------cancelled-----------'
                                acc_move.unlink(cr,uid,ids)
                            
                                print '------------DELETED-----------'
                                ###assigned to CRM#####

                            else:
                                print '*****************JV NOT CANCELLED!!!!!******************'
                        else:
                            print '*****************NO JV FOUND!!!!!******************'
                                
                        
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E
            


             
        print '-------------O V E R------------'                                                
        return True




    def LIVE_migrate_salesperson_nikunj_1(self,cr,uid,vals) :
        ''' Migrate BM'''
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        sale_obj=self.pool.get('sale.order')
        inv_obj=self.pool.get('account.invoice')
        vals={}
        count=0
        bm_id=301
        data=[]
      
        import ipdb;ipdb.set_trace()
        try: 
            
            with open('/home/bista/Downloads/LIVE/nikunj/1.csv','r') as e: 
    
                reader = csv.reader(e)
                for row in reader:
                    count+=1
                    if row[0]:
                        
                        partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',row[0].rsplit()[0].lstrip())])
                        if partner_id : 
                            ###assigned BM to partner
                            partner_obj.write(cr,uid,partner_id,{'user_id':bm_id})
                            
                            ###assigned to CRM#####
                            crm_id=crm_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                            if crm_id : 
                                print '******************TOTAL CRM *************',len(crm_id)
                                
                                    
                                for crm in crm_id : 
                                    user_id_onchange=crm_obj.on_change_user(cr,uid,[crm],bm_id)
                                    if user_id_onchange.get('value').get('employee_id') : 
                                        crm_obj.write(cr,uid,[crm],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                                    ,'user_id':bm_id})
                                        
                                        print '*****************CRM UPDATED******************'
                                        
                            
                            ######assigne to Sale order##########
                            sale_id=sale_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                            if sale_id : 
                                for sale in sale_id  :
                                    user_id_onchange=sale_obj.sale_onchange_user(cr, uid, [sale_id], bm_id)
                                    if user_id_onchange.get('value').get('employee_id') : 
                                        sale_obj.write(cr,uid,[sale],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                                         ,'user_id':bm_id})
    
                                        print '*****************SALE UPDATED******************'
                                    
                                    
                            #############assign invoices##########
                            inv_id=inv_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                            if inv_id : 
                                for inv in inv_id :
                                        inv_obj.write(cr,uid,[inv],{'user_id':bm_id})
                                        print '*****************INVOICE UPDATED******************'
                                        
                        else:
                            print '*****************N O !!! P A R T N E R FOUND!!!!!******************'
                            data.append([row[0],row[1]])
                        
                        
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E
            
        with open('/home/bista/Downloads/LIVE/nikunj/log_1.csv','wb') as csvfile:
        #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
            spamwriter = csv.writer(csvfile, delimiter=',')  
            #import ipdb;ipdb.set_trace()     
            for write_rows in data:
                spamwriter.writerow(write_rows)  
                        
             
        print '-------------O V E R------------'                                                
        return True  



    def LIVE_migrate_salesperson_keerti_Pateriya(self,cr,uid,vals) :
        ''' Migrate BM'''
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        sale_obj=self.pool.get('sale.order')
        inv_obj=self.pool.get('account.invoice')
        vals={}
        count=0
        bm_id=437
        data=[]
        #import ipdb;ipdb.set_trace()
        try: 
            
            with open('/home/bista/Downloads/keerti/keerti.csv','r') as e: 
    
                reader = csv.reader(e)
                for row in reader:
                    count+=1
                    if row[0] : 
                        #import ipdb;ipdb.set_trace()
                        partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',row[0].rsplit()[0].lstrip())])
                        if partner_id : 
                            ###assigned BM to partner
                            partner_obj.write(cr,uid,partner_id,{'user_id':bm_id})
                            
                            ###assigned to CRM#####
                            crm_id=crm_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                            if crm_id : 
                                print '******************TOTAL CRM *************',len(crm_id)
                                
                                    
                                for crm in crm_id : 
                                    user_id_onchange=crm_obj.on_change_user(cr,uid,[crm],bm_id)
                                    if user_id_onchange.get('value').get('employee_id') : 
                                        crm_obj.write(cr,uid,[crm],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                                    ,'user_id':bm_id})
                                        
                                        print '*****************CRM UPDATED******************'
                                        
                            
                            ######assigne to Sale order##########
                            sale_id=sale_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                            if sale_id : 
                                for sale in sale_id  :
                                    user_id_onchange=sale_obj.sale_onchange_user(cr, uid, [sale_id], bm_id)
                                    if user_id_onchange.get('value').get('employee_id') : 
                                        sale_obj.write(cr,uid,[sale],{'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                                         ,'user_id':bm_id})
    
                                        print '*****************SALE UPDATED******************'
                                    
                                    
                            #############assign invoices##########
                            inv_id=inv_obj.search(cr,uid,[('partner_id','=',partner_id[0])])
                            if inv_id : 
                                for inv in inv_id :
                                        inv_obj.write(cr,uid,[inv],{'user_id':bm_id})
                                        print '*****************INVOICE UPDATED******************'
                                        
                        else:
                            print '*****************N O !!! P A R T N E R FOUND!!!!!******************'
                            data.append([row[0],row[1]])
                        
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E
            
        with open('/home/bista/Downloads/keerti/logs/log_keerti.csv','wb') as csvfile:
        #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
            spamwriter = csv.writer(csvfile, delimiter=',')  
            #import ipdb;ipdb.set_trace()     
            for write_rows in data:
                spamwriter.writerow(write_rows)  
                        
             
        print '-------------O V E R------------'                                                
        return True



    def migrate_salesperson_Prateek_Jain(self,cr,uid,vals) :
        ''' Migrate BM'''
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        sale_obj=self.pool.get('sale.order')
        inv_obj=self.pool.get('account.invoice')
        vals={}
        count=0
        bm_id=449
        data=[]
        import ipdb;ipdb.set_trace()
        try: 
            
            with open('/home/bista/Downloads/neha/Prateek_Jain.csv','r') as e: 
    
                reader = csv.reader(e)
                for row in reader:
                    count+=1
                    if row[0] : 
                        
                        partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',row[0].rsplit()[0].lstrip())])
                        if partner_id : 
                            ###assigned BM to partner
                            partner_obj.write(cr,uid,partner_id,{'user_id':bm_id})
                            print '------------BM ASSIGNED-----------'
                            ###assigned to CRM#####

                        else:
                            print '*****************N O !!! P A R T N E R FOUND!!!!!******************'
                            data.append([row[0],row[1]])
                        
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E
            

        with open('/home/bista/Downloads/neha/logs/Prateek_Jain.csv','wb') as csvfile:
        #with open('/home/bista/shanky/routesms/csv_upload/sushma/partner_without_country.csv','wb') as csvfile: 
            spamwriter = csv.writer(csvfile, delimiter=',')  
            #import ipdb;ipdb.set_trace()     
            for write_rows in data:
                spamwriter.writerow(write_rows)  
                        
             
        print '-------------O V E R------------'                                                
        return True





    def remove_followers_final(self,cr,uid,vals) : 
        notification_obj=self.pool.get('mail.notification')
        count=0
        notification_ids=notification_obj.search(cr,uid,[])
        import ipdb;ipdb.set_trace()
        try : 
            
            for i in notification_ids :
                count+=1;print count
                notification_obj.unlink(cr,uid,[i],None)
                print '-----------FOLLOWER REMOVED------------'
                
                    
        except Exception as E : 
            print E,count
            import ipdb;ipdb.set_trace()
            
                
        print '*******************OVER*******************'
        return True


    def contact_person_correction(self,cr,uid,vals):
        ''' correct contact perosn BM'''
        partner_obj=self.pool.get('res.partner')
        count=0
        import ipdb;ipdb.set_trace()        
        cr.execute('''select id from res_partner where customer=True and user_id is NULL and is_company=True ''')
        partner_ids=map(lambda x:x[0],cr.fetchall())
        print '-----------total partner',partner_ids
        try : 
            
            for partner in partner_obj.browse(cr,uid,partner_ids) : 
                count+=1;print count
                
                if partner.parent_id :
                    vals={'user_id':partner.parent_id.user_id.id,'prepaid':partner.parent_id.prepaid,\
                          'postpaid':partner.parent_id.postpaid,'is_company':False}
                    partner_obj.write(cr,uid,[partner.id],vals)
                    
                    print '-----CONTACT PERSON UPDATED-----------------'

                
        except Exception as E : 
            
            print E,partner.id
            import ipdb;ipdb.set_trace()        
            
#                 with open("/home/bista/shanky/routesms/logs/LOCAL/contact_person/contact_person.txt", "a") as donefile_new:
#                     donefile_new.write()
        
        print '--------OVER------------------------------'           
        return True

    def set_partner_domain(self,cr,uid,vals):
        '''set patner domain '''
        partner_obj=self.pool.get('res.partner')
        count=0
        import ipdb;ipdb.set_trace()
        for partner in  partner_obj.browse(cr,uid,partner_obj.search(cr,uid,[])) :
            count+=1;print count 
            if partner.email : 
                
                domain=partner_obj._set_domain(cr,uid,partner.email)
                if domain : 
                    cr.execute(''' update res_partner set domain=%s where id=%s''',(domain,partner.id))
                    print '----------UPDATED------------'
        
        print '---------over------------'
        return True
        
        
    def update_crm_status_partner(self,cr,uid,vals):
        '''update crm status on partner '''
        crm_obj=self.pool.get('crm.lead')
        partner_obj=self.pool.get('res.partner')
        count=0
        cr.execute('''select partner_id from crm_lead ''')
        crm_partner_ids=map(lambda x:x[0],cr.fetchall())
        print '--------TOTAL PARTNER IDS------',len(crm_partner_ids)        
        import ipdb;ipdb.set_trace()
        data=[ x.partner_id.id for x in crm_obj.browse(cr,uid,(crm_obj.search(cr,uid,[])))  if crm_partner_ids.count(x.partner_id.id) > 1   ]
        
        ####update partner lead sttaus####
        
        for crm in crm_obj.browse(cr,uid,(crm_obj.search(cr,uid,[]))) : 
            count+=1;print count
            if crm.partner_id.id in data :
                cr.execute('''update res_partner set  crm_lead_state='DUPLICATE LEADS' where id=%s''',(crm.partner_id.id,)) 
                
                print '------skipped--------'
                
            else:
#                 if count==16153 : 
#                     import ipdb;ipdb.set_trace()
                    
                if not crm.partner_id : 
                    
                    print '------NO PARTNR ASSIGNED--------'
                else : 
                    
                    cr.execute('''update res_partner set  crm_lead_state=%s where id=%s''',(crm.stage_id.name,crm.partner_id.id))
                    print '------writed--------'
                
        #[ partner_obj.write(cr,uid,[x.partner_id.id],{'crm_lead_state':x.stage_id.name} ) for x in crm_obj.browse(cr,uid,(crm_obj.search(cr,uid,[]))) if x.partner_id.id not in data  ]
        print '------OVER--------'
        
        return True


    def qms_validate_query_integration(self,cr,uid,vals):
        '''API to integrated Odoo with QMS  to validate query before assignment '''
        uid=SUPERID
         
        try : 
            #######################1st step################
            crm_obj=self.pool.get('crm.lead')
            partner_obj=self.pool.get('res.partner')
            user_obj=self.pool.get('res.users')
            hr_obj=self.pool.get('hr.employee')
            
            ############get partner id####################
            
            
            #partner_id_for_swap=partner_obj.search(cr,uid,[('email','ilike',vals['email'])])
        #    import ipdb;ipdb.set_trace()    
            partner_id_for_swap=partner_obj.search(cr,uid,[('email','=',vals['email']),('is_company','=',True),\
                                                           ('state','=','confirm')])
            
            
            if not partner_id_for_swap :
                return '001'
            
            if len(partner_id_for_swap) > 1 : 
                return 'ERROR !!Multiple Partner Found With same Email Id'
            

            
           
            #############get BM data#############
            partner_id_for_bm=partner_obj.search(cr,uid,[('partner_sequence','=',vals['odooid'])])
            if not partner_id_for_bm :
                return 'ERROR !!No Business Manager Found'
            
            ###########validate partner BM##############


            bm_of_requested_partner=partner_obj.browse(cr,uid,partner_id_for_swap[0])
            bm_of_requested_odoo_id=user_obj.search(cr,uid,[('partner_id','=',partner_id_for_bm[0])])
            if not bm_of_requested_odoo_id : 
                return 'ERROR !!No User Found'
            
            if bm_of_requested_partner :
                if bm_of_requested_partner.user_id.id !=bm_of_requested_odoo_id[0] :
                    return 'Partner Is Assigned To {} & Odoo Id Is {} '.format(bm_of_requested_partner.user_id.name,bm_of_requested_partner.partner_sequence)
                
            else :
                    return 'No BM Assigned To Partner In Odoo'

        except Exception as E :
            return E

        return '001'

    def qms_swap_integration(self,cr,uid,vals):
        '''API to integrated Odoo with QMS SWAP QUERY '''
        uid=SUPERID
         
        try : 
            #######################1st step################
            crm_obj=self.pool.get('crm.lead')
            partner_obj=self.pool.get('res.partner')
            user_obj=self.pool.get('res.users')
            hr_obj=self.pool.get('hr.employee')
            
            ############get partner id####################
            
            #import ipdb;ipdb.set_trace() 
#            partner_id_for_swap=partner_obj.search(cr,uid,[('email','ilike',vals['email'])])
            partner_id_for_swap=partner_obj.search(cr,uid,[('email','=',vals['email']),('is_company','=',True),\
                                                           ('state','=','confirm')])
            
            if not partner_id_for_swap :
                return 'ERROR !!No Partner Found'
            
            if len(partner_id_for_swap) > 1 : 
                return 'ERROR !!Multiple Partner Found With same Email Id'
            
           
            #############get BM data#############
            partner_id_for_bm=partner_obj.search(cr,uid,[('partner_sequence','=',vals['odooid'])])
            if not partner_id_for_bm :
                return 'ERROR !!No Business Manager Found'
            
            if len(partner_id_for_bm) > 1 : 
                return 'ERROR !!Multiple Business Manager Found With same Odoo Id'
            
            bm_user_id=user_obj.search(cr,uid,[('partner_id','=',partner_id_for_bm[0])])
            
            if not bm_user_id :
                return 'ERROR !!No Business Manager User Id Found'
            
            if len(bm_user_id) > 1 : 
                return 'ERROR !!Multiple Business Manager User Id Found '
            
            ##########get Employee data###########
            
            employee_id=hr_obj.search(cr,uid,[('user_id','=',bm_user_id[0])])
            if not employee_id :
                return 'ERROR !!No Employee Id Found'
            
            if len(employee_id) > 1 : 
                return 'ERROR !!Multiple Employee Id Found '
            
            #######get CRM data#####################
            
            crm_ids=crm_obj.search(cr,uid,[('partner_id','=',partner_id_for_swap[0])])
            
            if not crm_ids :
                return 'ERROR !!No CRM Record Found'
            
            print '-----Total CRM Record----',len(crm_ids)
            try : 
                
                cr.execute(''' update crm_lead set user_id=%s ,employee_id=%s where id in %s ''',(bm_user_id[0],employee_id[0],tuple(crm_ids)))
                print '----QUERY UPADTED----'
                
                partner_obj.write(cr,uid,partner_id_for_swap,{'user_id':bm_user_id[0]})
                print '----PARTNER UPADTED----'
                
            except Exception as E : 
                return 'SQL QUERY ERROR----'
            
        except Exception as E : 
            return E
            

        print '-----------OVER-------'
        return 'QUERY SWAPPED SUCCESSFULLY'



    def qms_integration(self,cr,uid,vals):
        '''API to integrated Odoo with QMS unidirectionally '''
        uid=1 
        try : 
            
            #######################1st step################
            qms_name=[]
            qms_company=[]
            qms_email=[]
            qms_query=[]
            qms_c_date=[]
            qms_smobile=[]
            qms_clientip=[]
            qms_user_id=[]
            qms_vals_list=[]           
            qms_country=[]


            crm_obj=self.pool.get('crm.lead')
            partner_obj=self.pool.get('res.partner')
            user_obj=self.pool.get('res.users')

            request_url='http://121.241.242.108/parseqmsdata/createXml.aspx'
            response = urllib2.urlopen(request_url)
            response_from_url=response.read()
	    #import ipdb;ipdb.set_trace()            
            if response_from_url.splitlines()[0] =='0002': 
                ############################AFTER geting 002##########
                request_url_for_xml='http://121.241.242.108/parseqmsdata/data.xml'
                response_for_xml = urllib2.urlopen(request_url_for_xml)
                response_from_xml = response_for_xml.read()
                vals={}
                count=0
        
                #for i in response_from_xml.split('\r\n') :
                for k,i in enumerate(response_from_xml.splitlines()) :               
                    
                    count+=1;print count
                    
                    if '<name>' in i:
                        name=i.replace('<name>','')
                        print name
                        name2=name.replace('</name>','')
                        qms_name.append(name2.lstrip())
                        #vals.update({'name':qms_name})

                    elif '<Country>' in i:
                        
                        name=i.replace('<Country>','')
                        print name
                        name2=name.replace('</Country>','')
                        qms_country.append(name2.lstrip())  

                        
                    elif '<company>' in i:
                        name=i.replace('<company>','')
                        print name
                        name2=name.replace('</company>','')
                        qms_company.append(name2.lstrip())
                        #vals.update({'company':qms_company})    
                    
                    
                    elif '<email>' in i:
                        name=i.replace('<email>','')
                        print name
                        name2=name.replace('</email>','')
                        qms_email.append(name2.lstrip())
                        #vals.update({'email':qms_email})    
                    

                    elif '<query>' in i:
                       
                        qms_query_response=response_from_xml.splitlines()
                        start_query=qms_query_response[k]
                        start_query_count=k
                         
                        if '</query>' in i :
                            
                            
                            name=i.replace('<query>','')
                            print name
                            
                            name2=name.replace('</query>','')
                            qms_query.append(name2.lstrip())
                        
                        else:
                        
                            for index,end_index_val in enumerate(qms_query_response[k:]) : 
                                if '</query>' in end_index_val :
                                    
                                    end_query=index
                                    break
                            #        end_query-=1
                                    
                            query_val=','.join(qms_query_response[k:][:end_query]).replace('</query>','').replace('<query>','').lstrip()
                            qms_query.append(query_val)


                    
                    
#                     elif '<query>' in i:
#                         
#                         name=i.replace('<query>','')
#                         print name
#                         
#                         name2=name.replace('</query>','')
#                         qms_query.append(name2.lstrip())                        

                    
#                     elif '<query>' in i:
#                          
#                         qms_query_response=response_from_xml.split('\r\n')
#                         start_query=qms_query_response.index(i)
#                         
#                             
#                         if '</query>' in i :
#                             
#                             
#                             name=i.replace('<query>','')
#                             print name
#                             
#                             name2=name.replace('</query>','')
#                             qms_query.append(name2.lstrip())
#                         
#                         else:
#                         
#                             for end_index_val in qms_query_response : 
#                                 if '<c_date>' in end_index_val :
#                                     end_query=qms_query_response.index(end_index_val)
#                                     #end_query-=1
#                                     
#                                     query_val=','.join(qms_query_response[start_query:end_query]).replace('</query>','').replace('<query>','').lstrip()
#                             qms_query.append(query_val)
                            
                       # vals.update({'query':qms_query})    
                            
                    elif '<c_date>' in i:
                        name=i.replace('<c_date>','')
                        print name
                        name2=name.replace('</c_date>','')
                        qms_c_date.append(name2.lstrip())
                      #  vals.update({'date_open':qms_c_date})    
                            
                    elif '<smobile>' in i:
                        name=i.replace('<smobile>','')
                        print name
                        name2=name.replace('</smobile>','')
                        qms_smobile.append(name2.lstrip())
                     #   vals.update({'smobile':qms_smobile})    
                            
                    elif '<ClientIP>' in i:
                        name=i.replace('<ClientIP>','')
                        print name
                        name2=name.replace('</ClientIP>','')
                        qms_clientip.append(name2.lstrip())
                    #    vals.update({'client_ip':qms_clientip})   
                    
                    elif '<OdooId>' in i : 
                        name=i.replace('<OdooId>','')
                        print name
                        name2=name.replace('</OdooId>','')
                        qms_user_id.append(name2.lstrip().rstrip())     


                        
               
                vals.update({'name':qms_name,'company':qms_company,'email':qms_email,\
                    'query':qms_query,'date_open':qms_c_date\
                    ,'smobile':qms_smobile,'client_ip':qms_clientip,'user_id':qms_user_id,'country_id':qms_country})
                
                print vals
		#import ipdb;ipdb.set_trace()
                for i in range(len(vals['email'])) :
		    
                    user_partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',vals['user_id'][i])])
                    if user_partner_id : 
                        user_id=user_obj.search(cr,uid,[('partner_id','=',user_partner_id[0])])
                        if user_id : 
                            crm_user_id=user_id[0]
                        
                        else : 
                            crm_user_id=1
                            
                    else:
                        crm_user_id=1
                        
                        
                            
                    qms_vals_list.append({'name':vals['name'][i],'company':vals['company'][i],\
                                          'email':vals['email'][i],'query':vals['query'][i],\
                                          'date_open':vals['date_open'][i],'smobile':vals['smobile'][i],\
                                          'client_ip':vals['client_ip'][i],'user_id':crm_user_id,'country_id':vals['country_id'][i]})
                 
               
                for vals in qms_vals_list : 
                    
        	    #import ipdb;ipdb.set_trace()                
                    if vals : 
                        cr.execute(''' select id from res_partner where email=%s''',(vals['email'],))
                        partner_id=map(lambda x:x,cr.fetchall())
                        # CHECK FROM SECONDARY EMAIL
                        if not partner_id : 
                            cr.execute(''' select partner_id from res_partner_contact_line where email=%s''',(vals['email'],))
                            partner_id=map(lambda x:x,cr.fetchall())
                        
                        if partner_id :
                            ###############partner already exist########### 
                            print '----------PARTNER ALREADY EXIST---'
    
    
                            
                            crm_vals={'partner_id':partner_id[0],'name':vals['query'],'description':vals['query'],\
                                      'user_id':1,'employee_id':1,'date_open':vals['date_open'],\
                                      'qms_crm':True,'client_ip':vals['client_ip']}
                            
                            onchange_vals=crm_obj.on_change_partner_id(cr, uid, [], partner_id[0], context=None)
                            
                            if onchange_vals.has_key('value') : 
                                crm_vals.update(onchange_vals['value'])
                            
                            if crm_vals.has_key('date_open') :
                                
                                date=map(lambda x:int(x),crm_vals['date_open'].split('T')[0].split('-')) 
                                ctime=map(lambda x:int(x),crm_vals['date_open'].split('T')[-1].split('+')[0].split(':'))
                               #reduce 5hrz 30min as per UNIX UTC
                                dtime=datetime.datetime(date[0],date[1],date[2],ctime[0],ctime[1],ctime[2]) - datetime.timedelta(hours=5,minutes=30)
                                time_int_conversion = time.mktime(dtime.timetuple())
                               #convert accoridng to Odoo format
                                crm_lead_time=datetime.datetime.fromtimestamp(time_int_conversion).strftime('%Y-%m-%d %H:%M:%S')
                               #update time in doctionary
                                crm_vals['date_open']=crm_lead_time

                            user_id_onchange=crm_obj.on_change_user(cr,uid,[],vals['user_id'])
                            if user_id_onchange.get('value').get('employee_id') : 
                                crm_vals.update({'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                                ,'user_id':vals['user_id']})                                
                	    #import ipdb;ipdb.set_trace()               
                            new_crm_id= crm_obj.create(cr,uid,crm_vals)
                            print '--------------LEAD CREATED---------------'
                            crm_log_values=crm_obj.browse(cr,uid,new_crm_id)
                            with open("/home/routesms/logs/qms/qms_logs.txt", "a") as donefile_new:
                                donefile_new.write(str(crm_log_values.partner_id.name)+'{}'+str(crm_log_values.client_ip) + '{}' +datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '{}'\
                                                   'LEAD:' + str(new_crm_id) +'\n')   			  

        
                        else : 
                            ##############partner doesnt exist , create new###################
                            print '----------CREATING NEW PARTNER------------'
                            cr.execute('''select id from res_country where name like %s ''',('%'+vals['country_id']+'%',))
                            country=map(lambda x:x[0],cr.fetchall())
                            if country : 
                                country_id=country[0]
                            else : 
                                country_id=False


                            print vals
                            partner_vals={'comment': False, 'user_id':vals['user_id'],'function': False, 'property_account_position': False,\
                                          'notify_email': 'none', 'message_follower_ids': False, 'company_registery': False,\
                                          'image': False, 'property_stock_supplier': 8, 'use_parent_address': False, 'active': True, \
                                          'street': False, 'property_stock_customer': 9, 'payment_next_action_date': False, 'tan': False,\
                                           'property_product_pricelist': False, 'message_ids': False, 'city': False, 'opt_out': False,\
                                            'zip': False, 'title': False, 'property_account_receivable': 1225, 'country_id': country_id, 'company_id': 1, \
                                            'property_account_payable': 1117, 'parent_id': False, 'last_reconciliation_date': False, 'pan': False,\
                                            'supplier': False, 'routesms_cust_id': False, 'street2': False, 'is_company': True, 'website': False,\
                                            'lang': 'en_US', 'fax': False, 'bank_ids': [], 'vertical': 1, 'routesms_remark': 'PARTNER CREATED FROM QMS', 'child_ids': [],\
                                            'section_id': False, 'partner_type': False, 'credit_limit': 0, \
                                            'property_supplier_payment_term': False, 'signatory': False, 'date': False, 'unreconciled_aml_ids': [],\
                                            'vat_subjected': False, 'payment_responsible_id': False, 'customer': True, 'ref': False, 'name': vals['company'],\
                                            'property_product_pricelist_purchase': 2, 'phone': vals['smobile'], 'mobile':False , 'type': 'contact', 'cin': False,\
                                            'email': vals['email'], 'postpaid': False, 'payment_next_action': False, 'vat': False,\
                                            'property_payment_term': False, 'state_id': False, 'category_id': [[6, False, []]], 'prepaid': True, \
                                            'payment_note': False}
			    #import ipdb;ipdb.set_trace()
       
                            new_partner_id=partner_obj.create(cr,uid,partner_vals)
                            #add odoo od
                            
                            odoo_id=partner_obj.validate_partner(cr,uid,[new_partner_id],{})
                            
                            if not odoo_id :
                                print '--------------ODOO ID CREATION FAILED----------'
                    
                                with open("/home/routesms/logs/qms/qms_logs.txt", "a") as donefile_new:
                                    donefile_new.write(str(new_partner_id)+'{}'+ time.strftime("%H:%M:%S") +'\n')                                
                                return False 
                                
                            if new_partner_id : 
                                    crm_vals={'partner_id':new_partner_id,'name':vals['query'],'description':vals['query'],\
                                              'user_id':1,'employee_id':1,'date_open':vals['date_open'],\
                                              'qms_crm':True,'client_ip':vals['client_ip']}
                                    
                                    onchange_vals=crm_obj.on_change_partner_id(cr, uid, [], new_partner_id, context=None)
                                    
                                    if onchange_vals.has_key('value') : 
                                        crm_vals.update(onchange_vals['value'])
                                    if crm_vals.has_key('date_open') : 
                                        date=map(lambda x:int(x),crm_vals['date_open'].split('T')[0].split('-')) 
                                        ctime=map(lambda x:int(x),crm_vals['date_open'].split('T')[-1].split('+')[0].split(':'))
                                       #reduce 5hrz 30min as per UNIX UTC
                                        dtime=datetime.datetime(date[0],date[1],date[2],ctime[0],ctime[1],ctime[2]) - datetime.timedelta(hours=5,minutes=30)
                                        time_int_conversion = time.mktime(dtime.timetuple())
                                        #convert accoridng to Odoo format
                                        crm_lead_time=datetime.datetime.fromtimestamp(time_int_conversion).strftime('%Y-%m-%d %H:%M:%S')
                                        #update time in doctionary
                                        crm_vals['date_open']=crm_lead_time
                                    
                                    
                                    if onchange_vals.has_key('value') : 
                                        crm_vals.update(onchange_vals['value'])      
                                    ####isnert bm ###
                                    user_id_onchange=crm_obj.on_change_user(cr,uid,[],vals['user_id'])
                                    if user_id_onchange.get('value').get('employee_id') : 

                                        crm_vals.update({'employee_id':user_id_onchange.get('value').get('employee_id')\
                                                                        ,'user_id':vals['user_id']})
                              
                                    new_crm_id=crm_obj.create(cr,uid,crm_vals)
                                    print '--------------LEAD CREATED---------------' 
				    crm_log_values=crm_obj.browse(cr,uid,new_crm_id)
                                    with open("/home/routesms/logs/qms/qms_logs.txt", "a") as donefile_new:
                                        donefile_new.write(str(crm_log_values.partner_id.name)+'{}'+str(crm_log_values.client_ip) + '{}' +datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '{}'\
                                                           'LEAD:' + str(new_crm_id) +'\n')                                                                
                        
                ###########################update status####################    
                request_update_status_url='http://121.241.242.108/parseqmsdata/createXml.aspx?update=yes'
                response_for_update_status = urllib2.urlopen(request_update_status_url)
                response_from_update_url=response_for_update_status.read()
                if response_from_update_url.splitlines()[0] =='0001': 
                    print '--------STATUS UPDATED-----------'
                else :
                    print '--------STATUS NOT UPDATED-----------'
        
                
                
            elif response_from_url.splitlines()[0] =='0000':
                        print '------NO LEAD FOUND-----'
            else : 
                    
                print 'incorrect response'
                with open("/home/routesms/logs/qms/qms_logs.txt", "a") as donefile_new:
                    donefile_new.write('incorrect response'+'{}'+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +'\n')                                
                
                return False
        
            print '--------------EXITING SCRIPT-------------'        
            return True
        except Exception as E : 
	    #import ipdb;ipdb.set_trace()
            print 'CRM cannot be created'
            with open("/home/routesms/logs/qms/qms_logs.txt", "a") as donefile_new:
                donefile_new.write('CRM cannot be created'+'{}'+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '{}' + str(E) + '\n')               
            
            return False
        return True


    @api.cr_uid
    def qms_scheduler(self, cr, uid, ids=None, context=None):
	uid=1
        """scheduler for  QMS.
        """
	print '-----------------------------QMS SCHEDULER STARTED--------------------------------'        
       # import ipdb;ipdb.set_trace()
        if context is None:
            context = {}
        res=None
        try:
            # Force auto-commit - this is meant to be called by
            # the scheduler, and we can't allow rolling back the status
            # of previously sent emails!
            res = self.qms_integration(cr, uid, [])
        except Exception:
            print '-------------QMS SCHEDULER FAILED----------'
        return res



    def insert_crm_from_csv1(self,cr,uid,vals):
        '''parse excel sheet to import partner and then create crm '''
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        user_obj=self.pool.get('res.users')
        hr_obj=self.pool.get('hr.employee')
        crm_opp_obj=self.pool.get('crm.lead2opportunity.partner')
        count=0
      #  import ipdb;ipdb.set_trace()
        try : 
            #with open('/home/bista/shanky/routesms/csv_upload/sushma/CRM/lead_crm.csv','r') as e: 
            with open('/home/bista/Downloads/sushma/final.csv','r') as e:
            
                reader = csv.reader(e)
                
                for row in reader:
                    count+=1;print count
#                     if count==100:
#                         return True
#                     if count<744 : 
#                          continue
#                     else:
# #                          import ipdb;ipdb.set_trace()
#                           pass
                    ####check contact person######


                    if count<744 : 
                         continue

                    if not row[0] :
                        #with open("/home/bista/shanky/routesms/logs/CRM/lead.txt", "a") as donefile_new:
                        with open("/home/bista/Downloads/sushma/logs/lead.txt", "a") as donefile_new:
                            donefile_new.write(str(row[1])+'{}'+'contact person missing' + ' {}'+'count:'+ str(count)+'\n')
                        continue   
                        
                    #check email
                    if row[2] : 
                        cr.execute(''' select id from res_partner where email=%s''',(row[2].lstrip().rstrip(),))
                        partner_id=map(lambda x:x,cr.fetchall())
#                         if count==17:
#                             import ipdb;ipdb.set_trace()   
                        if partner_id :
                            ###############partner already exist########### 
                            print '----------PARTNER ALREADY EXIST ############ACTON DENIED###########---'
                            print '----------partner_id----{}'.format(partner_id)
                            #with open("/home/bista/shanky/routesms/logs/CRM/lead.txt", "a") as donefile_new:
                            with open("/home/bista/Downloads/sushma/logs/lead.txt", "a") as donefile_new:
                                donefile_new.write(str(row[1])+ '{}'+ 'note:'+'Email Id already exist' +'{}'+'count:'+ str(count)+'\n')   
                            continue
                            
                        else :
                            #import ipdb;ipdb.set_trace() 
                            ################proceed futher##############
                            business_manager_id=user_obj.search(cr,uid,[('name','=',row[5])])
                            if row[5]=='Rohan' : 
                                business_manager_id=[507]
                            if business_manager_id :
                                if len(business_manager_id) > 1 :
                                    print 'Dublicate BM name'
                                    #with open("/home/bista/shanky/routesms/logs/CRM/lead.txt", "a") as donefile_new:
                                    with open("/home/bista/Downloads/sushma/logs/lead.txt", "a") as donefile_new:
                                        donefile_new.write(str(row[1])+ '{}'+ 'note:'+'Dublicate BM name' + '{}'+'count:'+ str(count)+'\n')
                                    
                                     
                                     
                                business_manager=business_manager_id[0]
                            else :
                                print  'No bm found'
                                #with open("/home/bista/shanky/routesms/logs/CRM/lead.txt", "a") as donefile_new:
                                with open("/home/bista/Downloads/sushma/logs/lead.txt", "a") as donefile_new:
                                    donefile_new.write(str(row[1])+ '{}'+ 'note:'+'No BM name' + '{}'+'count:'+ str(count)+'\n')
                                business_manager=508                                 
                                
                            ##prepare customer data#########
                            partner_vals={}
                            partner_vals={'comment': False, 'user_id':business_manager,'function': False, 'property_account_position': False,\
                                          'notify_email': 'none', 'message_follower_ids': False, 'company_registery': False,\
                                          'image': False, 'property_stock_supplier': 8, 'use_parent_address': False, 'active': True, \
                                          'street': row[4], 'property_stock_customer': 9, 'payment_next_action_date': False, 'tan': False,\
                                           'property_product_pricelist': False, 'message_ids': False, 'city': False, 'opt_out': False,\
                                            'zip': False, 'title': False, 'property_account_receivable': 1225, 'country_id': 105, 'company_id': 1, \
                                            'property_account_payable': 1117, 'parent_id': False, 'last_reconciliation_date': False, 'pan': False,\
                                            'supplier': False, 'routesms_cust_id': False, 'street2': False, 'is_company': True, 'website': False,\
                                            'lang': 'en_US', 'fax': False, 'bank_ids': [], 'vertical': 1, 'routesms_remark': 'PARTNER IMPORTED VIA SHEET-OPPORTUNITY ONLY-2', 'child_ids': [],\
                                            'section_id': False, 'partner_type': False, 'credit_limit': 0, \
                                            'property_supplier_payment_term': False, 'signatory': False, 'date': False, 'unreconciled_aml_ids': [],\
                                            'vat_subjected': False, 'payment_responsible_id': False, 'customer': True, 'ref': False, 'name': row[1],\
                                            'property_product_pricelist_purchase': 2, 'phone': row[3], 'mobile':False , 'type': 'contact', 'cin': False,\
                                            'email': row[2].lstrip().rstrip(), 'postpaid': False, 'payment_next_action': False, 'vat': False,\
                                            'property_payment_term': False, 'state_id': False, 'category_id': [[6, False, []]], 'prepaid': True, \
                                            'payment_note': False}
                                                    
                            new_partner_id=partner_obj.create(cr,uid,partner_vals)
                                #add odoo od
                                
                            odoo_id=partner_obj.validate_partner(cr,uid,[new_partner_id],{})
#                             if count==5: 
#                                                              
                            if not odoo_id :
                                print '--------------ODOO ID CREATION FAILED----------'
                                #with open("/home/bista/shanky/routesms/logs/CRM/lead.txt", "a") as donefile_new:
                                with open("/home/bista/Downloads/sushma/logs/lead.txt", "a") as donefile_new:
                                    donefile_new.write(str(row[1])+ '{}'+ 'note:'+'Odoo id failed' + '{}'+'count:'+ str(count)+'\n')   
                                
                                                     
                        
                            #create contact perosn
                            vals_client={}
                            vals_client['name']=row[0]
                            vals_client['parent_id']=new_partner_id
                            vals_client['use_parent_address']=True
                            partner_obj.create(cr,uid,vals_client)                    
    
                            ##############create crm#############
                            
                            employee_id =hr_obj.search(cr,uid,[('user_id','=',business_manager)])
                            if employee_id : 
                                if len(employee_id) > 1:
                                    print 'Dublicate employe'
                                    with open("/home/bista/shanky/routesms/logs/CRM/lead.txt", "a") as donefile_new:
                                        donefile_new.write(str(row[1])+ '{}'+ 'note:'+'Dublicate employe' + '{}'+'count:'+ str(count)+'\n')   
                                    
                                    
                                
                            else : 
                                
                                employee_id=[235]
                                print 'No employee found '
                                with open("/home/bista/shanky/routesms/logs/CRM/lead.txt", "a") as donefile_new:
                                    donefile_new.write(+str(row[1])+ '{}'+ 'note:'+'No employee found' + '{}'+'count:'+ str(count)+'\n')   
                                
    
                                
                                    
                            crm_vals={'partner_id':new_partner_id,'name':'Messaging Enterprise','description':'Messaging Enterprise',\
                                          'user_id':business_manager,'employee_id':employee_id[0],\
                                          'qms_crm':False,'odoo_script_new_partner_opportunity':True,}
                                
                            onchange_vals=crm_obj.on_change_partner_id(cr, uid, [], new_partner_id, context=None)
                            crm_vals.update(onchange_vals['value'])                            
                                   
                            crm_id=crm_obj.create(cr,uid,crm_vals)
                            print '--------------LEAD CREATED---------------'
                            ##################create wizard id################################
                            cr.execute(''' insert into crm_lead2opportunity_partner(name,action,user_id,partner_id) VALUES('convert','exist',%s,%s)''',(business_manager,new_partner_id))
                            
                            cr.execute(''' select id from crm_lead2opportunity_partner where partner_id=%s''',(new_partner_id,))
                            wizard_id=map(lambda x:x[0],cr.fetchall())
                            if wizard_id :
                                
                 ###############convert to opportuntity###############
                                opp_context={'lang': 'en_US', 'tz': 'Asia/Calcutta', 'uid': business_manager, 'active_model': 'crm.lead', 'empty_list_help_model': 'crm.case.section', \
                                             'stage_type': 'lead', 'search_disable_custom_filters': True, \
                                             'needaction_menu_ref': 'crm.menu_crm_opportunities', 'active_ids': [crm_id], 'active_id': crm_id}
                                
                                crm_opp_obj.action_apply(cr, uid, [wizard_id[0]],opp_context)
                                
                                cr.execute('''update crm_lead set stage_id=9 where id=%s ''',(crm_id,))
                                print '-----------converted to opportunity------------'
                                                                
                            else : 
                                print 'No wizard id found'
                                with open("/home/bista/shanky/routesms/logs/crm_no_wizard.txt", "a") as donefile_new:
                                    donefile_new.write(str(crm_id)+'\n')
                                     
            
                                               
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E,count
        
        print '---------------O V  E   R ------------'
        return True







    def insert_crm_from_csv(self,cr,uid,vals):
        '''parse excel sheet to import partner and then create crm '''
        partner_obj=self.pool.get('res.partner')
        crm_obj=self.pool.get('crm.lead')
        user_obj=self.pool.get('res.users')
        hr_obj=self.pool.get('hr.employee')
        count=0
        try : 
            #with open('/home/bista/shanky/routesms/csv_upload/sushma/CRM/draft_crm.csv','r') as e:
            with open('/home/routesms/csv_file/sushma/draft_crm.csv','r') as e:
            
                reader = csv.reader(e)
                import ipdb;ipdb.set_trace() 
                for row in reader:
                    count+=1;print count
 #                   if count<4 : 
#                        continue

                   
                        
                    ####check contact person######
                    
                    if not row[0] : 
                        #with open("/home/bista/shanky/routesms/logs/CRM/lead.txt", "a") as donefile_new:
                        #with open("/home/bista/shanky/routesms/logs/CRM/lead.txt", "a") as donefile_new:
                        with open("/home/routesms/logs/lead.txt", "a") as donefile_new:
                            donefile_new.write('partner_name:'+str(row[1])+ '  '+ 'note:'+'contact person missing' + '  '+'count:'+ str(count)+'\n')
                            
                        continue   
                        
                    #check email
                    if row[2] : 
                        cr.execute(''' select id from res_partner where email=%s''',(row[2],))
                        partner_id=map(lambda x:x,cr.fetchall())
                            
                        if partner_id :
                            ###############partner already exist########### 
                            print '----------PARTNER ALREADY EXIST ############ACTON DENIED###########---'
                            #with open("/home/bista/shanky/routesms/logs/CRM/lead.txt", "a") as donefile_new:
                            with open("/home/routesms/logs/lead.txt", "a") as donefile_new:
                                donefile_new.write('partner_name:'+str(row[1])+ '  '+ 'note:'+'Email Id already exist' + '  '+'count:'+ str(count)+'\n')   
                            continue
                            
                        else : 
                            ################proceed futher##############
                            business_manager_id=user_obj.search(cr,uid,[('name','=',row[5])])
                            if row[5]=='Rohan' : 
                                business_manager_id=[507]
                            if business_manager_id :
                                if len(business_manager_id) > 1 :
                                    print 'Dublicate BM name'
                                    #with open("/home/bista/shanky/routesms/logs/CRM/lead.txt", "a") as donefile_new:
                                    with open("/home/routesms/logs/lead.txt", "a") as donefile_new:
                                        donefile_new.write('partner_name:'+str(row[1])+ '  '+ 'note:'+'Dublicate BM name' + '  '+'count:'+ str(count)+'\n')
                                business_manager=business_manager_id[0]
                            else : 
                                
                                     
                                business_manager=508
                            ##prepare customer data#########
                            partner_vals={}
                            partner_vals={'comment': False, 'user_id':business_manager,'function': False, 'property_account_position': False,\
                                          'notify_email': 'none', 'message_follower_ids': False, 'company_registery': False,\
                                          'image': False, 'property_stock_supplier': 8, 'use_parent_address': False, 'active': True, \
                                          'street': False, 'property_stock_customer': 9, 'payment_next_action_date': False, 'tan': False,\
                                           'property_product_pricelist': False, 'message_ids': False, 'city': False,'opt_out': False,\
                                            'zip': False, 'title': False, 'property_account_receivable': 1225, 'country_id': False, 'company_id': 1, \
                                            'property_account_payable': 1117, 'parent_id': False, 'last_reconciliation_date': False, 'pan': False,\
                                            'supplier': False, 'routesms_cust_id': False, 'street2': False, 'is_company': True, 'website': False,\
                                            'lang': 'en_US', 'fax': False, 'bank_ids': [], 'vertical': 1, 'routesms_remark': 'PARTNER IMPORTED VIA SHEET-LEAD ONLY', 'child_ids': [],\
                                            'section_id': False, 'partner_type': False, 'credit_limit': 0, \
                                            'property_supplier_payment_term': False, 'signatory': False, 'date': False, 'unreconciled_aml_ids': [],\
                                            'vat_subjected': False, 'payment_responsible_id': False, 'customer': True, 'ref': False, 'name': row[1],\
                                            'property_product_pricelist_purchase': 2, 'phone': row[3], 'mobile':False , 'type': 'contact', 'cin': False,\
                                            'email': row[2], 'postpaid': False, 'payment_next_action': False, 'vat': False,\
                                            'property_payment_term': False, 'state_id': False, 'category_id': [[6, False, []]], 'prepaid': True, \
                                            'payment_note': False}
                                                    
                            new_partner_id=partner_obj.create(cr,uid,partner_vals)
                                #add odoo od
                                
                            odoo_id=partner_obj.validate_partner(cr,uid,[new_partner_id],{})
#                             if count==5: 
#                                 import ipdb;ipdb.set_trace()                                
                            if not odoo_id :
                                print '--------------ODOO ID CREATION FAILED----------'
                                #with open("/home/bista/shanky/routesms/logs/CRM/lead.txt", "a") as donefile_new:
                                with open("/home/routesms/logs/lead.txt", "a") as donefile_new:
                                    donefile_new.write('partner_name:'+str(row[1])+ '  '+ 'note:'+'Odoo id failed' + '  '+'count:'+ str(count)+'\n')   
                                
                                                     
                        
                            #create contact perosn
                            vals_client={}
                            vals_client['name']=row[0]
                            vals_client['parent_id']=new_partner_id
                            vals_client['use_parent_address']=True
                            partner_obj.create(cr,uid,vals_client)                    
    
                            ##############create crm#############
                            employee_id =hr_obj.search(cr,uid,[('user_id','=',business_manager)])
                            if employee_id : 
                                if len(employee_id) > 1:
                                    print 'Dublicate employe'
                                    #with open("/home/bista/shanky/routesms/logs/CRM/lead.txt", "a") as donefile_new:
                                    with open("/home/routesms/logs/lead.txt", "a") as donefile_new:
                                        donefile_new.write('partner_name:'+str(row[1])+ '  '+ 'note:'+'Dublicate employe' + '  '+'count:'+ str(count)+'\n')   
                                    
                                    
                                
                            else : 
                                employee_id=[235]
                                print 'No employee found '
                                #with open("/home/bista/shanky/routesms/logs/CRM/lead.txt", "a") as donefile_new:
                                with open("/home/routesms/logs/lead.txt", "a") as donefile_new:
                                    donefile_new.write('partner_name:'+str(row[1])+ '  '+ 'note:'+'No employee found' + '  '+'count:'+ str(count)+'\n')   
                                
    
                                
                                    
                            crm_vals={'partner_id':new_partner_id,'name':'Messaging Enterprise','description':'Messaging Enterprise',\
                                          'user_id':business_manager,'employee_id':employee_id[0],\
                                          'qms_crm':False,'odoo_script_new_partner_lead':True}
                                
                            onchange_vals=crm_obj.on_change_partner_id(cr, uid, [], new_partner_id, context=None)
                            crm_vals.update(onchange_vals['value'])                            
                                   
                            crm_obj.create(cr,uid,crm_vals)
                            print '--------------LEAD CREATED---------------'
                    else : 
                        
                            #with open("/home/bista/shanky/routesms/logs/CRM/lead.txt", "a") as donefile_new:
                            with open("/home/routesms/logs/lead.txt", "a") as donefile_new:
                                donefile_new.write('partner_name:'+str(row[1])+ '  '+ 'note:'+'Email Id Empty' + '  '+'count:'+ str(count)+'\n')   
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E,count
        
        print '---------------O V  E   R ------------'




    def find_incorrect_partner_list(self,cr,uid,vals):    
        ''' Wrong partner/to be corrected'''
        count=0
        data=[]
        partner_obj=self.pool.get('res.partner')
        cr.execute(''' select id from res_partner where supplier=True ''')
        
        cust_inv_ids=map(lambda x:x[0],cr.fetchall())
        print '----------------total partner---------------',len(cust_inv_ids)
        import ipdb;ipdb.set_trace()
        for partner in partner_obj.browse(cr,uid,cust_inv_ids)  :
            count+=1;print count 
            partner_id=''
            vals={}
            if not partner.user_id : 
                partner_id=str(partner.id)
                vals['user_id']=507
            
            
            if partner.postpaid and partner.prepaid :
                partner_id=str(partner.id)
                vals.update({'prepaid':False,'postpaid':True})
                
            if not partner.postpaid and not partner.prepaid :
                partner_id=str(partner.id) 
                vals.update({'prepaid':False,'postpaid':True})
                
            if partner_id :
                    partner_obj.write(cr,uid,[partner.id],vals)
                    print '-------------CORECTION MADE-----------------'


            
        print '--------------------GAME OVER --------------------'        
        return True    



    def create_existing_customer_crm_leadonly(self,cr,uid,vals):
        
        '''create crm at draft state for exisitng customer '''
        crm_obj=self.pool.get('crm.lead')
        crm_opp_obj=self.pool.get('crm.lead2opportunity.partner')
        partner_obj=self.pool.get('res.partner')
        hr_obj=self.pool.get('hr.employee')
        count=0
        cr.execute(''' select id from res_partner where customer=True and is_company=True and state='draft' ''')
        cust_inv_ids=map(lambda x:x[0],cr.fetchall())
        print '----------------total partner---------------',len(cust_inv_ids)
	import ipdb;ipdb.set_trace()
        try :
           # import ipdb;ipdb.set_trace()      
            for partner in partner_obj.browse(cr,uid,cust_inv_ids) :
            #for partner in partner_obj.browse(cr,uid,[497]) :
                count+=1;print count 
                hr_ids=hr_obj.search(cr,uid,[('user_id','=',partner.user_id.id)])
                if hr_ids : 
                    if len (hr_ids) >1 : 
                        print 'DUBLICATE USER'
                    #    import ipdb;ipdb.set_trace()
#                         with open("/home/bista/shanky/routesms/logs/crm_logs.txt", "a") as donefile_new:
                        with open("/home/routesms/logs/crm_logs.txt", "a") as donefile_new:
                            donefile_new.write(str(partner.id)+'{}'+'Duplicate user' +'\n')                           
                    hr_id=hr_ids[0]
                
                else : 
                    hr_id=1
                    print 'NO EMPLOYEE FOUND'
                    #with open("/home/bista/shanky/routesms/logs/crm_logs.txt", "a") as donefile_new:
                    with open("/home/routesms/logs/crm_logs.txt", "a") as donefile_new:
                        donefile_new.write(str(partner.id)+'{}'+'employee not found' +'\n')
                        
                if not partner.user_id.id :
                   # import ipdb;ipdb.set_trace()
                   bm=507
                   #with open("/home/bista/shanky/routesms/logs/crm_logs.txt", "a") as donefile_new:
                   with open("/home/routesms/logs/crm_logs.txt", "a") as donefile_new:
                       donefile_new.write(str(partner.id)+'{}'+'user not found' +'\n')
                     
                else :
                    bm=partner.user_id.id                    
                    
                crm_vals={'partner_id':partner.id,'name':'Messaging Enterprise','description':'Messaging Enterprise',\
                          'user_id':bm,'employee_id':hr_id,'date_open':partner.create_date,\
                          'qms_crm':False,'odoo_script_lead':True}
                
                onchange_vals=crm_obj.on_change_partner_id(cr, uid, [],partner.id, context=None)
                crm_vals.update(onchange_vals['value'])   
                crm_id=crm_obj.create(cr,uid,crm_vals)
                print '--------------LEAD CREATED---------------'
                ##################create wizard id################################
        except Exception as E : 
            print '----------ERROR--------',count
            #with open("/home/bista/shanky/routesms/logs/crmerror.txt", "a") as donefile_new:
            with open("/home/routesms/logs/crmerror.txt", "a") as donefile_new:
                import ipdb;ipdb.set_trace()
                donefile_new.write(str(partner.id)+'\n')                 
            
        print '---------------OVER-------------------'
        return True
    

    def create_existing_customer_crm(self,cr,uid,vals):


        
        '''create crm for exisitng customer '''
        crm_obj=self.pool.get('crm.lead')
        crm_opp_obj=self.pool.get('crm.lead2opportunity.partner')
        partner_obj=self.pool.get('res.partner')
        hr_obj=self.pool.get('hr.employee')
        count=0
        cr.execute(''' select id from res_partner where customer=True and is_company=True and state='confirm' ''')
        cust_inv_ids=map(lambda x:x[0],cr.fetchall())
        print '----------------total partner---------------',len(cust_inv_ids)
        import ipdb;ipdb.set_trace()
        try :
         #   import ipdb;ipdb.set_trace()      
            for partner in partner_obj.browse(cr,uid,cust_inv_ids) :
            #for partner in partner_obj.browse(cr,uid,[497]) :
                count+=1;print count 
#                if count<11857 : 
#                    continue
#                else :
 #                   pass
                hr_ids=hr_obj.search(cr,uid,[('user_id','=',partner.user_id.id)])
                if hr_ids : 
                    if len (hr_ids) >1 : 
                        print 'DUBLICATE USER'
          #              import ipdb;ipdb.set_trace()
                        #with open("/home/bista/shanky/routesms/logs/converted_crm_logs.txt", "a") as donefile_new:
                        with open("/home/routesms/logs/converted_crm_logs.txt", "a") as donefile_new:
                            donefile_new.write(str(partner.id)+'{}'+'dublicate' +'\n')
                           
                    hr_id=hr_ids[0]
                
                else : 
                    hr_id=1
                    print 'NO EMPLOYEE FOUND'
                    with open("/home/bista/shanky/routesms/logs/converted_crm_logs.txt", "a") as donefile_new:
                        donefile_new.write(str(partner.id)+'{}'+'employee not found' +'\n')

                if not partner.user_id.id :
           #         import ipdb;ipdb.set_trace()
                    #with open("/home/bista/shanky/routesms/logs/converted_crm_logs.txt", "a") as donefile_new:
                    with open("/home/routesms/logs/converted_crm_logs.txt", "a") as donefile_new:
                        donefile_new.write(str(partner.id)+'{}'+'user not found' +'\n')
                    bm=507
                    
                else  :
                    bm=partner.user_id.id
                                        
                    
                crm_vals={'partner_id':partner.id,'name':'Messaging Enterprise','description':'Messaging Enterprise',\
                          'user_id':bm,'employee_id':hr_id,'date_open':partner.create_date,\
                          'qms_crm':False,'odoo_script_converted':True}
                
                onchange_vals=crm_obj.on_change_partner_id(cr, uid, [],partner.id, context=None)
                crm_vals.update(onchange_vals['value'])   
                crm_id=crm_obj.create(cr,uid,crm_vals)
                print '--------------LEAD CREATED---------------'
                ##################create wizard id################################
	
                cr.execute(''' insert into crm_lead2opportunity_partner(name,action,user_id,partner_id) VALUES('convert','exist',%s,%s)''',(partner.user_id.id,partner.id))
		print '----------------INSERTED INTO WIZARD-----------------'
            
            count=0
            #####################collect all crm ids###################
            crm_ids=crm_obj.search(cr,uid,[])
            print '----------------total crm---------------',len(crm_ids)
            
            for crm in crm_obj.browse(cr,uid,crm_ids) : 
                        count+=1;print count 
                        cr.execute(''' select id from crm_lead2opportunity_partner where partner_id=%s''',(crm.partner_id.id,))
                        wizard_id=map(lambda x:x[0],cr.fetchall())
                        if wizard_id : 
                              
             ###############convert to opportuntity###############
                            opp_context={'lang': 'en_US', 'tz': 'Asia/Calcutta', 'uid': crm.user_id.id, 'active_model': 'crm.lead', 'empty_list_help_model': 'crm.case.section', \
                                         'stage_type': 'lead', 'search_disable_custom_filters': True, \
                                         'needaction_menu_ref': 'crm.menu_crm_opportunities', 'active_ids': [crm.id], 'active_id': crm.id}
                            
                            crm_opp_obj.action_apply(cr, uid, [wizard_id[0]],opp_context)
                            
                            
                            print '-----------converted to opportunity------------'
                ################change to converted client############
                            #import ipdb;ipdb.set_trace()
                            crm_obj.write(cr,uid,[crm.id],{'stage_id':6})
                            
                            print '-----------converted to client------------'
                            print '########################SUCCESS########################'
                                
                        else : 
                            print 'No wizard id found'
                            #with open("/home/bista/shanky/routesms/logs/converted_crm_logs.txt", "a") as donefile_new:
                            with open("/home/routesms/logs/converted_crm_logs.txt", "a") as donefile_new:
                                donefile_new.write(str(partner.id)+'{}'+'wizard not found' +'\n')

        except Exception as E : 
            print '----------ERROR--------',count
            import ipdb;ipdb.set_trace()
            #with open("/home/bista/shanky/routesms/logs/crmerror.txt", "a") as donefile_new:
            with open("/home/routesms/logs/crmerror.txt", "a") as donefile_new:
            #    import ipdb;ipdb.set_trace()
                donefile_new.write(str(count)+'\n')                 
            
        print '---------------OVER-------------------'
        return True
    





    def configure_tax_refund_account(self,cr,uid,vals):    
        ''' Assign refund account in tax'''
        count=0
        tax_obj=self.pool.get('account.tax')
        tax_ids=tax_obj.search(cr,uid,[('active','=',True)])
        
        # 
	import ipdb;ipdb.set_trace()
        try :
            res=[tax_obj.write(cr,uid,[tax.id],{'account_paid_id':tax.account_collected_id.id}) for tax in \
                 tax_obj.browse(cr,uid,tax_ids) if tax.account_collected_id]
            
        except Exception as E : 
            import ipdb;ipdb.set_trace()
            print E
        print '----------------OVER---------------------'
        return True 


    

    def period_correction_29T(self,cr,uid,vals):
        '''period correction against invoice date for 29T '''
        count=0
        invoice_obj=self.pool.get('account.invoice')
        data=[]
        
####################################prepare partner list##################3
        try:
                                
            cr.execute(''' select id from account_invoice  where  company_id=3 ''')
            cust_inv_ids=map(lambda x:x[0],cr.fetchall())
            print '----------------total inv---------------',len(cust_inv_ids)
            import ipdb;ipdb.set_trace()
            for invoice in invoice_obj.browse(cr,uid,cust_inv_ids) :
                count+=1;print count
                
                if invoice.period_id : 
                    if invoice.period_id.name.split('/')[0] ==invoice.date_invoice.split('-')[1] :
                        #print '----MATCHED--'
                        pass
                    else:
                        
                        print '--------UNMATCHED-------'
                        #import ipdb;ipdb.set_trace()
                        cr.execute(''' select name,id from account_period  where  company_id=3 ''')
                        period_name=map(lambda x:(x[0],x[1]),cr.fetchall())
                        for period in   period_name : 
                            if period[0].split('/')[0] == invoice.date_invoice.split('-')[1] :
                                cr.execute(''' update account_invoice set period_id=%s where id=%s ''',(period[1],invoice.id))
                                print '---uPDATED----'

        except Exception as E : 
            
            #with open("/home/bista/shanky/routesms/logs/29Terror.txt", "a") as donefile_new:
            with open("/home/routesms/logs/29Terror.txt", "a") as donefile_new:
                donefile_new.write(str(invoice.id)+'\n')                     
            print '---------ERROR-----',count    

	return True




    
    def update_credit_debit_info_journal(self,cr,uid,vals):
        '''Update credit debit info'''
        account_move_obj=self.pool.get('account.move')
        move_ids=account_move_obj.search(cr,uid,[])
        count=0
        import ipdb;ipdb.set_trace()
        for move_id in move_ids:
            try : 
                count+=1;print count
                credit_info=account_move_obj._credit_info(cr, uid, [move_id], 'credit_info', '',{})
                debit_info=account_move_obj._debit_info(cr, uid, [move_id], 'debit_info', '',{})
                #import ipdb;ipdb.set_trace()
                cr.execute(''' update account_move set credit_info=%s ,debit_info=%s where id=%s''',(credit_info[credit_info.keys()[0]],debit_info[debit_info.keys()[0]],move_id))
#                account_move_obj.write(cr,uid,[move_id],{'credit_info':credit_info,'debit_info':debit_info})
                print '---DONE----'
            
            except Exception as E : 
                print '-----------ERROR-------',count
                import ipdb;ipdb.set_trace()
                
                
        print '---------------OVER---------------------'
        return True

        

    def import_invoices_rajendra(self,cr,uid,vals):
        ''' Import invoices frm csv'''
        comp_obj=self.pool.get('res.company')
        partner_obj=self.pool.get('res.partner')
        currency_obj=self.pool.get('res.currency')
        journal_obj=self.pool.get('account.journal')
        account_obj=self.pool.get('account.account')
        product_obj=self.pool.get('product.product')
        user_obj=self.pool.get('res.users')
        invoice_obj=self.pool.get('account.invoice')
        invoice_line_obj=self.pool.get('account.invoice.line')
        
        
        comp_ids=comp_obj.search(cr,uid,[])
        count=0
        vals={}
        vals_line={}
        import ipdb;ipdb.set_trace()
        with open('/home/routesms/csv_file/rajendra/spc_rajendra.csv','r') as e:
        
            reader = csv.reader(e)
            
            for row in reader:
                count+=1
                try :
                    
                    #search partner
#                     if count in [388,400,504,562,582,643,665] :
#                          
#                        import ipdb;ipdb.set_trace()
                    
                    partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',row[0])])
                    if len(partner_id)>1 :
                        import ipdb;ipdb.set_trace()
                        print '----------------DUBLPICATE PARTBER---------------',count
                    partner_id=partner_id[0]    
                    vals['partner_id']=partner_id
                    
                    #invoice date
                    vals['date_invoice']=row[2]
                    
                    #journal
                    #journal_id=journal_obj.search(cr,uid,[('name','=',row[2])])[0]
                    vals['journal_id']=58                   
                    
                    #account
                    #account_id=account_obj.search(cr,uid,[('name','=',row[3])])[0]
                    vals['account_id']=2035
                    
                    
                    #currency
                    
                    vals['currency_id']=1070
                    
                    #company
                    vals['type']='out_invoice'
                    vals['company_id']=16
                                      
                    #saleperson
                    
                    vals['comment']=row[12]
                    
                    vals['user_id']=partner_obj.browse(cr,uid,partner_id).user_id.id
                    vals['responsible']=384
                    vals['employee_id']=262
                    
                    vals['remark']='RAJENDRA SALE INVOICE IMPORT 29JULY'
                    #vals['partner_bank_id']=55
                    #vals['partner_bank_id']=58 #RSLUK paypal EUR
                    vals['payment_term']=1
                    #create invoice
                    
                    invoice_id =invoice_obj.create(cr,uid,vals)
                    print 'DONE  =',count
                    #create invoice line
                    #product
                    
                    #product_id=product_obj.search(cr,uid,[('name','=',row[5])])[0]
                    vals_line['product_id']=13                     
                    
                    #desc
                    
                    vals_line['name']='Enterprise Messaging (Bulk SMS)'
                    
                    #account
                    
                    vals_line['account_id']=2079
                                         
                    vals_line['quantity']=row[6]
                    
                    vals_line['price_unit']=row[7]
                    vals_line['invoice_id'] =invoice_id
                    
                    invoice_line_obj.create(cr,uid,vals_line)
                        
#                     else :
#                         pass
                    
                except Exception as E :
                    print 'ERROR -----',count
                    
            print '----------------OVER----------------------'                
            return True      
  
  
    def assign_group(self,cr,uid,vals):
        count=0
        import ipdb;ipdb.set_trace()
        cr.execute('''select id from res_users''')
        partner_ids=map(lambda x:x,cr.fetchall())
        if partner_ids : 
            for id in partner_ids : 
                count+=1;print count
                try : 
                    cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s ''',(80,id))
                    cr.execute(''' insert into res_groups_users_rel(gid,uid) VALUES(%s,%s)''',(80,id))
                except Exception as E :
                    print 'Already exist'

        print '-----------done-------------------'
                    
        return True



    def rectify_payment_term_invoices(self,cr,uid,vals):
        ''' Correct payment terms in invoices'''
        
        inv_obj=self.pool.get('account.invoice')
        import ipdb;ipdb.set_trace()
        
        cr.execute(''' update  account_invoice set payment_term=1 where payment_term in  (11,12)''',)
        
        return True
        


    def update_user_routesms_id(self,cr,uid,vals):
        count=0
        partner_obj=self.pool.get('res.partner')
        import ipdb;ipdb.set_trace()
        with open('/home/routesms/csv_file/rohini/RSL_Code.csv','r') as e:
            reader = csv.reader(e)
            li=[]
                
            for row in reader:
                count+=1
                partner_ids=partner_obj.search(cr,uid,[('partner_sequence','=',row[1])])
                if partner_ids : 
                    partner_obj.write(cr,uid,partner_ids,{'routesms_cust_id':row[2]})
                    print '-------------DONE-----------'
                else : 
                    print '-------------NO RECORD FOUND-----------',count
                    
                    
        return True


    def update_amount_to_word(self,cr,uid,vals):
        '''Update amount word invoices '''
        inv_obj=self.pool.get('account.invoice')
        inv_ids =inv_obj.search(cr,uid,[])
        count=0
        import ipdb;ipdb.set_trace()
        for inv_id in  inv_ids :
            
            count+=1
            try:
                
                result=inv_obj._amount_to_word_updated(cr, uid, [inv_id], 'amount_to_word_updated', [],{})
                
                cr.execute(''' update account_invoice set amount_to_word_updated=%s where id =%s''',(result[result.keys()[0]],inv_id))
                print '---------------DONE-----',count
            
            except Exception as E  :
                print '---------------ERROR-----',count
                import ipdb;ipdb.set_trace()
                with open("/home/routesms/logs/invoice_amount.txt", "a") as donefile_new:
                    donefile_new.write(str(count)+'\n')                 
                
        return True

    def remove_rsl_draft_invoice(self,cr,uid,vals):
        '''remove rsl draft invoice '''
        account_obj=self.pool.get('account.invoice')
        
        
        count=0
        vals={}
        
        #comp_li=(10,16,15)
#        cr.execute(''' select id  from account_invoice where create_date <='2015-08-31 17:30:16.887726'and type='out_invoice' and state='draft' ''',)
        cr.execute(''' select id  from account_invoice where date_invoice <='2015-12-07' and company_id in (16,10) and state='draft' ''',)
        #cr.execute(''' select id  from account_invoice where date_invoice <='2015-12-07' and company_id=10 and type='in_invoice' and state='draft' ''',)
        #cr.execute(''' select id  from account_invoice where date_invoice <='2015-12-07' and company_id=10 and type='in_refund' and state='draft' ''',)
        #cr.execute(''' select id  from account_voucher where date <='2015-12-07' and company_id=10  and state='draft' ''',)
        #cr.execute(''' select id  from account_invoice where date_invoice <='2015-12-07' and company_id=10 and type='out_refund' and state='draft' ''',)
        invoice_ids=map(lambda x:x[0],cr.fetchall())        
        #invoice_ids=account_obj.search(cr,uid,[('company_id','=',10),('type','=','out_invoice'),('state','=','draft')])
        print len(invoice_ids)
        import ipdb;ipdb.set_trace()
        for inv_id in invoice_ids :
            count+=1 
            try : 
                account_obj.unlink(cr,uid,[inv_id],{})
                print 'Sucesfully deleted',count
                
            except Exception as E : 
                #import ipdb;ipdb.set_trace()
                print '------------------ERROR-------------------',count
#                 with open("/home/bista/shanky/routesms/logs/delete_draft_invoice/delete_invoice.txt", "a") as donefile_new:
#                     donefile_new.write(str(count)+'\n')            

        print '---------------GAME OVER-----------'
        return True


    def update_payment_terms(self,cr,uid,vals):
        '''update payment terms '''
        partner_obj=self.pool.get('account.invoice')
        
        
        count=0
        vals={}
        vals_line={}
        import ipdb;ipdb.set_trace()
        with open('/home/routesms/csv_file/krupali/krupa_live_payment_term.csv','r') as e:
        
            reader = csv.reader(e)
            
            for row in reader:
                count+=1
                
                try :
                    val=int(row[0])
                    cr.execute('''update account_invoice set payment_term=1 where id=%s ''',(val,))
                    
                    print count

                
                except Exception as E :
                    print 'ERROR',count

        
        return True



    def update_employee_email_id(self,cr,uid,vals):
        
        user_obj=self.pool.get('res.users')
        partner_obj=self.pool.get('res.partner')
        user_ids=user_obj.search(cr,uid,[])
        count=0
        import ipdb;ipdb.set_trace()
        for id in user_ids :
             val=user_obj.browse(cr,uid,id)
             count+=1;print count
             partner_obj.write(cr,uid,[val.partner_id.id],{'email':val.login})
        print '-----------_FINSIH----------------------'
        return True

    def generate_odoo_id_user(self,cr,uid,vals):
        ''' generate odoo id for company user'''
        partner_obj=self.pool.get('res.partner')
        
        partner_ids=partner_obj.search(cr,uid,[('supplier','=',False),('customer','=',False),('partner_sequence','=',False)])
        #partner_ids=partner_obj.search(cr,uid,[('supplier','=',False),('customer','=',False),('partner_sequence','=','')])
        import ipdb;ipdb.set_trace()
        count=0
        print len(partner_ids)
        for id in partner_ids :
            count+=1;print count
            partner_obj.validate_partner(cr,uid,[id],None)
            print 'Upadting record'
            
            
        return True

    def update_partner_vertical(self,cr,uid,vals):
        ''' update partner vertical based on company asigned to partner'''
        partner_obj=self.pool.get('res.partner')
        company_obj=self.pool.get('res.company')
        partner_ids=partner_obj.search(cr,uid,[])
        count=0
        
        for id in partner_ids :
            count+=1;print count
            vertical=company_obj.browse(cr,uid,partner_obj.browse(cr,uid,id).company_id.id).vertical.id
            cr.execute(''' update res_partner set vertical=%s where id=%s''',(vertical,id))
            contact_id=partner_obj.search(cr,uid,[('parent_id','=',id)])
            print 'Parent Done'
            if contact_id : 
                cr.execute(''' update res_partner set vertical=%s where id=%s''',(vertical,contact_id[0]))
                print 'Contact DOne'
            
            
        
        return True
        
    def assign_warehouse_group(self,cr,uid,vals): 
        ''' Assign warehouse group to Sales team'''
        user_obj=self.pool.get('res.users')
        user_ids=user_obj.search(cr,uid,[])
        count=0
        
        for id in user_ids :
            count+=1
            print count 
            cr.execute(''' select * from res_groups_users_rel where uid=%s and gid in %s''',(id,(21,23,81)))
            value=cr.fetchall()
            if not value : 
            
                cr.execute(''' insert into res_groups_users_rel(gid,uid) VALUES(%s,%s)''',(36,id))
                print 'Warehouse Assigned'
                    
            else:
                
                print 'This is account USer'
                
        
        return True
        
        



    def holiday(self,cr,uid,vals):
        ''' nested'''
      # import ipdb;ipdb.set_trace() 
            
    
        def pnr_name(cr,uid,vals):
            '''Update pnr '''
            inv_obj=self.pool.get('account.invoice')
            inv_ids =inv_obj.search(cr,uid,[])
            count=0
            
            for inv_id in inv_ids :
                if inv_obj.browse(cr,uid,inv_id).company_id.id == 3 :
                        
                    name='pnr_no'
                    count+=1;print count
                    
                    pnr=inv_obj._pnr_no(cr, uid, [inv_id], name, None, {})

                    inv_obj.write(cr,uid,inv_id,{'pnr_no':pnr})
                    
            return True    
    
    
        def ticket(cr,uid,vals):
            '''Update ticket '''
            inv_obj=self.pool.get('account.invoice')
            inv_ids =inv_obj.search(cr,uid,[])
            count=0
            
            for inv_id in inv_ids :
                if inv_obj.browse(cr,uid,inv_id).company_id.id == 3 :
                    
                    name='ticket_no'
                    count+=1;print count
                    ticket=inv_obj._ticket_no(cr, uid, [inv_id], name, None, {})
                    inv_obj.write(cr,uid,inv_id,{'ticket_no':ticket})
                    
            return True
        
        
             
    
        def passenger(cr,uid,vals):
            '''Update passenger '''
            inv_obj=self.pool.get('account.invoice')
            inv_ids =inv_obj.search(cr,uid,[])
            count=0
            
            for inv_id in inv_ids :
                if inv_obj.browse(cr,uid,inv_id).company_id.id == 3 :
                    
                    name='passenger_names'
                    count+=1;print count
                    passenger=inv_obj._ticket_no(cr, uid, [inv_id], name, None, {})
                    inv_obj.write(cr,uid,inv_id,{'passenger_names':passenger})
                    
            return True
         
        pnr_name(cr,uid,vals);ticket(cr,uid,vals);passenger(cr,uid,vals) ;
        print '-------------OVER---------'
        return True
    def currency_rate_import_new(self,cr,uid,vals):
        ''' assign currency rate for companies'''
        #comp_obj=self.pool.get('res.company')
        currency_obj=self.pool.get('res.currency')
        currency_line_obj=self.pool.get('res.currency.rate')
        #comp_ids=comp_obj.search(cr,uid,[])
        counting=0
        
        with open('/home/bista/Desktop/routesms_data_uploading/sachin/gsp_cur.csv','r') as e:
        
            reader = csv.reader(e)
            
            for row in reader:
                counting+=1
                
                try :
                    currency_line_obj.create(cr,uid,{'currency_id':2348,'rate':row[3],'name':row[2]})
                    print 'DONE',counting
                except Exception as E : 
                    print 'ERROR',counting





    def update_invoice_saleperson_for_reporting(self,cr,uid,vals):
        ''' update all salepersons on invoices for reporting purpose'''
        invoice_obj=self.pool.get('account.invoice')
        invoice_ids=invoice_obj.search(cr,uid,[])
        count=0
        #import ipdb;ipdb.set_trace()
        for inv_id in invoice_ids :
            count+=1
            print count
            #flag=False
            try : 
                invoice_val=invoice_obj.browse(cr,uid,inv_id)
                current_user_id=invoice_val.user_id.id                
                if invoice_val.company_id.id == 3 :
                    print 'THIS IS 29T',count
                    continue
##########################################3


                if invoice_val.responsible : 
                    if current_user_id ==invoice_val.partner_id.user_id.id : 
                        emp_id=self.pool.get('hr.employee').search(cr,1,[('user_id','=',invoice_val.responsible.id)])
                        if emp_id :
                            emp_ids=emp_id[0]
                            invoice_obj.write(cr,uid,[inv_id],{'user_id':invoice_val.partner_id.user_id.id,\
                                                               'employee_id':emp_ids})                    
                            with open("/home/bista/shanky/routesms/logs/1.txt", "a") as donefile_new:
                                donefile_new.write(str(count)+'\n')
                        else :
                            print "No employee found",current_user_id
        
        
                            with open("/home/bista/shanky/routesms/logs/missing_employee.txt", "a") as myfile:
                                myfile.write(str(current_user_id)+'\n')
                            
                            
                                                         
                    else :
                        emp_id=self.pool.get('hr.employee').search(cr,1,[('user_id','=',current_user_id)])
                        if emp_id  :
                            emp_ids=emp_id[0]
                             
                            invoice_obj.write(cr,uid,[inv_id],{'user_id':invoice_val.partner_id.user_id.id,\
                                                               'responsible':current_user_id,'employee_id':emp_ids})                    
                            with open("/home/bista/shanky/routesms/logs/2.txt", "a") as donefile:
                                donefile.write(str(count)+'\n')
                        else :
                            

                            print "No employee found",current_user_id
        
        
                            with open("/home/bista/shanky/routesms/logs/missing_employee.txt", "a") as myfile:
                                myfile.write(str(current_user_id)+'\n')
                                
                else :
                    
                    emp_id=self.pool.get('hr.employee').search(cr,1,[('user_id','=',1)])
                    if emp_id  :
                        emp_ids=emp_id[0]
                         
                        invoice_obj.write(cr,uid,[inv_id],{'user_id':invoice_val.partner_id.user_id.id,'responsible':1,'employee_id':emp_ids})
                                                                            
                        with open("/home/bista/shanky/routesms/logs/3.txt", "a") as donefile:
                            donefile.write(str(count)+'\n')
                    else :
                        

                        print "No employee found",current_user_id
    
    
                        with open("/home/bista/shanky/routesms/logs/missing_employee.txt", "a") as myfile:
                                myfile.write(str(current_user_id)+'\n')                    
                    
                print 'DONE',count
                
            except Exception as E : 
                
                print 'ERROR',count
                with open("/home/bista/shanky/routesms/logs/error.txt", "a") as errorfile:
                    errorfile.write(str(count)+'\n')                

        return True                    
                
                
                            
                            
                                 
                    



##################################333                
#                 if count==2961 :
#                 import ipdb;ipdb.set_trace()
#                                      
# 
# 
#                 if current_user_id ==invoice_val.partner_id.user_id.id :
#                     emp_id=self.pool.get('hr.employee').search(cr,1,[('user_id','=',invoice_val.responsible.id)])
#                     flag=True
#                 else :
#                     
#                     emp_id=self.pool.get('hr.employee').search(cr,1,[('user_id','=',current_user_id)])
# 
#                 
#                                         
#                 if emp_id and flag==True : 
#                     
#                     emp_ids=emp_id[0]
#                      
#                     invoice_obj.write(cr,uid,[inv_id],{'user_id':invoice_val.partner_id.user_id.id,\
#                                                        'employee_id':emp_ids})                    
#                     with open("/home/bista/shanky/routesms/logs/logs_new.txt", "a") as donefile_new:
#                         donefile_new.write(str(count))
#                         
#                 elif emp_id and flag==False :
#                     emp_ids=emp_id[0]
#                      
#                     invoice_obj.write(cr,uid,[inv_id],{'user_id':invoice_val.partner_id.user_id.id,\
#                                                        'responsible':current_user_id,'employee_id':emp_ids})                    
#                     with open("/home/bista/shanky/routesms/logs/done.txt", "a") as donefile:
#                         donefile.write(str(count))
#                     
#                                                                     
#                 else : 
#                     
#                     print "No employee found",current_user_id
# 
# 
#                     with open("/home/bista/shanky/routesms/logs/missing.txt", "a") as myfile:
#                         myfile.write(str(current_user_id))
#                     
#                     
#                     
# 
# # 
# #                 cr.execute(''' update account_invoice set user_id=%s ,responsible=%s,employee_id=%s where id=%s ''',(invoice_val.partner_id.user_id.id,current_user_id,emp_ids,inv_id))
#                 

    
    
    def pay_invoice(self,cr,uid,vals):
        ''' Pay invoice auto'''
        invoice_obj=self.pool.get('account.invoice')
        voucher_obj=self.pool.get('account.voucher')
        move_line_obj=self.pool.get('account.move.line')
        voucher_line_obj=self.pool.get('account.voucher.line')
        idss=[7578]
        count=0
        context={}
        for ids in idss :
            try : 
                
                count+=1 
                res=invoice_obj.browse(cr,uid,ids)
                 #
                #reg_pay = sock.execute(database,uid, password,'account.invoice', 'invoice_pay_customer', [i2])
                ids=[ids]
                reg_pay = invoice_obj.invoice_pay_customer(cr,uid,ids)
                
                #create new coucher
                vo_cr={'journal_id':34,'amount':res.amount_total,'period_id':res.period_id.id,'account_id':1225,'partner_id':res.partner_id.id,'company_id':10}
                #vo_id=sock.execute(database,uid, password,'account.voucher','create',vo_cr)
                vo_id=voucher_obj.create(cr,uid,vo_cr)
                
                #move_line_id=sock.execute(database,uid, password,'account.move.line', 'search', [('ref','=',res['reference']),('name','=','/')])
                move_line_id=move_line_obj.search(cr,uid,[('ref','=',res.number),('name','=','/')])
                
                vo_line={'voucher_id':vo_id,'account_id':1225,'move_line_id':move_line_id[0],'amount':res.amount_total}
                #create voucher line
         
                #vo_line_cr=sock.execute(database,uid, password,'account.voucher.line','create',vo_line)
                vo_line_cr=voucher_line_obj.create(cr,uid,vo_line)
                #pay invoice
                context.update({'invoice_id':ids})
                
                pay_inv = voucher_obj.button_proforma_voucher(cr,uid,[vo_id],context)
                #state=paid
                #sock.exec_workflow (database, uid, password, 'account.voucher', 'proforma_voucher', vo_id)
                
                voucher_obj.signal_workflow(cr, uid, [vo_id], 'proforma_voucher')
                print '---------------INOVICED PAYED --------------'
                print count
                
            except Exception as E : 
                print 'ERROR ',count

        return True


    def update_partners(self,cr,uid,vals):
        '''update  '''
        partner_obj=self.pool.get('res.partner')
        
        
        count=0
        vals={}
        vals_line={}
        
        with open('/home/routesms/graphic_partner.csv','r') as e:
        
            reader = csv.reader(e)
            
            for row in reader:
                count+=1
                
                try :

                    partner_id=partner_obj.search(cr,uid,[('name','=',row[1])])
                    
                    partner_id=partner_obj.write(cr,uid,partner_id,{'company_id':6})
                    print 'DONE ------------NUMBER IS =',count

                
                except Exception as E :
                    print 'EXCEPTION = ',count
                    

        
        return True


    def create_partners(self,cr,uid,vals):
        '''partner creation '''
        partner_obj=self.pool.get('res.partner')
        
        
        count=0
        vals={}
        vals_line={}
        
        with open('/home/PAYPAL UK EURO NEW (TILL 15.05.2015) krupali.csv','r') as e:
        
            reader = csv.reader(e)
            
            for row in reader:
                count+=1
                
                try :
                    vals['user_id']=row[0]
                    vals['name']=row[1]
                    vals['street']=row[3]
                    vals['email']=row[4]
                    vals['postpaid']=True
                    vals['customer']=True
                    vals['is_company']=True
                    partner_id=partner_obj.create(cr,uid,vals)
                    #import ipdb;ipdb.set_trace()
                    #create contact perosn
                    
                    vals_line['name']=row[2]
                    vals_line['parent_id']=partner_id
                    vals_line['use_parent_address']=True
                    partner_obj.create(cr,uid,vals_line)
                
                except Exception as E :
                    print count
                    
                
                
        
        return True



    
    def update_supplier_saleperson(self,cr,uid,vals):
        '''update Salesperson '''
        partner_obj=self.pool.get('res.partner')
        partner_ids=partner_obj.search(cr,uid,[('supplier','=',True),('user_id','=',False)])
        
        count=0
       #
        for part_id in partner_ids :
            count+=1
            print count
            partner_obj.write(cr,uid,[part_id],{'user_id':237})
        
        
        return True
        


    
    def import_invoices(self,cr,uid,vals):
        ''' Import invoices frm csv'''
        comp_obj=self.pool.get('res.company')
        partner_obj=self.pool.get('res.partner')
        currency_obj=self.pool.get('res.currency')
        journal_obj=self.pool.get('account.journal')
        account_obj=self.pool.get('account.account')
        product_obj=self.pool.get('product.product')
        user_obj=self.pool.get('res.users')
        invoice_obj=self.pool.get('account.invoice')
        invoice_line_obj=self.pool.get('account.invoice.line')
        
        
        comp_ids=comp_obj.search(cr,uid,[])
        count=0
        vals={}
        vals_line={}
        #import ipdb;ipdb.set_trace()
        with open('/home/routesms/csv_file/krupali/PAYPAL INDIA EURO (25.05.2015 TILL 05.06.2015 )-1.csv','r') as e:
        
            reader = csv.reader(e)
            
            for row in reader:
                count+=1
                try :
                    
                    #search partner
#                     if count in [388,400,504,562,582,643,665] :
#                          
#                        import ipdb;ipdb.set_trace()
                        
                    partner_id=partner_obj.search(cr,uid,[('name','=',row[0])])[0]
                    vals['partner_id']=partner_id
                    
                    #invoice date
                    vals['date_invoice']=row[1]
                    
                    #journal
                    #journal_id=journal_obj.search(cr,uid,[('name','=',row[2])])[0]
                    vals['journal_id']=34                   
                    
                    #account
                    #account_id=account_obj.search(cr,uid,[('name','=',row[3])])[0]
                    vals['account_id']=1225
                    
                    
                    #currency
                    currency_id=currency_obj.search(cr,uid,[('name','=',row[4])])[0]
                    vals['currency_id']=currency_id
                    
                    #company
                    company_id=comp_obj.search(cr,uid,[('name','=',row[11])])[0]
                    vals['company_id']=company_id  
                                      
                    #saleperson
                    
                    user_id=user_obj.search(cr,uid,[('name','=',row[12])])[0]
                    vals['user_id']=user_id
                    vals['credit_type']='KRUPALI PAYPAL INDIA EURO (25.05.2015 TILL 05.06.2015 )-1'
                    #vals['partner_bank_id']=55
                    vals['partner_bank_id']=58 #RSLUK paypal EUR
                    vals['payment_term']=1
                    #create invoice
                    invoice_id =invoice_obj.create(cr,uid,vals)
                    print 'DONE  =',count
                    #create invoice line
                    #product
                    
                    product_id=product_obj.search(cr,uid,[('name','=',row[5])])[0]
                    vals_line['product_id']=product_id                     
                    
                    #desc
                    
                    vals_line['name']=row[6]
                    
                    #account
                    account_id=account_obj.search(cr,uid,[('name','=',row[7])])[0]
                    vals_line['account_id']=account_id                    
                                         
                    vals_line['quantity']=row[8]
                    
                    vals_line['price_unit']=row[9]
                    vals_line['invoice_id'] =invoice_id
                    
                    invoice_line_obj.create(cr,uid,vals_line)
                        
#                     else :
#                         pass
                    
                except Exception as E :
                    print 'ERROR -----',count
                    
                            
            return True    
  
    def import_invoices_RSL_7july(self,cr,uid,vals):
        ''' Import invoices frm csv'''
        comp_obj=self.pool.get('res.company')
        partner_obj=self.pool.get('res.partner')
        currency_obj=self.pool.get('res.currency')
        journal_obj=self.pool.get('account.journal')
        account_obj=self.pool.get('account.account')
        product_obj=self.pool.get('product.product')
        user_obj=self.pool.get('res.users')
        invoice_obj=self.pool.get('account.invoice')
        invoice_line_obj=self.pool.get('account.invoice.line')
        city_obj=self.pool.get('city.code')
        
        comp_ids=comp_obj.search(cr,uid,[])
        count=0
        vals={}
        vals_line={}
        import ipdb;ipdb.set_trace()
        with open('/home/routesms/csv_file/asmita/cust_inv_3.csv','r') as e:
        
            reader = csv.reader(e)
            
            for row in reader:
                count+=1
                try :
                    

                    partner_id=partner_obj.search(cr,uid,[('name','=',row[0])])[0]
                    vals['partner_id']=partner_id
                    
                    #invoice date
                    vals['date_invoice']=row[1]
                    
                    #journal
                    #journal_id=journal_obj.search(cr,uid,[('name','=',row[2])])[0]
                    vals['journal_id']=34         
                    
                    #account
                    #account_id=account_obj.search(cr,uid,[('name','=',row[3])])[0]
                    vals['account_id']=1225
                    
                    
                    #currency
                    #currency_id=currency_obj.search(cr,uid,[('name','=',row[4])])[0]
                    vals['currency_id']=798
                    
                    #company
                    #company_id=comp_obj.search(cr,uid,[('name','=',row[11])])[0]
                    vals['company_id']=10
                    #total amount
                    
                                      
                    #saleperson
                    
                    #user_id=user_obj.search(cr,uid,[('name','=',row[12])])[0]
                    vals['user_id']=partner_obj.browse(cr,uid,partner_id).user_id.id
                    vals['responsible']=521
                    vals['employee_id']=286
                    vals['remark']='Asmita Shigwan RSL 7july'
                    #vals['partner_bank_id']=55
                  #  vals['partner_bank_id']=54 #RSLUK paypal EUR
                    vals['payment_term']=1
                    #create invoice
                    #import ipdb;ipdb.set_trace()
                    invoice_id =invoice_obj.create(cr,uid,vals)
                    print 'DONE  =',count
                    #create invoice line
                    #product
                    
                   # product_id=product_obj.search(cr,uid,[('name','=',row[5])])[0]
                    vals_line['product_id']=13                     
                    
                    #desc
                    vals_line['name']=row[6]
                    
                    #account
                    
                    #account_id=account_obj.search(cr,uid,[('name','=',row[7])])[0]
                    vals_line['account_id']=1269                    
                                         
                    vals_line['quantity']=row[7]
                    
                    vals_line['price_unit']=row[8]
                    vals_line['invoice_id'] =invoice_id
                    
                    invoice_line_obj.create(cr,uid,vals_line)
                    
                except Exception as E :
                    print 'ERROR -----',count
                    
                            
            return True    


    def import_invoices_293(self,cr,uid,vals):
        ''' Import invoices frm csv'''
        comp_obj=self.pool.get('res.company')
        partner_obj=self.pool.get('res.partner')
        currency_obj=self.pool.get('res.currency')
        journal_obj=self.pool.get('account.journal')
        account_obj=self.pool.get('account.account')
        product_obj=self.pool.get('product.product')
        user_obj=self.pool.get('res.users')
        invoice_obj=self.pool.get('account.invoice')
        invoice_line_obj=self.pool.get('account.invoice.line')
        city_obj=self.pool.get('city.code')
        
        comp_ids=comp_obj.search(cr,uid,[])
        count=0
        vals={}
        vals_line={}
        
        with open('/home/routesms/csv_file/avinash/customer_inv1.csv','r') as e:
        
            reader = csv.reader(e)
            
            for row in reader:
                count+=1
                try :
                    

                    partner_id=partner_obj.search(cr,uid,[('name','=',row[0])])[0]
                    vals['partner_id']=partner_id
                    
                    #invoice date
                    vals['date_invoice']=row[1]
                    
                    #journal
                    #journal_id=journal_obj.search(cr,uid,[('name','=',row[2])])[0]
                    vals['journal_id']=148           
                    
                    #account
                    #account_id=account_obj.search(cr,uid,[('name','=',row[3])])[0]
                    vals['account_id']=415
                    
                    
                    #currency
                    #currency_id=currency_obj.search(cr,uid,[('name','=',row[4])])[0]
                    vals['currency_id']=1057
                    
                    #company
                    #company_id=comp_obj.search(cr,uid,[('name','=',row[11])])[0]
                    vals['company_id']=3 
                    #total amount
                    
                                      
                    #saleperson
                    
                    #user_id=user_obj.search(cr,uid,[('name','=',row[12])])[0]
                    vals['user_id']=int(row[20])
                    vals['credit_type']='AVINASH AIR TICKETING'
                    #vals['partner_bank_id']=55
                  #  vals['partner_bank_id']=54 #RSLUK paypal EUR
                    vals['payment_term']=1
                    #create invoice
                    #import ipdb;ipdb.set_trace()
                    invoice_id =invoice_obj.create(cr,uid,vals)
                    print 'DONE  =',count
                    #create invoice line
                    #product
                    
                   # product_id=product_obj.search(cr,uid,[('name','=',row[5])])[0]
                    vals_line['product_id']=int(row[5])                     
                    
                    #desc
                    
                    
                    vals_line['passenger_name_air']=row[6]
                    vals_line['pnr']=row[7]
                    vals_line['ticket_number']=row[8]
                    vals_line['flight_number']=row[9]
                    vals_line['travel_date']=row[10]
                    vals_line['holiday_refernce_number']=row[11]
                    from_city=city_obj.search(cr,uid,[('name','=',row[12])])
                    to_city=city_obj.search(cr,uid,[('name','=',row[13])])
                    if from_city and to_city : 
                        
                        vals_line['from']=from_city[0]
                        
                        vals_line['to']=to_city[0]
                    else :
                        print 'CITY CODE NOT FOUND'
                        print 'Iam raising error'
                        print db
                    #account
                    if vals_line['product_id'] == 42 :
                        
                    #account_id=account_obj.search(cr,uid,[('name','=',row[7])])[0]
                        vals_line['account_id']=459
                    
                    elif vals_line['product_id'] == 43 :
                        vals_line['account_id']=4212
                    
                    else :
                        print 'PRODUCT DOESNT EXIST'
                        print 'RAISING ERROR'
                        print cc         
                                       
                    vals_line['quantity']=1
                    
                    vals_line['basic_amount']=int(row[15])
                    vals_line['markup_air']=int(row[16])
                    vals_line['name']=row[17]
                    vals_line['invoice_id'] =invoice_id
                    
                    #sub amount
                    vals_line['sub_total_amount']=row[19]
                    vals_line['price_unit']=row[19]
                    invoice_line_id=invoice_line_obj.create(cr,uid,vals_line)

                    #tax
                    cr.execute(''' insert into account_invoice_line_tax (invoice_line_id,tax_id) values(%s,%s)''',(invoice_line_id,row[18]))
                    
                        
#                     else :
#                         pass
                    
                except Exception as E :
                    print 'ERROR -----',count
                    
                            
            return True    


    def import_invoices_293_supplier(self,cr,uid,vals):
        ''' Import invoices frm csv'''
        comp_obj=self.pool.get('res.company')
        partner_obj=self.pool.get('res.partner')
        currency_obj=self.pool.get('res.currency')
        journal_obj=self.pool.get('account.journal')
        account_obj=self.pool.get('account.account')
        product_obj=self.pool.get('product.product')
        user_obj=self.pool.get('res.users')
        invoice_obj=self.pool.get('account.invoice')
        invoice_line_obj=self.pool.get('account.invoice.line')
        city_obj=self.pool.get('city.code')
        
        comp_ids=comp_obj.search(cr,uid,[])
        count=0
        vals={}
        vals_line={}
        #import ipdb;ipdb.set_trace()
        with open('/home/bista/Desktop/routesms_data_uploading/avinash/27may/final_3.csv','r') as e:
            #import ipdb;ipdb.set_trace()
            reader = csv.reader(e)
            
            for row in reader:
                count+=1
                try :
                    
#                     if count== 461 : 
#                         import ipdb;ipdb.set_trace()
#                         pass
#                     else :
#                         dd
                    partner_id=partner_obj.search(cr,uid,[('name','=',row[0])])[0]
                    vals['partner_id']=partner_id
                    
                    #invoice date
                    vals['date_invoice']=row[1]
                    
                    #journal
                    #journal_id=journal_obj.search(cr,uid,[('name','=',row[2])])[0]
                    vals['journal_id']=149           
                    
                    #account
                    #account_id=account_obj.search(cr,uid,[('name','=',row[3])])[0]
                    vals['account_id']=307
                    
                    
                    #currency
                    #currency_id=currency_obj.search(cr,uid,[('name','=',row[4])])[0]
                    vals['currency_id']=1057
                    
                    #company
                    #company_id=comp_obj.search(cr,uid,[('name','=',row[11])])[0]
                    vals['company_id']=3 
                    #total amount
                    
                    vals['type']="in_invoice"          
                    #saleperson
                    
                    #user_id=user_obj.search(cr,uid,[('name','=',row[12])])[0]
                    vals['user_id']=int(row[19])
                    vals['credit_type']='NISBAT SUPPLIER AIR TICKETING'
                    #vals['partner_bank_id']=55
                  #  vals['partner_bank_id']=54 #RSLUK paypal EUR
                    vals['payment_term']=1
                    #create invoice
                    #import ipdb;ipdb.set_trace()
                    invoice_id =invoice_obj.create(cr,uid,vals)
                    print 'DONE  =',count
                    #create invoice line
                    #product
                    
                   # product_id=product_obj.search(cr,uid,[('name','=',row[5])])[0]
                    vals_line['product_id']=int(row[5])                     
                    
                    #desc
                    
                    
                    vals_line['passenger_name_air']=row[6]
                    vals_line['pnr']=row[7]
                    vals_line['ticket_number']=row[8]
                    vals_line['flight_number']=row[9]
                    vals_line['travel_date']=row[10]
                    vals_line['holiday_refernce_number']=row[11]
                    from_city=city_obj.search(cr,uid,[('name','=',row[12])])
                    to_city=city_obj.search(cr,uid,[('name','=',row[13])])
                    #import ipdb;ipdb.set_trace()
                    if from_city and to_city : 
                        
                        vals_line['from']=from_city[0]
                        
                        vals_line['to']=to_city[0]
                    else :
                        print 'CITY CODE NOT FOUND'
                        print 'Iam raising error'
                        print db
                    #account
                    if vals_line['product_id'] == 42 :
                        
                    #account_id=account_obj.search(cr,uid,[('name','=',row[7])])[0]
                        vals_line['account_id']=4123
                    
                    elif vals_line['product_id'] == 43 :
                        vals_line['account_id']=4121
                    
                    else :
                        print 'PRODUCT DOESNT EXIST'
                        print 'RAISING ERROR'
                        print cc         
                                       
                    vals_line['quantity']=1
                    
                    vals_line['basic_amount']=int(row[15])
                    vals_line['markup_air']=int(row[16])
                    vals_line['name']=row[17]
                    vals_line['invoice_id'] =invoice_id
                    
                    #sub amount
                    vals_line['sub_total_amount']=row[18]
                    vals_line['price_unit']=row[18]
                    invoice_line_id=invoice_line_obj.create(cr,uid,vals_line)

                    #tax
                  #  cr.execute(''' insert into account_invoice_line_tax (invoice_line_id,tax_id) values(%s,%s)''',(invoice_line_id,row[18]))
                    
                        
#                     else :
#                         pass
                    
                except Exception as E :
                    print 'ERROR -----',count
                    
                            
            return True    

  
    
    def update_tax_invoice_line(self,cr,uid,vals):
        '''Update Tax amount per invoice line'''
        context={}
        
        invoice_obj=self.pool.get('account.invoice')
        invoice_line_obj=self.pool.get('account.invoice.line')
        count=0
        for invoice_id in invoice_obj.search(cr,uid,[]) :
            count+=1

                
            if invoice_obj.browse(cr,uid,invoice_id).company_id.id == 3 :
                pass
            else :
                
                for invoice_line_id in invoice_line_obj.search(cr,uid,[('invoice_id','=',invoice_id)]) :
                    
                    res=invoice_line_obj._tax_amount(cr, uid, [invoice_line_id], 'tax_amount', None, context)
                    if res :
                        try :
                            invoice_line_obj.write(cr,uid,invoice_line_id,{'tax_amount':res.values()[0]})
                        except  Exception as E:
                            invoice_line_obj.write(cr,uid,invoice_line_id,{'tax_amount':0.00})
                        
                
        
        
        return True

    def update_period_name(self,cr,uid,vals):
        '''Update period  str value '''
        inv_obj=self.pool.get('account.invoice')
        inv_ids =inv_obj.search(cr,uid,[])
        count=0
        
        for inv_id in inv_ids :
            name='period_to_words'
            count+=1;print count
            month=inv_obj._period_to_words(cr, uid, [inv_id], name, None, {})
            inv_obj.write(cr,uid,inv_id,{'period_to_words':month})
                
        return True    

    def update_total_name(self,cr,uid,vals):
        '''Update Total amount str value '''
        inv_obj=self.pool.get('account.invoice')
        inv_ids =inv_obj.search(cr,uid,[])
        count=0
        
        for inv_id in inv_ids :
            updated_val=''
            amount=inv_obj.browse(cr,uid,inv_id).amount_total
            if amount : 
                numwords=num2words(int(amount)).split('-')
                for i in numwords:
                    b=i.split(' ')
                    for j in b:
        

                        updated_val+=j.capitalize() +' '            
                #updated_val=' '.join([x.capitalize() for x in numwords])
                count+=1;print count
                inv_obj.write(cr,uid,inv_id,{'amount_to_word':updated_val})
                
        return True

    def currency_rate_import(self,cr,uid,vals):
        ''' assign currency rate for INR companies'''
        comp_obj=self.pool.get('res.company')
        currency_obj=self.pool.get('res.currency')
        currency_line_obj=self.pool.get('res.currency.rate')
        comp_ids=comp_obj.search(cr,uid,[])
        counting=0
        
        with open('/home/bista/shanky/routesms/docs/currency_rate_import.csv','r') as e:
        
            reader = csv.reader(e)
            
            for row in reader:
                
                for comp in comp_ids :
                    counting+=1
                    print counting

                        
                    
                    cur_name=comp_obj.browse(cr,uid,comp).currency_id.name
                    if 'GBP' in cur_name :
                        #cur_id    =currency_obj.search(cr,uid,[('company_id','=',comp)])
                        eur=currency_obj.search(cr,uid,[('company_id','=',comp),('name','like','%EUR%')])
                        usd=currency_obj.search(cr,uid,[('company_id','=',comp),('name','like','%USD%')])
                        
                        if eur :
                            
                            value_euro={'currency_id':eur[0],'rate':row[2],'name':row[0]}
                            currency_line_obj.create(cr,uid,value_euro)
                        if usd :
                            
                            value_usd={'currency_id':usd[0],'rate':row[3],'name':row[0]}
                            currency_line_obj.create(cr,uid,value_usd)
                            
            return True
                
            
        


    def create_currency_rate(self,cr,uid,vals):
        
        currency_obj=self.pool.get('res.currency')
        currency_line_obj=self.pool.get('res.currency.rate')
        
        currency_ids=currency_obj.search(cr,uid,[])
        
        count=0
        for currency in currency_ids :
            count+=1;print count
            vals={'currency_id':currency,'name':date.today().strftime('%Y-%m-%d'),'rate':1.00}
            currency_line_obj.create(cr,uid,vals)
            
        return True

    def write_currency(self,cr,uid,vals):
        currency_obj=self.pool.get('res.currency')
        comp_obj=self.pool.get('res.company')
        curr_ids=currency_obj.search(cr,uid,[])
        count=0
        
        for i in curr_ids :
            count+=1;print count
            cur_get_name=currency_obj.browse(cr,uid,i).name + ' (' + currency_obj.browse(cr,uid,i).company_id.name_convention + ')' 
            
            currency_obj.write(cr,uid,i,{'name':cur_get_name})
        
        return True
        
    
    def create_currency(self,cr,uid,vals):
        ''' Create currency for all companies'''
        currency_obj=self.pool.get('res.currency')
        comp_obj=self.pool.get('res.company')
        curr_ids=currency_obj.search(cr,uid,[])
        count=0
        comp_1=0
        
        for cur in curr_ids :
            print '-----------------------CURRENCY'
            count+=1;print count
            cur_get=currency_obj.browse(cr,uid,cur)
            cur_vals={'name':cur_get.name,'rate_silent':cur_get.rate_silent,'rounding':cur_get.rounding,\
                      'symbol':cur_get.symbol,'accuracy':cur_get.accuracy,'position':cur_get.position,\
                      'base':cur_get.base,'active':True}
            comp_ids=comp_obj.search(cr,uid,[])
            
            for comp in comp_ids :
                
                print '-----------------------CREATING NEW CURRENCY'
                comp_1+=1;print comp_1
                if comp==1:
                    pass
                else:
                   
                    name_1=cur_get.name
                    comp_name=comp_obj.browse(cr,uid,comp).name_convention
                    updated_name=name_1 + ' (' + comp_name +')'
                    cur_vals.update({'company_id':comp,'name':updated_name})
                    currency_obj.create(cr,uid,cur_vals)
                
        return True
    
    
    def assign_companies_to_bank(self,cr,uid,vals):
        '''Assign companies to bank '''
        #import ipdb;ipdb.set_trace()
        bank_obj=self.pool.get('res.partner.bank')
        comp_obj=self.pool.get('res.company')
        bank_ids=bank_obj.search(cr,uid,[])
        
        count=0
        for id in bank_ids :
            count+=1
            partner_id=bank_obj.browse(cr,uid,id).partner_id.id
            if partner_id :
                
                comp_id=comp_obj.search(cr,uid,[('partner_id','=',partner_id)])
                if comp_id :
                    bank_obj.write(cr,uid,id,{'company_id':comp_id[0]})
                    print count
                    print 'ID',id
        return True
                
            
            
    
    
    def write_sequence(self,cr,uid,vals):
        ''' Update sequence name'''
        seq_obj=self.pool.get('ir.sequence')
        seq_ids=seq_obj.search(cr,uid,[])
        
        count=0
        for seq in seq_ids :
            count+=1;print count
            if seq_obj.browse(cr,uid,seq).company_id.id :
                updated_name=seq_obj.browse(cr,uid,seq).name + ' ' + seq_obj.browse(cr,uid,seq).company_id.name_convention
                seq_obj.write(cr,uid,seq,{'name':updated_name})
                    
        return True
    
    def write_account(self,cr,uid,vals):
        ''' Update account name'''
        acc_obj=self.pool.get('account.account')
        acc_ids=acc_obj.search(cr,uid,[])
        
        count=0
        for acc in acc_ids :
            count+=1;print count
            updated_name=acc_obj.browse(cr,uid,acc).name + ' ' + acc_obj.browse(cr,uid,acc).company_id.name_convention
            acc_obj.write(cr,uid,acc,{'name':updated_name})
        return True    
    
    def write_journals(self,cr,uid,vals):
        ''' Update journals name'''
        journal_obj=self.pool.get('account.journal')
        journal_ids=journal_obj.search(cr,uid,[])
        
        count=0
        for journal in journal_ids :
            count+=1;print count
            updated_name=journal_obj.browse(cr,uid,journal).name + ' ' + journal_obj.browse(cr,uid,journal).company_id.name_convention
            journal_obj.write(cr,uid,journal,{'name':updated_name})
        return True



    def create_employee(self,cr, uid,vals):
        
        emp_li=[]
        user_obj=self.pool.get('res.users')
        employee_obj=self.pool.get('hr.employee')
        
        emp_ids=employee_obj.search(cr,uid,[])
        counting=0
        
        for emp_id in  emp_ids:
            emp_user_id=employee_obj.browse(cr,uid,emp_id).user_id.id
            emp_li.append(emp_user_id)
        
        user_ids=user_obj.search(cr,uid,[])
        for user_id in user_ids:
            if user_id ==315:
                
                emp_user_id=employee_obj.browse(cr,uid,emp_id).name
            else:
                pass
            
            if user_id in emp_li :
                pass
            else:
                
                login_name=user_obj.browse(cr,uid,user_id).login
                name_val=login_name.split('@')
                update_login_name=name_val[0]+ ' Test'
                employee_obj.create(cr,uid,{'name':update_login_name,'user_id':user_id})
                counting+=1;print counting;print login_name
        return True
        

    def password(self,cr, uid, vals):
        ''' Test XMLRPC API'''
        #import ipdb;ipdb.set_trace()
        cr.execute(''' update res_users set password=%s where id=%s''',(vals[0],vals[1]))
        
        return True
    
    
    def allowed_companies(self,cr,uid,id,allowed_comp):
        
        cr.execute(''' delete from res_company_users_rel  where user_id=%s''',(id,))
        for comp in allowed_comp :
             
             
            cr.execute(''' insert into res_company_users_rel (cid,user_id) VALUES(%s,%s)''',(comp,id))
            
        return True
         
        
        
    def test_function(self,cr, uid, vals):
        ''' Test XMLRPC API'''
        
        if vals :
            
            return {'key':'XMLRPC api successfull!!!!'}
        
        return {'key':'XMLRPC api successfull!!!!'}
    
    
    def product_search(self,cr, uid, vals):
	uid=1
        ''' Return 1 if product found else 0'''
        ###############FORMAT#################
        #[ {'product_name':'product name'  } ]
#        vals=[ {'product_name':'Enterprise Messaging (Bulk SMS)'  } ]
        
        prod_tmpl_obj=self.pool.get('product.template')
        prod_obj=self.pool.get('product.product')
        
        
        if not (isinstance(vals,(list,dict))) :
            return {'result':0,'error':'Invalid input!! Type should be ARRAY'}
        if vals :
            try:
                
                if len(vals) >1:
                    return {'result':0,'error':'Multiple product detail not accepted'}
                template_id=prod_tmpl_obj.search(cr,uid,[('name','=',vals[0]['product_name'])])
                if template_id :
                    if len(template_id) > 1:
                        return {'result':0,'error':'Multiple products with same name found on Odoo'}
                    
                    prod_id=prod_obj.search(cr,uid,[('product_tmpl_id','=',template_id[0])])
                    if prod_id :
                        return 1
                    
                    else :
                        return 0
                    
                else :
                    return 0
            
            except Exception as e:
                return 0

        return 0
    

    def company_search(self,cr, uid, vals):
	uid=1
        ''' Return 1 if company found else 0'''
        ###############FORMAT#################
        #[ {'company_name':'company name'  } ] 
        #vals=[ {'company_name':'29 Three Holidays Pvt. Ltd'  } ]       
        obj=self.pool.get('res.company')
        
        
        if not (isinstance(vals,(list,dict))) :
            return {'result':0,'error':'Invalid input!! Type should be ARRAY'}
        
        if vals :
            try:
                if len(vals) > 1 :
                    return {'result':0,'error':'Multiple companies detail not accepted'}
                    
                comp_id=obj.search(cr,uid,[('name','=',vals[0]['company_name'])])
                if len(comp_id) > 1 :
                    return {'result':0,'error':'Multiple company with same name found on Odoo'}
                
                if comp_id :
                    return 1

                else:
                    return 0

            except Exception as exception_log:
                return {'result':0,'error':exception_log}
        
        return 0
    
        
    def user_search(self,cr,uid,vals):
	uid=1
        ''' Return 1 If customer exist else 0 '''
        ###############FORMAT#################
        #[ {'odoo_customer_id':odoo_customer_id,'routesms_remark':'routesms_remark'  } ]
        #vals=[ {'odoo_customer_id':'R110085','routesms_remark':'some remark','prepaid':True,'postpaid':False  } ]
       # vals=[ {'odoo_customer_id':'R110002','routesms_remark':'some remark','account_type':'prepaid' } ]
        
        #import ipdb;ipdb.set_trace()
	print '-------------------------------USER           SEARCH-------------------------------------------'
        
        obj=self.pool.get('res.partner')
        
        
        if not (isinstance(vals,(list,dict))) :
            return {'result':0,'error':'Invalid input!! Type should be ARRAY'}
        
        if vals :
            if len(vals) > 1:
                return {'result':0,'error':'Multiple user detail not accepted'}
            try:
                #import ipdb;ipdb.set_trace()
                if vals[0]['account_type']=='prepaid' :
                    cust_type=[('prepaid','=',True),('postpaid','=',False)]
                    
                elif vals[0]['account_type']=='postpaid' :
                    cust_type=[('postpaid','=',True),('prepaid','=',False),]
                    
                else :
                    return {'result':0,'error':'Invalid account type'}
                
                partner_id=obj.search(cr,uid,[('partner_sequence','=',vals[0]['odoo_customer_id']),cust_type[0]])
                if len(partner_id) > 1 :
                    return {'result':0,'error':'Multiple partner with same ID found on Odoo'}
                if partner_id :
                    obj.write(cr,uid,partner_id,{'routesms_remark':vals[0]['routesms_remark']})
                    return 1
                else:
                    return 0
            
            except Exception as e:
                return 0
        return 0
    
    def default_emp_id(self, cr, uid, context=None):
        '''Return current employee associated with  '''
        # ipdb;ipdb.set_trace()
	uid=1
        if uid : 
            
            emp_id=self.pool.get('hr.employee').search(cr,1,[('user_id','=',uid)])
            if emp_id :
                if len(emp_id) >1 :
                    raise osv.except_osv(_('Multiple users assigned to employee!'), _(""))
                
                return emp_id[0]
            
            else :
                return 0
        return 0
    


    def user_invoice_test123(self,cr,uid,vals):
        ''' return 1 if invoice created else 0 on fail'''
        uid=1    
        ############FORMAT#################
# [ {'params': {'currency_id': 'INR', 'due_date': 'yy-mm-dd', 'user_id': 'Saleperson', 'product_detail': [{'price_unit': 0.0, 'product_id': 'product name', 'quantity': 1}], 'partner_bank_id': 'Account Number', 'invoice_date': 'yy-mm-dd', 'partner_id': 'your_customer_id','routesms_remark':'Remark', 'company_id': 'Company Name'}} ]
#
#         vals=[ {'params': {'credit_type':'credit_type','transaction_type':'out_invoice','currency_id': 'INR', 'due_date': '2015-01-10', 'saleperson_name': 'Karishma Ghaghda',\
#                             
#             'product_detail': [{'price_unit': 2000.0, 'product_name': 'Enterprise Messaging (Bulk SMS)', \
#             'quantity': 1}], 'invoice_date': '2015-03-30', 'partner_id': 'R110054','routesms_remark':'some remark', 'company_id': \
#             'RSL (Group)'}} ]
        
        currency_obj=self.pool.get('res.currency')
        users_obj=self.pool.get('res.users')
        bank_obj=self.pool.get('res.partner.bank')
        partner_obj=self.pool.get('res.partner')
        company_obj=self.pool.get('res.company')
        invoice_obj=self.pool.get('account.invoice')
        invoice_line_obj=self.pool.get('account.invoice.line')
        prod_tmpl_obj=self.pool.get('product.template')
        prod_obj=self.pool.get('product.product')
        
        invoice={}
        invoice_line={}
        
        #import ipdb;ipdb.set_trace()
        if not (isinstance(vals,(list,dict))) :
            return {'result':0,'error':'Invalid input!! Type should be ARRAY'}
        
        if vals :
            try :
         #       import ipdb;ipdb.set_trace()
                if len(vals) > 1 :
                    return {'result':0,'error':'Multiple Invoices not accepted'}
                
                for val in vals :
                    invoice.update({'credit_type':val['params']['credit_type']})
                    transaction_type=["out_invoice","out_refund","in_invoice","in_refund"]
                    if (val['params']['transaction_type'] in transaction_type): 
                        
                        invoice.update({'type':val['params']['transaction_type']})
                    
                    else:
                        return {'result':0,'error':'Invalid transaction type'}
                        
                    
#                     #assign journal
#                     
#                     
#                     
#                     if invoice['type'] =='out_refund' :
#                         invoice.update({'journal_id':3})
#                         
#                     elif invoice['type'] =='in_invoice' :
#                         invoice.update({'journal_id':2})
#                         
#                     elif invoice['type'] =='in_refund' :
#                         invoice.update({'journal_id':4})
                        
                                        
                    #assign dates
                    
                    invoice.update({'date_invoice':val['params']['invoice_date']})
                    invoice.update({'date_due':val['params']['due_date']})
                    
                    
                    #search currency
                    currency_id=currency_obj.search(cr,uid,[('name','=',val['params']['currency_id'])])
                    if currency_id :
                        invoice.update({'currency_id':currency_id[0]})
                        
                    else :
                        
                        return {'result':0,'error':'Currency not found or invalid currency'}
                    


                    

                    
#                     #product search
#                     
#                     template_id=prod_tmpl_obj.search(cr,uid,[('name','=',val['params']['product_detail'][0]['product_name'])])
#                     if template_id :
#                         
#                         if len(template_id) > 1:
#                             return {'result':0,'error':'Multiple products with same name found on Odoo'}
# 
#                         product_id=prod_obj.search(cr,uid,[('product_tmpl_id','=',template_id[0])])    
#                         
#                         if product_id :
#                             invoice_line.update({'product_id':product_id[0]})
#                             invoice_line.update({'name':val['params']['product_detail'][0]['product_name']})
#                             invoice_line.update({'quantity':val['params']['product_detail'][0]['quantity']})
#                             
#                             if invoice['type'] in ['out_invoice','out_refund']:
#                                 invoice_line.update({'account_id':189})
#                                 
#                             
#                                 
#                             invoice_line.update({'price_unit':val['params']['product_detail'][0]['price_unit']})
#                         
#                         else :
#                             
#                             return {'result':0,'error':'Product not found'}
#                     #search bank
#                     
#                     bank_id=bank_obj.search(cr,uid,[('acc_number','=',val['params']['partner_bank_id'])])
#                     if bank_id :
#                         
#                         invoice.update({'partner_bank_id':bank_id[0]})
#                         
#                     else :
#                         
#                         return {'result':0,'error':'Bank Account number found'}
                    
                    #search partner
                    
                    partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',val['params']['partner_id'])])
                    if partner_id:
                        partner_obj.write(cr,uid,partner_id,{'routesms_remark':val['params']['routesms_remark']})
                        
                        invoice.update({'partner_id':partner_id[0]})
                        invoice.update({'remark':val['params']['routesms_remark']})
                    
                    else :
                        return {'result':0,'error':'Customer not found'}
                    

                    #search user/saleperson
#                     saleperson_id=partner_obj.search(cr,uid,[('name','=',val['params']['saleperson_name'])])
#                     if saleperson_id :
#                         
#                         user_id=users_obj.search(cr,uid,[('partner_id','=',saleperson_id[0])])
#                         if user_id :
#                             invoice.update({'user_id':user_id[0]})
#                             
#                         else :
#                             
#                             return {'result':0,'error':'Saleperson/User not found '}
#                     
#                     else :
#                         
#                             return {'result':0,'error':'Saleperson/User not found '}
# 
#                     
                    
                    saleperson_id=partner_obj.browse(cr,uid,partner_id[0]).user_id.id
                    if saleperson_id :
                        invoice.update({'user_id':saleperson_id})
                        
                    else:
                        invoice.update({'user_id':1})
                        #return {'result':0,'error':'Saleperson/User not found '}
                    

                    #emloyee id search
                    # ipdb;ipdb.set_trace()
                    emp_id=self.default_emp_id(cr,invoice['user_id'],context=None)
                    if emp_id :
                        if isinstance(emp_id,(int)):
                            invoice.update({'employee_id':emp_id})
                        else:
                            return {'result':0,'error':'No user is assigned to Employee '}
                    
                        
                    else:
                         return {'result':0,'error':'No user is assigned to Employee '}
                                         
                    #assign partner account id
                    
                    if invoice['type'] in ['out_invoice','out_refund' ] :
                        account_id=partner_obj.browse(cr,uid,partner_id).property_account_receivable.id
                        
                        
                    elif invoice['type'] in ['in_invoice','in_refund' ]:
                        account_id=partner_obj.browse(cr,uid,partner_id).property_account_payable.id
                        
                    else :
                        return {'result':0,'error':'Account not assigned to user'}
                    
                    invoice.update({'account_id':account_id})
                    #search company
                    
                    company_id=company_obj.search(cr,uid,[('name','=',val['params']['company_id'])])
                    if company_id:
                        invoice.update({'company_id':company_id[0]})
                    
                    else :
                        return {'result':0,'error':'Company not found'}



                    #assign journal
                    company_id=company_id[0]
                    
                    import ipdb;ipdb.set_trace()
                    if val['params']['od'] : 

                        invoice.update({'company_id':1})
                        
                        
                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':3})
                            invoice.update({'product_account':189})
                            invoice.update({'account_id':145})
                            
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':2})
                            invoice.update({'product_account':199})
                            invoice.update({'account_id':37})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':4})
                            invoice.update({'product_account':199})
                            invoice.update({'account_id':37})
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':1})
                            invoice.update({'product_account':189})
                            invoice.update({'account_id':145})
                        
                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}
                         
                    else : 
                        
                    
                        if company_id == 1 : #RSL Group
                            
                         
                            if invoice['type'] =='out_refund' :
                                invoice.update({'journal_id':3})
                                invoice.update({'product_account':189})
                                invoice.update({'account_id':145})
                                
                                
                            elif invoice['type'] =='in_invoice' :
                                invoice.update({'journal_id':2})
                                invoice.update({'product_account':199})
                                invoice.update({'account_id':37})
                                
                            elif invoice['type'] =='in_refund' :
                                invoice.update({'journal_id':4})
                                invoice.update({'product_account':199})
                                invoice.update({'account_id':37})
                                
                            elif invoice['type'] =='out_invoice' :
                                invoice.update({'journal_id':1})
                                invoice.update({'product_account':189})
                                invoice.update({'account_id':145})
                            
                            else :
                                
                                return {'result':0,'error':'Invalid Invoice Type format'}
                                
                                                            
    #                     elif company_id == 3 : # 29 THREE HOLIDAYS PVT. LTD 
    # 
    #                         if invoice['type'] =='out_refund' :
    #                             invoice.update({'journal_id':12})
    #                             
    #                         elif invoice['type'] =='in_invoice' :
    #                             invoice.update({'journal_id':149})
    #                             
    #                         elif invoice['type'] =='in_refund' :
    #                             invoice.update({'journal_id':13})
    #                             
    #                         elif invoice['type'] =='out_invoice' :
    #                             invoice.update({'journal_id':148})                        
    # 
    #                         else :
    #                             
    #                             return {'result':0,'error':'Invalid Invoice Type format'}                        
                            
                        elif company_id == 4 : # AHANA ENTERTAINMENT PVT. LTD 
    
                            if invoice['type'] =='out_refund' :
                                invoice.update({'journal_id':20})
                                invoice.update({'product_account':729})
                                invoice.update({'account_id':685})
                                
                            elif invoice['type'] =='in_invoice' :
                                invoice.update({'journal_id':19})
                                invoice.update({'product_account':739})
                                invoice.update({'account_id':577})
                                
                            elif invoice['type'] =='in_refund' :
                                invoice.update({'journal_id':21})
                                invoice.update({'product_account':739})
                                invoice.update({'account_id':577})
                                
                            elif invoice['type'] =='out_invoice' :
                                invoice.update({'journal_id':18})  
                                invoice.update({'product_account':729})
                                invoice.update({'account_id':685})                      
    
                            else :
                                
                                return {'result':0,'error':'Invalid Invoice Type format'}                        
                                                    
    
                        elif company_id == 5 : # GRAPHIXIDE INC
    
                            if invoice['type'] =='out_refund' :
                                invoice.update({'journal_id':68})
                                invoice.update({'product_account':2349}) 
                                invoice.update({'account_id':2305})
                                
                            elif invoice['type'] =='in_invoice' :
                                invoice.update({'journal_id':67})
                                invoice.update({'product_account':2359})
                                invoice.update({'account_id':2197})
                                
                            elif invoice['type'] =='in_refund' :
                                invoice.update({'journal_id':69})
                                invoice.update({'product_account':2359})
                                invoice.update({'account_id':2197})
                                
                            elif invoice['type'] =='out_invoice' :
                                invoice.update({'journal_id':66})       
                                invoice.update({'product_account':2349})                  
                                invoice.update({'account_id':2305})
                            else :
                                
                                return {'result':0,'error':'Invalid Invoice Type format'}                         
                        
    
                        elif company_id == 6 : #  GRAPHIXIDE SERVICES PVT.LTD
    
                            if invoice['type'] =='out_refund' :
                                invoice.update({'journal_id':28})
                                invoice.update({'product_account':999}) 
                                invoice.update({'account_id':955})
                                
                            elif invoice['type'] =='in_invoice' :
                                invoice.update({'journal_id':27})
                                invoice.update({'product_account':1009}) 
                                invoice.update({'account_id':847})
                                
                            elif invoice['type'] =='in_refund' :
                                invoice.update({'journal_id':29})
                                invoice.update({'product_account':1009})
                                invoice.update({'account_id':847}) 
                                
                            elif invoice['type'] =='out_invoice' :
                                invoice.update({'journal_id':26})       
                                invoice.update({'product_account':999})
                                invoice.update({'account_id':955})                  
    
                            else :
                                
                                return {'result':0,'error':'Invalid Invoice Type format'}                         
                        
                        
                        elif company_id == 7 : #  REMARKABLE INNOVATIONS 
    
                            if invoice['type'] =='out_refund' :
                                invoice.update({'journal_id':76})
                                invoice.update({'product_account':2619}) 
                                invoice.update({'account_id':2575})
                                
                            elif invoice['type'] =='in_invoice' :
                                invoice.update({'journal_id':75})
                                invoice.update({'product_account':2629}) 
                                invoice.update({'account_id':2467})
                                
                            elif invoice['type'] =='in_refund' :
                                invoice.update({'journal_id':77})
                                invoice.update({'product_account':2629}) 
                                invoice.update({'account_id':2467})
                                
                            elif invoice['type'] =='out_invoice' :
                                invoice.update({'journal_id':74})       
                                invoice.update({'product_account':2619})
                                invoice.update({'account_id':2575})                  
    
                            else :
                                
                                return {'result':0,'error':'Invalid Invoice Type format'}                         
                                            
                        elif company_id == 8 : #  ROUTESMS SOLUTIONS NIGERIA LIMITED
    
                            if invoice['type'] =='out_refund' :
                                invoice.update({'journal_id':84})
                                invoice.update({'product_account':2889}) 
                                invoice.update({'account_id':2845})  
                                
                            elif invoice['type'] =='in_invoice' :
                                invoice.update({'journal_id':83})
                                invoice.update({'product_account':2899})
                                invoice.update({'account_id':2737})  
                                
                            elif invoice['type'] =='in_refund' :
                                invoice.update({'journal_id':85})
                                invoice.update({'product_account':2899})
                                invoice.update({'account_id':2737})  
                                
                            elif invoice['type'] =='out_invoice' :
                                invoice.update({'journal_id':82})       
                                invoice.update({'product_account':2889})  
                                invoice.update({'account_id':2845})                  
    
                            else :
                                
                                return {'result':0,'error':'Invalid Invoice Type format'}                         
    
    
                        elif company_id == 9 : #  ROUTESMS SOLUTIONS FZE
    
                            if invoice['type'] =='out_refund' :
                                invoice.update({'journal_id':92})
                                invoice.update({'product_account':3159}) 
                                invoice.update({'account_id':3115})
                                
                            elif invoice['type'] =='in_invoice' :
                                invoice.update({'journal_id':91})
                                invoice.update({'product_account':3169}) 
                                invoice.update({'account_id':3007})
                                
                            elif invoice['type'] =='in_refund' :
                                invoice.update({'journal_id':93})
                                invoice.update({'product_account':3169})
                                invoice.update({'account_id':3007}) 
                                
                            elif invoice['type'] =='out_invoice' :
                                invoice.update({'journal_id':90})       
                                invoice.update({'product_account':3159})
                                invoice.update({'account_id':3115})                  
    
                            else :
                                
                                return {'result':0,'error':'Invalid Invoice Type format'}                                          
                                            
                        elif company_id == 10 : #  ROUTESMS SOLUTIONS LIMITED 
    
                            if invoice['type'] =='out_refund' :
                                invoice.update({'journal_id':36})
                                invoice.update({'product_account':1269})
                                invoice.update({'account_id':1225}) 
                                
                            elif invoice['type'] =='in_invoice' :
                                invoice.update({'journal_id':35})
                                invoice.update({'product_account':1279})
                                invoice.update({'account_id':1117}) 
                                
                            elif invoice['type'] =='in_refund' :
                                invoice.update({'journal_id':37})
                                invoice.update({'product_a13479ccount':1279})
                                invoice.update({'account_id':1117}) 
                                
                            elif invoice['type'] =='out_invoice' :
                                invoice.update({'journal_id':34})       
                                invoice.update({'product_account':1269}) 
                                invoice.update({'account_id':1225})                  
    
                            else :
                                
                                return {'result':0,'error':'Invalid Invoice Type format'}                                         
                                        
                        elif company_id == 11 : #  ROUTESMS SOLUTIONS (UK) LIMITED
    
                            if invoice['type'] =='out_refund' :
                                invoice.update({'journal_id':100})
                                invoice.update({'product_account':3429}) 
                                invoice.update({'account_id':3385})       
                                
                                
                            elif invoice['type'] =='in_invoice' :
                                invoice.update({'journal_id':99})
                                invoice.update({'product_account':3439})
                                invoice.update({'account_id':3277}) 
                                
                            elif invoice['type'] =='in_refund' :
                                invoice.update({'journal_id':101})
                                invoice.update({'product_account':3439})
                                invoice.update({'account_id':3277}) 
                                
                                
                            elif invoice['type'] =='out_invoice' :
    #                            invoice.update({'journal_id':98}) 
                                invoice.update({'journal_id':211})
                                invoice.update({'product_account':3429})
                                invoice.update({'account_id':3385})                      
    
                            else :
                                
                                return {'result':0,'error':'Invalid Invoice Type format'}                                         
                                        
    
    
                        elif company_id == 12 : #  ROUTEVOICE LIMITED
    
                            if invoice['type'] =='out_refund' :
                                invoice.update({'journal_id':108})
                                invoice.update({'product_account':3699})
                                invoice.update({'account_id':3655})      
                                  
                                
                            elif invoice['type'] =='in_invoice' :
                                invoice.update({'journal_id':107})
                                invoice.update({'product_account':3709})
                                invoice.update({'account_id':3547})
                                
                            elif invoice['type'] =='in_refund' :
                                invoice.update({'journal_id':109})
                                invoice.update({'product_account':3709})
                                invoice.update({'account_id':3547})
                                
                            elif invoice['type'] =='out_invoice' :
                                invoice.update({'journal_id':106}) 
                                invoice.update({'product_account':3699})
                                invoice.update({'account_id':3655})                      
    
                            else :
                                
                                return {'result':0,'error':'Invalid Invoice Type format'}                                         
                                                                            
    
                        elif company_id == 13 : #  SANRAJ INFRA DEVELOPERS PVT. LTD 
    
                            if invoice['type'] =='out_refund' :
                                invoice.update({'journal_id':108})
                                invoice.update({'product_account':1539})
                                invoice.update({'account_id':1495})        
                                
                            elif invoice['type'] =='in_invoice' :
                                invoice.update({'journal_id':107})
                                invoice.update({'product_account':1549})
                                invoice.update({'account_id':1387})  
                                
                            elif invoice['type'] =='in_refund' :
                                invoice.update({'journal_id':109})
                                invoice.update({'product_account':1549})
                                invoice.update({'account_id':1387})  
                                
                            elif invoice['type'] =='out_invoice' :
                                invoice.update({'journal_id':42}) 
                                invoice.update({'product_account':1539})  
                                invoice.update({'account_id':1495})                    
    
                            else :
                                
                                return {'result':0,'error':'Invalid Invoice Type format'}                                         
                                                        
    
                        elif company_id == 14 : #  SPECTRA TELESERVICES PVT. LTD 
    
                            if invoice['type'] =='out_refund' :
                                invoice.update({'journal_id':52})
                                invoice.update({'product_account':1809})  
                                invoice.update({'account_id':1765})     
                                
                            elif invoice['type'] =='in_invoice' :
                                invoice.update({'journal_id':51})
                                invoice.update({'product_account':1819})
                                invoice.update({'account_id':1657}) 
      
      
                            elif invoice['type'] =='in_refund' :
                                invoice.update({'journal_id':53})
                                invoice.update({'product_account':1819})
                                invoice.update({'account_id':1657})
                                
                            elif invoice['type'] =='out_invoice' :
                                invoice.update({'journal_id':50}) 
                                invoice.update({'product_account':1809})
                                invoice.update({'account_id':1765})                      
    
                            else :
                                
                                return {'result':0,'error':'Invalid Invoice Type format'}      
                                                                                              
                        elif company_id == 15 : #  SPER
    
                            if invoice['type'] =='out_refund' :
                                invoice.update({'journal_id':116})
                                invoice.update({'product_account':3969})  
                                invoice.update({'account_id':3925})      
                                
                            elif invoice['type'] =='in_invoice' :
                                invoice.update({'journal_id':115})
                                invoice.update({'product_account':3979})
                                invoice.update({'account_id':3817})
                                
                            elif invoice['type'] =='in_refund' :
                                invoice.update({'journal_id':117})
                                invoice.update({'product_account':3979})
                                invoice.update({'account_id':3817})
                                
                            elif invoice['type'] =='out_invoice' :
                                invoice.update({'journal_id':114}) 
                                invoice.update({'product_account':3969})
                                invoice.update({'account_id':3925})                      
    
                            else :
                                
                                return {'result':0,'error':'Invalid Invoice Type format'}                                                                                             
    
                        elif company_id == 16 : #  SPHERE EDGE CONSULTING INDIA PVT. LTD
    
                            if invoice['type'] =='out_refund' :
                                invoice.update({'journal_id':60})
                                invoice.update({'product_account':2079})       
                                invoice.update({'account_id':2035}) 
                                
                            elif invoice['type'] =='in_invoice' :
                                invoice.update({'journal_id':59})
                                invoice.update({'product_account':2089})
                                invoice.update({'account_id':1927}) 
                                
                            elif invoice['type'] =='in_refund' :
                                invoice.update({'journal_id':61})
                                invoice.update({'product_account':2089})
                                invoice.update({'account_id':1927}) 
                                
                            elif invoice['type'] =='out_invoice' :
                                invoice.update({'journal_id':58}) 
                                invoice.update({'product_account':2079})
                                invoice.update({'account_id':2035})                      
    
                            else :
                                
                                return {'result':0,'error':'Invalid Invoice Type format'} 
                    
                    
                        else :
                            
                            return {'result':0,'error':'Company - Journal Error'}
                    
                            
                    #product search
                    
                    template_id=prod_tmpl_obj.search(cr,uid,[('name','=',val['params']['product_detail'][0]['product_name'])])
                    if template_id :
                        
                        if len(template_id) > 1:
                            return {'result':0,'error':'Multiple products with same name found on Odoo'}

                        product_id=prod_obj.search(cr,uid,[('product_tmpl_id','=',template_id[0])])    
                        
                        if product_id :
                            invoice_line.update({'product_id':product_id[0]})
                            invoice_line.update({'name':val['params']['product_detail'][0]['product_name']})
                            invoice_line.update({'quantity':val['params']['product_detail'][0]['quantity']})
                            invoice_line.update({'account_id':invoice['product_account']})                              
                            invoice_line.update({'price_unit':val['params']['product_detail'][0]['price_unit']})
                        
                        else :
                            
                            return {'result':0,'error':'Product not found'}


                                   
                    #create invoice 
                    try :
                        
                          
                        new_invoice_id=invoice_obj.create(cr,uid,invoice)
                        
                    except Exception as invoice_create_exception :
                        return {'result':0,'error':invoice_create_exception}
                    
                    
                    #create invoice line
                    try :
                        
                        invoice_obj.write(cr, uid, [new_invoice_id], {'invoice_line': [(0, 0, invoice_line)]})
                        return 1
                        
                    except Exception as invoice_line_create_exception :
                        return {'result':0,'error':invoice_line_create_exception}
                
                    
                
            except Exception as exception_log :
                return {'result':0,'error':exception_log}
                            
        return 0     






            
    def user_invoice(self,cr,uid,vals):
        ''' return 1 if invoice created else 0 on fail'''
    	uid=1    
       # import ipdb;ipdb.set_trace()
	print '----------------------------------USER INVOICE-----------------------------'
        ############FORMAT#################
# [ {'params': {'currency_id': 'INR', 'due_date': 'yy-mm-dd', 'user_id': 'Saleperson', 'product_detail': [{'price_unit': 0.0, 'product_id': 'product name', 'quantity': 1}], 'partner_bank_id': 'Account Number', 'invoice_date': 'yy-mm-dd', 'partner_id': 'your_customer_id','routesms_remark':'Remark', 'company_id': 'Company Name'}} ]
#
#         vals=[ {'params': {'credit_type':'credit_type','transaction_type':'out_invoice','currency_id': 'INR', 'due_date': '2015-01-10', 'saleperson_name': 'Karishma Ghaghda',\
#                             
#             'product_detail': [{'price_unit': 2000.0, 'product_name': 'Enterprise Messaging (Bulk SMS)', \
#             'quantity': 1}], 'invoice_date': '2015-03-30', 'partner_id': 'R110054','routesms_remark':'some remark', 'company_id': \
#             'RSL (Group)'}} ]
        
        currency_obj=self.pool.get('res.currency')
        users_obj=self.pool.get('res.users')
        bank_obj=self.pool.get('res.partner.bank')
        partner_obj=self.pool.get('res.partner')
        company_obj=self.pool.get('res.company')
        invoice_obj=self.pool.get('account.invoice')
        invoice_line_obj=self.pool.get('account.invoice.line')
        prod_tmpl_obj=self.pool.get('product.template')
        prod_obj=self.pool.get('product.product')
        
        invoice={}
        invoice_line={}
        
        #import ipdb;ipdb.set_trace()
        if not (isinstance(vals,(list,dict))) :
            return {'result':0,'error':'Invalid input!! Type should be ARRAY'}
        
        if vals :
            try :
         #       import ipdb;ipdb.set_trace()
                if len(vals) > 1 :
                    return {'result':0,'error':'Multiple Invoices not accepted'}
                
                for val in vals :
                    invoice.update({'credit_type':val['params']['credit_type']})
                    transaction_type=["out_invoice","out_refund","in_invoice","in_refund"]
                    if (val['params']['transaction_type'] in transaction_type): 
                        
                        invoice.update({'type':val['params']['transaction_type']})
                    
                    else:
                        return {'result':0,'error':'Invalid transaction type'}
                        
                    
#                     #assign journal
#                     
#                     
#                     
#                     if invoice['type'] =='out_refund' :
#                         invoice.update({'journal_id':3})
#                         
#                     elif invoice['type'] =='in_invoice' :
#                         invoice.update({'journal_id':2})
#                         
#                     elif invoice['type'] =='in_refund' :
#                         invoice.update({'journal_id':4})
                        
                                        
                    #assign dates
                    
                    invoice.update({'date_invoice':val['params']['invoice_date']})
                    invoice.update({'date_due':val['params']['due_date']})
                    
                    
                    #search currency
                    currency_id=currency_obj.search(cr,uid,[('name','=',val['params']['currency_id'])])
                    if currency_id :
                        invoice.update({'currency_id':currency_id[0]})
                        
                    else :
                        
                        return {'result':0,'error':'Currency not found or invalid currency'}
                    


                    

                    
#                     #product search
#                     
#                     template_id=prod_tmpl_obj.search(cr,uid,[('name','=',val['params']['product_detail'][0]['product_name'])])
#                     if template_id :
#                         
#                         if len(template_id) > 1:
#                             return {'result':0,'error':'Multiple products with same name found on Odoo'}
# 
#                         product_id=prod_obj.search(cr,uid,[('product_tmpl_id','=',template_id[0])])    
#                         
#                         if product_id :
#                             invoice_line.update({'product_id':product_id[0]})
#                             invoice_line.update({'name':val['params']['product_detail'][0]['product_name']})
#                             invoice_line.update({'quantity':val['params']['product_detail'][0]['quantity']})
#                             
#                             if invoice['type'] in ['out_invoice','out_refund']:
#                                 invoice_line.update({'account_id':189})
#                                 
#                             
#                                 
#                             invoice_line.update({'price_unit':val['params']['product_detail'][0]['price_unit']})
#                         
#                         else :
#                             
#                             return {'result':0,'error':'Product not found'}
#                     #search bank
#                     
#                     bank_id=bank_obj.search(cr,uid,[('acc_number','=',val['params']['partner_bank_id'])])
#                     if bank_id :
#                         
#                         invoice.update({'partner_bank_id':bank_id[0]})
#                         
#                     else :
#                         
#                         return {'result':0,'error':'Bank Account number found'}
                    
                    #search partner
                    
#                    partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',val['params']['partner_id'])])
		    #import ipdb;ipdb.set_trace()
                    partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',val['params']['partner_id']),\
                                                          ('active','=',True),('is_company','=',True)])
                    if partner_id:
                        partner_obj.write(cr,uid,partner_id,{'routesms_remark':val['params']['routesms_remark']})
                        
                        invoice.update({'partner_id':partner_id[0]})
                        invoice.update({'remark':val['params']['routesms_remark']})

                        ###Fetch partner country
			
                        partner_value=partner_obj.browse(cr,uid,partner_id[0])
                        if partner_value.country_id  :
                            invoice.update({'partner_country':partner_value.country_id.name})
                    
                    else :
#                        return {'result':0,'error':'Customer not found'}
                        return {'result':-1,'error':'Customer Not Found or Customer Might Be Inactive'}
                    

                    #search user/saleperson
#                     saleperson_id=partner_obj.search(cr,uid,[('name','=',val['params']['saleperson_name'])])
#                     if saleperson_id :
#                         
#                         user_id=users_obj.search(cr,uid,[('partner_id','=',saleperson_id[0])])
#                         if user_id :
#                             invoice.update({'user_id':user_id[0]})
#                             
#                         else :
#                             
#                             return {'result':0,'error':'Saleperson/User not found '}
#                     
#                     else :
#                         
#                             return {'result':0,'error':'Saleperson/User not found '}
# 
#                     
                    
                    saleperson_id=partner_obj.browse(cr,uid,partner_id[0]).user_id.id
                    if saleperson_id :
                        invoice.update({'user_id':saleperson_id})
                        
                    else:
                        invoice.update({'user_id':1})
                        #return {'result':0,'error':'Saleperson/User not found '}
                    

                    #emloyee id search
                    # ipdb;ipdb.set_trace()
                    emp_id=self.default_emp_id(cr,invoice['user_id'],context=None)
                    if emp_id :
                        if isinstance(emp_id,(int)):
                            invoice.update({'employee_id':emp_id})
                        else:
                            return {'result':0,'error':'No user is assigned to Employee '}
                    
                        
                    else:
                         return {'result':0,'error':'No user is assigned to Employee '}
                                         
                    #assign partner account id
                    
                    if invoice['type'] in ['out_invoice','out_refund' ] :
                        account_id=partner_obj.browse(cr,uid,partner_id).property_account_receivable.id
                        
                        
                    elif invoice['type'] in ['in_invoice','in_refund' ]:
                        account_id=partner_obj.browse(cr,uid,partner_id).property_account_payable.id
                        
                    else :
                        return {'result':0,'error':'Account not assigned to user'}
                    
                    invoice.update({'account_id':account_id})
                    #search company
                    
                    company_id=company_obj.search(cr,uid,[('name','=',val['params']['company_id'])])
                    if company_id:
                        invoice.update({'company_id':company_id[0]})
                    
                    else :
                        return {'result':0,'error':'Company not found'}



                    #assign journal
                    company_id=company_id[0]
                    if company_id == 1 : #RSL Group
                        
                     
                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':3})
                            invoice.update({'product_account':189})
                            invoice.update({'account_id':145})
                            
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':2})
                            invoice.update({'product_account':199})
                            invoice.update({'account_id':37})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':4})
                            invoice.update({'product_account':199})
                            invoice.update({'account_id':37})
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':1})
                            invoice.update({'product_account':189})
                            invoice.update({'account_id':145})
                        
                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}
                            
                                                        
#                     elif company_id == 3 : # 29 THREE HOLIDAYS PVT. LTD 
# 
#                         if invoice['type'] =='out_refund' :
#                             invoice.update({'journal_id':12})
#                             
#                         elif invoice['type'] =='in_invoice' :
#                             invoice.update({'journal_id':149})
#                             
#                         elif invoice['type'] =='in_refund' :
#                             invoice.update({'journal_id':13})
#                             
#                         elif invoice['type'] =='out_invoice' :
#                             invoice.update({'journal_id':148})                        
# 
#                         else :
#                             
#                             return {'result':0,'error':'Invalid Invoice Type format'}                        
                        
                    elif company_id == 4 : # AHANA ENTERTAINMENT PVT. LTD 

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':20})
                            invoice.update({'product_account':729})
                            invoice.update({'account_id':685})
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':19})
                            invoice.update({'product_account':739})
                            invoice.update({'account_id':577})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':21})
                            invoice.update({'product_account':739})
                            invoice.update({'account_id':577})
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':18})  
                            invoice.update({'product_account':729})
                            invoice.update({'account_id':685})                      

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                        
                                                

                    elif company_id == 5 : # GRAPHIXIDE INC

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':68})
                            invoice.update({'product_account':2349}) 
                            invoice.update({'account_id':2305})
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':67})
                            invoice.update({'product_account':2359})
                            invoice.update({'account_id':2197})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':69})
                            invoice.update({'product_account':2359})
                            invoice.update({'account_id':2197})
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':66})       
                            invoice.update({'product_account':2349})                  
                            invoice.update({'account_id':2305})
                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                         
                    

                    elif company_id == 6 : #  GRAPHIXIDE SERVICES PVT.LTD

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':28})
                            invoice.update({'product_account':999}) 
                            invoice.update({'account_id':955})
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':27})
                            invoice.update({'product_account':1009}) 
                            invoice.update({'account_id':847})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':29})
                            invoice.update({'product_account':1009})
                            invoice.update({'account_id':847}) 
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':26})       
                            invoice.update({'product_account':999})
                            invoice.update({'account_id':955})                  

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                         
                    
                    
                    elif company_id == 7 : #  REMARKABLE INNOVATIONS 

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':76})
                            invoice.update({'product_account':2619}) 
                            invoice.update({'account_id':2575})
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':75})
                            invoice.update({'product_account':2629}) 
                            invoice.update({'account_id':2467})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':77})
                            invoice.update({'product_account':2629}) 
                            invoice.update({'account_id':2467})
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':74})       
                            invoice.update({'product_account':2619})
                            invoice.update({'account_id':2575})                  

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                         
                                        
                    elif company_id == 8 : #  ROUTESMS SOLUTIONS NIGERIA LIMITED

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':84})
                            invoice.update({'product_account':2889}) 
                            invoice.update({'account_id':2845})  
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':83})
                            invoice.update({'product_account':2899})
                            invoice.update({'account_id':2737})  
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':85})
                            invoice.update({'product_account':2899})
                            invoice.update({'account_id':2737})  
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':82})       
                            invoice.update({'product_account':2889})  
                            invoice.update({'account_id':2845})                  

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                         


                    elif company_id == 9 : #  ROUTESMS SOLUTIONS FZE

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':92})
                            invoice.update({'product_account':3159}) 
                            invoice.update({'account_id':3115})
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':91})
                            invoice.update({'product_account':3169}) 
                            invoice.update({'account_id':3007})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':93})
                            invoice.update({'product_account':3169})
                            invoice.update({'account_id':3007}) 
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':90})       
                            invoice.update({'product_account':3159})
                            invoice.update({'account_id':3115})                  

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                                          
                                        
                    elif company_id == 10 : #  ROUTESMS SOLUTIONS LIMITED 

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':36})
                            invoice.update({'product_account':1269})
                            invoice.update({'account_id':1225}) 
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':35})
                            invoice.update({'product_account':1279})
                            invoice.update({'account_id':1117}) 
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':37})
                            invoice.update({'product_a13479ccount':1279})
                            invoice.update({'account_id':1117}) 
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':34})       
                            invoice.update({'product_account':1269}) 
                            invoice.update({'account_id':1225})                  

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                                         
                                    
                    elif company_id == 11 : #  ROUTESMS SOLUTIONS (UK) LIMITED

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':100})
                            invoice.update({'product_account':3429}) 
                            invoice.update({'account_id':3385})       
                            
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':99})
                            invoice.update({'product_account':3439})
                            invoice.update({'account_id':3277}) 
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':101})
                            invoice.update({'product_account':3439})
                            invoice.update({'account_id':3277}) 
                            
                            
                        elif invoice['type'] =='out_invoice' :
#                            invoice.update({'journal_id':98}) 
                            invoice.update({'journal_id':211})
                            invoice.update({'product_account':3429})
                            invoice.update({'account_id':3385})                      

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                                         
                                    


                    elif company_id == 12 : #  ROUTEVOICE LIMITED

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':108})
                            invoice.update({'product_account':3699})
                            invoice.update({'account_id':3655})      
                              
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':107})
                            invoice.update({'product_account':3709})
                            invoice.update({'account_id':3547})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':109})
                            invoice.update({'product_account':3709})
                            invoice.update({'account_id':3547})
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':106}) 
                            invoice.update({'product_account':3699})
                            invoice.update({'account_id':3655})                      

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                                         
                                                                        

                    elif company_id == 13 : #  SANRAJ INFRA DEVELOPERS PVT. LTD 

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':108})
                            invoice.update({'product_account':1539})
                            invoice.update({'account_id':1495})        
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':107})
                            invoice.update({'product_account':1549})
                            invoice.update({'account_id':1387})  
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':109})
                            invoice.update({'product_account':1549})
                            invoice.update({'account_id':1387})  
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':42}) 
                            invoice.update({'product_account':1539})  
                            invoice.update({'account_id':1495})                    

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                                         
                                                    

                    elif company_id == 14 : #  SPECTRA TELESERVICES PVT. LTD 

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':52})
                            invoice.update({'product_account':1809})  
                            invoice.update({'account_id':1765})     
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':51})
                            invoice.update({'product_account':1819})
                            invoice.update({'account_id':1657}) 
  
  
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':53})
                            invoice.update({'product_account':1819})
                            invoice.update({'account_id':1657})
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':50}) 
                            invoice.update({'product_account':1809})
                            invoice.update({'account_id':1765})                      

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}      
                                                                                          
                    elif company_id == 15 : #  SPER

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':116})
                            invoice.update({'product_account':3969})  
                            invoice.update({'account_id':3925})      
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':115})
                            invoice.update({'product_account':3979})
                            invoice.update({'account_id':3817})
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':117})
                            invoice.update({'product_account':3979})
                            invoice.update({'account_id':3817})
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':114}) 
                            invoice.update({'product_account':3969})
                            invoice.update({'account_id':3925})                      

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'}                                                                                             

                    elif company_id == 16 : #  SPHERE EDGE CONSULTING INDIA PVT. LTD

                        if invoice['type'] =='out_refund' :
                            invoice.update({'journal_id':60})
                            invoice.update({'product_account':2079})       
                            invoice.update({'account_id':2035}) 
                            
                        elif invoice['type'] =='in_invoice' :
                            invoice.update({'journal_id':59})
                            invoice.update({'product_account':2089})
                            invoice.update({'account_id':1927}) 
                            
                        elif invoice['type'] =='in_refund' :
                            invoice.update({'journal_id':61})
                            invoice.update({'product_account':2089})
                            invoice.update({'account_id':1927}) 
                            
                        elif invoice['type'] =='out_invoice' :
                            invoice.update({'journal_id':58}) 
                            invoice.update({'product_account':2079})
                            invoice.update({'account_id':2035})                      

                        else :
                            
                            return {'result':0,'error':'Invalid Invoice Type format'} 
                    
                    
                    else :
                        
                        return {'result':0,'error':'Company - Journal Error'}
                    
                            
                    #product search
                    
                    template_id=prod_tmpl_obj.search(cr,uid,[('name','=',val['params']['product_detail'][0]['product_name'])])
                    if template_id :
                        
                        if len(template_id) > 1:
                            return {'result':0,'error':'Multiple products with same name found on Odoo'}

                        product_id=prod_obj.search(cr,uid,[('product_tmpl_id','=',template_id[0])])    
                        
                        if product_id :
                            invoice_line.update({'product_id':product_id[0]})
                            invoice_line.update({'name':val['params']['product_detail'][0]['product_name']})
                            invoice_line.update({'quantity':val['params']['product_detail'][0]['quantity']})
                            invoice_line.update({'account_id':invoice['product_account']})                              
                            invoice_line.update({'price_unit':val['params']['product_detail'][0]['price_unit']})
                        
                        else :
                            
                            return {'result':0,'error':'Product not found'}


                                   
                    #create invoice 
                    try :
                        
         		#import ipdb;ipdb.set_trace()
                        new_invoice_id=invoice_obj.create(cr,uid,invoice)
                        
                    except Exception as invoice_create_exception :
                        return {'result':0,'error':invoice_create_exception}
                    
                    
                    #create invoice line
                    try :
                        
                        invoice_obj.write(cr, uid, [new_invoice_id], {'invoice_line': [(0, 0, invoice_line)]})
                        return 1
                        
                    except Exception as invoice_line_create_exception :
                        return {'result':0,'error':invoice_line_create_exception}
                
                    
                
            except Exception as exception_log :
                return {'result':0,'error':exception_log}
                            
        return 0     



    def customer_register_payment_old_21dec(self,cr,uid,vals):

	uid=1
	#import ipdb;ipdb.set_trace()
        ''' return 1 if voucher created else 0 on fail'''
        ############FORMAT#################
#         vals=[  {'transaction_type':'receipt','currency_id':'currency code','partner_id':'customer odoo id','routesms_remark':'remark','date':'yyyy-mm-dd','amount':0.0,
#             'reference': 'Payment Ref' ,'company_name':'company name','saleperson_name': 'saleperson name' } ]

# 
#     
#     vals=[  {'transaction_type':'receipt','currency_id':'INR','partner_id':'R100001','routesms_remark':'remark','date':'2015-03-30','amount':12,
#              'reference': 'Payment Ref' ,'company_name':'RSL (Group)','saleperson_name': 'Karishma Ghaghda' } ]

        


        currency_obj=self.pool.get('res.currency')
        partner_obj=self.pool.get('res.partner')
        company_obj=self.pool.get('res.company')
        voucher_obj=self.pool.get('account.voucher')
        journal_obj=self.pool.get('account.journal')
        users_obj=self.pool.get('res.users')
        
        #import ipdb;ipdb.set_trace()
        voucher={}
        if not (isinstance(vals,(list,dict))) :
            return {'result':0,'error':'Invalid input!! Type should be ARRAY'}


        if vals :
            try :
                
                
                if len(vals) > 1 :
                    return {'result':0,'error':'Multiple Payments not accepted'}
                
                for val in vals :
                    
                    transaction_type=["receipt","purchase"]
                    if (val['transaction_type'] in transaction_type): 
                        
                        voucher.update({'type':val['transaction_type']})
                    
                    else:
                        return {'result':0,'error':'Invalid transaction type'}
                    
                    #assign account
                    if val['transaction_type']=="receipt":
                         voucher.update({'account_id':270})
                    
                    else:
                        return {'result':0,'error':'Invalid attempt '}
                    
                        
                    
                    #search currency
                    currency_id=currency_obj.search(cr,uid,[('name','=',val['currency_id'])])
                    if currency_id :
                        voucher.update({'currency_id':currency_id[0]})
                        
                    else :
                        
                        return {'result':0,'error':'Currency not found or invalid currency'}
                    
                    #assign journal
                    
                    if val['currency_id'] =='EUR (RG)' :
                        voucher.update({'journal_id':162})
                    
                    elif val['currency_id'] =='INR (RG)' :
                        voucher.update({'journal_id':8}) 
                        

#AHANA ENTERTAINMENT PVT. LTD

                    elif val['currency_id'] =='INR (AEP)' :
                        voucher.update({'journal_id':25}) 

#GRAPHIXIDE INC

                    elif val['currency_id'] =='USD (GRAPH INC)' :
                        voucher.update({'journal_id':73}) 


#GRAPHIXIDE SERVICES PVT.LTD

                    elif val['currency_id'] =='INR (GSPL)' :
                        voucher.update({'journal_id':33})                         
                        

#REMARKABLE INNOVATIONS

                    elif val['currency_id'] =='USD (REI)' :
                        voucher.update({'journal_id':81})                         
                                                
                        
#ROUTESMS SOLUTIONS FZE

                    elif val['currency_id'] =='AED (RFZE)' :
                        voucher.update({'journal_id':97})

                    elif val['currency_id'] =='USD (RFZE)' :
                        voucher.update({'journal_id':45})   
                                                                         
                    elif val['currency_id'] =='EUR (RFZE)' :
                        voucher.update({'journal_id':146})   
                                                                                                 
#ROUTESMS SOLUTIONS LIMITED                                     

                    elif val['currency_id'] =='INR (RSL)' :
                        voucher.update({'journal_id':41})

                    elif val['currency_id'] =='EUR (RSL)' :
                        voucher.update({'journal_id':147})   
                                                                         
                    elif val['currency_id'] =='USD (RSL)' :
                        voucher.update({'journal_id':132}) 
       
#ROUTESMS SOLUTIONS NIGERIA LIMITED
                    elif val['currency_id'] =='NGN (RSNL)' :
                        voucher.update({'journal_id':134})

                    elif val['currency_id'] =='EUR (RSNL)' :
                        voucher.update({'journal_id':187})

# ROUTESMS SOLUTIONS (UK) LIMITED

                    elif val['currency_id'] =='GBP (RSUK)' :
                        voucher.update({'journal_id':105})

                    elif val['currency_id'] =='EUR (RSUK)' :
                        voucher.update({'journal_id':141})                        

                    elif val['currency_id'] =='USD (RSUK)' :
                        voucher.update({'journal_id':174})
                        
# ROUTEVOICE LIMITED
                    elif val['currency_id'] =='HKD (RVL)' :
                        voucher.update({'journal_id':113})

# SANRAJ INFRA DEVELOPERS PVT. LTD

                    elif val['currency_id'] =='INR (SAN)' :
                        voucher.update({'journal_id':49})
                        
# SPECTRA TELESERVICES PVT. LTD

                    elif val['currency_id'] =='INR (SPECTRA)' :
                        voucher.update({'journal_id':57})
                         
# SPER

                    elif val['currency_id'] =='INR (SPER)' :
                        voucher.update({'journal_id':121})
                        
# SPHERE EDGE CONSULTING INDIA PVT. LTD
                        
                    elif val['currency_id'] =='INR (SPC)' :
                        voucher.update({'journal_id':65})                        
                        
           
                    else:
                        return {'result':0,'error':'Journal not set for currency'}
                        
                           
                    
                    #search partner
                    
                    partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',val['partner_id'])])
                    if partner_id:
                        partner_obj.write(cr,uid,partner_id,{'routesms_remark':val['routesms_remark']})
                        voucher.update({'partner_id':partner_id[0]})
                        voucher.update({'remark':val['routesms_remark']})
                    
                    else :
                        return {'result':0,'error':'Customer not found'}
                    
                    #search company
                    
                    company_id=company_obj.search(cr,uid,[('name','=',val['company_name'])])
                    if company_id:
                        voucher.update({'company_id':company_id[0]})
                        
                    else :
                        return {'result':0,'error':'Company not found'}

                    #search user/saleperson
#                     saleperson_id=partner_obj.search(cr,uid,[('name','=',val['saleperson_name'])])
#                     if saleperson_id :
#                         
#                         user_id=users_obj.search(cr,uid,[('partner_id','=',saleperson_id[0])])
#                         if user_id :
#                             voucher.update({'user_id':user_id[0]})
#                             
#                         else :
#                             
#                             return {'result':0,'error':'Saleperson/User not found '}
#                     
#                     else :
#                         
#                             return {'result':0,'error':'Saleperson/User not found '}
                    
                    saleperson_id=partner_obj.browse(cr,uid,partner_id[0]).user_id.id
                    if saleperson_id :
                        voucher.update({'user_id':saleperson_id})
                            
                    else :
                        voucher.update({'user_id':1})
                        #return {'result':0,'error':'Saleperson/User not found '}
                    
                   
                    
                    
                    #emloyee id search
                    
                    emp_id=self.default_emp_id(cr,voucher['user_id'],context=None)
                    if emp_id : 
                        
                        if isinstance(emp_id,(int)):
                            voucher.update({'employee_id':emp_id})
                        else :
                            return {'result':0,'error':'No user is assigned to Employee '} 
                            
                    else:
                         return {'result':0,'error':'No user is assigned to Employee '}

                    
                    #assign remaining values
                    voucher.update({'date':val['date']})
                    voucher.update({'amount':val['amount']})
                                    
                         
                    #create voucher
                    try :
                        voucher['amount']=float(voucher['amount'])
                        
                        voucher_obj.create(cr,uid,voucher)
                        
                    except Exception as voucher_create_exception :
                        return {'result':0,'error':voucher_create_exception}
                    
                
                    return 1
                
            except Exception as exception_log :
                return {'result':0,'error':exception_log}
                            
        return 0     



    def customer_register_payment(self,cr,uid,vals):

	uid=1
	#import ipdb;ipdb.set_trace()
	print '-------------------------------REGISTER PAYMENT-----------------------'
        ''' return 1 if voucher created else 0 on fail'''
        ############FORMAT#################
#         vals=[  {'transaction_type':'receipt','currency_id':'currency code','partner_id':'customer odoo id','routesms_remark':'remark','date':'yyyy-mm-dd','amount':0.0,
#             'reference': 'Payment Ref' ,'company_name':'company name','saleperson_name': 'saleperson name' } ]

# 
#     
#     vals=[  {'transaction_type':'receipt','currency_id':'INR','partner_id':'R100001','routesms_remark':'remark','date':'2015-03-30','amount':12,
#              'reference': 'Payment Ref' ,'company_name':'RSL (Group)','saleperson_name': 'Karishma Ghaghda' } ]

        


        currency_obj=self.pool.get('res.currency')
        partner_obj=self.pool.get('res.partner')
        company_obj=self.pool.get('res.company')
        voucher_obj=self.pool.get('account.voucher')
        journal_obj=self.pool.get('account.journal')
        users_obj=self.pool.get('res.users')
        
        #import ipdb;ipdb.set_trace()
        voucher={}
        if not (isinstance(vals,(list,dict))) :
            return {'result':0,'error':'Invalid input!! Type should be ARRAY'}


        if vals :
            try :
                
                
                if len(vals) > 1 :
                    return {'result':0,'error':'Multiple Payments not accepted'}
                
                for val in vals :
                    
                    transaction_type=["receipt","purchase"]
                    if (val['transaction_type'] in transaction_type): 
                        
                        voucher.update({'type':val['transaction_type']})
                    
                    else:
                        return {'result':0,'error':'Invalid transaction type'}
                    
                    #assign account
                    if val['transaction_type']=="receipt":
                         voucher.update({'account_id':270})
                    
                    else:
                        return {'result':0,'error':'Invalid attempt '}
                    
                        
                    
                    #search currency
                    currency_id=currency_obj.search(cr,uid,[('name','=',val['currency_id'])])
                    if currency_id :
                        voucher.update({'currency_id':currency_id[0]})
                        
                    else :
                        
                        return {'result':0,'error':'Currency not found or invalid currency'}
                    
                    #assign journal
                    
                    if val['currency_id'] =='EUR (RG)' :
                        voucher.update({'journal_id':162})
                    
                    elif val['currency_id'] =='INR (RG)' :
                        voucher.update({'journal_id':8}) 
                        

#AHANA ENTERTAINMENT PVT. LTD

                    elif val['currency_id'] =='INR (AEP)' :
                        voucher.update({'journal_id':25}) 

#GRAPHIXIDE INC

                    elif val['currency_id'] =='USD (GRAPH INC)' :
                        voucher.update({'journal_id':73}) 


#GRAPHIXIDE SERVICES PVT.LTD

                    elif val['currency_id'] =='INR (GSPL)' :
                        voucher.update({'journal_id':33})                         
                        

#REMARKABLE INNOVATIONS

                    elif val['currency_id'] =='USD (REI)' :
                        voucher.update({'journal_id':81})                         
                                                
                        
#ROUTESMS SOLUTIONS FZE

                    elif val['currency_id'] =='AED (RFZE)' :
                        voucher.update({'journal_id':97})

                    elif val['currency_id'] =='USD (RFZE)' :
                        voucher.update({'journal_id':45})   
                                                                         
                    elif val['currency_id'] =='EUR (RFZE)' :
                        voucher.update({'journal_id':146})   
                                                                                                 
#ROUTESMS SOLUTIONS LIMITED                                     

                    elif val['currency_id'] =='INR (RSL)' :
                        voucher.update({'journal_id':41})

                    elif val['currency_id'] =='EUR (RSL)' :
                        voucher.update({'journal_id':147})   
                                                                         
                    elif val['currency_id'] =='USD (RSL)' :
                        voucher.update({'journal_id':132}) 
       
#ROUTESMS SOLUTIONS NIGERIA LIMITED
                    elif val['currency_id'] =='NGN (RSNL)' :
                        voucher.update({'journal_id':134})

                    elif val['currency_id'] =='EUR (RSNL)' :
                        voucher.update({'journal_id':187})

# ROUTESMS SOLUTIONS (UK) LIMITED

                    elif val['currency_id'] =='GBP (RSUK)' :
                        voucher.update({'journal_id':105})

                    elif val['currency_id'] =='EUR (RSUK)' :
                        voucher.update({'journal_id':141})                        

                    elif val['currency_id'] =='USD (RSUK)' :
                        voucher.update({'journal_id':174})
                        
# ROUTEVOICE LIMITED
                    elif val['currency_id'] =='HKD (RVL)' :
                        voucher.update({'journal_id':113})

# SANRAJ INFRA DEVELOPERS PVT. LTD

                    elif val['currency_id'] =='INR (SAN)' :
                        voucher.update({'journal_id':49})
                        
# SPECTRA TELESERVICES PVT. LTD

                    elif val['currency_id'] =='INR (SPECTRA)' :
                        voucher.update({'journal_id':57})
                         
# SPER

                    elif val['currency_id'] =='INR (SPER)' :
                        voucher.update({'journal_id':121})
                        
# SPHERE EDGE CONSULTING INDIA PVT. LTD
                        
                    elif val['currency_id'] =='INR (SPC)' :
                        voucher.update({'journal_id':65})                        
                        
           
                    else:
                        return {'result':0,'error':'Journal not set for currency'}
                        
                           
                    
                    #search partner
                    
                    partner_id=partner_obj.search(cr,uid,[('partner_sequence','=',val['partner_id'])])
                    if partner_id:
                        partner_obj.write(cr,uid,partner_id,{'routesms_remark':val['routesms_remark']})
                        voucher.update({'partner_id':partner_id[0]})
                        voucher.update({'remark':val['routesms_remark']})
                    
                    else :
                        return {'result':0,'error':'Customer not found'}
                    
                    #search company
                    
                    company_id=company_obj.search(cr,uid,[('name','=',val['company_name'])])
                    if company_id:
                        voucher.update({'company_id':company_id[0]})
                        
                    else :
                        return {'result':0,'error':'Company not found'}

                    #search user/saleperson
#                     saleperson_id=partner_obj.search(cr,uid,[('name','=',val['saleperson_name'])])
#                     if saleperson_id :
#                         
#                         user_id=users_obj.search(cr,uid,[('partner_id','=',saleperson_id[0])])
#                         if user_id :
#                             voucher.update({'user_id':user_id[0]})
#                             
#                         else :
#                             
#                             return {'result':0,'error':'Saleperson/User not found '}
#                     
#                     else :
#                         
#                             return {'result':0,'error':'Saleperson/User not found '}
                    
                    saleperson_id=partner_obj.browse(cr,uid,partner_id[0]).user_id.id
                    if saleperson_id :
                        voucher.update({'user_id':saleperson_id})
                            
                    else :
                        voucher.update({'user_id':1})
                        #return {'result':0,'error':'Saleperson/User not found '}
                    
                   
                    
                    
                    #emloyee id search
                    
                    emp_id=self.default_emp_id(cr,voucher['user_id'],context=None)
                    if emp_id : 
                        
                        if isinstance(emp_id,(int)):
                            voucher.update({'employee_id':emp_id})
                        else :
                            return {'result':0,'error':'No user is assigned to Employee '} 
                            
                    else:
                         return {'result':0,'error':'No user is assigned to Employee '}

                    
                    #assign remaining values
                    voucher.update({'date':val['date']})
                    voucher.update({'amount':val['amount']})
                                    
                         
                    #create voucher
                    try :
                        voucher['amount']=float(voucher['amount'])

#                        import ipdb;ipdb.set_trace()
                        if users_obj.browse(cr,uid,uid).company_id.id !=voucher['company_id']  :
			    write_context={} 
                            assigned_voucher_company_id=users_obj.write(cr,uid,[582],{'company_id':voucher['company_id']},write_context)
                            #cr.execute('''update res_users set company_id=%s where id=%s ''',(voucher['company_id'],582))
                            uid=582
                        else : 
                            
                            uid=uid#241
                      	#import ipdb;ipdb.set_trace() 
                        voucher_id=voucher_obj.create(cr,uid,voucher)
                        
                    except Exception as voucher_create_exception :
                        return {'result':0,'error':voucher_create_exception}
                    
                
                    return 1
                
            except Exception as exception_log :
                return {'result':0,'error':exception_log}
                            
        return 0 


#     def customer_insert_script(self,cr,uid,vals):
#         

#
#         values=(vals['is_company'],vals['name'],vals['routesms_cust_id'],vals['street'],vals['country_id']/
#                 vals['email'],vals['vat'],vals['fax'],vals['user_id'],vals['vertical'],vals['customer'])
#         
#         values=(vals['is_company'],vals['name'],vals['routesms_cust_id'],vals['street'].encode('ascii','ignore')
#                 ,vals['country_id'],vals['email'],vals['vat'],vals['fax'],vals['user_id'],vals['vertical'],vals['customer'])
#         
#         
#         cr.execute(''' insert into res_partner (is_company,name,routesms_cust_id,street,country_id,email,\
#                      vat,phone,fax,user_id,vertical,customer) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''\
#                      ,values)
# 
#         
#     
#         master_partner_id=map(lambda x:x[0], cr.fetchall())
#         return master_partner_id
# 
#     def contact_insert_script(self,cr,uid,vals):
#         
#         
#         values=(vals['parent_id'],vals['name'],vals['use_parent_address'],vals['type'],vals['customer'])
#         
# 
#         
#         cr.execute(''' insert into res_partner (parent_id,name,use_parent_address,type,customer) /
#         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',values)
#                 
# 
#         
#     
#         contact_partner_id=map(lambda x:x[0], cr.fetchall())
#         return contact_partner_id
#                 
#         
#         
        
        
            
routesms_api()




