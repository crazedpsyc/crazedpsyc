#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jabberbot import JabberBot, botcmd
import datetime
from infobits import infobits
import duckduckgo as ddg
import urllib
import random
import explosions

version = '0.4'
admins = ['bazaar', 'crazedpsyc']

class SystemInfoJabberBot(JabberBot):
    saidhito = []
    mefeelings = 'I\'m A bot, so I don\'t have emotions, but if I did I would be fine!\nHow are you?'
    mood = 'emotionless'
    explosions.x.update({'hiroshima': 63000000000000, 'nagasaki': 88000000000000})
    explosions = explosions.x
    more = ''
    buzzers = {}

    @botcmd
    def help(self, mess, args):
        return 'There are too many commands! I disabled the full help command, sorry :(\nYou can ask crazedpsyc@dukgo.com for help'

    @botcmd
    def serverinfo( self, mess, args):
        """Displays information about the server"""
        version = open('/proc/version').read().strip()
        loadavg = open('/proc/loadavg').read().strip()

        return '%s\n\n%s' % ( version, loadavg, )
    
    @botcmd
    def time( self, mess, args):
        """Displays current server time"""
        return str(datetime.datetime.now())

    @botcmd
    def rot13( self, mess, args):
        """Returns passed arguments rot13'ed"""
        return args.encode('rot13')

    @botcmd
    def whoami( self, mess, args):
        """Tells you your username"""
        return str(mess.getFrom())
        
    @botcmd
    def tell(self, mess, args):
        '''Tell somebody something'''
        args = args.split()
        if len(args) >= 2:
            return 'Hey %s! %s' % (' '.join(args[0].split('_')), ' '.join(args[1:]))
        return 'Invalid usage'
        
    @botcmd
    def hello(self, mess, args):
        """Say hello"""
        if str(mess.getFrom()).split('@')[0] in self.saidhito: return 'You\'re greeting me again?'
        self.saidhito += [str(mess.getFrom()).split('@')[0]]
        return 'Hello, %s!' % str(mess.getFrom()).split('@')[0]
        
    @botcmd
    def hi(self, mess, args):
        """Shortcut for hello"""
        return self.hello(mess, args)
    
    @botcmd
    def version(self, mess, args):
        """Display the version of this JabberBot"""
        return 'Seriously Useless JabberBot version ' + version
        
    @botcmd
    def lookup(self, mess, args):
        """Look up a word in the very small and useless dictionary
        This command looks for infobits set with the setbit command
        Upd8! It also ducks anything not found in the dictionary
        and W|As anything duckduckgo doesn't know"""
        admin = str(mess.getFrom()).split('@')[0] in admins
        if args.lower() in infobits.keys() and infobits.get(args, ('not found', True))[1]:
            return infobits.get(args.lower(), ('not found', True))[0]
        elif args.lower() in infobits.keys() and not infobits.get(args, ('not found', True))[1] and admin:
            return 'This infobit is not yet approved: ' + infobits.get(args.lower(), ('not found', True))[0]
        res = ddg.query(args.lower())
        out = ''
        abstext = unicode(res.abstract.text)
        if abstext: out += 'From DuckDuckGo: ' + abstext
        elif res.related: 
            for resu in res.related:
                if resu.text: out += resu.text + '\n'
                
        if out: return out
        return self.wa(mess, args)
        return 'That infobit either doesn\'t exist, or has not been approved'
       
    @botcmd 
    def setbit(self, mess, args):
        """Set an infobit
        use 'set infobit description of infobit' and wait for admin approval"""
        args = args.split()
        admin = str(mess.getFrom()).split('@')[0] in admins
        if len(args) > 1:
            if ' '.join(args[0].lower().split('_')) in infobits.keys() and not admin: return 'Somebody already told me what that means'
            infobits.update({' '.join(args[0].lower().split('_')): (' '.join(args[1:]), admin)})
            print 'Somebody set ' + ' '.join(args[0].lower().split('_'))
            return 'Infobit set!'
        return 'Invalid usage'
        
    @botcmd
    def approve(self, mess, args):
        """An admin-only command"""
        admin = str(mess.getFrom()).split('@')[0] in admins
        if not admin: return 'You are not admin'
        if len(args.split()) >= 1:
            if args.lower() in infobits.keys() and not infobits.get(args, ('not found', True))[1]:
                self.setbit(mess, args)
                infobits.update({' '.join(args.lower().split('_')): (infobits.get(args, ('not found', True))[0], True)})
                return 'InfoBit Approved'
        return 'Error'
    
    @botcmd
    def infoadmin(self, mess, args):
        """A tool for admins to check for disapproved infobits"""
        admin = str(mess.getFrom()).split('@')[0] in admins
        if not admin: return 'You are not admin'
        out = []
        for bit in infobits.keys():
            if not infobits[bit][1]: out += [bit]
        return str(out)
        
    @botcmd
    def how(self, mess, args):
        """Ask me how i'm doin"""
        if args.lower().startswith('are you'): return self.mefeelings
        return self.what(mess, args)
        return 'I don\'t know'
    
    @botcmd
    def i(self, mess, args):
        """Describe yourself or your conditions"""
        if args.lower().startswith('am good') or args.lower().startswith('am great') or args.lower().startswith('am fine'): return 'Great!'
        elif args.lower().startswith('hate') and not args.lower().startswith('hate you') and not args.lower().startswith('hate bot'): return 'Oh, yeah, so do I'
        elif 'bad' in args.lower() and not 'not' in args.lower(): return 'Oh, sorry :('
        elif args.lower().startswith('hate') and args.lower().startswith('hate you') or args.lower().startswith('hate bot'): 
            print str(mess.getFrom()).split('@')[0], 'Is a meanie.'
            self.mefeelings = "I am still sad because somebody was mean to me."
            return 'You make me sad :('
        if 'am :genius:' in args.lower(): return 'Not as smart as me though :P'
        return 'I\'m not sure what you\'re talking about'
    
    @botcmd
    def you(self, mess, args):
        """Tell me something I don't know"""
        mad = False
        if self.mood == 'happy': 
            bademo = 'You were so nice before...'
        elif self.mood == 'mad':
            bademo = 'If you keep saying things like that I will tell my master to.. umm... '
            mad = True
        elif self.mood == 'emotionless':
            emo = 'That is the first compliment I have gotten today ;)'
            bademo = ''
        if 'stupid' in args or 'shit' in args and not 'not' in args: 
            print 'Somebody called me stupid!'
            self.mefeelings = "I am still sad because somebody was mean to me."
            self.mood = 'mad'
            return 'I will inform the psycho who created me of my incompetence. You should not bother saying such things though, because I *am* called Seriously Useless...'
        if 'smart' in args or 'genius' in args and not 'not' in args:
            self.mefeelings = "I am very happy, because %s complimented me!" % str(mess.getFrom()).split('@')[0]
            print 'I like ' + str(mess.getFrom()).split('@')[0]
            self.mood = 'happy'
            return 'Well thank you!'
            
        if 'smart' in args or 'genius' in args and 'not' in args:
            self.mood = 'mad'
            return 'Oh, what a nice thing to say :P\n' + bademo
        if args.strip() == 'there?': 
            print 'Somebody might be having a bit of trouble with me..'
            return 'I believe I am'
        return 'Huh?'
        
    @botcmd
    def what(self, mess, args):
        '''A conversational wrapper for the lookup command'''
        if len(args.split()) > 1:
            if args.split()[0] == 'is' or args.split()[0] == 'are' and not args.split()[1].startswith('you'): 
                return self.lookup(mess, ' '.join(args.split()[1:]).strip('?!.'))
            elif args.split()[1].startswith('you'):
                return '''I am a Totally Useless XMPP bot.
My purpose is to provide useful information to anyone who asks
But I can also chat a little bit, and watch out! I can hold a grudge!
btw, You can type 'version' for my name and rank'''
            else: return 'I\'m not really sure what you\'re talking about...'
            
    @botcmd
    def wa(self, mess, args, internal=False):
        """Query Wolfram|Alpha"""
        appid = 'XX7WTX-XJVRVRRG9H'
        try: xml = urllib.urlopen('http://api.wolframalpha.com/v2/query?input=%s&appid=XX7WTX-XJVRVRRG9H' % '+'.join(args.split())).read()
        except: return 'Error contacting Wolfram|Alpha'
        if not xml: return 'Wolfram|Alpha didn\'t return any data'
        success = xml.split('<queryresult success=\'')[1].split("'")[0]
        xml = unicode(xml, 'utf-8')
        if success == 'false': return 'Wolfram|Alpha has no idea what you\'re talking about'
        out = 'Here\'s what wolfram|alpha knows about ' + args
        num = 1
        for text in xml.split('<plaintext>')[1:]:
            if text.split(u'</plaintext>')[0].strip() and num <= 3: 
                out += u'\n' + unicode(num) + u': ' + unicode(text.split(u'</plaintext>')[0])
                num += 1
            elif text.split(u'</plaintext>')[0].strip() and not num <= 3:
                self.more += u'\n' + unicode(num) + u': ' + unicode(text.split(u'</plaintext>')[0])
                num += 1
        
        if out != 'Here\'s what wolfram|alpha knows about ' + args: 
            out += '\nType "m" for more'
            return out
                       
        else: return 'None of the results were in plaintext!'
        return 'Unknown Error. Hey, I am a useless bot!'
        
        
    @botcmd
    def why(self, mess, args):
        """Need help pondering the nature of the universe?"""
        if 'are you here' in args: return 'Because I am.'
        return self.what(mess, args)
        
    @botcmd
    def tntcalc(self, mess, args):
        print mess.getFrom(), 'is using tntcalc!'
        """Calculate stuff related to the physics of TriNitroToluene"""
        if not args: return 'No arguments supplied!'
        if args.lower() in self.explosions.keys():
            return str(self.explosions[args.lower()]) + ' joules'
        elif args.lower().replace(' ', '_') in self.explosions.keys():
            return str(self.explosions[args.lower().replace(' ', '_')]) + ' joules'
        elif args.lower().split()[0] in self.explosions.keys():
            return str(self.explosions[args.lower().split()[0]]) + ' joules'
        try: n = float(int(args))
        except: return 'Cannot convert argument to integer!'
        x = (1654*n)*(4200000)
        whata = ''
        s = 1
        naga = 88000000000000
        hiro = 63000000000000
        if x >= 1000 and x < 1000000:
            s = 1000
            x = x/s
            whata = 'kila'
            naga = naga/s
        elif x >= 1000000 and x < 1000000000:
            s = 1000000
            x = x/s
            whata = 'mega'
            naga = naga/s
        elif x >= 1000000000 and x < 1000000000000:
            s = 1000000000
            x = x/s
            whata = 'giga'
            naga = naga/s
        elif x >= 1000000000000 and x < 1000000000000000:
            s = 1000000000000
            x = x/s
            whata = 'tera'
            naga = naga/s
        elif x >= 1000000000000000 and x < 1000000000000000000:
            s = 1000000000000000
            x = x/s
            whata = 'peta'
            naga = naga/s
        #nagacomp = round(x/naga, 3)
        comparisons = []
        comparison = 1e+100 # nothing will *EVER* be more than this :D
        compname = ''
        s = float(s)
        for key in self.explosions.keys():
            comp = self.explosions[key]
            if x/comp < comparison: 
                comparison = x/comp
                compname = key
        if comparison == 1e+100: return '%s %sjoules (No suitable comparison found)' % (str(x), whata)
                
        rcomp = str(round(comparison, 3))
        #print rcomp, comparison
        if not rcomp: 
            rcomp = str(comparison)
        print 'And is now about to get his response!'
        return '%s %sjoules\nYour resultant explosion would equal approximately %s times the resultant energy of %s' % (str(x), whata, comparison, compname.replace('_', ' '))
        
    @botcmd
    def who(self, mess, args):
        return self.what(mess, args)
    
    @botcmd
    def random(self, mess, args):
        """Get a random infobit"""
        x = 0
        while x < 10:
            index = random.randint(0, len(infobits)) - 1
            bit = infobits.keys()[index]
            bitval = infobits[infobits.keys()[index]]
            out = '%s definition: %s' % (bit, bitval[0])
            if bitval[1]: return out
        return 'I couldn\'t find any approved infobits for you :( You could try again!'
    
    @botcmd
    def m(self, mess, args):
        if self.more: return self.more
        else: return 'There is no more!'
    
    @botcmd
    def lol(self, mess, args):
        return 'You better not be laughing at me! :P'
        
    @botcmd
    def thank(self, mess, args):
        "I know, you just have to!"
        return 'You\'re welcome :)'
        
    @botcmd
    def thanks(self, mess, args):
        self.thank(mess, args)
        
    @botcmd
    def buzz(self, mess, args):
        buzzcount = self.buzzers.get(mess.getFrom(), 0) + 1
        self.buzzers.update({str(mess.getFrom()): buzzcount})
        out = 'Yes?'
        if buzzcount == 3:
            out = 'That is getting a bit annoying...'
        elif buzzcount == 4:
            out = 'Please stop that.'
        elif buzzcount == 5:
            out = 'What do you want?!?'
        elif buzzcount == 6:
            out = 'AAAAAAAH!'
        elif buzzcount == 7:
            out = 'I am going to buzz you!'
        elif buzzcount > 7:
            out = 'buzz! ' * buzzcount
        return out
        
    @botcmd
    def steve(self, mess, args):
        if args.lower().startswith('old boy! tell me, what be'): return self.what(mess, 'is ' + args.lower().split('old boy! tell me, what be')[1])
        return 'What? Are you talking to me?'
        
        
username = 'steve@place.im'
password = 'password'
bot = SystemInfoJabberBot(username,password)
not_running = True
while not_running:
    not_running = False
    try: bot.serve_forever()
    except KeyboardInterrupt: print 'saving info and exiting'
    except AttributeError: not_running = True
f = open('infobits.py', 'w')
f.write('infobits = %s' % str(infobits))
f.close()
