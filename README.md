# wxblessing 

微信祝福消息发送
====

    只是为了简化发送祝福消息。最真诚的祝福还是亲手为ta做一顿丰盛的晚餐。

使用说明
---

安装 wxpy 模块
<pre><code> pip3 install wxpy
</code></pre>

主要文件列表

    main.py 主程序
    config
        ../send.py  扫描运行生成的二维码，登陆微信后生成的发送祝福消息对象列表 。
        ../bless.py 祝福短消息模板

    
main.py 参数说明

    祝福模板中替换昵称的参数格式
    self.blessReplace = "%!sendname!%"
    
send.py 参数说明：

    "kk":{"sendName":"kk","send":"Y","order":"A","puid":"e22084ab"}

    键名是用昵称，<strong>sendName </strong>是发送祝福时候使用的昵称；<strong>send</strong> 是否发送祝福，群组默认为'N'；<strong>order</strong> 是发送第几条祝福短信,'A' 表示随机，这里如果填写bless.py不存在的键会报错，毕竟自己使用，就不要难为自己了；puid 这个不用管，每个微信号的唯一值

bless.py 参数说明

    "0":"%!sendname!%，新年好！新年到，好事全到了！祝您及全家新年快乐！身体健康！工作顺利！吉祥如意！"
    键名可以取你想取的名字，我一般喜欢用数字，%!sendname!% 是替换的昵称

---


详细说明及反馈请转[我的博客](http://blog.c1ker.top)




# Enjoy! :)



