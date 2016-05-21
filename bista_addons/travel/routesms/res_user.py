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

class res_users(osv.osv):
    _inherit = 'res.users'
    
    
    _columns={
              
              #'employee_id':fields.function(default_emp_id,string='Employee User',type='many2one',relation='hr.employee',store=True),
              'partner_type': fields.selection([('india','India'), ('international','International')] ,'Type'),
              'holiday_vertical_list':fields.selection([('air','AIR TICKETING'), ('other','Other'), ], 'Verticals', required=False),
                
#               'holiday_vertical_list':fields.selection([('air','AIR TICKETING'), ('tour','TOURS & PACKAGES'), ('hotel','HOTEL BOOKING'), ('visa','VISA SERVICE'),\
#                 ('rent','RENT A CAB SERVICE'),('insurance','INSURANCE SERVICE')], 'Verticals', required=False),
              
              }
    
#     _defaults={
#                
#                'partner_type':'india'
#                }



    def preference_save(self, cr, uid, ids, context=None):
        ''' Overide method to hide/unhide travel menu from accounting'''
        #import ipdb;ipdb.set_trace()
        if self.browse(cr,uid,uid).company_id.id == 3 :
            cr.execute(''' select id from res_groups where name=%s''',('293 Holiday user',))
            group_id=cr.fetchall()
            cr.execute(''' select id from res_groups where name=%s''',('Activate Invoice Line',))
            active_invoice_line_group=cr.fetchall()
            
            if group_id :
                    cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(group_id[0],uid))
                    cr.execute(''' insert into res_groups_users_rel(gid,uid) VALUES(%s,%s)''',(group_id[0],uid))
            
            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.'))            
                    
            if active_invoice_line_group :
                    cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(active_invoice_line_group[0],uid))
            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.'))                    
                    

                
        else :
            
            cr.execute(''' select id from res_groups where name=%s''',('Activate Invoice Line',))
            active_invoice_line_group=cr.fetchall()
            if active_invoice_line_group :
                    cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(active_invoice_line_group[0],uid))
                    cr.execute(''' insert into res_groups_users_rel(gid,uid) VALUES(%s,%s)''',(active_invoice_line_group[0],uid))
            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.'))                    
            
            cr.execute(''' select id from res_groups where name=%s''',('293 Holiday Users AIR Ticket',))
            air_ticket_group=cr.fetchall()
            
            if air_ticket_group :
                cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(air_ticket_group[0],uid))

            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.'))                
                
            
            cr.execute(''' select id from res_groups where name=%s''',('293 Holiday Users Others',))
            non_air_ticket_group=cr.fetchall()
            if non_air_ticket_group :
                cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(non_air_ticket_group[0],uid))

            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.'))
            
            cr.execute(''' select id from res_groups where name=%s''',('293 Holiday user',))
            group_id=cr.fetchall()
            if group_id :
                    cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(group_id[0],uid))
            
            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.')) 
            

        
        #report baner loop
        
        if self.browse(cr,uid,uid).company_id.id in [8,9,10,11] :

            #active report baner
            cr.execute(''' select id from res_groups where name=%s''',('Activate Report Baner',))
            baner_active_id=cr.fetchall()
            if baner_active_id :
                    cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(baner_active_id[0],uid))
                    cr.execute(''' insert into res_groups_users_rel(gid,uid) VALUES(%s,%s)''',(baner_active_id[0][0],uid))
                    
            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.'))

            cr.execute(''' select id from res_groups where name=%s''',('Deactivate Report Baner',))
            baner_deactive_id=cr.fetchall()
            if baner_deactive_id :
                    cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(baner_deactive_id[0],uid))
            
                                    
                
        else : 
            
            #deactive report baner
            cr.execute(''' select id from res_groups where name=%s''',('Deactivate Report Baner',))
            baner_deactive_id=cr.fetchall()
            if baner_deactive_id :
                    cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(baner_deactive_id[0],uid))
                    cr.execute(''' insert into res_groups_users_rel(gid,uid) VALUES(%s,%s)''',(baner_deactive_id[0][0],uid))
                    
            else :
                
                raise osv.except_osv(_('Error!'), _('Group Name Not Exist.'))  


            cr.execute(''' select id from res_groups where name=%s''',('Activate Report Baner',))
            baner_active_id=cr.fetchall()
            if baner_active_id :                      
                cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(baner_active_id[0],uid))
            
        return {
            'type': 'ir.actions.client',
            'tag': 'reload_context',
        }
