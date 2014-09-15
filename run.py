#!/usr/bin/env python
# encoding: utf-8

'''
Created on 2014-9-12
'''
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
from flask import Flask, request, render_template
import alipay
app = Flask(__name__)


alipayTool=alipay.alipay(  
                partner="2088701390367738",
                key="vwggdo5pdtbk3adqm8p2n23z6ijpjiek",
                sellermail="admin@shopqi.com",
                notifyurl="http://115.29.170.111:5000/notify_page",
                returnurl="http://115.29.170.111:5000/return_page",
                showurl="/"  
            )  

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/form', methods=['GET'])
def form():
    return render_template('form.html')

@app.route('/paypage', methods=['POST'])
def paypage():
	out_trade_no=request.form.get('out_trade_no'),
	subject=request.form.get('subject'),
	body=request.form.get('body'),
	total_fee=request.form.get('total_fee')
	if (out_trade_no!=None and subject!=None and body!=None and total_fee!=None):
		params={  
	      'out_trade_no':request.form.get('out_trade_no'),
	      'subject'     :request.form.get('subject'),
	      'body'        :request.form.get('body'),
	      'total_fee'   :request.form.get('total_fee')
		}  
		payhtml=alipayTool.createPayForm(params)
		print(payhtml)
		return render_template('paypage.html',payhtml=payhtml)
	#if error show, the message
	return render_template('payform.html', message='Infomation incomplete！Please checkand submit again.')

#notifyurl notice
@app.route('/notify_page', methods=['GET','POST'])
def notify_page():
	rlt=alipayTool.notifiyCall(f,verify=True)
	if rlt=='success':  
   		# refresh browser here 
   		paySuccess(f['out_trade_no'])
   	return rlt

#returnurl notice
@app.route('/return_page', methods=['GET'])
def return_page():
	rlt=alipayTool.notifiyCall(f,verify=True)
	if rlt=='success':  
		# refresh browser here 
   		paySuccess(f['out_trade_no'])  
    	return render_template('return_page.html',{'rlt':rlt})
	return render_template('return_page.html',{'rlt':rlt})



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')


