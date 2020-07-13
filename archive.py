import sys
import time

from urllib.parse import urlencode
import requests
import json

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
URLS = [
    # i2p
    'https://github.com/i2p/i2p.i2p', 'https://github.com/i2p/i2p.i2p/archive/master.zip',
    'https://github.com/i2p/i2psam', 'https://github.com/i2p/i2psam/archive/master.zip',
    'https://github.com/i2p/i2p-rs', 'https://github.com/i2p/i2p-rs/archive/master.zip',
    'https://github.com/i2p/libsam3', 'https://github.com/i2p/libsam3/archive/master.zip',
    'https://github.com/i2p/i2p.android.base', 'https://github.com/i2p/i2p.android.base/archive/master.zip',
    'https://github.com/i2p/i2p.i2p-bote', 'https://github.com/i2p/i2p.i2p-bote/archive/master.zip',

    # monero
    'https://github.com/monero-project/monero', 'https://github.com/monero-project/monero/archive/master.zip',
    'https://github.com/monero-project/monero-gui', 'https://github.com/monero-project/monero-gui/archive/master.zip',
    'https://github.com/monero-project/monero-site', 'https://github.com/monero-project/monero-site/archive/master.zip',
    # kovri
    'https://gitlab.com/kovri-project/kovri', 'https://gitlab.com/kovri-project/kovri/-/archive/master/kovri-master.zip',
    'https://gitlab.com/kovri-project/kovri-docs', 'https://gitlab.com/kovri-project/kovri-docs/-/archive/master/kovri-docs-master.zip',
    'https://gitlab.com/kovri-project/kovri-site', 'https://gitlab.com/kovri-project/kovri-site/-/archive/master/kovri-site-master.zip',

    # v2ray
    'https://github.com/v2ray/v2ray-core', 'https://github.com/v2ray/v2ray-core/archive/master.zip',
    'https://github.com/v2fly/v2ray-core', 'https://github.com/v2fly/v2ray-core/archive/master.zip',

    # trojan
    'https://github.com/trojan-gfw/trojan', 'https://github.com/trojan-gfw/trojan/archive/master.zip',
    'https://github.com/trojan-gfw/igniter', 'https://github.com/trojan-gfw/igniter/archive/master.zip',
    'https://github.com/trojan-gfw/trojan-manager', 'https://github.com/trojan-gfw/trojan-manager/archive/master.zip',
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

    # chinadns
    'https://github.com/shadowsocks/ChinaDNS', 'https://github.com/shadowsocks/ChinaDNS/archive/master.zip',
    'https://github.com/shadowsocks/ChinaDNS-Python', 'https://github.com/shadowsocks/ChinaDNS-Python/archive/master.zip',
    'https://github.com/aa65535/openwrt-chinadns', 'https://github.com/aa65535/openwrt-chinadns/archive/master.zip',

    # badvpn
    'https://github.com/ambrop72/badvpn', 'https://github.com/ambrop72/badvpn/archive/master.zip',
    'https://github.com/shadowsocks/badvpn', 'https://github.com/shadowsocks/badvpn/archive/shadowsocks-android.zip',

    # clash
    'https://github.com/Dreamacro/clash', 'https://github.com/Dreamacro/clash/archive/master.zip',
    'https://github.com/trojan-gfw/clash', 'https://github.com/trojan-gfw/clash/archive/igniter-go-libs.zip',

    # gost
    'https://github.com/ginuerzh/gost', 'https://github.com/ginuerzh/gost/archive/master.zip',

    # accesser
    'https://github.com/URenko/Accesser', 'https://github.com/URenko/Accesser/archive/master.zip',

    # gfwlist
    'https://github.com/gfwlist/gfwlist', 'https://github.com/gfwlist/gfwlist/archive/master.zip',
    'https://github.com/gfwlist/tinylist', 'https://github.com/gfwlist/tinylist/archive/master.zip',
    'https://github.com/gfwlist/apollyon', 'https://github.com/gfwlist/apollyon/archive/master.zip',
    'https://github.com/gfwlist/tsilwfg', 'https://github.com/gfwlist/tsilwfg/archive/master.zip',
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
    for url in URLS:
        print('=' * 50)

        # retry if not successfully
        left = 10
        while left > 0:
            try:
                res = save(url)
                if res.status_code == 429:
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
