import smtplib
import urllib
def sendmail_old(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.logix.in:2525'):
    try : 
        header  = 'From: %s\n' % from_addr
        header += 'To: %s\n' % ','.join(to_addr_list)
        header += 'Cc: %s\n' % ','.join(cc_addr_list)
        header += 'Subject: %s\n\n' % subject
        message = header + message
       # import ipdb;ipdb.set_trace()
        server = smtplib.SMTP(smtpserver)
        server.starttls()
        server.login(login,password)
        
        problems = server.sendmail(from_addr, to_addr_list + cc_addr_list ,message)
        server.quit()
        return True
    
    except Exception as E :
        
        return False


def sendmail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='czismtp.logix.in:587'):
    try : 
        header  = 'From: %s\n' % from_addr
        header += 'To: %s\n' % ','.join(to_addr_list)
        header += 'Cc: %s\n' % ','.join(cc_addr_list)
        header += 'Subject: %s\n\n' % subject
        message = header + message
        #import ipdb;ipdb.set_trace()
        server = smtplib.SMTP(smtpserver)
        server.starttls()
        server.login(login,password)
        
        problems = server.sendmail(from_addr, to_addr_list + cc_addr_list ,message)
        server.quit()
        return True
    
    except Exception as E :
        
        return False 

def check_internet_connection(erp_url):
#	import ipdb;ipdb.set_trace()  
	try :
	    data = urllib.urlopen(erp_url)
	    return True
	except Exception as e:
	    return False



