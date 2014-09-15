#!/usr/bin/env python
# encoding: utf-8
'''
Created on 2014-9-12
'''
import hashlib
import urllib2

# The verfy request link:
# https://mapi.alipay.com/gateway.do?partner=合作者 身份 ID&notify_id=通知 ID 的值

verfyURL={
    # "https":"https://www.alipay.com/cooperate/gateway.do?service=notify_verify",  #out of date
    # "http" :"http://notify.alipay.com/trade/notify_query.do?",                    #out of date
    'https':'https://mapi.alipay.com/gateway.do?'
    }
gateway="https://mapi.alipay.com/cooperate/gateway.do"


class alipay:
    def __init__(self,
                 partner="partner ID",
                 key="partner key",
                 sellermail="partner email",
                 notifyurl="notifyurl call-back by alipay",
                 returnurl="returnurl skip in browser",
                 showurl="/"):
            
            self.key=key;
            self.conf={
              'partner'         :   partner,
              'service'         :   "create_direct_pay_by_user",
              'payment_type'    :   "1",
              'seller_email'    :   sellermail,
              'notify_url'      :   notifyurl,
              'return_url'      :   returnurl,
              'show_url'        :   showurl,
              '_input_charset'  :   "UTF-8",
              'sign_type'       :   "MD5",
              #if there are other params，write there default value below：
              'paymethod'       :   "",
              'mainname'        :   "",
              }

    def populateURLStr(self,params):
        ks=params.keys()
        ks.sort()
        rlt=''
        for k in ks:
            if params[k]==None or len(params[k])==0 \
                or k=="sign" or k=="sign_type" or k=="key":
                continue
            rlt=rlt+"&%s=%s"%(k,params[k])
        print "URL:"+rlt[1:]
        return rlt[1:]
        

    def buildSign(self,params):
        sign=hashlib.md5(self.populateURLStr(params)+self.key).hexdigest()
        print "md5 sign is %s" % sign;
        return sign
    
    
    '''
      Check the returned parameters from alipay, trading success notification callback.
      Two steps：
      Check whether the signature is correct,
      visit alipay to confirm the current params is returned from alipay.
      
    '''
    def notifiyCall(self,params,verify=True,transport="https"):
        sign=None
        if params.has_key('sign'):
            sign=params['sign']
        locSign=self.buildSign(params)
        
        if sign==None or locSign!=sign:
            print "sign error."
            return "fail"
        
        if params['trade_status']!='TRADE_FINISHED' and  params['trade_status']!='TRADE_SUCCESS':
            return "fail"
        
        if not verify:
            return "success"
        else:
            print "Verify the request is call by alipay.com...."
            url = verfyURL[transport] + "&partner=%s&notify_id=%s"%(self.conf['partner'],params['notify_id'])
            response=urllib2.urlopen(url)
            html=response.read()
       
            print "aliypay.com return: %s" % html
            if html=='true':
                return "success"
            
            return "fail"

    '''
        Generate the form submitted to alipay:
        
        Must contain the following items:
        out_trade_no：your trade number
        subject     :name of your subject
        body        :discription of your subject
        total_fee   :price of your subject
    '''
    def createPayForm(self,params,method="POST",title="Confirm!Pay by Alipay."):
        params.update(self.conf)
        sign=self.buildSign(params)
        params['sign']=sign
        
        ele=""
        for nm in params:
           
            print "key in params : %s"%nm
            
            if params[nm]==None or len(params[nm])==0 or nm=='_input_charset':
                continue
            ele = ele + " <input type='hidden' name='%s' value='%s' />" % (nm,params[nm])
        html='<form name="alipaysubmit" action="%s?_input_charset=%s" method="%s" target="_blank">%s<input type="submit" value="%s" /></form>' \
             % (gateway,params['_input_charset'],method,ele,title)
        return html
