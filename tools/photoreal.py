# Usage: python3 photoreal.py <input still.jpg> <out dir> [seedream55] [gpt26-sunburst] [gpt26-flare]
# Sends a measured Blender still to image models on Wiro and saves the photoreal versions.
# Needs WIRO_API_KEY and WIRO_API_SECRET in the environment. Costs money (about 4-7 cents per image on 2026-11-14):
# get ben's OK before running. The prompt describes the 2026-11-14 layout; edit PROMPT when the room changes.
import os,sys,json,hmac,hashlib,time,urllib.request
K=os.environ['WIRO_API_KEY']; S=os.environ['WIRO_API_SECRET']
def call(path,body):
    n=str(int(time.time())); sig=hmac.new(K.encode(),(S+n).encode(),hashlib.sha256).hexdigest()
    r=urllib.request.Request('https://api.wiro.ai/v1/'+path,data=json.dumps(body).encode(),headers={'x-api-key':K,'x-nonce':n,'x-signature':sig,'Content-Type':'application/json','User-Agent':'room-render/1.0'})
    try: return json.load(urllib.request.urlopen(r,timeout=60))
    except urllib.error.HTTPError as e: return {'http':e.code,'body':e.read().decode()[:500]}
import subprocess
PROMPT=("Turn this 3D render into a photorealistic interior photograph of the same room. Keep the exact camera angle, room shape, "
"and every object in the same position, size and proportion. Do not add, remove, move or resize any furniture or wall item. "
"Replace the simplified shapes with realistic versions: a walnut desk with matte black legs and two monitors on arms, a gray mesh ergonomic office chair "
"with a white frame, three charcoal fabric acoustic panels on the back wall, an acoustic guitar and a red electric guitar hanging on the wall, "
"a black digital piano on an X-stand with an X-style bench, a small walnut floating shelf, a charcoal fabric loveseat under the window, "
"a charcoal roller shade half lowered, a walnut media console with a soundbar and a wall-mounted TV on the left, a fiddle leaf fig in a white planter, "
"a gray low-pile rug on gray-brown wood plank flooring, a black ceiling fan, warm greige walls and white baseboards. "
"Natural daylight from the window, soft realistic shadows, real material textures, interior design magazine photography, wide-angle lens.")
def run(owner,proj,fields,img):
    n=str(int(time.time())); sig=hmac.new(K.encode(),(S+n).encode(),hashlib.sha256).hexdigest()
    cmd=['curl','-s','-m','120','-X','POST',f'https://api.wiro.ai/v1/Run/{owner}/{proj}','-H',f'x-api-key: {K}','-H',f'x-nonce: {n}','-H',f'x-signature: {sig}','-F',f'inputImage=@{img}','-F',f'prompt={PROMPT}']
    for k,v in fields.items(): cmd+=['-F',f'{k}={v}']
    return json.loads(subprocess.run(cmd,capture_output=True,text=True).stdout or '{}')
jobs={'seedream55':('bytedance','seedream-5-5',{'resolution':'2k','aspectRatio':'3:2','outputFormat':'jpeg'}),
      'gpt26-sunburst':('openai','gpt-image-2-6-sunburst',{'resolution':'2k','ratio':'3:2','quality':'high','samples':'1','outputFormat':'jpeg'}),
      'gpt26-flare':('openai','gpt-image-2-6-flare',{'resolution':'2k','ratio':'3:2','quality':'high','samples':'1','outputFormat':'jpeg'})}
OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True); only=sys.argv[3:] or list(jobs); tok={}
for name in only:
    o,p,f=jobs[name]; r=run(o,p,f,sys.argv[1]); print(name,'->',{k:r.get(k) for k in ('result','errors','taskid')}); 
    if r.get('socketaccesstoken'): tok[name]=r['socketaccesstoken']
t0=time.time()
while tok and time.time()-t0<400:
    time.sleep(6)
    for name in list(tok):
        d=call('Task/Detail',{'tasktoken':tok[name]}); t=(d.get('tasklist') or [{}])[0]; st=t.get('status')
        if st in ('task_postprocess_end','task_cancel'):
            outs=[o.get('url') for o in t.get('outputs',[])]; print(name,st,'cost',t.get('totalcost'),outs, (t.get('debugerror') or '')[:300])
            for i,u in enumerate(outs): subprocess.run(['curl','-s','-m','120','-o',f'{OUT}/{name}{"-"+str(i) if i else ""}.jpg',u])
            del tok[name]
print('pending',list(tok))
