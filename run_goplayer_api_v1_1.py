import requests
from datetime import datetime
import urllib
import sys
import os
import re
import time

fout= sys.stdout
errout = sys.stderr
log = open('./my_log_v1_1', "w")

def formatRequest(command, ai_version):
    # this token will be valid until 12/26/2015
    # access_token = "CAANu9rt94scBACy39ZAMdJUxc8K8yvvUrLAE9H41V7pbRSBgXZBZB3iIJFXeCx3PHzJIFe0MjLD0CXGke9CsIKdKKwOgpvhqNf2JOWAvWDAPNHp55gdazhZBKbZA1FCh1hKVjcZAV6VIShyaWFxz5399XEZA5GX1LP6VfE7UumNRswK148RZAJDybrzHaCb43f9M0W0B7deOFAZDZD"
    access_token = "966430916731591|bc3abd45648a95ade0c78dd35b393ebe"
    api_url = "https://graph.facebook.com/v2.5/ai_demos/generate_go_player/?"
    arguments = {
        "access_token": access_token,
        "opponent_command": command,
        "ai_version": ai_version,
    }
    query = api_url + urllib.urlencode(arguments)
    max_test = 100
    testCnt = 0
    while True:
        testCnt = testCnt + 1
        ret = requests.post(query)
        if checkConnection(ret.text) or testCnt > max_test:
            break
        else:
            logging("%d failed at %s" % (testCnt, ret.text))
            time.sleep(0.1)
    return ret.text

def checkConnection(ret):
    searchObj = re.search("ai_command", ret)
    return searchObj is not None

def parseRet(ret):
    searchObj = re.search("\"ai_command\":\"(=?.+)\"}",ret, re.DOTALL)
    if searchObj is None:
        print(ret)
        raise Exception("parse ret failure!")
    kgsRet = searchObj.group(1)
    return kgsRet.decode('unicode_escape')

def logging(s):
    signature = datetime.now().strftime("%Y_%m_%d:%H:%M:%S:%f")
    log.write(signature + " " + s + '\n')
    log.flush()

if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1] == '-nngs':
        nngs = True
    else:
        nngs = False

    ai_version = '0.1'
    logging("start: ")
    ply = 0
    color = "unknown"
    urgent = False
    while True:
        content = raw_input()
        if len(content) == 0:
            continue
        logging("command: \"%s\"" % content)
        if re.search("clear_board", content) is not None:
            ply = 0
            urgent = False
            color = "unknown"
            ret = formatRequest(content, ai_version)
            retCommand = parseRet(ret)
        elif re.search("genmove", content) is not None:
            if color == "unknown":
                thiscolor = content.split()[1]
                color = thiscolor
            ply = ply + 1
            ret = formatRequest(content, ai_version)
            retCommand = parseRet(ret)
        elif re.search("time_left", content) is not None:
            timeleft_secs = int(content.split()[2])
            thiscolor = content.split()[1]
            if ply < 25 or urgent == True or thiscolor != color:
                retCommand = str(ply) + "? ?\n"  # filter these time_left commands
            else:
                if thiscolor == color and timeleft_secs < 130:
                    logging("very urgent, dont care time_left")
                    urgent = True
                ret = formatRequest(content, ai_version)
                retCommand = parseRet(ret)

        elif re.search("time_settings", content) is not None:
            retComand = "? ??--\n"
        elif False and re.search("kgs-game_over", content) is not None:
            retCommand = "? ???over"
            break
        else:
            ret = formatRequest(content, ai_version)
            retCommand = parseRet(ret)

        if nngs == False:
            fout.write(retCommand)
            fout.flush()
            fout.write("\n\n")
            fout.flush()
        else:
            fout.write(retCommand)
            print(" \n")
#            print("content:" + content +" | ret: " + retCommand)
            fout.flush()

        logging("Response received: \"%s\"" % retCommand)

        if content == "quit":
            break

