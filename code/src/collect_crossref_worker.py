import sys, json, random
sys.path.insert(0,"/home/user/rp_c_8/code/src")
import collect_crossref as C
from concurrent.futures import ThreadPoolExecutor
mode=sys.argv[1]
fr=json.load(open(C.RAW+"frame_eligible.json"))
if mode=="rev": fr=fr[::-1]
else: random.Random(int(sys.argv[2])).shuffle(fr)
with ThreadPoolExecutor(4) as ex: list(ex.map(C.do,fr))
