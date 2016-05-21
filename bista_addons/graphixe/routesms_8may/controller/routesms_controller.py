
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

class Home(openerp.addons.web.controllers.main.Home):



    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
       # import ipdb;ipdb.set_trace()
        return ''' <html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Coming Soon</title>
<link href="tools/style.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="tools/jquery.min.js"></script> 
<script type="text/javascript" src="tools/cufon-yui.js"></script>
<script >

function validateForm() {
    var x = document.forms["myForm"]["fname"].value;
    //if (x == null || x == "") {
        if (x) {
            body="Dear Shashank ,"
        window.location="mailto:shashank.verma@bistacloud.com?subject=ROUTESMS SERVER DOWN &body="+body;
        //alert("Name must be filled out");
        return false;
    
    }
}

</script>
<script type="text/javascript" src="tools/Bebas_400.font.js"></script>
<script type="text/javascript" src="tools/Bell_Gothic_Std_300.font.js"></script>
<script type="text/javascript">
    Cufon.replace('a.logo', {fontFamily: 'Bebas'});
    Cufon.replace('a.logo span', {fontFamily: 'Bell Gothic Std'});
</script>
<style>
body,div,dl,dt,dd,ul,ol,li,h1,h2,h3,h4,h5,h6,pre,code,form,fieldset,legend,input,textarea,p,blockquote,th,td{margin:0;padding:0;}table{border-collapse:collapse;border-spacing:0;}fieldset,img{border:0;}address,caption,dfn,th,var{font-style:normal;font-weight:normal;}li{list-style:none;}caption,th{text-align:left;}h1,h2,h3,h4,h5,h6{font-size:100%;font-weight:normal;}
.submit11{
width: 150px;
height: 61px;
float: left;
background: url(http://res.cloudinary.com/shazz0020/image/upload/v1429382462/submit_thi8cw.png) left top no-repeat;
border: none;
}

.submit11:hover{
float: left;
background: url(http://res.cloudinary.com/shazz0020/image/upload/v1429382462/submit_thi8cw.png) left bottom no-repeat;
}

body{
margin:0;
padding:0;
background:url(http://res.cloudinary.com/shazz0020/image/upload/v1429382281/odoo_tcs6yq.jpg) top center no-repeat;
background-size: 100% 150%;
font-family: Helvetica Neue, Helvetica, Arial;
}

.main_container{
width: 940px;
margin: 0 auto;
}

.header{
width: 940px;
float: left;
}

a{
color: #fff;
text-decoration: none;
}

a:hover
{
text-decoration: underline;
}

a.logo{
width: 418px;
padding-top: 20px;
margin: 0 auto ;
height: 145px;
text-align: center;
font-size: 31px;
color: #fff;
display: block;
background: url(http://res.cloudinary.com/shazz0020/image/upload/v1429382546/routesms_ttgzvq.jpg) center top  no-repeat;
}

a.logo span{
display: block;
font-size: 10px;
font-family: Bell Gothic Std;
font-weight: 100;
text-transform: uppercase;
text-align: center;
letter-spacing: 1px;
}

a:hover.logo{
text-decoration: none;
} 

.content{
width: 940px;
float: left;
padding-bottom: 70px;
background: url(http://res.cloudinary.com/shazz0020/image/upload/v1429382596/divider_j3mzws.png) center bottom no-repeat;
margin-bottom: 25px;
}

h1{
font-size: 152px;
font-weight: bold;
line-height: 90px;
letter-spacing: -2px;
color: #fff;
float: left;
text-shadow:0px 5px 5px #162647;
}

h1 span{
display: block;
font-size: 44px;
font-weight: 200;
color: #d2e1ff;
letter-spacing: 0;
}

.right_side{
width: 376px;
float: right;
margin-top: 10px;
}

.right_side p{
font-size: 30px;
letter-spacing: -1px;
color: #fff;
font-weight: 200;
line-height: 50px;
}

ul.s_icons{
width: 376px;
height: 27px;
margin-top: 15px;
}

ul.s_icons li{
float: left;
background: url(/home/bista/shanky/routesms/code/addons/routesms/controller/images/s_icons.png) 0 0 no-repeat;
height: 27px;
}

ul.s_icons li a{
display: block;
height: 27px;
}

ul.s_icons li.fb{
margin-right: 36px;
width: 100px;
height: 27px;
background-position: 0 0;
}

ul.s_icons li.fb:hover{
background-position: left bottom;
}

ul.s_icons li.tw{
margin-right: 38px;
background-position: -136px 0;
width: 100px;
height: 27px;
}

ul.s_icons li.tw:hover{
background-position: -136px bottom;
}

ul.s_icons li.in{
width: 101px;
height: 27px;
background-position: -275px 0;
}

ul.s_icons li.in:hover{
background-position: -275px bottom;
}

.email{
width: 643px;
margin: 0 auto;
}

.field{
width: 423px;
height: 61px;
float: left;
background: url(http://res.cloudinary.com/shazz0020/image/upload/v1429382637/field_kle5zn.png) left top no-repeat;
border: 0;
padding: 0 35px;
font-size: 26px;
color: #8598bb;
font-family: Helvetica Neue, Helvetica, Arial;
}





</style>
</head>
<body>
<div class="main_container">
    <div class="header">
        <a class="logo" href="http://routesms.com/"><span></span></a>
    </div>
    <div class="content">
        <h1>Hello.<span>Site is updating ,We are coming  back soon</span></h1>
        <div class="right_side">
            <!--<p>// <a href="#">info@somename.com</a><br/>// 506-200-5871</p>
            <ul class="s_icons">
                <li class="fb"><a href="#"></a></li>
                <li class="tw"><a href="#"></a></li>
                <li class="in"><a href="#"></a></li>
            </ul>-->
        </div>
    </div>
    
    

<form name="myForm" action="demo_form.asp1"
 method="post" onsubmit="return validateForm()" >
<input type="text" class="field" name="fname" onfocus="if(this.value=='Get Notified (Email Address)') this.value='';" onblur="if(this.value=='' || this.value==' ') this.value='Get Notified (Email Address)';" value="support@bistasolutions">
<input type="submit" class="submit11" value="">
</form>
    
</div>
</body>
</html>

'''



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
