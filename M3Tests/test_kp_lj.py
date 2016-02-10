#!/usr/bin/python
# -*- coding: utf-8 -*-

#namespaces:
#foaf http://xmlns.com/foaf/spec/index.rdf
#scribo http://cs.karelia.ru#

from M3Core.m3_kp import *
import signal
import time
import LiveJournal
import base64
import uuid
import inspect
import sys

#SIB_IP = "194.85.173.9"
SIB_IP = "192.168.0.33"
#SIB_IP = "172.20.0.62"

PROXY = "proxy.karelia.ru:81"

POST = "2"     # read 
COMMENT = "3"  # comment
noexit = True

# property constants
PERSON_INFO = "http://www.cs.karelia.ru/smartscribo#personInformation"
ACCOUNT = "http://xmlns.com/foaf/0.1/account"
LOGIN = "http://www.cs.karelia.ru/smartscribo#login"
PASSWORD = "http://www.cs.karelia.ru/smartscribo#password"
NICKNAME = "http://www.cs.karelia.ru/smartscribo#nickname"
HAS_POST = "http://www.cs.karelia.ru/smartscribo#hasPost"
HAS_COMMENT = "http://www.cs.karelia.ru/smartscribo#hasComment"
POSTER = "http://www.cs.karelia.ru/smartscribo#poster"
SERVICE = "http://www.cs.karelia.ru/smartscribo#service"
USERPIC = "http://www.cs.karelia.ru/smartscribo#userpic"
BDATE = "http://www.cs.karelia.ru/smartscribo#bdate"
SYNCDATE = "http://www.cs.karelia.ru/smartscribo#syncdate"
JOURNAL = "http://www.cs.karelia.ru/smartscribo#journal"
ITEMID = "http://www.cs.karelia.ru/smartscribo#itemid"
ANUM = "http://www.cs.karelia.ru/smartscribo#anum"
DTALKID = "http://www.cs.karelia.ru/smartscribo#dtalkid"
PDATE = "http://www.cs.karelia.ru/smartscribo#pdate"
TITLE = "http://www.cs.karelia.ru/smartscribo#title"
TEXT = "http://www.cs.karelia.ru/smartscribo#text"
TYPE = "type"

# class constants
CLASS_POST = "http://www.cs.karelia.ru/smartscribo#Post"
CLASS_COMMENT = "http://www.cs.karelia.ru/smartscribo#Comment"
CLASS_NOTIFICATION = "http://www.cs.karelia.ru/smartscribo#Notification"
CLASS_ACCOUNT = "http://xmlns.com/foaf/0.1/OnlineAccount"

#notification constants
NOTIF_REFRESH_ACC = "http://www.cs.karelia.ru/smartscribo#refreshAccount"
NOTIF_REFRESH_POSTS = "http://www.cs.karelia.ru/smartscribo#refreshPosts"
NOTIF_SEND_POST = "http://www.cs.karelia.ru/smartscribo#sendPost"
NOTIF_EDIT_POST = "http://www.cs.karelia.ru/smartscribo#editPost" 
NOTIF_DEL_POST = "http://www.cs.karelia.ru/smartscribo#delPost"
NOTIF_REFRESH_COMMENTS = "http://www.cs.karelia.ru/smartscribo#refreshComments"
NOTIF_REFRESH_POST_COMMENTS = "http://www.cs.karelia.ru/smartscribo#refreshPostComments"
NOTIF_SEND_COMMENT = "http://www.cs.karelia.ru/smartscribo#sendComment"
NOTIF_DEL_COMMENT = "http://www.cs.karelia.ru/smartscribo#delComment"

#notification parameters constants
NOTIF_PARAM_POSTACC = "http://www.cs.karelia.ru/smartscribo#postAcc"
NOTIF_PARAM_POSTID = "http://www.cs.karelia.ru/smartscribo#postId"
NOTIF_PARAM_OLDPOST = "http://www.cs.karelia.ru/smartscribo#oldPost"
NOTIF_PARAM_NEWPOST = "http://www.cs.karelia.ru/smartscribo#newPost"
NOTIF_PARAM_COMACC = "http://www.cs.karelia.ru/smartscribo#comAcc"
NOTIF_PARAM_COMID = "http://www.cs.karelia.ru/smartscribo#comId"
NOTIF_PARAM_PARID = "http://www.cs.karelia.ru/smartscribo#parId"


# class which handles notifications subscription
class NotificationHandler:
    def handle(self, added, removed):
        global bp
        print "Subscription:"
        for i in added:
            print "Added:", i
            if str(i[1]) == NOTIF_REFRESH_ACC:
                print 'EEEE'
                bp.refresh_account(i[2])
            elif str(i[1]) == NOTIF_REFRESH_POSTS:
                bp.refresh_posts(i[2])
            elif str(i[1]) == NOTIF_SEND_POST:
                print 'get send post note'
                bp.send_post(i[2])
            elif str(i[1]) == NOTIF_EDIT_POST:
                bp.edit_post(i[2])
            elif str(i[1]) == NOTIF_DEL_POST:
                bp.delete_post(i[2])
            elif str(i[1]) == NOTIF_REFRESH_COMMENTS:
                bp.refresh_comments(i[2])
            elif str(i[1]) == NOTIF_REFRESH_POST_COMMENTS:
                bp.refresh_post_comments(i[2])
            elif str(i[1]) == NOTIF_SEND_COMMENT:
                bp.send_comment(i[2])
            elif str(i[1]) == NOTIF_DEL_COMMENT:
                pass
                # and other notifications

# blog processor class, derived from KP class from smart_m3 package
class BlogProcessor(KP):
    def __init__(self):
        '''
        init connection with SIB and open subscription
        '''
        KP.__init__(self, "Blog Processor")
        self.ss_handle = ("X", (TCPConnector, (SIB_IP, 10010)))
        
        if not self.join(self.ss_handle):
            print 'Could not join to Smart Space'    
            sys.exit('Could not join to Smart Space')
        
        #self.lj = LiveJournal.LiveJournal(PROXY)
        self.lj = LiveJournal.LiveJournal()
        self.open_subscribe()
    
    def open_subscribe(self):
        '''
        open subscription on all notification triples for this type
        of blog processor
        NotificationLJ,*,*
        '''
        self.rs1 = self.CreateSubscribeTransaction(self.ss_handle)
        try:
            result_rdf = self.rs1.subscribe_rdf([Triple(URI('NotificationLJ'), None, None)],
                                   NotificationHandler())
            print "RDF Subscribe initial result:", result_rdf
        except M3Exception:
            print "RDF subscription failed:", M3Exception
    
    def close_subscribe(self):
        self.CloseSubscribeTransaction(self.rs1)

    def send_notification(self, client_id, ntype, result):
        ins = self.CreateInsertTransaction(self.ss_handle)
        (a, uid) = str(client_id).split("-",1)
        subj = "Notification-" + uid
        notif = [Triple(URI(subj),URI('rdf:type'),URI(CLASS_NOTIFICATION)),
                 Triple(URI(subj),URI(ntype+"Result"),Literal(result))]
        print 'Send notification: ', notif
        try:
            ins.send(notif, confirm = True)
        except M3Exception:
            print "Insert failed:", M3Exception
        self.CloseInsertTransaction(ins)

    def remove_notification(self, ntype, param, deep=False):
        '''
        remove getting notifications
        ntype - type of notification (predicate)
        param - object of notification triple
        deep - if true - delete all chain of notification triple
        '''
        
        delete = [Triple(URI('NotificationLJ'),URI(ntype), URI(param)),
                  Triple(URI('NotificationLJ'),URI('rdf:type'),URI(CLASS_NOTIFICATION))]
        ds = self.CreateRemoveTransaction(self.ss_handle)
        ds.remove(delete, confirm = "True")
        self.CloseRemoveTransaction(ds)   
        
        # we delete it separately, as if some triples with None
        # are added with other triple - sibd has segmentation fault
        if deep:
            delete = [Triple(URI(param),None,None)]
            ds = self.CreateRemoveTransaction(self.ss_handle)
            ds.remove(delete, confirm = "True")
            self.CloseRemoveTransaction(ds) 

    def get_auth_data(self, acc_id):
        '''
        Function receives login and password of account via acc_id
        returns: (login, password)
        '''
        qs = self.CreateQueryTransaction(self.ss_handle)
        # get login information from SIB
        result = qs.wql_values_query(acc_id, ['seq',LOGIN])
        if len(result) != 1:
            print 'Ontology corrupted! ', _line()
            return
        login = result[0]
                
        # get password information from SIB
        result = qs.wql_values_query(acc_id, ['seq',PASSWORD])
        if len(result) != 1:
            print 'Ontology corrupted! ', _line()
            return
        print result
        password = result[0]
        self.CloseQueryTransaction(qs)

        return (login, password)


    def refresh_account(self, acc_id):
        print 'EEE'
        qs = self.CreateQueryTransaction(self.ss_handle)
        
        # get profile id, using WQL to send notification to client
        
        #['seq',['inv',ACCOUNT],['inv',PERSON_INFO]]
        #result = qs.wql_values_query(acc_id, ['inv', ACCOUNT, 'inv',  PERSON_INFO])
        result = qs.wql_values_query(acc_id, ['seq',['inv',ACCOUNT],['inv', PERSON_INFO]])
        if len(result) != 1:
            print 'Ontology corrupted! ', _line()
            return
        print result[0]
        profile = result[0]
        print profile
        
        # get login information from SIB
        result = qs.wql_values_query(acc_id, ['seq',LOGIN])
        if len(result) != 1:
            print 'Ontology corrupted! ', _line()
            return
        login = result[0]
                
        # get password information from SIB
        result = qs.wql_values_query(acc_id, ['seq',PASSWORD])
        if len(result) != 1:
            print 'Ontology corrupted! ', _line()
            return
        print result
        password = result[0]
        
        self.CloseQueryTransaction(qs)
        
        # remove received notification
        self.remove_notification(NOTIF_REFRESH_ACC, acc_id)
        
        
        # check login and refresh account information
        # ...
        try:
            res = self.lj.check_login(str(login), str(password))
        except Exception, exc:
            print "exception = " + str(exc)
            self.send_notification(profile, NOTIF_REFRESH_ACC, 'error')
            return

        #fullname = self._parse_string(res['fullname'])      
        fullname = base64.encodestring(str(res['fullname']))      

        # send data from service
        
        ins = self.CreateInsertTransaction(self.ss_handle)
        ins_triplets = [Triple(acc_id,URI(SERVICE),Literal('LJ')),
                        Triple(acc_id,URI(USERPIC),Literal(res['defaultpicurl'])),
                        Triple(acc_id,URI(NICKNAME),Literal(fullname)),
                        #Triple(acc_id,URI(BDATE),Literal('12.03.1990')),
                        Triple(acc_id,URI('rdf:type'),URI(CLASS_ACCOUNT))]
        try:
            ins.send(ins_triplets, confirm = True)
        except M3Exception:
            print "Insert failed:", M3Exception
     
        # if ok - send notification
        self.send_notification(profile, NOTIF_REFRESH_ACC, 'ok')

    def refresh_posts(self, acc_id, notification=True):
        # get profile id, using WQL to send notification to client
        qs = self.CreateQueryTransaction(self.ss_handle)
        result = qs.wql_values_query(acc_id, ['seq',['inv',ACCOUNT],['inv', PERSON_INFO]])
        if len(result) != 1:
            print 'Ontology corrupted! ', _line()
            return
        print result[0]
        profile = result[0]
        
        # get sync date from SIB
        sync_date_res = qs.wql_values_query(acc_id, ['seq',SYNCDATE])
        
        if len(sync_date_res) > 1:
            print 'Ontology corrupted in refresh posts: several sync dates! ', _line()
            return
        elif len(sync_date_res) == 1:
            sync_date = sync_date_res[0]
        else:
            sync_date = None
            
        self.CloseQueryTransaction(qs)

        (login, password) = self.get_auth_data(acc_id)

        # remove received notification
        self.remove_notification(NOTIF_REFRESH_POSTS, acc_id)

        # get information about posts of account       
        if not sync_date:
            (res_ins, res_upd) = self.lj._get_all_posts(login, password)
        else:
            self.lj.sync_date = sync_date
            (res_ins, res_upd) = self.lj._get_new_posts(login, password)
        
        '''
        ins_triples = [Triple(acc_id,URI('HAS_POST'),URI('post-4355654')),
                       Triple(URI('post-4355654'),URI('rdf:type'),URI('scribo_Post')),
                       Triple(URI('post-4355654'),URI(TITLE),Literal('Post Title')),
                       Triple(URI('post-4355654'),URI(TEXT),Literal('Text of post'))]
        '''
        ins_triples = []
        
        
        # delete old value of sync data time
        ds = self.CreateRemoveTransaction(self.ss_handle)
        ds.remove([Triple(URI(acc_id),URI(SYNCDATE),None)], confirm = "True")
        self.CloseRemoveTransaction(ds)
 
 
        # publish to SIB new posts       
        for i in res_ins:
            print 'start writing post...'
            uid = str(uuid.uuid4())
            ins_triples.append(Triple(acc_id, URI(HAS_POST), URI('post-'+uid)))
            ins_triples.append(Triple(URI('post-'+uid), URI('rdf:type'), URI(CLASS_POST)))
            #ADDED: add properties journal and poster
            ins_triples.append(Triple(URI('post-'+uid), URI(POSTER), Literal(login)))
            ins_triples.append(Triple(URI('post-'+uid), URI(JOURNAL), Literal(login)))
            #ADDED END
            ins_triples.append(Triple(URI('post-'+uid), URI(ITEMID), Literal(i['itemid'])))
            ins_triples.append(Triple(URI('post-'+uid), URI(ANUM), Literal(i['anum'])))
            ins_triples.append(Triple(URI('post-'+uid), URI(PDATE), 
                                                        Literal(i['eventtime'])))
            if 'subject' in i:
                ins_triples.append(Triple(URI('post-'+uid), URI(TITLE), Literal(base64.encodestring(str(i['subject'])))))
            else:
                ins_triples.append(Triple(URI('post-'+uid), URI(TITLE), Literal(base64.encodestring(""))))
            ins_triples.append(Triple(URI('post-'+uid), URI(TEXT), Literal(base64.encodestring(str(i['event'])))))

        
        ins_triples.append(Triple(URI(acc_id), URI(SYNCDATE), Literal(self.lj.sync_date)))
               

        # send posts information to SIB
        ins = self.CreateInsertTransaction(self.ss_handle)
        
        try:
            ins.send(ins_triples, confirm = True)
        except M3Exception:
            print "Insert failed:", M3Exception
        
        self.CloseInsertTransaction(ins)   
    
        ins_triples = []
    
        # update in SIB edited posts 
        for i in res_upd:
            print 'updating post'
            self._ss_del_post(acc_id, i['itemid'])
            uid = str(uuid.uuid4())
            ins_triples.append(Triple(acc_id, URI(HAS_POST), URI('post-'+uid)))
            ins_triples.append(Triple(acc_id, URI('rdf:type'), URI(CLASS_POST)))
            #ADDED: add properties journal and poster
            ins_triples.append(Triple(URI('post-'+uid), URI(POSTER), Literal(login)))
            ins_triples.append(Triple(URI('post-'+uid), URI(JOURNAL), Literal(login)))
            #ADDED END
            ins_triples.append(Triple(URI('post-'+uid), URI(ITEMID), Literal(i['itemid'])))
            ins_triples.append(Triple(URI('post-'+uid), URI(ANUM), Literal(i['ANUM'])))
            ins_triples.append(Triple(URI('post-'+uid), URI(PDATE), 
                                                        Literal(i['eventtime'])))
            ins_triples.append(Triple(URI('post-'+uid), URI(TITLE), Literal(base64.encodestring(str(i['subject'])))))
            ins_triples.append(Triple(URI('post-'+uid), URI(TEXT), Literal(base64.encodestring(str(i['event'])))))
            ins_triples.append(Triple(URI('post-'+uid),URI('scribo_type'), Literal(POST)))


    
        try:
            #ADDED: add properties journal and poster
            ins = self.CreateInsertTransaction(self.ss_handle)
            #ADDED END 
            ins.send(ins_triples, confirm = True)
        except M3Exception:
            print "Insert failed:", M3Exception
        #ADDED: add properties journal and poster
        self.CloseInsertTransaction(ins)
        #ADDED END 
        # if ok - send notification
        if notification:
            self.send_notification(profile, NOTIF_REFRESH_POSTS, 'ok')

    def send_post(self, notif_id):
        
        # get profile id, using WQL to send notification to client
        qs = self.CreateQueryTransaction(self.ss_handle)
        acc_res = qs.wql_values_query(notif_id, ['seq', NOTIF_PARAM_POSTACC])
        post_res = qs.wql_values_query(notif_id,  ['seq', NOTIF_PARAM_POSTID])
        journals = qs.wql_values_query(notif_id,  ['seq', 'journal'])

        #journals can be several times
        if len(acc_res) != 1 or len(post_res) != 1:
            print 'Ontology corrupted! ', _line()
            return
        acc = acc_res[0]
        post = post_res[0]
        result = qs.wql_values_query(acc, ['seq',['inv',ACCOUNT],['inv',PERSON_INFO]])
        if len(result) != 1:
            print 'Ontology corrupted! ', _line()
            return
        print result[0]
        profile = result[0]

        #ADDED: get poster
        result = qs.wql_values_query(acc, ['seq',LOGIN])
        if len(result) != 1:
            print 'Ontology corrupted! ', _line()
            return
        print result[0]
        poster = result[0]
        #ADDED END

        # get post data from SIB
        title_res = qs.wql_values_query(post,  ['seq', TITLE])
        #ADDED: base64
        
        title_base = title_res[0]
        print title_base
        title = base64.decodestring(str(title_base))


        text_res = qs.wql_values_query(post,  ['seq', TEXT])
        #ADDED: base64
        text_base = text_res[0]
        text = base64.decodestring(str(text_base))

        #tags_res = qs.wql_values_query(post,  ['seq', 'scribo_tags'])
        #tags = tags_res[0]

        self.CloseQueryTransaction(qs)

        (login, password) = self.get_auth_data(acc)

        # remove received notification
        self.remove_notification(NOTIF_SEND_POST, notif_id, True)

         # send post data to service
        try:
            self.lj.send_post(login, password, title, text)
        except Exception as ex:
            print ex
            self.send_notification(profile, NOTIF_SEND_POST, 'error')
            return
        '''
        # if ok - link post with account
        ins = self.CreateInsertTransaction(self.ss_handle)
        #ADDED: poster
        ins_triplets = [Triple(acc, URI(HAS_POST),URI(post)),
                        Triple(URI(post),URI('rdf:type'),URI(CLASS_POST)),
                        Triple(URI(post),URI(POSTER),Literal(poster)),
                        Triple(URI(post),URI('scribo_type'), Literal(POST))]
        for journal in journals:
            #ADDED: Literal(journal)
            ins_triplets.append(Triple(URI(post),URI(JOURNAL),Literal(journal)))
        try:
            ins.send(ins_triplets, confirm = True)
        except M3Exception:
            print "Insert failed:", M3Exception
        
        self.CloseInsertTransaction(ins)   
        '''
        # receive sended post using post refreshing
        self.refresh_posts(acc, False)
        
        # delete data for sended post
        delete = [Triple(URI(post), None, None)] 
        ds = self.CreateRemoveTransaction(self.ss_handle)
        ds.remove(delete, confirm = "True")
        self.CloseRemoveTransaction(ds)  
        
        # if ok - send notification
        self.send_notification(profile, NOTIF_SEND_POST, 'ok')

    def edit_post(self, notif_id):
        print 'STEP1'
        # get notification params - oldPost and newPost
        qs = self.CreateQueryTransaction(self.ss_handle)
        old_post_res = qs.wql_values_query(notif_id, ['seq', NOTIF_PARAM_OLDPOST])
        old_post = old_post_res[0]
        new_post_res = qs.wql_values_query(notif_id, ['seq', NOTIF_PARAM_NEWPOST])
        new_post = new_post_res[0]

        # get profile name
        profile_res = qs.wql_values_query(old_post, ['seq',['inv',HAS_POST],['inv',ACCOUNT],
                      ['inv',PERSON_INFO]])

        account_res = qs.wql_values_query(old_post, ['inv',HAS_POST])
        account = account_res[0]

        print 'EDIT POST:', profile_res

        if len(profile_res) != 1:
            print 'Ontology corrupted in edit post: profile ', _line()
            #return
        print profile_res[0]
        profile = profile_res[0]
        #ADDED: get poster
        print "account="+str(account)
        result = qs.wql_values_query(account, ['seq',LOGIN])
        if len(result) != 1:
            print 'Ontology corrupted! ', _line()
            return
        print result[0]
        poster = result[0]
        #ADDED END 

        self.CloseQueryTransaction(qs)
       
        # get from smart space required posts data
        # send to blog service information about editing post
        # ... TODO!!!!!!
        
        # if editing succeed, then change account link from old post to new one

        upd = self.CreateUpdateTransaction(self.ss_handle)
        try:
            upd.update([Triple(URI(account),URI(HAS_POST),URI(new_post))], "RDF-M3", 
                        [Triple(URI(account),URI(HAS_POST),URI(old_post))], "RDF-M3", confirm = True)
        except M3Exception:
            print "Update failed:", M3Exception
        #ADDED: update poster
        try:
            upd.update([Triple(URI(new_post),URI(POSTER),Literal(poster))], "RDF-M3", 
                        [Triple(URI(old_post),URI(POSTER),Literal(poster))], "RDF-M3", confirm = True)
        except M3Exception:
            print "Update failed:", M3Exception
        #ADDED END 
        self.CloseUpdateTransaction(upd)
       

        # delete received triple chain notification
        
        print 'STEP2'
        # delete received notifications
        delete = [Triple(URI(notif_id),URI(NOTIF_PARAM_OLDPOST),URI(old_post)),
                  Triple(URI(notif_id),URI(NOTIF_PARAM_NEWPOST),URI(new_post)),
                  Triple(URI('NotificationLJ'),URI(NOTIF_EDIT_POST),URI(notif_id))]
        ds = self.CreateRemoveTransaction(self.ss_handle)
        ds.remove(delete, confirm = "True")
        self.CloseRemoveTransaction(ds)

        self.send_notification(profile, NOTIF_EDIT_POST, 'ok')


    def delete_post(self, notif_id):
        '''
        Handling of delete post notification
        Notification contains triplets:
            Notification<service> - delPost - post_notif<id>
            post_notif<id> - postAcc - <acc_id>
            post_notif<id> - postId - <post_id>
            post_notif<id> - journal - <journal_name> 
        
        <acc_id> - from which account we delete post
        <post_id> - id of post in smart space (account - hasPost - post_id)
        <journal_name> - on which journals post was sent from this account
            
        For Smart Conference notification can be simplified to: Notification<service> - delPost - <post_id>
        and deleting post without checks on the presence on other accounts
        '''
        # get params of notification
        qs = self.CreateQueryTransaction(self.ss_handle)
        acc_id_res = qs.wql_values_query(notif_id, ['seq', NOTIF_PARAM_POSTACC])
        acc_id = acc_id_res[0]
        
        post_id_res = qs.wql_values_query(notif_id, ['seq', NOTIF_PARAM_POSTID])
        post_id = post_id_res[0]
        
        journal_res = qs.wql_values_query(notif_id, ['seq', 'journal'])
        
        profile_res = qs.wql_values_query(acc_id, ['seq',['inv',ACCOUNT],['inv',PERSON_INFO]])
        
        profile = profile_res[0]
        #ADDED: get poster
        result = qs.wql_values_query(acc_id, ['seq',LOGIN])
        if len(result) != 1:
            print 'Ontology corrupted! ', _line()
            return
        print result[0]
        poster = result[0]
        #ADDED END
        self.CloseQueryTransaction(qs)
        
        if len(post_id_res) != 1:
            print 'Ontology corrupted: in deleting post, post_id ', _line()
            return
        post_id = post_id_res[0]
      

        qs = self.CreateQueryTransaction(self.ss_handle)      
        # get information about post from smart space
        # <post_id> - <property> - <value>
        
        itemid_res = qs.wql_values_query(post_id, ['seq', ITEMID])
        itemid = itemid_res[0]
        self.CloseQueryTransaction(qs)

        (login, password) = self.get_auth_data(acc_id)

        for i in journal_res:
            # delete post from journals on service
            # ...
            
            # delete journals info from smart space
            ds = self.CreateRemoveTransaction(self.ss_handle)
            ds.remove([Triple(URI(post_id),URI(JOURNAL),Literal(i))], confirm = "True")
            self.CloseRemoveTransaction(ds)
       
        # remove received notification
        self.remove_notification(NOTIF_DEL_POST, notif_id, True)

        # delete post from blog on service
        try:
            self.lj.del_post(login, password, itemid)
        except:
            self.send_notification(profile, NOTIF_DEL_POST, 'error')
            return
        
        # if post was left on some other accounts
        # then delete only triple <acc_id> - scribo_hasPost - <post_id>
        # else delete triple with scribo_hasPost and post himself
        qs = self.CreateQueryTransaction(self.ss_handle)
        post_accs_res = qs.wql_values_query(post_id, ['inv', HAS_POST])
        self.CloseQueryTransaction(qs)
        
        if len(post_accs_res) == 0:
            print 'Ontology corrupted: in deleting post, get accounts of post ', _line()
            return
        elif len(post_accs_res) >= 1:
            ds = self.CreateRemoveTransaction(self.ss_handle)
            ds.remove([Triple(URI(acc_id),URI(HAS_POST),URI(post_id))], confirm = "True")
            ds.remove([Triple(URI(post_id),URI(POSTER),Literal(poster))], confirm = "True")
            self.CloseRemoveTransaction(ds)
        
        # if only one account has this post - delete post completely
        if len(post_accs_res) == 1:
            ds = self.CreateRemoveTransaction(self.ss_handle)
            ds.remove([Triple(URI(post_id),None,None)], confirm = "True")
            self.CloseRemoveTransaction(ds)
        
        # if function succeed - send ok notification
        self.send_notification(profile, NOTIF_DEL_POST, 'ok')
            
    def refresh_post_comments(self, post_id):
        '''
        function for updating all comments of post
        now - without multiblog idea
        '''
        qs = self.CreateQueryTransaction(self.ss_handle)
        acc_id = qs.wql_values_query(post_id, ['inv', HAS_POST])[0]
        profile_res = qs.wql_values_query(post_id, ['seq',['inv',HAS_POST],['inv',ACCOUNT],
                      ['inv',PERSON_INFO]])
        profile = profile_res[0]
        itemid = qs.wql_values_query(post_id, ['seq', ITEMID])[0]
        anum = qs.wql_values_query(post_id, ['seq', ANUM])[0]
        self.CloseQueryTransaction(qs)
        
        (login, password) = self.get_auth_data(acc_id)
        
        # delete all comments from post
        self._ss_del_comments(post_id)
        
        # get information about comments of this post on service
        # and write comments information to smart space
        com = self.lj.get_comments(login, password, itemid, anum)
        for i in com['comments']:
            self._write_comment_child(post_id, i)
              
        # remove received notification
        self.remove_notification(NOTIF_REFRESH_POST_COMMENTS, post_id)
        
        # send notification to client      
        self.send_notification(profile, NOTIF_REFRESH_POST_COMMENTS, 'ok')


    def _write_comment_child(self, parent, comment):
        com_id = 'comment-' + str(uuid.uuid4())
        #print comment
        ins = self.CreateInsertTransaction(self.ss_handle)
        ins_triplets = [Triple(URI(parent),URI(HAS_COMMENT),URI(com_id)),
                        Triple(URI(com_id),URI('rdf:type'),URI(CLASS_COMMENT)),
                        Triple(URI(com_id),URI(TYPE), Literal(COMMENT)),
                        Triple(URI(com_id),URI(TITLE),Literal(base64.encodestring(str(comment['body'])))),
                        Triple(URI(com_id),URI(TEXT),Literal(base64.encodestring(str(comment['subject'])))),
                        Triple(URI(com_id),URI(POSTER),Literal(comment['postername'])),
                        Triple(URI(com_id),URI(PDATE),Literal(comment['datepost'])),
                        Triple(URI(com_id),URI(DTALKID),Literal(comment['dtalkid']))]        
        # send to SIB
        try:
            ins.send(ins_triplets, confirm = True)
        except M3Exception:
            print "Insert failed:", M3Exception
        self.CloseInsertTransaction(ins)
        
        if 'children' in comment.keys():
            for i in comment['children']:
                self._write_comment_child(com_id, i)

    
    def refresh_comments(self, acc_id):
        '''
        function for updating all comments of account
        now - without multiblog idea
        '''
        # get information about comments of this post on service
        # and synchronize comments information between smart space and service
        # ...
        
        # remove received notification
        self.remove_notification(NOTIF_REFRESH_COMMENTS, acc_id)
        
        # get profile id and send notification to client
        qs = self.CreateQueryTransaction(self.ss_handle)
        post_id = qs.wql_values_query(acc_id, ['seq',HAS_POST])[0]
        profile_res = qs.wql_values_query(post_id, ['seq',['inv',HAS_POST],['inv',ACCOUNT],
                      ['inv',PERSON_INFO]])
        profile = profile_res[0]
        result = qs.wql_values_query(acc_id, ['seq',LOGIN])
        if len(result) != 1:
            print 'Ontology corrupted! ', _line()
            return
        print result[0]
        poster = result[0]   
        self.CloseQueryTransaction(qs)
        '''
        if not post_id:
            print "there are not posts on this account"+str(acc_id)
            self.send_notification(profile, NOTIF_REFRESH_COMMENTS, 'ok')
            return
        '''
        # publish new comments on first post to smart space
        """
        ins = self.CreateInsertTransaction(self.ss_handle)
        u = str(uuid.uuid4())
        print "refresh commnets of post "+str(post_id)
        ins_triplets = [Triple(post_id,URI(HAS_COMMENT),URI('comment-'+str(u))),
                        Triple(URI('comment-'+str(u)),URI(POSTER), Literal(poster)),
                        Triple(URI('comment-'+str(u)),URI('scribo_type'), Literal(COMMENT)),
                        Triple(URI('comment-'+str(u)),URI('rdf:type'),URI('scribo_Comment')),
                        Triple(URI('comment-'+str(u)),URI(TITLE),Literal(base64.encodestring('Test Comment Title'))),
                        Triple(URI('comment-'+str(u)),URI(TEXT),Literal(base64.encodestring('Test of comments')))]
        try:
            ins.send(ins_triplets, confirm = True)
        except M3Exception:
            print "Insert failed:", M3Exception
        self.CloseInsertTransaction(ins)
        """
        self.send_notification(profile, NOTIF_REFRESH_COMMENTS, 'ok')
    
        
    def send_comment(self, notif_id):
        '''
        sending comment to several accounts
        
        notification in triplets:
        Notification<service> - sendComment - com_notif<id>
        com_notif<id> - comAcc - <acc_id>
        com_notif<id> - comId - <com_id>
        com_notif<id> - parId - <parrent_id>
        com_notif<id> - journal - <journal_name> 
        
        For Smart Conference notification can be simplified to:
        Notification<service> - sendComment - <comment_id>
        '''
        
        # get params of notification
        qs = self.CreateQueryTransaction(self.ss_handle)
        acc_id_res = qs.wql_values_query(notif_id, ['seq', NOTIF_PARAM_COMACC])
        acc_id = acc_id_res[0]
        
        com_id_res = qs.wql_values_query(notif_id, ['seq', NOTIF_PARAM_COMID])
        com_id = com_id_res[0]
         
        journal_res = qs.wql_values_query(notif_id, ['seq', 'journal'])
        journal = journal_res[0]
        
        parent_res = qs.wql_values_query(notif_id, ['seq', NOTIF_PARAM_PARID])
        parent = parent_res[0]
        
        profile_res = qs.wql_values_query(acc_id, ['seq',['inv',ACCOUNT],['inv',PERSON_INFO]])
        profile = profile_res[0]
        result = qs.wql_values_query(acc_id, ['seq',LOGIN])
        if len(result) != 1:
            print 'Ontology corrupted! ', _line()
            return
        poster = result[0]
        
        # get post uuid which have this comment
        print parent
        post_id_res = qs.wql_values_query(parent, ['rep*',['inv', HAS_COMMENT]])
        print 'Parents: ', post_id_res
        if len(post_id_res) > 0:
            for i in post_id_res:
                if str(i)[:4] == 'post':
                    print 'Found post!'
                    post_id = i
                    break
                else:
                    print 'Post not found!', _line()
        else:
            print 'No posts received!', _line()
            self.CloseQueryTransaction(qs)
            return
            post_id = ''    
                    
        print post_id
        
        post_itemid = qs.wql_values_query(post_id, ['seq', ITEMID])[0]
        post_anum = qs.wql_values_query(post_id, ['seq', ANUM])[0]
        
        com_title = qs.wql_values_query(com_id, ['seq', TITLE])[0]
        com_title = base64.decodestring(str(com_title))
        com_text = qs.wql_values_query(com_id, ['seq', TEXT])[0]
        com_text = base64.decodestring(str(com_text))
        
        dtalkid_res = qs.wql_values_query(parent, ['seq', DTALKID])

        if len(dtalkid_res) == 1:
            dtalkid = dtalkid_res[0]
        else:
            dtalkid = '0'
        
        self.CloseQueryTransaction(qs)
        
        (login, password) = self.get_auth_data(acc_id)
        
        # send comment information to services
        res = self.lj.send_comment(login, password, com_title, com_text, post_itemid, post_anum, dtalkid)
        
        # if ok - link comment with post and send notification
        ins = self.CreateInsertTransaction(self.ss_handle)
        ins_triplets = [Triple(URI(parent),URI(HAS_COMMENT),URI(com_id)),
                        Triple(URI(com_id),URI(POSTER),Literal(poster)),
                        Triple(URI(com_id),URI('rdf:type'),URI(CLASS_COMMENT)),
                        Triple(URI(com_id),URI(DTALKID),Literal(res['dtalkid']))]

        # send to SIB
        try:
            ins.send(ins_triplets, confirm = True)
        except M3Exception:
            print "Insert failed:", M3Exception
        self.CloseInsertTransaction(ins)
        
        # remove received notification
        self.remove_notification(NOTIF_SEND_COMMENT, notif_id, True)
        
        self.send_notification(profile, NOTIF_SEND_COMMENT, 'ok')
             
    def _parse_string(self, lj_field):
        """
        Convert response from LJ to utf-8. sqlite3 need utf-8 strings
        """

        return str(lj_field)
        
    def _ss_del_post(self, acc_id, itemid):
        '''
        Delete post from SS on account with specified service itemid
        '''
        qs = self.CreateQueryTransaction(self.ss_handle)
        acc_posts = qs.wql_values_query(acc_id, ['seq', HAS_POST])
        item_posts = qs.wql_values_query(itemid, ['inv', ITEMID])
        self.CloseQueryTransaction(qs)
        
        intersec = set(acc_posts) & set(item_posts)
        if len(intersec) == 1:
            post_id = intersec.pop()
        else:
            print 'error in intersection!'
            return
            
        delete = [Triple(URI(post_id), None, None), Triple(URI(acc_id),URI(HAS_POST),URI(post_id))]
        ds = self.CreateRemoveTransaction(self.ss_handle)
        ds.remove(delete, confirm = "True")
        self.CloseRemoveTransaction(ds)  

        
    def _ss_del_comments(self, post_id):
        '''
        Delete comments on particular post from SS 
        '''
        qs = self.CreateQueryTransaction(self.ss_handle)
        com_list = qs.wql_values_query(post_id, ['rep+', HAS_COMMENT])
        print com_list
        self.CloseQueryTransaction(qs)
        
        ds = self.CreateRemoveTransaction(self.ss_handle)
        ds.remove([Triple(URI(post_id), URI(HAS_COMMENT), None)], confirm = "True")
        self.CloseRemoveTransaction(ds)
          
        for i in com_list:            
            ds = self.CreateRemoveTransaction(self.ss_handle)
            ds.remove([Triple(URI(i), None, None)], confirm = "True")
            self.CloseRemoveTransaction(ds)          
        

# handler of ctrl+c pressing
def KeyHandler(signum, frame):
    global bp, noexit  
    print "Exitting"    
    bp.close_subscribe()
    noexit = False


def _line():
    c = inspect.currentframe().f_back
    return "[" + str(c.f_lineno) + "]"

# set signal to exit from KP on ctrl+c
signal.signal(signal.SIGINT, KeyHandler)

bp = BlogProcessor()

print "START"

# cycle to keep main thread alive
while noexit:
    time.sleep(10000)

'''
THIS IS PART OF ONTOLOGY EXAMPLE and it's insertion

node = KP("PubExample")
ss_handle = ("X", (TCPConnector, ("127.0.0.1", 10010)))

if not node.join(ss_handle):
    sys.exit('Could not join to Smart Space')

pro = node.CreateInsertTransaction(ss_handle)

init_triples = [Triple(URI("profile-3a7a8815"),URI("rdf:type"),URI("scribo_Profile")),
                Triple(URI("profile-3a7a8815"),URI(PERSON_INFO), URI("person-9d166448")),
                Triple(URI("person-9d166448"),URI("rdf:type"),URI("foaf_Person")),
                Triple(URI("person-9d166448"),URI("foaf_name"),Literal("John Connor")),
                Triple(URI("person-9d166448"),URI("foaf_age"),Literal("25")),
                Triple(URI("person-9d166448"),URI("foaf_account"),URI("account-4d45454")),
                Triple(URI("account-4d45454"),URI("rdf:type"),URI("foaf_OnlineAccount")),
                Triple(URI("account-4d45454"),URI("scribo_login"),Literal("scribo-rpc")),
                Triple(URI("account-4d45454"),URI(PASSWORD),Literal("test12345"))]

# send profile and account information
pro.send(init_triples)
node.CloseInsertTransaction(pro)

# send refreshAccount notification
pro = node.CreateInsertTransaction(ss_handle)
notif = [Triple(URI("NotificationLJ"),URI(NOTIF_REFRESH_ACC),URI("account-4d45454"))]
pro.send(notif)
node.CloseInsertTransaction(pro)

node.leave(ss_handle)
'''
