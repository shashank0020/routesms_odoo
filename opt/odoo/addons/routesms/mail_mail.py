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

SUPERID=1

class mail_compose_message(osv.Model):
    _inherit = 'mail.compose.message'

    def onchange_template_id(self, cr, uid, ids, template_id, composition_mode, model, res_id, context=None):
        """ - mass_mailing: we cannot render, so return the template values
            - normal mode: return rendered values """
        ###Added hardoced to attatch pdf report for sale user
        uid=SUPERID
        if template_id and composition_mode == 'mass_mail':
            fields = ['subject', 'body_html', 'email_from', 'reply_to', 'mail_server_id']
            template = self.pool['email.template'].browse(cr, uid, template_id, context=context)
            values = dict((field, getattr(template, field)) for field in fields if getattr(template, field))
            
            if template.attachment_ids:
                values['attachment_ids'] = [att.id for att in template.attachment_ids]
            if template.mail_server_id:
                values['mail_server_id'] = template.mail_server_id.id
            if template.user_signature and 'body_html' in values:
                signature = self.pool.get('res.users').browse(cr, uid, uid, context).signature
                values['body_html'] = tools.append_content_to_html(values['body_html'], signature, plaintext=False)
        elif template_id:
            values = self.generate_email_for_composer_batch(cr, uid, template_id, [res_id], context=context)[res_id]
            # transform attachments into attachment_ids; not attached to the document because this will
            # be done further in the posting process, allowing to clean database if email not send
            ir_attach_obj = self.pool.get('ir.attachment')
            for attach_fname, attach_datas in values.pop('attachments', []):
                data_attach = {
                    'name': attach_fname,
                    'datas': attach_datas,
                    'datas_fname': attach_fname,
                    'res_model': 'mail.compose.message',
                    'res_id': 0,
                    'type': 'binary',  # override default_type from context, possibly meant for another model!
                }
                values.setdefault('attachment_ids', list()).append(ir_attach_obj.create(cr, uid, data_attach, context=context))
        else:
            default_context = dict(context, default_composition_mode=composition_mode, default_model=model, default_res_id=res_id)
            default_values = self.default_get(cr, uid, ['composition_mode', 'model', 'res_id', 'parent_id', 'partner_ids', 'subject', 'body', 'email_from', 'reply_to', 'attachment_ids', 'mail_server_id'], context=default_context)
            values = dict((key, default_values[key]) for key in ['subject', 'body', 'partner_ids', 'email_from', 'reply_to', 'attachment_ids', 'mail_server_id'] if key in default_values)

        if values.get('body_html'):
            values['body'] = values.pop('body_html')
        return {'value': values}   

    def send_mail_to_partner(self,send_from, send_to, send_bcc,report_name,subject,body,filename, server,binary):
        import smtplib
        
        import os
        
        from email.MIMEMultipart import MIMEMultipart
        
        from email.MIMEBase import MIMEBase
        
        from email.MIMEText import MIMEText
        from email.mime.application import MIMEApplication
        
        from email.Utils import COMMASPACE, formatdate
        
        from email import Encoders            
    
#         assert type(send_to)==list
#         
#         assert type(files)==list
        try : 
            
            msg = MIMEMultipart()
            
            msg['From'] = send_from
            
            msg['To'] = COMMASPACE.join(send_to)
            
            msg['Date'] = formatdate(localtime=True)
            
            msg['Subject'] = subject
            
            msg.attach( MIMEText(body,"html",_charset="utf-8")  )
            
    
            #https://bugs.python.org/issue9298
            part = MIMEBase("application","pdf")
            part.add_header('Content-Transfer-Encoding', 'base64') 
            part.add_header('Content-Disposition', 'attachment',filename=report_name +'.pdf')
            part.set_payload(binary)
            msg.attach(part)
    
            
            smtp = smtplib.SMTP(server.get('host',''))
            smtp.starttls()
            smtp.login(server.get('username',''),server.get('password',''))
            

            smtp.sendmail(send_from,send_to+send_bcc, msg.as_string())
            
            smtp.close()
            
        except Exception as E : 
            raise osv.except_osv(_('Email Sending Failed'), _("Invalid Email Configuration Or Mail Server Is Down!\nContact I.T Team"))

    def get_mailserver_details(self,cr,uid ): 
        '''get outgoing  mail server credentials to send email '''
        SUPERID=1
        uid=SUPERID
        mail_server_obj=self.pool.get('ir.mail_server')
        
        mail_server=mail_server_obj.search(cr,uid,[])
        if not mail_server : 
            raise osv.except_osv(_('Email Sending Failed'), _("Outgoing Mail Server Not Found!"))

        if len(mail_server) > 1 : 
            raise osv.except_osv(_('Email Sending Failed'), _("Multiple Outgoing Mail Server Found!"))
        server= mail_server_obj.browse(cr,uid,mail_server[0])
        
        return {'host':server.smtp_host + ':' +str(server.smtp_port),'username':server.smtp_user,'password':\
                server.smtp_pass}   
        
        
    def collect_primary_secondary_email(self,cr,uid,partner): 
        '''fetch email addresses '''
        partner_obj=self.pool.get('res.partner')
        email_vals=[]
       
        if not partner :
            raise osv.except_osv(_('Email Sending Failed'), _("No Partner Record Found!"))
        
        if partner.exclude_primary_email and not partner.partner_line : 
            raise osv.except_osv(_('Email Sending Failed'), _("Primary Email Is Disabled & No Secondary Email Found!"))
        
        if partner.exclude_primary_email and partner.partner_line : 
            send_email=[x.send_email for x in partner.partner_line if x.send_email ]
            if not send_email : 
                raise osv.except_osv(_('Email Sending Failed'), _("Atleast One Email Address Must Be Active!"))
            
        if not partner.exclude_primary_email : 
            ##check email##
            check_mail=partner_obj.email_validation(cr,uid,[partner.email])
            if not check_mail : 
                raise osv.except_osv(_('Email Sending Failed'), _("Primary Email Address Is Invalid!"))  
            email_vals.append(partner.email) 
        
        ##insert secondary email##
        
        secondary_email=[jj.email for jj in partner.partner_line if jj.send_email ]
        if secondary_email : 
            check_mail=partner_obj.email_validation(cr,uid,secondary_email)
            if not check_mail : 
                raise osv.except_osv(_('Email Sending Failed'), _("Secondary Email Address Is Invalid!"))
              
            [email_vals.append(email) for email in secondary_email]
        
        return email_vals

            

                
    def get_order_details(self,cr,uid,order_id,model): 
        '''fetch details from sale order document require to send email like To,FROM,CC '''
       # import ipdb;ipdb.set_trace()
        partner_obj=self.pool.get('res.partner')
        BCC_email_vals=[]
        report_name=''
       
        if not model.get('model') : 
            raise osv.except_osv(_('Email Sending Failed'), _("Source Model Not Found!"))
        if not order_id : 
            raise osv.except_osv(_('Email Sending Failed'), _("Source Document Not Found!"))
        
        if model.get('model')=='account.invoice' : 
            obj=self.pool.get('account.invoice')
        
        elif model.get('model')=='sale.order' : 
            obj=self.pool.get('sale.order')
        
        else : 
            raise osv.except_osv(_('Email Sending Failed'), _("Source Document Missing From Configuration !"))
        
            
            
        document=obj.browse(cr,uid,order_id)
        ###fetch primary & secondary email address###
        report_name= document.name
        partner_email_vals=self.collect_primary_secondary_email(cr,uid,document.partner_id)
        if not partner_email_vals : 
            raise osv.except_osv(_('Email Sending Failed'), _("No Partner Email Found!"))

        
        check_mail=partner_obj.email_validation(cr,uid,[document.user_id.login])
        if not check_mail : 
            raise osv.except_osv(_('Email Sending Failed'), _("Salesperson's Email Address Is Invalid!"))
        BCC_email_vals.append(document.user_id.login)

        if model.get('model')=='account.invoice' :
            report_name= document.number
            check_mail=partner_obj.email_validation(cr,uid,[document.responsible.login])
            if not check_mail : 
                raise osv.except_osv(_('Email Sending Failed'), _("Accountant's Email Address Is Invalid!"))
            BCC_email_vals.append(document.responsible.login)   
        
        if not BCC_email_vals: 
            raise osv.except_osv(_('Email Sending Failed'), _("BCC (Blind Carbon Copy) Not Found!"))         
        
        if 'sandip@routesms.com' in partner_email_vals or 'sandip@routesms.com' in BCC_email_vals : 
            raise osv.except_osv(_('Email Sending Failed'), _("Cannot Send Email On SuperAdmin (CEO DESK)!"))
        
        return {'from':document.user_id.login,'to':partner_email_vals,'bcc':BCC_email_vals,'report_name':report_name or 'Draft'}   
        
    def parse_body(self,body,model): 
        '''remove data from body '''
        final_body=body
        if model=='sale.order' : 
            
            for i in body.split('<a style="display:block') :
                final_body=''
                if 'View Order' in  i or 'View Quotation' in  i:
                    for jj in i.split('</a>'):
                        if 'View Order' in jj or 'View Quotation' in jj :
                            print '----------------------'
                            replace_content='<a style="display:block' +jj+'</a>'
                            #import ipdb;ipdb.set_trace()
                            final_body=body.replace(replace_content,'')
         
            
        
        return final_body.replace('Administrator</span>','</span>')
                              

    def send_mail(self, cr, uid, ids, context=None):
        context = context or {}
        
        msg=self.browse(cr,uid,ids[0])
        
        if not msg.attachment_ids : 
            raise osv.except_osv(_('Email Sending Failed!'), _("No PDF Attachment Found"))
            
        if len(msg.attachment_ids) > 1 : 
            raise osv.except_osv(_('Email Sending Failed!'), _("Multiple PDF Attachment Found\nContact Odoo Team"))
        
        body=self.parse_body(msg.body,context.get('active_model',''))
        
        server=self.get_mailserver_details(cr,uid,)
        #import ipdb;ipdb.set_trace()
        document_detail=self.get_order_details(cr,uid,msg.res_id,{'model':context.get('active_model','')})
        
        
        self.send_mail_to_partner(document_detail.get('from'), document_detail.get('to'),\
                         document_detail.get('bcc'),document_detail.get('report_name'),\
                         msg.subject, body, document_detail, server,msg.attachment_ids.datas )

        return True   



class mail_mail(osv.Model):
    """ Update of mail_mail class, to add the signin URL to notifications. """
    _inherit = 'mail.mail'

    def _get_partner_access_link(self, cr, uid, mail, partner=None, context=None):
        """ Generate URLs for links in mails:
            - partner is not an user: signup_url
            - partner is an user: fallback on classic URL
        """
        if context is None:
            context = {}
        partner_obj = self.pool.get('res.partner')
        if partner and not partner.user_ids:
            contex_signup = dict(context, signup_valid=True)
            signup_url = partner_obj._get_signup_url_for_action(cr, SUPERUSER_ID, [partner.id],
                                                                action='mail.action_mail_redirect',
                                                                model=mail.model, res_id=mail.res_id,
                                                                context=contex_signup)[partner.id]
                      
            model_name, record_name ='',''                                                    
            return ", <span class='oe_mail_footer_access'><small>%(access_msg)s <a style='color:inherit' href='%(portal_link)s'>%(portal_msg)s</a></small></span>" % {
                'access_msg': _(''),
                'portal_link': '',
                'portal_msg': '%s %s' % (model_name, record_name) if mail.record_name else _('your messages '),
            }
        else:
            return super(mail_mail, self)._get_partner_access_link(cr, uid, mail, partner=partner, context=context)
        


class mail_notification(osv.Model):
    ''' Stop auto notification mail for invocing'''
    _inherit = 'mail.notification'
    
    def _notify(self, cr, uid, message_id, partners_to_notify=None, context=None,
                force_send=False, user_signature=True):
        """ Send by email the notification depending on the user preferences

            :param list partners_to_notify: optional list of partner ids restricting
                the notifications to process
            :param bool force_send: if True, the generated mail.mail is
                immediately sent after being created, as if the scheduler
                was executed for this message only.
            :param bool user_signature: if True, the generated mail.mail body is
                the body of the related mail.message with the author's signature
        """
        
        notif_ids = self.search(cr, SUPERUSER_ID, [('message_id', '=', message_id), ('partner_id', 'in', partners_to_notify)], context=context)

        # update or create notifications
        new_notif_ids = self.update_message_notification(cr, SUPERUSER_ID, notif_ids, message_id, partners_to_notify, context=context)

        # mail_notify_noemail (do not send email) or no partner_ids: do not send, return
        if context and context.get('mail_notify_noemail'):
            return True
       
        if context.get('type') in ['out_invoice','in_invoice','out_refund','in_refund','receipt','payment'] :
             
            return True

        # browse as SUPERUSER_ID because of access to res_partner not necessarily allowed
        self._notify_email(cr, SUPERUSER_ID, new_notif_ids, message_id, force_send, user_signature, context=context)
            
                
        
