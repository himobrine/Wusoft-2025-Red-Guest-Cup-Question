from scapy.all import *
import random
import os
from scapy.layers.dns import DNS, DNSQR, DNSRR


def generate_stealthy_pcap():
    # 配置参数
    flag = "wrhklm{72a0826a0ec193e33c8c8c4f010f7ff24c91fcf0}"
    total_packets = 1200
    source_ip = "192.168.120.3"
    dest_ip = "192.168.120.254"

    # 路由路径设置
    router_ips = ["192.168.120.1", "192.168.120.64",
                  "192.168.120.128", "192.168.120.192"]

    # 协议权重与典型包长范围（字节）
    protocols = {
        'icmp': {'weight': 0.4, 'min_len': 60, 'max_len': 150},
        'tcp': {'weight': 0.35, 'min_len': 80, 'max_len': 250},
        'udp': {'weight': 0.2, 'min_len': 70, 'max_len': 200},
        'dns': {'weight': 0.05, 'min_len': 50, 'max_len': 120}
    }

    packets = []
    flag_inserted = False
    flag_position = random.randint(400, 800)  # 在中间段隐藏flag

    # 生成流量
    for i in range(total_packets):
        # 动态路由选择
        hop_idx = (i // 200) % len(router_ips)
        current_hop = router_ips[hop_idx]
        ttl = 32 - hop_idx

        # 选择协议
        proto = random.choices(
            list(protocols.keys()),
            weights=[p['weight'] for p in protocols.values()],
            k=1
        )[0]
        proto_conf = protocols[proto]

        # 确定包长度（flag包取中间值）
        if (not flag_inserted) and (i >= flag_position):
            pkt_len = random.randint(
                (proto_conf['min_len'] + proto_conf['max_len']) // 2 - 20,
                (proto_conf['min_len'] + proto_conf['max_len']) // 2 + 20
            )
            hide_flag = True
            flag_inserted = True
            print(f"[+] Flag being inserted in packet {i}")
        else:
            pkt_len = random.randint(proto_conf['min_len'], proto_conf['max_len'])
            hide_flag = False

        # ICMP协议
        if proto == 'icmp':
            payload = os.urandom(pkt_len - 28)  # 减去IP+ICMP头
            if hide_flag:
                payload = f"ICMP[{flag}]".encode() + os.urandom(pkt_len - 28 - len(flag) - 6)

            pkt = Ether(src=RandMAC(), dst=RandMAC()) / \
                  IP(src=current_hop, dst=dest_ip, ttl=ttl, id=i) / \
                  ICMP() / payload

        # TCP协议
        elif proto == 'tcp':
            payload = os.urandom(pkt_len - 40)  # 减去IP+TCP头
            if hide_flag:
                payload = f"TCP<{flag}>".encode() + os.urandom(pkt_len - 40 - len(flag) - 6)

            pkt = Ether(src=RandMAC(), dst=RandMAC()) / \
                  IP(src=current_hop, dst=dest_ip, ttl=ttl, id=i) / \
                  TCP(sport=random.randint(32768, 60999),
                      dport=random.choice([22, 80, 443, 3389]),
                      flags=random.choice(["S", "A", "PA"])) / payload

        # UDP协议
        elif proto == 'udp':
            payload = os.urandom(pkt_len - 28)  # 减去IP+UDP头
            if hide_flag:
                payload = f"UDP#{flag}#".encode() + os.urandom(pkt_len - 28 - len(flag) - 6)

            pkt = Ether(src=RandMAC(), dst=RandMAC()) / \
                  IP(src=current_hop, dst=dest_ip, ttl=ttl, id=i) / \
                  UDP(sport=random.randint(32768, 60999),
                      dport=random.choice([53, 123, 161])) / payload

        # DNS协议
        elif proto == 'dns':
            if hide_flag:
                pkt = Ether(src=RandMAC(), dst=RandMAC()) / \
                      IP(src=current_hop, dst="8.8.4.4", ttl=ttl, id=i) / \
                      UDP(sport=5353, dport=53) / \
                      DNS(rd=1,
                          qd=DNSQR(qname="dns"),
                          an=DNSRR(rrname="dns",
                                   type="TXT",
                                   rdata='"' + flag + '"'))
            else:
                pkt = Ether(src=RandMAC(), dst=RandMAC()) / \
                      IP(src=current_hop, dst="8.8.8.8", ttl=ttl, id=i) / \
                      UDP(sport=random.randint(32768, 60999), dport=53) / \
                      DNS(rd=1, qd=DNSQR(
                          qname=random.choice(["huawei.com", "baidu.com"]),
                          qtype=random.choice(["A", "AAAA"])
                      ))

        # 添加8%概率的假flag干扰
        if random.random() < 0.08 and not hide_flag:
            fake_flag = "wrhklm﻿﻿}"
            if proto in ['tcp', 'udp']:
                pkt = pkt / fake_flag.encode()
            elif proto == 'dns':
                pkt.an = DNSRR(rrname="fake.ctf", type="TXT", rdata='"' + fake_flag + '"')

        packets.append(pkt)

    # 确保flag已被插入
    if not flag_inserted:
        mid_len = (protocols['tcp']['min_len'] + protocols['tcp']['max_len']) // 2
        packets[-1] = packets[-1] / f"EMERGENCY_FLAG:{flag}".ljust(mid_len - 40, '_').encode()
        print(f"[+] Emergency flag inserted into the last packet.")

    # Flag Search Improvement: Look directly in the payload of each packet
    flag_pkt = None
    for pkt in packets:
        if flag.encode() in bytes(pkt.payload):  # Check in the payload (raw bytes)
            flag_pkt = pkt
            break

    if flag_pkt:
        print(f"[+] Flag found in packet {packets.index(flag_pkt)}")
    else:
        print("[!] Flag not found in any packet.")

    # 写入文件
    wrpcap("flag.pcapng", packets)

    # 统计flag包信息
    if flag_pkt:
        print(f"[+] 生成完成！关键特征：")
        print(f"    - Flag隐藏在{packets.index(flag_pkt)}号包（{flag_pkt.summary()}）")
        print(f"    - Flag包长度：{len(flag_pkt)}字节（中等范围）")
        print(f"    - 路由路径：{' → '.join([source_ip] + router_ips + [dest_ip])}")
        print(f"    - 协议分布：ICMP({protocols['icmp']['weight'] * 100}%) "
              f"TCP({protocols['tcp']['weight'] * 100}%) "
              f"UDP({protocols['udp']['weight'] * 100}%) "
              f"DNS({protocols['dns']['weight'] * 100}%)")
    else:
        print("[!] Flag insertion failed.")


generate_stealthy_pcap()
