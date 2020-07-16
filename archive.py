import sys
import time
import random

from urllib.parse import urlencode
import requests
import json

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
URLS = [
    # linux
    'https://github.com/torvalds/linux', 'https://github.com/torvalds/linux/archive/master.zip',

    # i2p
    'https://github.com/i2p/i2p.i2p', 'https://github.com/i2p/i2p.i2p/archive/master.zip',
    'https://github.com/i2p/i2psam', 'https://github.com/i2p/i2psam/archive/master.zip',
    'https://github.com/i2p/i2p-rs', 'https://github.com/i2p/i2p-rs/archive/master.zip',
    'https://github.com/i2p/libsam3', 'https://github.com/i2p/libsam3/archive/master.zip',
    'https://github.com/i2p/i2p.android.base', 'https://github.com/i2p/i2p.android.base/archive/master.zip',
    'https://github.com/i2p/i2p.i2p-bote', 'https://github.com/i2p/i2p.i2p-bote/archive/master.zip',

    # tor
    'https://gitweb.torproject.org/tor.git/',
    'https://github.com/torproject/tor', 'https://github.com/torproject/tor/archive/master.zip',
    # orbot
    'https://github.com/guardianproject/orbot', 'https://github.com/guardianproject/orbot/archive/master.zip',
    'https://gitlab.com/guardianproject/orbot', 'https://gitlab.com/guardianproject/orbot/-/archive/master/orbot-master.zip',

    # zeronet
    'https://github.com/HelloZeroNet/ZeroNet', 'https://github.com/HelloZeroNet/ZeroNet/archive/py3.zip',
    'https://github.com/HelloZeroNet/ZeroMail', 'https://github.com/HelloZeroNet/ZeroMail/archive/master.zip',
    'https://github.com/HelloZeroNet/ZeroBundle', 'https://github.com/HelloZeroNet/ZeroBundle/archive/py3.zip',
    'https://github.com/HelloZeroNet/ZeroNet-kivy', 'https://github.com/HelloZeroNet/ZeroNet-kivy/archive/master.zip',
    'https://github.com/HelloZeroNet/ZeroBlog', 'https://github.com/HelloZeroNet/ZeroBlog/archive/master.zip',
    'https://github.com/HelloZeroNet/ZeroMe', 'https://github.com/HelloZeroNet/ZeroMe/archive/master.zip',

    # tox
    'https://github.com/TokTok/c-toxcore', 'https://github.com/TokTok/c-toxcore/archive/master.zip',

    # ipfs
    'https://github.com/ipfs/ipfs', 'https://github.com/ipfs/ipfs/archive/master.zip',
    'https://github.com/ipfs/ipfs-docs', 'https://github.com/ipfs/ipfs-docs/archive/master.zip',
    'https://github.com/ipfs/js-ipfs', 'https://github.com/ipfs/js-ipfs/archive/master.zip',
    'https://github.com/ipfs/go-ipfs', 'https://github.com/ipfs/go-ipfs/archive/master.zip',
    'https://github.com/ipfs/team-mgmt', 'https://github.com/ipfs/team-mgmt/archive/master.zip',
    'https://github.com/ipfs/awesome-ipfs', 'https://github.com/ipfs/awesome-ipfs/archive/master.zip',
    'https://github.com/ipfs/community', 'https://github.com/ipfs/community/archive/master.zip',

    # syncthing
    'https://github.com/syncthing/syncthing', 'https://github.com/syncthing/syncthing/archive/main.zip',
    'https://github.com/syncthing/syncthing-android', 'https://github.com/syncthing/syncthing-android/archive/master.zip',
    'https://github.com/syncthing/syncthing-macos', 'https://github.com/syncthing/syncthing-macos/archive/develop.zip',
    'https://github.com/syncthing/docs', 'https://github.com/syncthing/docs/archive/main.zip',

    # monero
    'https://github.com/monero-project/monero', 'https://github.com/monero-project/monero/archive/master.zip',
    'https://github.com/monero-project/monero-gui', 'https://github.com/monero-project/monero-gui/archive/master.zip',
    'https://github.com/monero-project/monero-site', 'https://github.com/monero-project/monero-site/archive/master.zip',
    # kovri
    'https://gitlab.com/kovri-project/kovri', 'https://gitlab.com/kovri-project/kovri/-/archive/master/kovri-master.zip',
    'https://gitlab.com/kovri-project/kovri-docs', 'https://gitlab.com/kovri-project/kovri-docs/-/archive/master/kovri-docs-master.zip',
    'https://gitlab.com/kovri-project/kovri-site', 'https://gitlab.com/kovri-project/kovri-site/-/archive/master/kovri-site-master.zip',

    # bitcoin
    'https://github.com/bitcoin/bitcoin', 'https://github.com/bitcoin/bitcoin/archive/master.zip',
    'https://github.com/bitcoin/bips', 'https://github.com/bitcoin/bips/archive/master.zip',

    # ethereum
    'https://github.com/ethereum/go-ethereum', 'https://github.com/ethereum/go-ethereum/archive/master.zip',
    'https://github.com/ethereum/EIPs', 'https://github.com/ethereum/EIPs/archive/master.zip',
    'https://github.com/ethereum/solidity', 'https://github.com/ethereum/solidity/archive/develop.zip',
    'https://github.com/ethereum/remix', 'https://github.com/ethereum/remix/archive/master.zip',
    'https://github.com/ethereum/web3.js', 'https://github.com/ethereum/web3.js/archive/1.x.zip',

    # utls
    'https://github.com/refraction-networking/utls', 'https://github.com/refraction-networking/utls/archive/master.zip',

    # symtcp
    'https://github.com/seclab-ucr/SymTCP', 'https://github.com/seclab-ucr/SymTCP/archive/master.zip',
    # intang
    'https://github.com/seclab-ucr/INTANG', 'https://github.com/seclab-ucr/INTANG/archive/master.zip',

    # node.js
    'https://github.com/nodejs/node', 'https://github.com/nodejs/node/archive/master.zip',

    # v2ray
    'https://github.com/v2ray/v2ray-core', 'https://github.com/v2ray/v2ray-core/archive/master.zip',
    'https://github.com/v2fly/v2ray-core', 'https://github.com/v2fly/v2ray-core/archive/master.zip',
    'https://github.com/v2ray/manual', 'https://github.com/v2ray/manual/archive/master.zip',
    'https://github.com/v2fly/manual', 'https://github.com/v2fly/manual/archive/master.zip',

    # trojan
    'https://github.com/trojan-gfw/trojan', 'https://github.com/trojan-gfw/trojan/archive/master.zip',
    'https://github.com/trojan-gfw/igniter', 'https://github.com/trojan-gfw/igniter/archive/master.zip',
    'https://github.com/trojan-gfw/trojan-manager', 'https://github.com/trojan-gfw/trojan-manager/archive/master.zip',
    'https://github.com/trojan-gfw/trojan-panel', 'https://github.com/trojan-gfw/trojan-panel/archive/master.zip',
    # trojan-go
    'https://github.com/p4gefau1t/trojan-go', 'https://github.com/p4gefau1t/trojan-go/archive/master.zip',
    'https://github.com/p4gefau1t/trojan-go-android', 'https://github.com/p4gefau1t/trojan-go-android/archive/trojan-go.zip',

    # naiveproxy
    'https://github.com/klzgrad/naiveproxy', 'https://github.com/klzgrad/naiveproxy/archive/master.zip',

    # shadowsocks
    'https://github.com/shadowsocks/shadowsocks-libev', 'https://github.com/shadowsocks/shadowsocks-libev/archive/master.zip',
    'https://github.com/shadowsocks/go-shadowsocks2', 'https://github.com/shadowsocks/go-shadowsocks2/archive/master.zip',
    'https://github.com/shadowsocks/shadowsocks-rust', 'https://github.com/shadowsocks/shadowsocks-rust/archive/master.zip',
    'https://github.com/shadowsocks/ShadowsocksX-NG', 'https://github.com/shadowsocks/ShadowsocksX-NG/archive/develop.zip',
    'https://github.com/shadowsocks/shadowsocks-windows', 'https://github.com/shadowsocks/shadowsocks-windows/archive/master.zip',
    'https://github.com/shadowsocks/shadowsocks-android', 'https://github.com/shadowsocks/shadowsocks-android/archive/master.zip',
    'https://github.com/shadowsocks/shadowsocks-manager', 'https://github.com/shadowsocks/shadowsocks-manager/archive/master.zip',
    'https://github.com/shadowsocks/v2ray-plugin', 'https://github.com/shadowsocks/v2ray-plugin/archive/master.zip',
    'https://github.com/shadowsocks/v2ray-plugin-android', 'https://github.com/shadowsocks/v2ray-plugin-android/archive/master.zip',
    'https://github.com/shadowsocks/Shadowsocks-Net', 'https://github.com/shadowsocks/Shadowsocks-Net/archive/master.zip',
    'https://github.com/shadowsocks/luci-app-shadowsocks', 'https://github.com/shadowsocks/luci-app-shadowsocks/archive/master.zip',

    # udp2raw
    'https://github.com/wangyu-/udp2raw-tunnel', 'https://github.com/wangyu-/udp2raw-tunnel/archive/unified.zip',
    'https://github.com/wangyu-/udp2raw-multiplatform', 'https://github.com/wangyu-/udp2raw-multiplatform/archive/mp.zip',
    'https://github.com/wangyu-/UDPspeeder', 'https://github.com/wangyu-/UDPspeeder/archive/branch_libev.zip',
    'https://github.com/wangyu-/UDPping', 'https://github.com/wangyu-/UDPping/archive/master.zip',
    'https://github.com/wangyu-/tinyPortMapper', 'https://github.com/wangyu-/tinyPortMapper/archive/branch_libev.zip',
    'https://github.com/wangyu-/tinyfecVPN', 'https://github.com/wangyu-/tinyfecVPN/archive/master.zip',

    # geph
    'https://github.com/geph-official/geph2', 'https://github.com/geph-official/geph2/archive/master.zip',
    'https://github.com/geph-official/gephgui', 'https://github.com/geph-official/gephgui/archive/master.zip',
    'https://github.com/geph-official/geph-android', 'https://github.com/geph-official/geph-android/archive/master.zip',

    # xx-net
    'https://github.com/XX-net/XX-Net', 'https://github.com/XX-net/XX-Net/archive/master.zip',

    # chinadns
    'https://github.com/shadowsocks/ChinaDNS', 'https://github.com/shadowsocks/ChinaDNS/archive/master.zip',
    'https://github.com/shadowsocks/ChinaDNS-Python', 'https://github.com/shadowsocks/ChinaDNS-Python/archive/master.zip',
    'https://github.com/aa65535/openwrt-chinadns', 'https://github.com/aa65535/openwrt-chinadns/archive/master.zip',

    # badvpn
    'https://github.com/ambrop72/badvpn', 'https://github.com/ambrop72/badvpn/archive/master.zip',
    'https://github.com/shadowsocks/badvpn', 'https://github.com/shadowsocks/badvpn/archive/shadowsocks-android.zip',

    # clash
    'https://github.com/Dreamacro/clash', 'https://github.com/Dreamacro/clash/archive/master.zip',
    'https://github.com/Dreamacro/clash-dashboard', 'https://github.com/Dreamacro/clash-dashboard/archive/master.zip',
    'https://github.com/trojan-gfw/clash', 'https://github.com/trojan-gfw/clash/archive/igniter-go-libs.zip',

    # gost
    'https://github.com/ginuerzh/gost', 'https://github.com/ginuerzh/gost/archive/master.zip',

    # gotox
    'https://github.com/SeaHOH/GotoX', 'https://github.com/SeaHOH/GotoX/archive/master.zip',

    # accesser
    'https://github.com/URenko/Accesser', 'https://github.com/URenko/Accesser/archive/master.zip',

    # gfwlist/a
    'https://github.com/gfwlist/gfwlist', 'https://github.com/gfwlist/gfwlist/archive/master.zip',
    'https://github.com/gfwlist/tinylist', 'https://github.com/gfwlist/tinylist/archive/master.zip',
    'https://github.com/gfwlist/apollyon', 'https://github.com/gfwlist/apollyon/archive/master.zip',
    'https://github.com/gfwlist/tsilwfg', 'https://github.com/gfwlist/tsilwfg/archive/master.zip',
    # gfwlist/b
    'https://github.com/Loukky/gfwlist-by-loukky', 'https://github.com/Loukky/gfwlist-by-loukky/archive/master.zip',
    'https://github.com/poctopus/gfwlist-plus', 'https://github.com/poctopus/gfwlist-plus/archive/master.zip',

    # i
    'https://github.com/BlueSedDragon/task', 'https://github.com/BlueSedDragon/task/archive/master.zip',
]


def log(*args):
    print(f'[{time.time()}] ;', *args)


def display(res):
    log('Url:', res.url)
    log('Status:', res.status_code)
    log('Headers:', json.dumps(dict(res.headers), indent=2))
    log('Body Length:', len(res.content))


def save(url):
    body = urlencode({
        'url': url,
        'capture_all': 'on'
    })
    body = body.encode('utf-8')

    head = {
        'user-agent': USER_AGENT,
        'referer': 'https://web.archive.org/',
        'content-type': 'application/x-www-form-urlencoded',
        'content-length': str(len(body))
    }

    log('SAVE-REQUEST:', url)
    res = requests.post('https://web.archive.org/save',
                        data=body, headers=head)
    log('SAVE-RESPONSE:', url)

    return res


def main():
    random.shuffle(URLS)
    for url in URLS:
        print('=' * 50)

        # retry if not successfully
        left = 10
        while left > 0:
            try:
                res = save(url)
                if res.status_code == 429:
                    left += 1
                    time.sleep(2)
                    raise Exception('HTTP Status == 429')
                if str(res.status_code)[0] != '2':
                    raise Exception('HTTP Status != 2XX')
            except BaseException as err:
                print(repr(err))
                left -= 1
                time.sleep(1)
            else:
                left = 1
                break

        if left <= 0:
            # now failed
            continue

        # now successfully
        display(res)
        time.sleep(5)


main()
