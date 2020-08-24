import sys
import time
import random

from urllib.parse import urlencode
import requests
import json

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
URLS = list({
    # rust
    'https://github.com/rust-lang/rust', 'https://github.com/rust-lang/rust/archive/master.zip',
    'https://github.com/rust-lang/cargo', 'https://github.com/rust-lang/cargo/archive/master.zip',
    'https://github.com/rust-lang/rfcs', 'https://github.com/rust-lang/rfcs/archive/master.zip',

    # python
    'https://github.com/python/cpython', 'https://github.com/python/cpython/archive/master.zip',
    'https://github.com/python/pythondotorg', 'https://github.com/python/pythondotorg/archive/master.zip',
    'https://github.com/python/peps', 'https://github.com/python/peps/archive/master.zip',
    'https://github.com/python/mypy', 'https://github.com/python/mypy/archive/master.zip',
    'https://github.com/python/typeshed', 'https://github.com/python/typeshed/archive/master.zip',
    'https://github.com/python/devguide', 'https://github.com/python/devguide/archive/master.zip',

    # java
    'https://github.com/openjdk/jdk', 'https://github.com/openjdk/jdk/archive/master.zip',
    'https://github.com/openjdk/loom', 'https://github.com/openjdk/loom/archive/fibers.zip',
    'https://github.com/openjdk/amber', 'https://github.com/openjdk/amber/archive/master.zip',
    'https://github.com/openjdk/valhalla', 'https://github.com/openjdk/valhalla/archive/lworld.zip',
    'https://github.com/openjdk/jfx', 'https://github.com/openjdk/jfx/archive/master.zip',
    'https://github.com/openjdk/jmc', 'https://github.com/openjdk/jmc/archive/master.zip',

    # go
    'https://github.com/golang/go', 'https://github.com/golang/go/archive/master.zip',

    # php
    'https://github.com/php/php-src', 'https://github.com/php/php-src/archive/master.zip',

    # v8
    'https://github.com/v8/v8', 'https://github.com/v8/v8/archive/master.zip',

    # llvm
    'https://github.com/llvm/llvm-project', 'https://github.com/llvm/llvm-project/archive/master.zip',

    # linux
    'https://github.com/torvalds/linux', 'https://github.com/torvalds/linux/archive/master.zip',

    # freebsd
    'https://github.com/freebsd/freebsd', 'https://github.com/freebsd/freebsd/archive/master.zip',
    'https://github.com/freebsd/freebsd-ports', 'https://github.com/freebsd/freebsd-ports/archive/master.zip',
    'https://github.com/freebsd/freebsd-doc', 'https://github.com/freebsd/freebsd-doc/archive/master.zip',

    # openbsd
    'https://github.com/openbsd/src', 'https://github.com/openbsd/src/archive/master.zip',
    'https://github.com/openbsd/ports', 'https://github.com/openbsd/ports/archive/master.zip',
    'https://github.com/openbsd/xenocara', 'https://github.com/openbsd/xenocara/archive/master.zip',
    'https://github.com/openbsd/www', 'https://github.com/openbsd/www/archive/master.zip',

    # dragonfly bsd
    'https://github.com/DragonFlyBSD/DragonFlyBSD', 'https://github.com/DragonFlyBSD/DragonFlyBSD/archive/master.zip',

    # systemd
    'https://github.com/systemd/systemd', 'https://github.com/systemd/systemd/archive/master.zip',
    'https://github.com/systemd/casync', 'https://github.com/systemd/casync/archive/master.zip',
    'https://github.com/systemd/mkosi', 'https://github.com/systemd/mkosi/archive/master.zip',

    # apt
    'https://github.com/Debian/apt', 'https://github.com/Debian/apt/archive/master.zip',

    # quic
    'https://github.com/cloudflare/quiche', 'https://github.com/cloudflare/quiche/archive/master.zip',
    'https://github.com/lucas-clemente/quic-go', 'https://github.com/lucas-clemente/quic-go/archive/master.zip',
    'https://github.com/ngtcp2/ngtcp2', 'https://github.com/ngtcp2/ngtcp2/archive/master.zip',
    'https://github.com/ngtcp2/nghttp3', 'https://github.com/ngtcp2/nghttp3/archive/master.zip',
    'https://github.com/aiortc/aioquic', 'https://github.com/aiortc/aioquic/archive/main.zip',
    'https://github.com/microsoft/msquic', 'https://github.com/microsoft/msquic/archive/master.zip',
    'https://github.com/litespeedtech/lsquic', 'https://github.com/litespeedtech/lsquic/archive/master.zip',

    # kcp
    'https://github.com/skywind3000/kcp', 'https://github.com/skywind3000/kcp/archive/master.zip',
    'https://github.com/xtaci/kcp-go', 'https://github.com/xtaci/kcp-go/archive/master.zip',
    'https://github.com/xtaci/kcptun', 'https://github.com/xtaci/kcptun/archive/master.zip',

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
    # shipyard
    'https://github.com/ipfs-shipyard/shipyard', 'https://github.com/ipfs-shipyard/shipyard/archive/master.zip',
    'https://github.com/ipfs-shipyard/ipfs-companion', 'https://github.com/ipfs-shipyard/ipfs-companion/archive/master.zip',
    'https://github.com/ipfs-shipyard/ipfs-desktop', 'https://github.com/ipfs-shipyard/ipfs-desktop/archive/master.zip',
    'https://github.com/ipfs-shipyard/ipfs-webui', 'https://github.com/ipfs-shipyard/ipfs-webui/archive/master.zip',
    'https://github.com/ipfs-shipyard/npm-on-ipfs', 'https://github.com/ipfs-shipyard/npm-on-ipfs/archive/master.zip',

    # syncthing
    'https://github.com/syncthing/syncthing', 'https://github.com/syncthing/syncthing/archive/main.zip',
    'https://github.com/syncthing/syncthing-android', 'https://github.com/syncthing/syncthing-android/archive/master.zip',
    'https://github.com/syncthing/syncthing-macos', 'https://github.com/syncthing/syncthing-macos/archive/develop.zip',
    'https://github.com/syncthing/docs', 'https://github.com/syncthing/docs/archive/main.zip',

    # nebula
    'https://github.com/slackhq/nebula', 'https://github.com/slackhq/nebula/archive/master.zip',

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

    # cloak
    'https://github.com/cbeuw/Cloak', 'https://github.com/cbeuw/Cloak/archive/master.zip',
    'https://github.com/cbeuw/Cloak-android', 'https://github.com/cbeuw/Cloak-android/archive/master.zip',
    'https://github.com/cbeuw/iiiD6', 'https://github.com/cbeuw/iiiD6/archive/master.zip',
    'https://github.com/cbeuw/GoQuiet', 'https://github.com/cbeuw/GoQuiet/archive/master.zip',

    # nginx
    'https://hg.nginx.org/nginx', 'https://hg.nginx.org/nginx/archive/tip.zip',
    'https://github.com/nginx/nginx', 'https://github.com/nginx/nginx/archive/master.zip',

    # node.js
    'https://github.com/nodejs/node', 'https://github.com/nodejs/node/archive/master.zip',

    # wireshark
    'https://github.com/wireshark/wireshark', 'https://github.com/wireshark/wireshark/archive/master.zip',
    'https://github.com/wireshark/winpcap', 'https://github.com/wireshark/winpcap/archive/master.zip',

    # tcpdump
    'https://github.com/the-tcpdump-group/tcpdump', 'https://github.com/the-tcpdump-group/tcpdump/archive/master.zip',
    'https://github.com/the-tcpdump-group/tcpdump-htdocs', 'https://github.com/the-tcpdump-group/tcpdump-htdocs/archive/master.zip',
    'https://github.com/the-tcpdump-group/libpcap', 'https://github.com/the-tcpdump-group/libpcap/archive/master.zip',

    # nmap
    'https://github.com/nmap/nmap', 'https://github.com/nmap/nmap/archive/master.zip',
    'https://github.com/nmap/npcap', 'https://github.com/nmap/npcap/archive/master.zip',
    'https://github.com/nmap/ncrack', 'https://github.com/nmap/ncrack/archive/master.zip',

    # openvpn
    'https://github.com/OpenVPN/openvpn', 'https://github.com/OpenVPN/openvpn/archive/master.zip',
    'https://github.com/OpenVPN/openvpn3', 'https://github.com/OpenVPN/openvpn3/archive/master.zip',
    'https://gitlab.com/openvpn/openvpn', 'https://gitlab.com/openvpn/openvpn/-/archive/master/openvpn-master.zip',

    # wireguard
    'https://git.zx2c4.com/wireguard-linux/',
    'https://github.com/WireGuard/wireguard-linux', 'https://github.com/WireGuard/wireguard-linux/archive/stable.zip',
    'https://github.com/WireGuard/wireguard-go', 'https://github.com/WireGuard/wireguard-go/archive/master.zip',
    'https://github.com/WireGuard/wireguard-tools', 'https://github.com/WireGuard/wireguard-tools/archive/master.zip',
    'https://github.com/WireGuard/wireguard-android', 'https://github.com/WireGuard/wireguard-android/archive/master.zip',
    'https://github.com/WireGuard/wireguard-apple', 'https://github.com/WireGuard/wireguard-apple/archive/master.zip',
    'https://github.com/WireGuard/wireguard-windows', 'https://github.com/WireGuard/wireguard-windows/archive/master.zip',

    # softether
    'https://github.com/SoftEtherVPN/SoftEtherVPN', 'https://github.com/SoftEtherVPN/SoftEtherVPN/archive/master.zip',
    'https://github.com/SoftEtherVPN/SoftEtherVPN_Stable', 'https://github.com/SoftEtherVPN/SoftEtherVPN_Stable/archive/master.zip',
    'https://github.com/SoftEtherVPN/EtherMirror', 'https://github.com/SoftEtherVPN/EtherMirror/archive/master.zip',

    # geneva
    'https://github.com/kkevsterrr/geneva', 'https://github.com/Kkevsterrr/geneva/archive/master.zip',

    # v2ray
    'https://github.com/v2ray/v2ray-core', 'https://github.com/v2ray/v2ray-core/archive/master.zip',
    'https://github.com/v2fly/v2ray-core', 'https://github.com/v2fly/v2ray-core/archive/master.zip',
    'https://github.com/v2ray/manual', 'https://github.com/v2ray/manual/archive/master.zip',
    'https://github.com/v2fly/manual', 'https://github.com/v2fly/manual/archive/master.zip',  # read-only
    'https://github.com/v2fly/v2fly-github-io', 'https://github.com/v2fly/v2fly-github-io/archive/master.zip',
    # qv2ray
    'https://github.com/Qv2ray/Qv2ray', 'https://github.com/Qv2ray/Qv2ray/archive/master.zip',
    'https://github.com/Qv2ray/qv2ray.github.io', 'https://github.com/Qv2ray/qv2ray.github.io/archive/source.zip',
    'https://github.com/Qv2ray/QvPlugin-SSR', 'https://github.com/Qv2ray/QvPlugin-SSR/archive/master.zip',
    'https://github.com/Qv2ray/QvPlugin-Trojan', 'https://github.com/Qv2ray/QvPlugin-Trojan/archive/master.zip',
    'https://github.com/Qv2ray/QvPlugin-Template', 'https://github.com/Qv2ray/QvPlugin-Template/archive/master.zip',
    'https://github.com/Qv2ray/QvPlugin-Interface', 'https://github.com/Qv2ray/QvPlugin-Interface/archive/interface-v2.zip',
    # v2rayng
    'https://github.com/2dust/v2rayNG', 'https://github.com/2dust/v2rayNG/archive/master.zip',
    'https://github.com/2dust/v2rayN', 'https://github.com/2dust/v2rayN/archive/master.zip',
    # mellow
    'https://github.com/mellow-io/mellow', 'https://github.com/mellow-io/mellow/archive/master.zip',
    'https://github.com/mellow-io/go-tun2socks', 'https://github.com/mellow-io/go-tun2socks/archive/master.zip',
    'https://github.com/eycorsican/go-tun2socks', 'https://github.com/eycorsican/go-tun2socks/archive/master.zip',

    # trojan
    'https://github.com/trojan-gfw/trojan', 'https://github.com/trojan-gfw/trojan/archive/master.zip',
    'https://github.com/trojan-gfw/trojan-manager', 'https://github.com/trojan-gfw/trojan-manager/archive/master.zip',
    'https://github.com/trojan-gfw/trojan-panel', 'https://github.com/trojan-gfw/trojan-panel/archive/master.zip',
    # igniter
    'https://github.com/trojan-gfw/igniter', 'https://github.com/trojan-gfw/igniter/archive/master.zip',
    'https://github.com/trojan-gfw/igniter-go-libs', 'https://github.com/trojan-gfw/igniter-go-libs/archive/master.zip',

    # trojan-go
    'https://github.com/p4gefau1t/trojan-go', 'https://github.com/p4gefau1t/trojan-go/archive/master.zip',
    'https://github.com/p4gefau1t/trojan-go-android', 'https://github.com/p4gefau1t/trojan-go-android/archive/trojan-go.zip',
    # trojan-qt5
    'https://github.com/Trojan-Qt5/Trojan-Qt5', 'https://github.com/Trojan-Qt5/Trojan-Qt5/archive/master.zip',
    # climber
    'https://github.com/Climber7/Climber', 'https://github.com/Climber7/Climber/archive/master.zip',

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

    # brook
    'https://github.com/txthinking/brook', 'https://github.com/txthinking/brook/archive/master.zip',
    'https://github.com/txthinking/mr2', 'https://github.com/txthinking/mr2/archive/master.zip',
    'https://github.com/txthinking/joker', 'https://github.com/txthinking/joker/archive/master.zip',

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

    # frp
    'https://github.com/fatedier/frp', 'https://github.com/fatedier/frp/archive/master.zip',

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

    # git
    'https://github.com/git/git', 'https://github.com/git/git/archive/master.zip',

    # make
    'https://github.com/mirror/make', 'https://github.com/mirror/make/archive/master.zip',

    # cmake
    'https://github.com/Kitware/CMake', 'https://github.com/Kitware/CMake/archive/master.zip',

    # busybox
    'https://github.com/mirror/busybox', 'https://github.com/mirror/busybox/archive/master.zip',

    # docker
    'https://github.com/docker/docker-ce', 'https://github.com/docker/docker-ce/archive/master.zip',
    'https://github.com/docker/compose', 'https://github.com/docker/compose/archive/master.zip',
    'https://github.com/docker/roadmap', 'https://github.com/docker/roadmap/archive/master.zip',
    'https://github.com/docker/github-actions', 'https://github.com/docker/github-actions/archive/master.zip',
    'https://github.com/docker/awesome-compose', 'https://github.com/docker/awesome-compose/archive/master.zip',
    'https://github.com/docker/build-push-action', 'https://github.com/docker/build-push-action/archive/master.zip',
    'https://github.com/docker/ecs-plugin', 'https://github.com/docker/ecs-plugin/archive/master.zip',

    # openssh
    'https://github.com/openssh/openssh-portable', 'https://github.com/openssh/openssh-portable/archive/master.zip',

    # dropbear
    'https://github.com/mkj/dropbear', 'https://github.com/mkj/dropbear/archive/master.zip',

    # fish
    'https://github.com/fish-shell/fish-shell', 'https://github.com/fish-shell/fish-shell/archive/master.zip',
    'https://github.com/fish-shell/fish-site', 'https://github.com/fish-shell/fish-site/archive/master.zip',

    # zsh
    'https://github.com/zsh-users/zsh', 'https://github.com/zsh-users/zsh/archive/master.zip',
    'https://github.com/ohmyzsh/ohmyzsh', 'https://github.com/ohmyzsh/ohmyzsh/archive/master.zip',

    # retdec
    'https://github.com/avast/retdec', 'https://github.com/avast/retdec/archive/master.zip',
    'https://github.com/avast/llvm', 'https://github.com/avast/llvm/archive/master.zip',

    # upx
    'https://github.com/upx/upx', 'https://github.com/upx/upx/archive/master.zip',

    # graphviz
    'https://gitlab.com/graphviz/graphviz', 'https://gitlab.com/graphviz/graphviz/-/archive/master/graphviz-master.zip',

    # openwrt
    'https://github.com/openwrt/openwrt', 'https://github.com/openwrt/openwrt/archive/master.zip',
    'https://github.com/openwrt/packages', 'https://github.com/openwrt/packages/archive/master.zip',
    'https://github.com/openwrt/luci', 'https://github.com/openwrt/luci/archive/master.zip',
    'https://github.com/openwrt/chaos_calmer', 'https://github.com/openwrt/chaos_calmer/archive/chaos_calmer.zip',
    'https://github.com/openwrt/archive', 'https://github.com/openwrt/archive/archive/master.zip',

    # bind
    'https://github.com/isc-projects/bind9', 'https://github.com/isc-projects/bind9/archive/main.zip',
    'https://github.com/isc-projects/kea', 'https://github.com/isc-projects/kea/archive/master.zip',
    'https://github.com/isc-projects/stork', 'https://github.com/isc-projects/stork/archive/master.zip',
    'https://github.com/isc-projects/bind9-stats', 'https://github.com/isc-projects/bind9-stats/archive/master.zip',
    'https://github.com/isc-projects/dhcp', 'https://github.com/isc-projects/dhcp/archive/master.zip',

    # kdig
    'https://github.com/CZ-NIC/knot', 'https://github.com/CZ-NIC/knot/archive/master.zip',

    # curl
    'https://github.com/curl/curl', 'https://github.com/curl/curl/archive/master.zip',
    'https://github.com/curl/curl-www', 'https://github.com/curl/curl-www/archive/master.zip',

    # openssl
    'https://github.com/openssl/openssl', 'https://github.com/openssl/openssl/archive/master.zip',
    'https://github.com/openssl/web', 'https://github.com/openssl/web/archive/master.zip',

    # gnutls
    'https://gitlab.com/gnutls/gnutls', 'https://gitlab.com/gnutls/gnutls/-/archive/master/gnutls-master.zip',
    'https://github.com/gnutls/gnutls', 'https://github.com/gnutls/gnutls/archive/master.zip',

    # wolfssl
    'https://github.com/wolfSSL/wolfssl', 'https://github.com/wolfSSL/wolfssl/archive/master.zip',
    'https://github.com/wolfSSL/wolfMQTT', 'https://github.com/wolfSSL/wolfMQTT/archive/master.zip',
    'https://github.com/wolfSSL/wolfssh', 'https://github.com/wolfSSL/wolfssh/archive/master.zip',
    'https://github.com/wolfSSL/wolfTPM', 'https://github.com/wolfSSL/wolfTPM/archive/master.zip',
    'https://github.com/wolfSSL/wolfBoot', 'https://github.com/wolfSSL/wolfBoot/archive/master.zip',

    # gecko
    'https://github.com/mozilla/gecko-dev', 'https://github.com/mozilla/gecko-dev/archive/master.zip',
    # servo
    'https://github.com/servo/servo', 'https://github.com/servo/servo/archive/master.zip',

    # mediawiki
    'https://github.com/wikimedia/mediawiki', 'https://github.com/wikimedia/mediawiki/archive/master.zip',

    # vscode
    'https://github.com/microsoft/vscode', 'https://github.com/microsoft/vscode/archive/master.zip',

    # i
    'https://github.com/BlueSedDragon/task', 'https://github.com/BlueSedDragon/task/archive/master.zip',
})


def log(*args):
    print(f'[{time.time()}]', *args)


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
                        data=body, headers=head, timeout=60)
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
                if len(str(res.status_code)) != 3:
                    raise Exception(f'Bad HTTP Status {res.status_code}')
                if res.status_code == 429:
                    left += 1
                    time.sleep(2)
                    raise Exception('HTTP Status == 429')
                if str(res.status_code)[0] != '2':
                    raise Exception(f'HTTP Status {res.status_code} != 2XX')
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
