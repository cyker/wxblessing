#-*- coding:utf-8 -*-
#author:ciker
#version:0.0.1
'''
    微信发送祝福信息，可以自定义发送祝福信息
    
'''

import wxpy
import re
import sys
import os
import time
import queue
import random


class WXBLESSING:
    def __init__(self, debugLevel=1, update=True):
        self.debugLevel = debugLevel
        self.path = os.getcwd() + "\\"
        self.wxCachePath = self.path + "cache"
        self.configPath = self.path + "config\\send.py"
        self.bot = wxpy.Bot(cache_path=True)
        self.bot.enable_puid()
        self.blessQ = queue.Queue()
        self.blessReplace = "%!sendname!%"
        if update:
            self.Inition()

    def debug(self, msg, level=1):
        if level <= self.debugLevel:
            print("[debug:%s]" % (msg))

    def Filter(self, s):
        tmp = str(s).replace('"','\\\"')
        return tmp

    def Inition(self):
        friends = self.bot.friends(update=True)
        groups = self.bot.groups(update=True)
        print(self.wxCachePath)
        self.debug("friends :%s"%str(friends),3)
        self.debug("groups :%s"%str(groups), 3)
        with open(self.configPath, mode='w', encoding='utf-8') as file:
            writeData = "#-*- coding:utf-8 -*-\n" \
                        "sendtime = \"2018-02-16 00:00:00\"\n" \
                        "groups={\n\t" \

            for group in groups:
                writeData = writeData + "\"{0}\":{{\"send\":\"N\",\"order\":\"A\",\"puid\":\"{1}\"}},\n\t".format(self.Filter(group.name),self.Filter(group.puid))
            writeData = writeData + "}\n" \
                                    "friends={"


            for friend in friends:
                writeData = writeData + "\"{0}\":{{\"sendName\":\"{1}\",\"send\":\"Y\",\"order\":\"A\",\"puid\":\"{2}\"}},\n\t".format(self.Filter(friend.name),self.Filter(friend.name),self.Filter(friend.puid))
            writeData = writeData + "}\n"

            self.debug("writeDate %s"%writeData)
            file.write(writeData)

    def LoadConfig(self):
        import config.send as conf
        import config.bless as bless

        self.sendtime = int(time.mktime(time.strptime(conf.sendtime,"%Y-%m-%d %H:%M:%S")))
        self.blessStr = bless.bless
        count = len(self.blessStr)
        for group in conf.groups.values():
            if group['send'] == 'Y':
                self.debug(group)
                if group['order'] == 'A':
                    queue = {"type":"group","puid":group['puid'],"bless":(self.blessStr[str(random.randint(0,count-1))]).replace(self.blessReplace,group['sendName'])}
                else:
                    queue = {"type":"group","puid":group['puid'],"bless":(self.blessStr[group['order']]).replace(self.blessReplace,group['sendName'])}
                self.blessQ.put(queue)

        for friend in conf.friends.values():
            if friend['send'] == 'Y':
                if friend['order'] == 'A':
                    queue = {"type":"friend","puid":friend['puid'],"bless":(self.blessStr[str(random.randint(0,count-1))]).replace(self.blessReplace,friend['sendName'])}
                else:
                    queue = {"type":"friend","puid":friend['puid'],"bless":(self.blessStr[friend['order']]).replace(self.blessReplace,friend['sendName'])}
                self.blessQ.put(queue)

    def SendBless(self, type, puid, bless):
        # self.bot.
        # self.bot.search()
        # wxs = self.bot.chats().search(puid=puid)
        self.debug('type :%s'%type,3)
        if type == 'friend':
            wxs = self.bot.friends().search(puid=puid)[0]
        else:
            wxs = self.bot.groups.search(puid=puid)

        try:
            wxs.send_msg(str(bless))
            return False
        except wxpy.ResponseError as e:
            self.debug("error_code:%s ; error_message:%s"%(str(e.err_code),str(e.err_msg)))
            return e.err_code
        # wxpy.embed()


    def Moniter(self):
        while True:
            now = int(time.time())
            if now < self.sendtime:
                time.sleep(1)
                continue
            else:
                return True

    def wxmain(self):
        if os.path.exists(self.configPath) == False:
            self.Inition()
            exit(0)
        self.LoadConfig()
        self.Moniter()
        while self.blessQ.empty() == False:
            wxq = self.blessQ.get()
            if self.SendBless(wxq['type'],wxq['puid'],wxq['bless']):
                self.debug('error puid%s', 2)
                self.blessQ.put(wxq)




if __name__ == '__main__':
    wx = WXBLESSING(debugLevel=3, update=False)
    wx.wxmain()
