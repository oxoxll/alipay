支付宝第三方接口 使用说明：


1、在处理支付的模块中，引入alipay模块（alipay.py），并创建alipay类的实例： 
#以下包含的内容替换为实际的内容。 
#多商家用户，以下内容都为动态生成：
import alipay  
alipayTool=alipay.alipay(  
                partner="支付宝身份ID",  
                key="支付宝生成的key",  
                sellermail="商家支付宝帐号（邮箱）",  
                notifyurl="异步回调的URL",  
                returnurl="跳转回的URL",  
                showurl="显示网站商品的URL"  
                )  


2、在支付页面（即用户点击支付按钮即转到支付宝付款的页面），我们需要在这个页面产生一个隐藏的表单，用来提交订单信息： 

#支付信息，订单号必须唯一。  
#以下包含的内容替换为实际的内容。  
params={  
      'out_trade_no':<订单号>,  
      'subject'     :<订单subject>,  
      'body'        :<订单说明>,  
      'total_fee'   :<订单总额>  
}  
payhtml=alipayTool.createPayForm(params)  
#将payhtml写到页面，这是个包含有提交按钮的表单  


3、异步回调处理： 
# f 为包含POST过来的数据python字典，即名-值对。  
# verify 是否回调支付宝确认数据是否真实有效  
# rlt为处理的结果，为success或fail  
  
rlt=alipayTool.notifiyCall(f,verify=True)  
  
#依据支付宝的要求，此URL返回的值为success或fail  
#因此，当rlt为success时（即支付成功），做相应的处理  
#然后，直接将rlt写到输出流。  
  
if rlt=='success':  
     paySuccess(f['out_trade_no'])  
  
return rlt  


4、跳转回调处理： 
Python代码  收藏代码
#注意，与异步回处理相同，在跳转回调的处理上，仍是调用notifiyCall函数  
#并且参数与返回完全一样。  
  
rlt=alipayTool.notifiyCall(f,verify=True)  
  
#只是验证后的处理不同，这里需要给用户显示一个页面。  
if rlt=='success':  
   paySuccess(f['out_trade_no'])  
   #显示支付成功的页面  
   .....  
else:  
   #显示未能成功支付的页面  
  .....  


通过上面的4个步骤，我们就可以成功的与支付宝集成，并且实现了回调验证。 

alipay模块依赖的两个外部模块为hashlib与urllib2，另外，使用的字符编码UTF-8。