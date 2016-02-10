#!/usr/bin/python
# -*- coding: utf-8 -*-

import xmlrpclib
import urllib2, urllib
from urllib import urlencode
import os
import time
import hashlib
import socket
import re
import string
from ProxyedTransp import ProxyedTransp

MAX_EVENTS = 50
MAX_SKIP = 100
MAX_ITEMS = 50
ONE_PAGE = 20

LJ_SERVER = "http://www.livejournal.com/interface/xmlrpc:80"
LJ_USERPICS = 'http://l-userpic.livejournal.com/'
LJ_SHORT = "http://www.livejournal.com/"

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class LiveJournal:
    """
    This class provide funct to access LivrJournal API
    http://www.livejournal.com/doc/server/ljp.csp.xml-rpc.protocol.html
    """
    def __init__(self, proxy=""):
        
        self.sync_date = None
        if proxy == "":
            self.server = xmlrpclib.Server(LJ_SERVER)
            self.opener = urllib2.build_opener(urllib2.HTTPHandler)
        else:
            proxyed = ProxyedTransp()
            proxyed.set_proxy(proxy)
            self.server = xmlrpclib.ServerProxy(LJ_SERVER,
                                                transport=proxyed)
            proxy_support = urllib2.ProxyHandler(
                                        {'http': 'http://' + proxy})
            self.opener = urllib2.build_opener(proxy_support,
                                               urllib2.HTTPHandler)
                                               
        urllib2.install_opener(self.opener)
    
    def exec_xmlrpc(self, funct, param):
        """
        execute XML-RPc query, return result and convert for errors
        """

        param.update({'ver': '1'})


        req = 'self.server.LJ.XMLRPC.' + funct + '(' + repr(param) + ')'
            
        res = eval(req)

        return res
        
    def check_login(self, name, password):
        param = {}
        param.update({
            'username': name,
            'hpassword': hashlib.md5(str(password)).hexdigest(),
            'getpickws': '1',
            'getpickwurls': '1'
        })
        
        res = self.exec_xmlrpc('login', param)
        
        return res

     
    def send_post(self, name, password, title, text, tags=''):
        """
        Send post to LiveJournal
        
        """

        moment = time.localtime()

        param = {}
        param.update({
                      'username': name,
                      'hpassword': hashlib.md5(str(password)).hexdigest(),
                      'event': str(text).replace('\n', '<br />'),
                      'subject': title,
                      'props': {
                                'taglist': tags,
                                'opt_preformatted': True,
                                'opt_nocomments': 0
                               },
                      'security': 'public',
                      'allowmask': '1',
                      'year': moment[0],
                      'mon': moment[1],
                      'day': moment[2],
                      'hour': moment[3],
                      'min': moment[4],
                      'lineendings': 'unix'
                     })

        #if msg.journal:
        #param['usejournal'] = 'scribo_test_grp'

        return self.exec_xmlrpc('postevent', param)
  
 
    def edit_post(self, name, password, itemid, title, text, tags=''):
        """
        Edit existing post on LiveJournal
        
        """

        #moment = time.strptime(msg.date, TIME_FORMAT)
        moment = time.localtime()

        param = {}
        param.update({
                      'username': name,
                      'hpassword': hashlib.md5(str(password)).hexdigest(),
                      'itemid': itemid,
                      'event': text,
                      'subject': title,
                      'props': {
                                'taglist': tags,
                                'opt_preformatted': True,
                                'opt_nocomments': 0
                               },
                      'security': 'public',
                      'allowmask': '1',
                      'year': moment[0],
                      'mon': moment[1],
                      'day': moment[2],
                      'hour': moment[3],
                      'min': moment[4],
                      'lineendings': 'unix'
                     })
                     
        return self.exec_xmlrpc('editevent', param)


    def _get_all_posts(self, name, password):
        """
        Get all posts for new account and add it
        
        @return None
        """

        param = {}
        param.update({
                      'username': name,
                      'hpassword': hashlib.md5(str(password)).hexdigest(),
                      'lineendings': 'unix',
                      'selecttype': 'lastn',
                      'howmany': str(MAX_EVENTS),
                      #'howmany': '4',
                      'itemid': '-1',
                     })

        ret = self.exec_xmlrpc('getevents', param)

        lj_posts = ret['events']

        if not lj_posts: # TODO: test this funct on account without posts
            print 'No Posts!'
            return
            
                
        while MAX_EVENTS == len(ret['events']):

            param = {}
            param.update({
                          'username': name,
                      'hpassword': hashlib.md5(str(password)).hexdigest(),
                          'lineendings': 'unix',
                          'selecttype': 'lastn',
                          'howmany': str(MAX_EVENTS),
                          'itemid': '-1',
                          'beforedate': lj_posts[-1]['eventtime']
                         })

            ret = self.exec_xmlrpc('getevents', param)

            lj_posts = lj_posts + ret['events']
               
        
        
        """
        ============== BUG FIX TO UPDATE TIME ==================
        Note: We cant take lj_posts[-1]['eventtime'] as 'lastsync' in 
              syncitems. So we have to run syncitems and take date of last
              result + 1 second as last update time. 
        """
        
        param = {'username': name,
                 'hpassword': hashlib.md5(str(password)).hexdigest()}
        param['lastsync'] = ''

        result = self.exec_xmlrpc('syncitems', param)['syncitems']

        # add 1 second to date
        last_sync = result[-1]['time']
        last_sync = time.strptime(last_sync, TIME_FORMAT)
        last_sync = time.mktime(last_sync)
        last_sync = last_sync + 1
        last_sync = time.localtime(last_sync)
        last_sync = time.strftime(TIME_FORMAT, last_sync)
        print 'last sync: ', last_sync
        
        self.sync_date = last_sync
           
        return (lj_posts, [])


    def _get_new_posts(self, name, password):
        """
        For updates from LJ we can use getevent or syncitems functions
        """


        """
        #we can search for updates using getevent, but it doesn't works well
        param = {
         'username': self.username,
         'hpassword': self.hpassword,
         'ver': '1',
         'lineendings': 'unix',
         "selecttype": "syncitems",
         #'beforedate': self.date,
         "lastsync": self.date
        }
        result = self._server.LJ.XMLRPC.getevents(param)
        """

        if not self.sync_date:
            print 'Error: no sync date!'
            return

        # syncitems works better than getevents, but getting posts one by one 
        # may take much longer
        param = {'username': name,
                 'hpassword': hashlib.md5(str(password)).hexdigest()}
        param['lastsync'] = self.sync_date

        result = self.exec_xmlrpc('syncitems', param)['syncitems']
        print result

        lj_posts_ins = []
        lj_posts_upd = []

        for i in result:
            #TODO: i['item'] can be 'L-'(posts) or 'C-'(new comments)
            if 'L' == i['item'][0]:
                item_id = i['item'][2:]
                lj_post = self._get_post(item_id, name, password)
                
                if 'update' == i['action']:
                    lj_posts_upd.append(lj_post)
                elif 'create' == i['action']:
                    lj_posts_ins.append(lj_post)

        # save new date for syncitems
        if result:
            self.sync_date = result[-1]['time']

        return (lj_posts_ins, lj_posts_upd)
        

    def del_post(self, name, password, itemid):
        """
        Delete post with this itemid from LJ
        """

        param = {}
        param.update({
                      'username': name,
                      'hpassword': hashlib.md5(str(password)).hexdigest()
                    })
        param['itemid'] = itemid

        result = self.exec_xmlrpc('editevent', param)

        return result
        
        
    def _get_post(self, postid, name, password):
        """
        Get post from LJ by itemid
        """
        param = {
                 'username': name,
                 'hpassword': hashlib.md5(str(password)).hexdigest(),
                 'lineendings': 'unix',
                 'selecttype': 'one',
                 'itemid': postid,
                 'howmany': '1'
                }
        result = self.exec_xmlrpc('getevents', param)
        if result['events'] == []:
            return  None
        return result['events'][0]


    def get_comments(self, name, password, itemid, anum):
        """
        Get comments from LJ by post's itemid and anum
        ditemid = itemid * 256 + anum
        """
        param = {}
        param.update({
                      'username': name,
                      'hpassword': hashlib.md5(str(password)).hexdigest(),
                      'ditemid': str(int(str(itemid))*256+int(str(anum))),
                      'journal':'scribo_fruct10',
                      'page': '1'
                     })

        return self.exec_xmlrpc('getcomments', param)

    def send_comment(self, name, password, title, text, itemid, anum, dtalkid='0'):
        """
        Send comment to LiveJournal post with itemid and anum 
        and parent with dtalkid
        """
        param = {}
        param.update({
                      'username': name,
                      'hpassword': hashlib.md5(str(password)).hexdigest(),
                      'body': text.encode('utf-8').replace('\n', '<br />'),
                      'subject': title,
                      'ditemid': str(int(str(itemid))*256+int(str(anum))),
                      'journal':'scribo_fruct10',
                      'parent': str(dtalkid)
                     })

        #if msg.journal:
        #param['usejournal'] = 'scribo_test_grp'
        
        return self.exec_xmlrpc('addcomment', param)
        
          
'''
param.update({
    'username': 'scribo_fruct10',
    'hpassword': hashlib.md5('test1234').hexdigest(),
    'ver': '1'
})
'''

if __name__ == "__main__":
    import uuid
    def show_child(parent, comment):
        uid = 'comment-' + str(uuid.uuid4())
        print parent, 'hasComment', uid
        print uid, 'dtalkid', comment['dtalkid']
        if 'children' in comment.keys():
            for i in comment['children']:
                show_child(uid, i)
        

    lj = LiveJournal()
    lj.sync_date = '2011-08-01 06:00:00';
    #r = lj.send_post('scribo-rpc', 'test123', 'titititit', 'tetetetet')
    r = lj._get_all_posts('scribo-rpc', 'test123')
    #r = lj._get_new_posts('scribo-rpc', 'test123')
    #r = lj.edit_post('scribo-rpc', 'test123', '973', 'updated title', 'new text 359!!', 'new')
    #r = lj.send_comment('scribo-rpc', 'test123', 'another', 'stupid comment!', 993, 177, 36017)
    #r = lj.get_comments('scribo-rpc', 'test123', '993', '177')
    print r
    #for i in r['comments']:
    #    show_child('post-123', i)
    
    '''
    for i in r:
        print "//////////////////////////////////////////////////"
        print i['itemid']
        print i['eventtime']
        print i['subject']
        print i['event']
        print "//////////////////////////////////////////////////"
    '''
