import os
import subprocess
import time
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.cm as cm
from ftplib import FTP

timestr = time.strftime("%d%m%Y-%H%M")
pcap = "D:/LiveCapture/PCAP/"+timestr+".pcap"
csv = "D:/LiveCapture/CSV/"+timestr+".csv"
image= "D:/LiveCapture/IMAGE/"+timestr+".png"
dot= "D:/LiveCapture/DOT/"+timestr+".dot"

def CaptureData():
    print('Memulai Proses Capturing...')
    #os.system("tshark -i \\Device\\NPF_{330F3553-1DDF-4852-8CA8-86ECC4276E88} -f arp -a duration:30 -w "+pcap+" -F pcap -T fields -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4 > /dev/null")
    cmd = subprocess.run("tshark -i \\Device\\NPF_{330F3553-1DDF-4852-8CA8-86ECC4276E88} -f arp -a duration:120 -w "+pcap+" -F pcap -T fields -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4", capture_output=True)
    print('Proses Capturing Selesai.')

def PcapConversion():
    print('Memulai Proses Konversi .pcap > .csv...')
    #cmd = subprocess.run("tshark -r "+pcap+" -T fields -E separator=, -E header=y -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4 > "+csv")
    os.system("tshark -r "+pcap+" -T fields -E separator=, -E header=y -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4 > "+csv)
    print('Proses Konversi Selesai')

def Visualization():
    print('Memulai Visualisasi...')
    df = pd.read_csv(csv, delimiter = ',')
    with open(csv, "r") as f:
        next(f, '')
        G = nx.parse_edgelist(f.readlines(), delimiter=",") 
        df['weight'] = df.groupby(['arp.src.proto_ipv4', 'arp.dst.proto_ipv4'])['arp.src.proto_ipv4'].transform('size')
        G = nx.from_pandas_edgelist(df, 'arp.src.proto_ipv4', 'arp.dst.proto_ipv4', create_using=nx.DiGraph(), edge_attr='weight')

        deg_centrality = nx.out_degree_centrality(G)
        #deg_centrality = nx.degree_centrality(G)
        #pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
        pos = nx.shell_layout(G)
        cent = np.fromiter(deg_centrality.values(), float)
        sizes = cent / np.max(cent) * 250
        #normalize = mcolors.Normalize(vmin=cent.min(), vmax=cent.max())
        colormap = cm.autumn_r
        labels = [i for i in dict(G.nodes).keys()]
        labels = {i:i for i in dict(G.nodes).keys()}
        edges, weights = zip(*nx.get_edge_attributes(G,'weight').items())
        fig, ax = plt.subplots(figsize=(10,5))
        #scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
        #scalarmappaple.set_array(cent)

        #plt.colorbar(scalarmappaple)
        nx.draw(G, pos, node_size=sizes, node_color=sizes, cmap=colormap, edgelist=edges, edge_color=weights, width=1, edge_cmap=plt.cm.Reds, arrowstyle='-|>')
        #nx.draw(G, pos, node_color=sizes, cmap=colormap, edgelist=edges, edge_color=weights, width=1, edge_cmap=plt.cm.Reds, arrowstyle='-|>')
        _ = nx.draw_networkx_labels(G, pos, labels, font_size=3, ax=ax)
        plt.savefig(image, dpi=300, bbox_inches='tight')
    print('Proses Visualisasi Selesai...')

def CsvConversion():
    print('Memulai Proses Konversi .csv > .dot...')
    with open(csv, 'rb') as inf:
        next(inf, '') #Skip nama kolom
        G = nx.read_edgelist(inf, delimiter=',', nodetype=str, encoding="utf-8")
        nx.nx_pydot.write_dot(G, dot)
    print('Konversi Selesai...')

def TransferFile():
    print('Memulai Proses Unggah File...')
    ftp = FTP("files.000webhost.com")
    ftp.login("mhid","AdioEdio00")
    Output_Directory = "public_html/image/"
    File2Send = image
    file = open(File2Send, "rb")
    ftp.cwd(Output_Directory)
    ftp.storbinary('STOR ' + os.path.basename(File2Send), file) 
    print('Proses Unggah Selesai...')

CaptureData()
PcapConversion()
Visualization()
TransferFile()