$config = {
  'NNGS' => {
    'server'=>'jsb.cs.uec.ac.jp',
#    'server'=>'nngs.computer-go.jp',
#    'server'=>'192.168.1.1',
    'port'=>'9696',
    'user'=>'tester',    # your account
    'pass'=>'tester'       # your password (any)
  },
  'GTP' => {            # command to start your program
#    'command'=>'zen-10.4 --threads=1 --games=999999 --memory=400'
#    'command'=>'/home/yss/aya/ayamc -gtp'
#    'command'=>'/usr/games/bin/gnugo --mode gtp --quiet'
#     'command'=>'/usr/local/bin/gnugo --mode gtp --chinese-rules'
     'command'=>'python /home/ubuntu/workspace/pyspace/gtp_client/run_goplayer_api_v1_1.py -nngs'
  },
  'SIZE' => 19,
  'TIME' => 15,         # minutes
  'KOMI' => 7.0,
  'BYO_YOMI' => 0
}
