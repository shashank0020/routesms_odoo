# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2011 OpenERP S.A (<http://www.openerp.com>).
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

from openerp import SUPERUSER_ID
from openerp.osv import osv
from openerp.tools.translate import _
import smtplib

import os

from email.MIMEMultipart import MIMEMultipart

from email.MIMEBase import MIMEBase

from email.MIMEText import MIMEText
from email.mime.application import MIMEApplication

from email.Utils import COMMASPACE, formatdate

from email import Encoders    

SUPERID=1


class send_email_with_attactment(osv.osv_memory): 
    '''structure to send email with attachments '''

    _name='send.email.with.attactment'
    
    def send_mail(self,send_from, send_to, send_bcc,report_name,subject,body,extension, server,binary,body_type):
        
    
        try : 
            
            msg = MIMEMultipart()
            
            msg['From'] = send_from
            
            msg['To'] = COMMASPACE.join(send_to)
            
            msg['Date'] = formatdate(localtime=True)
            
            msg['Subject'] = subject
            if body_type=='plain' : 
                
                msg.attach( MIMEText(body,"plain",_charset="utf-8")  )
            else : 
                msg.attach( MIMEText(body,"html",_charset="utf-8")  )
                
            #https://bugs.python.org/issue9298
            if report_name : 
                part = MIMEBase("application",extension)
                part.add_header('Content-Transfer-Encoding', 'base64')                 
                part.add_header('Content-Disposition', 'attachment',filename=report_name +'.' +extension)
                part.set_payload(binary)
                Encoders.encode_base64(part)
                msg.attach(part)   
            
            smtp = smtplib.SMTP(server.get('host',''))
            smtp.starttls()
            smtp.login(server.get('username',''),server.get('password',''))
            
    
            smtp.sendmail(send_from,send_to+send_bcc, msg.as_string())
            
            smtp.close()
            return True
            
        except Exception as E : 
            raise osv.except_osv(_('Email Sending Failed'), _("Invalid Email Configuration Or Mail Server Is Down!\nContact I.T Team"))



    def get_mailserver_details(self,cr,uid ): 
        '''get outgoing  mail server credentials to send email '''
        
        mail_server_obj=self.pool.get('ir.mail_server')
        
        mail_server=mail_server_obj.search(cr,uid,[])
        if not mail_server : 
            raise osv.except_osv(_('Email Sending Failed'), _("Outgoing Mail Server Not Found!"))

        if len(mail_server) > 1 : 
            raise osv.except_osv(_('Email Sending Failed'), _("Multiple Outgoing Mail Server Found!"))
        server= mail_server_obj.browse(cr,uid,mail_server[0])
        
        return {'host':server.smtp_host + ':' +str(server.smtp_port),'username':server.smtp_user,'password':\
                server.smtp_pass}    







        
