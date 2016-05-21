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

import time

from openerp.osv import fields, osv
from openerp.tools.translate import _

class account_invoice_holiday_wizard(osv.osv_memory):
    _name = 'account.invoice.holiday.wizard'
    _description = 'Selection of Holiday business verticals'

    _columns = {
        'holiday_vertical_list':fields.selection([('air','AIR TICKETING'), ('other','Other')], 'Verticals', required=True),
                
#         'holiday_vertical_list':fields.selection([('air','AIR TICKETING'), ('tour','TOURS & PACKAGES'), ('hotel','HOTEL BOOKING'), ('visa','VISA SERVICE'),\
#         ('rent','RENT A CAB SERVICE'),('insurance','INSURANCE SERVICE')], 'Verticals', required=False),
#                 

    }


    def submit(self,cr,uid,ids,context):
        
        user_obj=self.pool.get('res.users')
        
        if ids :
            holiday_vertical_val=self.browse(cr,uid,ids[0]).holiday_vertical_list
            if holiday_vertical_val :
                if user_obj.browse(cr,uid,uid).company_id.id == 3 :  
                    user_obj.write(cr,1,[uid],{'holiday_vertical_list':holiday_vertical_val})
                    
                    cr.execute(''' select id from res_groups where name=%s''',('293 Holiday Users AIR Ticket',))
                    air_group_id=cr.fetchall()
                    cr.execute(''' select id from res_groups where name=%s''',('293 Holiday Users Others',))
                    other_group_id=cr.fetchall()
                    
                    if holiday_vertical_val=='air' :
                        
                        if air_group_id:
                            
                            cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(air_group_id[0],uid))
                            cr.execute(''' insert into res_groups_users_rel(gid,uid) VALUES(%s,%s)''',(air_group_id[0],uid))
                        
                        if other_group_id :
                            cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(other_group_id[0],uid))
                    else :
                        
                        
                        
                        if air_group_id:
                            
                            cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(air_group_id[0],uid))
                            
                        
                        if other_group_id :
                            cr.execute(''' delete from  res_groups_users_rel where gid=%s and uid=%s''',(other_group_id[0],uid))
                            cr.execute(''' insert into res_groups_users_rel(gid,uid) VALUES(%s,%s)''',(other_group_id[0],uid))
    
        return {
            'type': 'ir.actions.client',
            'tag': 'reload_context',
        }

class partner_custom_filter(osv.osv_memory):
    _name = 'partner.custom.filter'
    _description = 'Filter Partner'

    _columns = {
        'partner_name':fields.char('Enter Partner Name',required=True),
        
    }


    def submit(self,cr,uid,ids,context):
        uid=1
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window') 
        user_obj=self.pool.get('res.users')
        partner_obj=self.pool.get('res.partner')
        partner_dashboard_obj=self.pool.get('routsms.partner.filter')
        #02ltd
        try :
                
            if ids :
                partner_name=self.browse(cr,uid,ids[0]).partner_name
                cr.execute(''' delete  from routsms_partner_filter''')
                if partner_name :
                    cr.execute(''' select id,user_id from res_partner where display_name=%s ''',(partner_name,))
                    vals=cr.fetchall()
                    
                    if vals :
                        for values in vals :
                            partner_type=user_obj.browse(cr,uid,values[1]).partner_type
                            partner_display_name=partner_obj.browse(cr,uid,values[0]).name
                            current_partner_type=user_obj.browse(cr,uid,uid).partner_type
                            if partner_type==current_partner_type :
                                    
                                cr.execute(''' insert into routsms_partner_filter(name,user_id) VALUES(%s,%s)''',(partner_display_name,values[1]))
                                result = mod_obj.get_object_reference(cr, uid, 'routesms', 'action_routesms_partner_filter')
                                id = result and result[1] or False
                                result = act_obj.read(cr, uid, [id], context=context)[0]
                                return result
                            elif partner_type==False and current_partner_type==False :

                                cr.execute(''' insert into routsms_partner_filter(name,user_id) VALUES(%s,%s)''',(partner_display_name,values[1]))
                                result = mod_obj.get_object_reference(cr, uid, 'routesms', 'action_routesms_partner_filter')
                                id = result and result[1] or False
                                result = act_obj.read(cr, uid, [id], context=context)[0]
                                return result
                                
                        
                    else :
                        raise osv.except_osv(_('Sorry!'),_("No Record Found")) 
                            
        except Exception as error_log :
            
            raise osv.except_osv(_('Sorry!'),_("No Record Found"))
            
                    
        else :
            
            raise osv.except_osv(_('Sorry!'),_("No Record Found"))
                  
            

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
