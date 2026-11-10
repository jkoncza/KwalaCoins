import hashlib, struct, sys, time, calendar
def dsha(b): return hashlib.sha256(hashlib.sha256(b).digest()).digest()
def compact_to_target(c):
    e=c>>24; m=c&0x7fffff
    return m<<(8*(e-3))
def genesis(ts_msg, ntime, nbits, reward, pubkey_hex, search=True):
    msg=ts_msg.encode()
    assert len(msg)<76
    script_sig=bytes([4])+bytes.fromhex("ffff001d")+bytes([1,4])+bytes([len(msg)])+msg
    pk=bytes.fromhex(pubkey_hex)
    spk=bytes([len(pk)])+pk+bytes([0xac])
    tx=struct.pack("<i",1)+b"\x01"+b"\x00"*32+struct.pack("<I",0xffffffff)+bytes([len(script_sig)])+script_sig+struct.pack("<I",0xffffffff)
    tx+=b"\x01"+struct.pack("<q",reward)+bytes([len(spk)])+spk+struct.pack("<I",0)
    merkle=dsha(tx)
    target=compact_to_target(nbits)
    nonce=0
    while True:
        hdr=struct.pack("<i",1)+b"\x00"*32+merkle+struct.pack("<III",ntime,nbits,nonce)
        h=dsha(hdr)
        if int.from_bytes(h,"little")<=target: return nonce,h[::-1].hex(),merkle[::-1].hex()
        nonce+=1
if __name__=="__main__":
    ntime=calendar.timegm((2026,11,5,21,30,0))
    msg="KwalaCoins 05/Nov/2026 Fast, fair money for everyone"
    pub="04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f"
    n,h,m=genesis(msg,ntime,0x1e0fffff,100*10**8,pub)
    print(ntime,n,h,m)
