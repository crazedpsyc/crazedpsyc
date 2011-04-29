#!/usr/bin/env python
from urllib import urlopen

def main(line, ld, conf):
    if len(line) > 1:
        print 'Searching %s for %s...' % (conf.search_engine['name'], ' '.join(line[1:]))
        queryurl = conf.search_engine['url'] % '+'.join(line[1:])

        try: raw = urlopen(queryurl).read()
        except: return 'error'
        tmp = open(ld + '/dostmp.py', 'w')
        tmp.write('data = ' + raw)
        tmp.close()
        
        import dostmp
        reload(dostmp)
        
        resulted = False
        
        if dostmp.data['Definition']: 
            print 'Definition:', dostmp.data['Definition']
            resulted = True
        if dostmp.data['Answer']: 
            print 'Answer:', dostmp.data['Answer']
            resulted = True
        if dostmp.data['AbstractText']: 
            print 'Abstract Text:', dostmp.data['AbstractText']
            resulted = True
        if dostmp.data['Abstract'] and dostmp.data['Abstract'] != dostmp.data['AbstractText']: 
            print 'Abstract:', dostmp.data['Abstract']
            resulted = True
            
        if resulted: return

        if dostmp.data['RelatedTopics']:
            print 'Related topics:'
            for res in dostmp.data['RelatedTopics']:
                print res['Text']
                
                
class conf: # a quick class to simulate the configuration module for running without DOSprompt
    search_engine = {'name': 'DuckDuckGo', 'url': 'https://api.duckduckgo.com/?q=%s&o=json'}
    
if __name__ == '__main__':
    import sys, os
    main(sys.argv, os.getcwd(), conf)
