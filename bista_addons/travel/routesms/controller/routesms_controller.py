
#import web.http as http
##from http import request
#import openerp.pooler as pooler
#        {'params': {'a': 65765, 'b': 213},{'a': 65765, 'b': 213},{'a': 65765, 'b': 213}} calling data format  su openerp -c 'python openerp-server --db-filter=odoo_demo'
from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import module_boot, login_redirect
import openerp.pooler as pooler
from openerp import SUPERUSER_ID
import ast
import base64
import csv
import functools
import glob
import itertools
import jinja2
import logging
import operator
import datetime
import hashlib
import os
import re
import simplejson
import sys
import time
import urllib2
import zlib
from xml.etree import ElementTree
from cStringIO import StringIO

import babel.messages.pofile
import werkzeug.utils
import werkzeug.wrappers
try:
    import xlwt
except ImportError:
    xlwt = None

import openerp
import openerp.modules.registry
from openerp.addons.base.ir.ir_qweb import AssetsBundle, QWebTemplateNotFound
from openerp.modules import get_module_resource
from openerp.tools import topological_sort
from openerp.tools.translate import _
from openerp import http
from openerp.addons.web.http import Controller, route, request
from openerp.addons.web.controllers.main import _serialize_exception
from openerp.osv import osv
from openerp.tools import html_escape

import simplejson
from werkzeug import exceptions, url_decode
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse
from werkzeug.datastructures import Headers
from reportlab.graphics.barcode import createBarcodeDrawing

from openerp.addons.web.http import Controller, route, request
from openerp.addons.web.controllers.main import _serialize_exception
from openerp.osv import osv
from openerp.tools import html_escape

import simplejson
from werkzeug import exceptions, url_decode
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse
from werkzeug.datastructures import Headers
from reportlab.graphics.barcode import createBarcodeDrawing







class ReportController(openerp.addons.report.controllers.main.ReportController):


    @route([
        '/report/<path:converter>/<reportname>',
        '/report/<path:converter>/<reportname>/<docids>',
    ], type='http', auth='user', website=True)
    def report_routes(self, reportname, docids=None, converter=None, **data):
#        import ipdb;ipdb.set_trace()
        report_obj = request.registry['report']
        cr, uid, context = request.cr, request.uid, request.context
        uid=1
        if docids:
            docids = [int(i) for i in docids.split(',')]
        options_data = None
        if data.get('options'):
            options_data = simplejson.loads(data['options'])
        if data.get('context'):
            # Ignore 'lang' here, because the context in data is the one from the webclient *but* if
            # the user explicitely wants to change the lang, this mechanism overwrites it. 
            data_context = simplejson.loads(data['context'])
            if data_context.get('lang'):
                del data_context['lang']
            context.update(data_context)

        if converter == 'html':
            html = report_obj.get_html(cr, uid, docids, reportname, data=options_data, context=context)
            return request.make_response(html)
        elif converter == 'pdf':
            pdf = report_obj.get_pdf(cr, uid, docids, reportname, data=options_data, context=context)
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            raise exceptions.HTTPException(description='Converter %s not implemented.' % converter)




    @http.route(['/report/download'], type='http', auth="user")
    def report_download(self, data, token):
        """This function is used by 'qwebactionmanager.js' in order to trigger the download of
        a pdf/controller report.

        :param data: a javascript array JSON.stringified containg report internal url ([0]) and
        type [1]
        :returns: Response with a filetoken cookie and an attachment header
        """
        
        requestcontent = simplejson.loads(data)
        url, type = requestcontent[0], requestcontent[1]
        try:
            if type == 'qweb-pdf':
                    
                reportname = url.split('/report/pdf/')[1].split('?')[0]

                docids = None
                if '/' in reportname:
                    reportname, docids = reportname.split('/')
                #############FOr INVOCIES ONLY#############
                 
                if 'account.report_invoice' in url :
                    
                    if url.count(',') == 0 : 
                        
                        state=http.request.env['account.invoice'].browse(int(url.split('/')[-1])).state
                        if state in ['open','paid'] : 
                             
                            reportname=http.request.env['account.invoice'].browse(int(url.split('/')[-1])).number
                    
                #############FOr INVOCIES ONLY ENDS#############
                if docids:
                    # Generic report:
                    response = self.report_routes(reportname, docids=docids, converter='pdf')
                else:
                    # Particular report:
                    data = url_decode(url.split('?')[1]).items()  # decoding the args represented in JSON
                    response = self.report_routes(reportname, converter='pdf', **dict(data))

                response.headers.add('Content-Disposition', 'attachment; filename=%s.pdf;' % reportname)
                response.set_cookie('fileToken', token)
                return response
            elif type =='controller':
                reqheaders = Headers(request.httprequest.headers)
                response = Client(request.httprequest.app, BaseResponse).get(url, headers=reqheaders, follow_redirects=True)
                response.set_cookie('fileToken', token)
                return response
            else:
                return
        except Exception, e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return request.make_response(html_escape(simplejson.dumps(error)))







class Academy(http.Controller):
    #@http.route('/academy/academy/', auth='public')
    #path='/web?debug=#view_type=kanban&model=hr.employee&menu_id=383&action=468'
    @http.route('/news',type='http', auth='public')
    def index(self, **kw):
        #import ipdb;ipdb.set_trace()
        #return http.request.render('routesms.listing')
        return '''<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="bista" >

    <title>Odoo News Updates</title>

    <!-- Bootstrap Core CSS -->
    <link href="http://103.16.101.59/news_style/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="http://103.16.101.59/news_style/clean-blog.min.css" rel="stylesheet">

    <!-- Custom Fonts -->
    <link href="http://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet" type="text/css">
    <link href='http://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic' rel='stylesheet' type='text/css'>
    <link href='http://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800' rel='stylesheet' type='text/css'>

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>

    <!-- Navigation -->
    <nav class="navbar navbar-default navbar-custom navbar-fixed-top">
        <div class="container-fluid">
            <!-- Brand and toggle get grouped for better mobile display -->
            <div class="navbar-header page-scroll">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <!--<a class="navbar-brand" href="index.html">Start Bootstrap</a>-->
            </div>

            <!-- Collect the nav links, forms, and other content for toggling -->
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul class="nav navbar-nav navbar-right">
                    <!--<li>
                        <a href="index.html">Home</a>
                    </li>
                    <li>
                        <a href="about.html">About</a>
                    </li>
                    <li>
                        <a href="post.html">Sample Post</a>
                    </li>-->
                    <li>
                        <a href="http://www.bistasolutions.com/" target="new" >Contact US</a>
                    </li>
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </div>
        <!-- /.container -->
    </nav>

    <!-- Page Header -->
    <!-- Set your background image for this header on the line below. -->
    <header class="intro-header" style="background-image: url('http://103.16.101.59/news_style/home-bg.jpeg')">
        <div class="container">
            <div class="row">
                <div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
                    <div class="site-heading">
                        <!--<h1>News Updates</h1>-->
                        
                        <!--<span class="subheading">A Clean Blog Theme by Start Bootstrap</span>-->
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <div class="container">
        <div class="row">
            <div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
                <div class="post-preview">
                <h1 style="color: #AF1173"><u>     News Updates </u></h1>
                    <a href="http://103.16.101.59/page/31may/reject_partner/partner_rejection.html" target="new" >
                        <h2 class="post-title">
                                    Partner (Customer / Supplier) Rejection / Cancellation with Auto Mail Notification
                        </h2>
                        <h3 class="post-subtitle">
                            Rejecting partner form by accounts team
                        </h3>
                    </a>
                    <p class="post-meta">Posted by <b>Shashank Verma</b> on May 31, 2015</p>
                </div>
                <hr>
                <div class="post-preview">
                    <a href="http://103.16.101.59/page/31may/partner/partner.html" target="new" >
                        <h2 class="post-title">
                            Modification in Partner (Customer / Supplier) form
                        </h2>

                        <h3 class="post-subtitle">
                            Diplaying Odoo Id in partner list view & default is_company=True functionality
                        </h3>                        
                    </a>
                    <p class="post-meta">Posted by <b>Shashank Verma</b> on May 31, 2015</p>
                </div>
                <hr>
                <div class="post-preview">
                    <a href="http://103.16.101.59/page/31may/bank_validation/bank_validation.html" target="new" >
                        <h2 class="post-title">
                            Bank Account Validation On Customer Invoices
                        </h2>
                        <h3 class="post-subtitle">
                            Validate invoices if bank account currency matches invoice currency
                        </h3>
                    </a>
                    <p class="post-meta">Posted by <b>Shashank Verma</b> on May 31, 2015</p>
                </div>
                <hr>
                <div class="post-preview">
                    <a href="http://103.16.101.59/page/31may/inv_salperson/inv_salesperson.html" target="new" >
                        <h2 class="post-title">
                            Modification in Salesperson & Account Users For Invoicing
                        </h2>
                        <h3 class="post-subtitle">
                                    Adding partner's business manager and responsible user in invoice document
                        </h3>
                    </a>
                    <p class="post-meta">Posted by <b>Shashank Verma</b> on May 31, 2015</p>
                </div>

                <hr>
                <div class="post-preview">
                    <a href="http://103.16.101.59/page/31may/293duplicate_invoice/29T_inv_duplication.html" target="new" >
                        <h2 class="post-title">
                            Supplier Invoices Duplication for 29 THREE HOLIDAYS PVT. LTD Company
                        </h2>
                        <h3 class="post-subtitle">
                                    Creating customer invoice in draft state from supplier invoice 
                        </h3>
                    </a>
                    <p class="post-meta">Posted by <b>Shashank Verma</b> on May 31, 2015</p>
                </div>                
                <hr>
                <!-- Pager -->
                <ul class="pager">
                    <!--<li class="next">
                        <a href="#">Older Posts &rarr;</a>
                    </li>-->
                </ul>
            </div>
        </div>
    </div>

    <hr>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="row">
                <div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
                    <ul class="list-inline text-center">
                        <li>
                            <a href="https://twitter.com/bistasolutions1" target="new">
                                <span class="fa-stack fa-lg">
                                    <i class="fa fa-circle fa-stack-2x"></i>
                                    <i class="fa fa-twitter fa-stack-1x fa-inverse"></i>
                                </span>
                            </a>
                        </li>
                        <li>
                            <a href="https://www.facebook.com/BistaSolutionsInc" target="new" >
                                <span class="fa-stack fa-lg">
                                    <i class="fa fa-circle fa-stack-2x"></i>
                                    <i class="fa fa-facebook fa-stack-1x fa-inverse"></i>
                                </span>
                            </a>
                        </li>
                        <li>
<!--                            <a href="#">
                                <span class="fa-stack fa-lg">
                                    <i class="fa fa-circle fa-stack-2x"></i>
                                    <i class="fa fa-github fa-stack-1x fa-inverse"></i>
                                </span>
                            </a>-->
                        </li>
                    </ul>
                    <p class="copyright text-muted">Copyright &copy; Bista Solutions 2015</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- jQuery -->
    <script src="http://103.16.101.59/news_style/jquery.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="http://103.16.101.59/news_style/bootstrap.min.js"></script>

    <!-- Custom Theme JavaScript -->
    <script src="http://103.16.101.59/news_style/clean-blog.min.js"></script>

</body>

</html>
       '''













# class Home(openerp.addons.web.controllers.main.Home):
# 
# 
# 
#     @http.route('/web', type='http', auth="none")
#     def web_client(self, s_action=None, **kw):
#        # import ipdb;ipdb.set_trace()
#         return ''' <html xmlns="http://www.w3.org/1999/xhtml">
# <head>
# <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
# <title>Coming Soon</title>
# <link href="tools/style.css" rel="stylesheet" type="text/css" />
# <script type="text/javascript" src="tools/jquery.min.js"></script> 
# <script type="text/javascript" src="tools/cufon-yui.js"></script>
# <script >
# 
# function validateForm() {
#     var x = document.forms["myForm"]["fname"].value;
#     //if (x == null || x == "") {
#         if (x) {
#             body="Dear Shashank ,"
#         window.location="mailto:shashank.verma@bistacloud.com?subject=ROUTESMS SERVER DOWN &body="+body;
#         //alert("Name must be filled out");
#         return false;
#     
#     }
# }
# 
# </script>
# <script type="text/javascript" src="tools/Bebas_400.font.js"></script>
# <script type="text/javascript" src="tools/Bell_Gothic_Std_300.font.js"></script>
# <script type="text/javascript">
#     Cufon.replace('a.logo', {fontFamily: 'Bebas'});
#     Cufon.replace('a.logo span', {fontFamily: 'Bell Gothic Std'});
# </script>
# <style>
# body,div,dl,dt,dd,ul,ol,li,h1,h2,h3,h4,h5,h6,pre,code,form,fieldset,legend,input,textarea,p,blockquote,th,td{margin:0;padding:0;}table{border-collapse:collapse;border-spacing:0;}fieldset,img{border:0;}address,caption,dfn,th,var{font-style:normal;font-weight:normal;}li{list-style:none;}caption,th{text-align:left;}h1,h2,h3,h4,h5,h6{font-size:100%;font-weight:normal;}
# .submit11{
# width: 150px;
# height: 61px;
# float: left;
# background: url(http://res.cloudinary.com/shazz0020/image/upload/v1429382462/submit_thi8cw.png) left top no-repeat;
# border: none;
# }
# 
# .submit11:hover{
# float: left;
# background: url(http://res.cloudinary.com/shazz0020/image/upload/v1429382462/submit_thi8cw.png) left bottom no-repeat;
# }
# 
# body{
# margin:0;
# padding:0;
# background:url(http://res.cloudinary.com/shazz0020/image/upload/v1429382281/odoo_tcs6yq.jpg) top center no-repeat;
# background-size: 100% 150%;
# font-family: Helvetica Neue, Helvetica, Arial;
# }
# 
# .main_container{
# width: 940px;
# margin: 0 auto;
# }
# 
# .header{
# width: 940px;
# float: left;
# }
# 
# a{
# color: #fff;
# text-decoration: none;
# }
# 
# a:hover
# {
# text-decoration: underline;
# }
# 
# a.logo{
# width: 418px;
# padding-top: 20px;
# margin: 0 auto ;
# height: 145px;
# text-align: center;
# font-size: 31px;
# color: #fff;
# display: block;
# background: url(http://res.cloudinary.com/shazz0020/image/upload/v1429382546/routesms_ttgzvq.jpg) center top  no-repeat;
# }
# 
# a.logo span{
# display: block;
# font-size: 10px;
# font-family: Bell Gothic Std;
# font-weight: 100;
# text-transform: uppercase;
# text-align: center;
# letter-spacing: 1px;
# }
# 
# a:hover.logo{
# text-decoration: none;
# } 
# 
# .content{
# width: 940px;
# float: left;
# padding-bottom: 70px;
# background: url(http://res.cloudinary.com/shazz0020/image/upload/v1429382596/divider_j3mzws.png) center bottom no-repeat;
# margin-bottom: 25px;
# }
# 
# h1{
# font-size: 152px;
# font-weight: bold;
# line-height: 90px;
# letter-spacing: -2px;
# color: #fff;
# float: left;
# text-shadow:0px 5px 5px #162647;
# }
# 
# h1 span{
# display: block;
# font-size: 44px;
# font-weight: 200;
# color: #d2e1ff;
# letter-spacing: 0;
# }
# 
# .right_side{
# width: 376px;
# float: right;
# margin-top: 10px;
# }
# 
# .right_side p{
# font-size: 30px;
# letter-spacing: -1px;
# color: #fff;
# font-weight: 200;
# line-height: 50px;
# }
# 
# ul.s_icons{
# width: 376px;
# height: 27px;
# margin-top: 15px;
# }
# 
# ul.s_icons li{
# float: left;
# background: url(/home/bista/shanky/routesms/code/addons/routesms/controller/images/s_icons.png) 0 0 no-repeat;
# height: 27px;
# }
# 
# ul.s_icons li a{
# display: block;
# height: 27px;
# }
# 
# ul.s_icons li.fb{
# margin-right: 36px;
# width: 100px;
# height: 27px;
# background-position: 0 0;
# }
# 
# ul.s_icons li.fb:hover{
# background-position: left bottom;
# }
# 
# ul.s_icons li.tw{
# margin-right: 38px;
# background-position: -136px 0;
# width: 100px;
# height: 27px;
# }
# 
# ul.s_icons li.tw:hover{
# background-position: -136px bottom;
# }
# 
# ul.s_icons li.in{
# width: 101px;
# height: 27px;
# background-position: -275px 0;
# }
# 
# ul.s_icons li.in:hover{
# background-position: -275px bottom;
# }
# 
# .email{
# width: 643px;
# margin: 0 auto;
# }
# 
# .field{
# width: 423px;
# height: 61px;
# float: left;
# background: url(http://res.cloudinary.com/shazz0020/image/upload/v1429382637/field_kle5zn.png) left top no-repeat;
# border: 0;
# padding: 0 35px;
# font-size: 26px;
# color: #8598bb;
# font-family: Helvetica Neue, Helvetica, Arial;
# }
# 
# 
# 
# 
# 
# </style>
# </head>
# <body>
# <div class="main_container">
#     <div class="header">
#         <a class="logo" href="http://routesms.com/"><span></span></a>
#     </div>
#     <div class="content">
#         <h1>Hello.<span>Site is updating ,We are coming  back soon</span></h1>
#         <div class="right_side">
#             <!--<p>// <a href="#">info@somename.com</a><br/>// 506-200-5871</p>
#             <ul class="s_icons">
#                 <li class="fb"><a href="#"></a></li>
#                 <li class="tw"><a href="#"></a></li>
#                 <li class="in"><a href="#"></a></li>
#             </ul>-->
#         </div>
#     </div>
#     
#     
# 
# <form name="myForm" action="demo_form.asp1"
#  method="post" onsubmit="return validateForm()" >
# <input type="text" class="field" name="fname" onfocus="if(this.value=='Get Notified (Email Address)') this.value='';" onblur="if(this.value=='' || this.value==' ') this.value='Get Notified (Email Address)';" value="support@bistasolutions">
# <input type="submit" class="submit11" value="">
# </form>
#     
# </div>
# </body>
# </html>

#'''



# class Home(http.Controller):
#     @http.route('/web', type='http', auth="public")
#     def api_url(self, **req):
#         import ipdb;ipdb.set_trace()
#         return "<h1>Sorry !  Only Administartor has authoirty to Manage Database</h1>"
        #{'params': {'partner_id': 'your_customer_id', 'invoice_date': 'yy-mm-dd','due_date':'yy-mm-dd','currency_id':'INR','company_id':'Company Name','user_id':'Saleperson','partner_bank_id':'Account Number','product_detail':[{'product_id':'product name','quantity':1,'price_unit':0.0}]}}
#        osv_pool = pooler.get_pool('odoo_demo')
#         
#         print "fields-------------",req
#         
#         inv_obj = request.registry.get('account.invoice').search(request.cr, SUPERUSER_ID, [])
#         
        
        
        

#        params = dict(map(operator.itemgetter('name', 'value'), fields))
#        print "params--------------",params
##        print "users+++++++++++++++",cert_type
#        user = osv_pool.get('res.users')
#        print "users------------",user
##        return "<h1>This is a test</h1>"
        #return {'odoo_response':'API Successfull!!!'}
 #       '''
