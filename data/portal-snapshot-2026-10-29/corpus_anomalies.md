# QPX 语料异常与不确定项

本报告不替多个 QPX 哈希选择代表版本。缺少定量视图不自动等同格式错误。

## HEAD 接口不支持

browse 文件 HEAD 返回 405；GET 的签名目标 HEAD 返回 403。早期失败请求按要求重试两次；后续不对每个文件重复已知无效的 HEAD。
全部大小改用成功 206 响应的 Content-Range 总长度。详见 head_probe.json、corpus_files.csv.size_source。

## 采集启动阶段的并发偏离

早期取消终端后两个采集子进程未退出，曾与当前进程重叠，三个进程各配置 8 worker，未满足全程并发上限 8。
2026-10-30T02:05 UTC 后已识别并终止两个早期进程，只保留一个 8 worker 进程。脚本现加入进程锁，避免重复启动。未改动系统服务或其他任务。

## 没有 QPX 子目录的数据集

数量：52。
- MSV000079033
- MSV000087095
- PDC000111
- PDC000126
- PMID24274931
- PXD002179
- PXD004143
- PXD004691
- PXD004873
- PXD005445
- PXD005736
- PXD006559
- PXD008441
- PXD008467
- PXD008468
- PXD008934
- PXD009219
- PXD010271
- PXD011349
- PXD011839
- PXD012755
- PXD013523
- PXD014194
- PXD014943
- PXD016999
- PXD017052
- PXD017834
- PXD018678
- PXD019123
- PXD019817
- PXD019909
- PXD020727
- PXD022661
- PXD023423
- PXD023650
- PXD025560
- PXD027125
- PXD029009
- PXD030598
- PXD030881
- PXD032212
- PXD032263
- PXD033169
- PXD034244
- PXD036609
- PXD037340
- PXD037682
- PXD038526
- PXD038669
- PXD038674
- PXD039023
- PXD040438

## 多个 QPX 子目录的数据集

数量：19。

### IPX0001804002

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 0e8d80a52200 | [] | ["chengxin","qpx"] | ["1.0.1"] | 233 | 451 | 1426890 | None | None | 8357798087 | dataset,ontology,provenance,psm,run,sample |
| 85e196217f8c | [] | ["chengxin","qpx"] | ["1.0.1"] | 233 | 451 | 1426890 | None | None | 7922524304 | dataset,ontology,provenance,psm,run,sample |

### MSV000085836

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 8e4c044b513d | ["1.1.5"] | ["openms-consensus","qpx"] | ["1.1"] | 460 | 552 | 6194163 | 6194163 | 4843700 | 3191736214 | dataset,feature,ontology,pg,provenance,psm,run,sample |
| a1f8a70ca82d | ["1.1.4"] | ["openms-consensus","qpx"] | ["1.1"] | 460 | 552 | 6375964 | 6375964 | 4891140 | 3239169208 | dataset,feature,ontology,pg,provenance,psm,run,sample |

### PMID23933261

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 173d20caf9ec | ["1.1.4"] | ["openms-consensus","qpx"] | ["1.1"] | 120 | 791 | 6427317 | 2770774 | 324304 | 513973729 | dataset,feature,ontology,pg,provenance,psm,run,sample |
| c1da3b2adbb3 | ["1.1.4"] | ["openms-consensus","qpx"] | ["1.1"] | 9 | 216 | 1414304 | 1161217 | 59130 | 193932764 | dataset,feature,ontology,pg,provenance,psm,run,sample |

### PXD000865

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 4e8f893120ff | [] | ["chengxin","qpx"] | ["1.0.1"] | 34 | 767 | 4990369 | None | None | 3948150844 | dataset,ontology,provenance,psm,run,sample |
| 5e3c1f8ac4cb | [] | ["chengxin","qpx"] | ["1.0.1"] | 12 | 288 | 528554 | None | None | 379555225 | dataset,ontology,provenance,psm,run,sample |
| 64b391b9e5f0 | [] | ["chengxin","qpx"] | ["1.0.1"] | 12 | 288 | 148863 | None | None | 122633626 | dataset,ontology,provenance,psm,run,sample |
| add2e6b6d09e | [] | ["chengxin","qpx"] | ["1.0.1"] | 12 | 288 | 148863 | None | None | 123994549 | dataset,ontology,provenance,psm,run,sample |

### PXD002395

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 8393835554c6 | ["1.1.4"] | ["openms-consensus","qpx"] | ["1.1"] | 33 | 198 | 3430841 | 2560647 | 241791 | 325820035 | dataset,feature,ontology,pg,provenance,psm,run,sample |
| f87700c3dc02 | [] | ["chengxin","qpx"] | ["1.0.1"] | 33 | 198 | 3796341 | None | None | 6406826419 | dataset,ontology,provenance,psm,run,sample |

### PXD004452

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 0630ad88d3d8 | [] | ["chengxin","qpx"] | ["1.0.1"] | 13 | 620 | 5495744 | None | None | 7062133085 | dataset,ontology,provenance,psm,run,sample |
| 37e008c13798 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 39 | 154347 | None | None | 250439686 | dataset,ontology,provenance,psm,run,sample |

### PXD009449

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 22f1c199c7eb | [] | ["chengxin","qpx"] | ["1.0.1"] | 26 | 26 | 201402 | None | None | 1197876904 | dataset,ontology,provenance,psm,run,sample |
| ff35aa00d5b8 | [] | ["chengxin","qpx"] | ["1.0.1"] | 39 | 39 | 697583 | None | None | 1518237294 | dataset,ontology,provenance,psm,run,sample |

### PXD009737

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 2eb11e97949a | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 36 | 347580 | None | None | 769150807 | dataset,ontology,provenance,psm,run,sample |
| 45331c925ca2 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 36 | 428263 | None | None | 979514595 | dataset,ontology,provenance,psm,run,sample |
| 6c54e9cd8136 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 36 | 428263 | None | None | 982989228 | dataset,ontology,provenance,psm,run,sample |
| 71aaf28cc8ba | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 36 | 573439 | None | None | 1560375508 | dataset,ontology,provenance,psm,run,sample |

### PXD010899

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 6b1d29c2c3f2 | [] | ["chengxin","qpx"] | ["1.0.1"] | 26 | 1803 | 1570723 | None | None | 3659976177 | dataset,ontology,provenance,psm,run,sample |
| 75753f784246 | [] | ["chengxin","qpx"] | ["1.0.1"] | 26 | 1803 | 1570723 | None | None | 3673135825 | dataset,ontology,provenance,psm,run,sample |

### PXD012636

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 24099cedae93 | [] | ["chengxin","qpx"] | ["1.0.1"] | 89 | 89 | 1132652 | None | None | 3450352253 | dataset,ontology,provenance,psm,run,sample |
| 7ba1c0f999a7 | [] | ["qpx"] | ["1.0.1"] | 120 | 120 | 741507 | None | None | 1711687684 | dataset,ontology,provenance,psm,run,sample |
| 8bed4e5ecf4d | [] | ["qpx"] | ["1.0.1"] | 120 | 120 | 372148 | None | None | 913441601 | dataset,ontology,provenance,psm,run,sample |
| bcda99599fb4 | [] | ["qpx"] | ["1.0.1"] | 124 | 124 | 111163 | None | None | 270609522 | dataset,ontology,provenance,psm,run,sample |
| cbac7e076dc6 | [] | ["qpx"] | ["1.0.1"] | None | 120 | 1328836 | None | None | 3002377964 | dataset,ontology,provenance,psm,run |
| f2e29e04cfec | [] | ["qpx"] | ["1.0.1"] | 58 | 58 | 98759 | None | None | 204019687 | dataset,ontology,provenance,psm,run,sample |

### PXD014877

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 0079a1a0cddc | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 3608 | None | None | 4749532 | dataset,ontology,provenance,psm,run,sample |
| 05fcb8f8fffd | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 20811 | None | None | 24762269 | dataset,ontology,provenance,psm,run,sample |
| 12842b7a98c7 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 7 | 126526 | None | None | 129798038 | dataset,ontology,provenance,psm,run,sample |
| 16d4ba616103 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 26601 | None | None | 31358406 | dataset,ontology,provenance,psm,run,sample |
| 1d71cf9a83ae | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 7 | 265766 | None | None | 621657583 | dataset,ontology,provenance,psm,run,sample |
| 236ee48e5d00 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 31720 | None | None | 30267648 | dataset,ontology,provenance,psm,run,sample |
| 325d45e1eb37 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 7 | 4310 | None | None | 4736886 | dataset,ontology,provenance,psm,run,sample |
| 3e14de6f60dc | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 31395 | None | None | 23057228 | dataset,ontology,provenance,psm,run,sample |
| 5049d389133f | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 40367 | None | None | 40903938 | dataset,ontology,provenance,psm,run,sample |
| 5b9291f80b08 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 34529 | None | None | 43806058 | dataset,ontology,provenance,psm,run,sample |
| 5fd219bdb167 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 21831 | None | None | 18074474 | dataset,ontology,provenance,psm,run,sample |
| 60276dde84d2 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 11032 | None | None | 12419434 | dataset,ontology,provenance,psm,run,sample |
| 6394a99c8b43 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 7 | 4310 | None | None | 4822424 | dataset,ontology,provenance,psm,run,sample |
| 639c34eccbd3 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 8 | 217125 | None | None | 388125463 | dataset,ontology,provenance,psm,run,sample |
| 667179404f57 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 30734 | None | None | 34423074 | dataset,ontology,provenance,psm,run,sample |
| 69227d2f0923 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 5 | 68644 | None | None | 52422145 | dataset,ontology,provenance,psm,run,sample |
| 7031613618e2 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 54455 | None | None | 83256059 | dataset,ontology,provenance,psm,run,sample |
| 7be8d9598918 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 11032 | None | None | 12719817 | dataset,ontology,provenance,psm,run,sample |
| 7f763f444c61 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 26424 | None | None | 26931652 | dataset,ontology,provenance,psm,run,sample |
| 8292fde0ce8a | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 22013 | None | None | 20639315 | dataset,ontology,provenance,psm,run,sample |
| 84fa58904700 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 17156 | None | None | 11636143 | dataset,ontology,provenance,psm,run,sample |
| aa549478e27e | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 8 | 248653 | None | None | 277281073 | dataset,ontology,provenance,psm,run,sample |
| b37da9c013a7 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 30124 | None | None | 29375007 | dataset,ontology,provenance,psm,run,sample |
| b5b498bbdeb8 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 32736 | None | None | 33370028 | dataset,ontology,provenance,psm,run,sample |
| bd077d4a10cf | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 17139 | None | None | 13063218 | dataset,ontology,provenance,psm,run,sample |
| c3f45bb746d6 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 1926 | None | None | 2033544 | dataset,ontology,provenance,psm,run,sample |
| c6cc08263c39 | [] | ["chengxin","qpx"] | ["1.0.1"] | 4 | 11 | 185361 | None | None | 159750787 | dataset,ontology,provenance,psm,run,sample |
| c933f3cf414f | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 8 | 294035 | None | None | 454459029 | dataset,ontology,provenance,psm,run,sample |
| c9bba9d82c4e | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 7 | 267991 | None | None | 434047246 | dataset,ontology,provenance,psm,run,sample |
| ce4624e887a2 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 7 | 340169 | None | None | 520912178 | dataset,ontology,provenance,psm,run,sample |
| cf3a19e0813b | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 51628 | None | None | 100933877 | dataset,ontology,provenance,psm,run,sample |
| d46c60994357 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 28061 | None | None | 27649086 | dataset,ontology,provenance,psm,run,sample |
| dcae5aa6734b | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 7 | 203696 | None | None | 177278796 | dataset,ontology,provenance,psm,run,sample |
| e0d4174d1dfc | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 27689 | None | None | 34853652 | dataset,ontology,provenance,psm,run,sample |
| ea474b486b0c | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 3608 | None | None | 4859602 | dataset,ontology,provenance,psm,run,sample |
| ec2d96088881 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 1926 | None | None | 2094538 | dataset,ontology,provenance,psm,run,sample |
| eca3cfc4d136 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 20232 | None | None | 19677158 | dataset,ontology,provenance,psm,run,sample |
| eec763b2b182 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 50460 | None | None | 65658816 | dataset,ontology,provenance,psm,run,sample |
| f0adae9aac96 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 23775 | None | None | 25081721 | dataset,ontology,provenance,psm,run,sample |
| f6b218c74636 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 7 | 78622 | None | None | 81588702 | dataset,ontology,provenance,psm,run,sample |
| ffa252045067 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 39236 | None | None | 41153307 | dataset,ontology,provenance,psm,run,sample |

### PXD017199

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 72ea224b5db7 | ["1.1.4"] | ["diann","qpx"] | ["1.1"] | 200 | 206 | None | 21564723 | 1715098 | 2184027218 | dataset,feature,ontology,pg,provenance,run,sample |
| c29f87a1e559 | ["1.1.4"] | ["diann","qpx"] | ["1.1"] | 191 | 197 | None | 20788230 | 1644966 | 2089750650 | dataset,feature,ontology,pg,provenance,run,sample |

### PXD018830

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 5afa726ca1ad | [] | ["qpx","quantms"] | ["1.0.2"] | 25 | 25 | 963471 | 963471 | 137757 | 79065498 | dataset,feature,ontology,pg,provenance,psm,run,sample |
| cd7751176142 | [] | ["chengxin","qpx"] | ["1.0.1"] | 276 | 276 | 2527193 | None | None | 2169812001 | dataset,ontology,provenance,psm,run,sample |

### PXD019483

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 05b90171c8ea | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 3288 | None | None | 3853844 | dataset,ontology,provenance,psm,run,sample |
| 13632f8ce583 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 2339 | None | None | 4176963 | dataset,ontology,provenance,psm,run,sample |
| 2d1030090289 | [] | ["chengxin","qpx"] | ["1.0.1"] | 2 | 2 | 835 | None | None | 2620444 | dataset,ontology,provenance,psm,run,sample |
| 2fb69fb71518 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 3288 | None | None | 3354878 | dataset,ontology,provenance,psm,run,sample |
| 5579d1e5db33 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 2339 | None | None | 4220564 | dataset,ontology,provenance,psm,run,sample |
| 5978da4231af | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 2 | 1429 | None | None | 3225670 | dataset,ontology,provenance,psm,run,sample |
| 5f28441d1bac | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 819 | None | None | 2472227 | dataset,ontology,provenance,psm,run,sample |
| a3578f6d9889 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 819 | None | None | 2452968 | dataset,ontology,provenance,psm,run,sample |
| b4001cf5b39c | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 1 | 151 | None | None | 517603 | dataset,ontology,provenance,psm,run,sample |
| b42d35fa09ac | [] | ["chengxin","qpx"] | ["1.0.1"] | 2 | 2 | 835 | None | None | 2526498 | dataset,ontology,provenance,psm,run,sample |
| db89baf48a68 | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 2 | 1429 | None | None | 3152040 | dataset,ontology,provenance,psm,run,sample |
| e5461f0f5e96 | [] | ["chengxin","qpx"] | ["1.0.1"] | 14 | 112 | 4001686 | None | None | 5705224127 | dataset,ontology,provenance,psm,run,sample |

### PXD022992

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 004371a95fdc | ["1.1.4"] | ["diann","qpx"] | ["1.1"] | 12 | 12 | None | 539604 | 81300 | 72464848 | dataset,feature,ontology,pg,provenance,run,sample |
| 473a6fdbf46d | [] | ["qpx","quantms"] | ["1.0.2"] | 6 | 12 | 1491773 | 1491773 | 114680 | 127990549 | dataset,feature,ontology,pg,provenance,psm,run,sample |

### PXD023508

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 0e3f6a8fa278 | [] | ["qpx","quantms"] | ["1.0.2"] | 80 | 80 | 157506 | 196157 | 21092 | 19727937 | dataset,feature,ontology,pg,provenance,psm,run,sample |
| 105e86a003fb | [] | ["qpx","quantms"] | ["1.0.2"] | 80 | 80 | 157275 | 194877 | 21053 | 19703405 | dataset,feature,ontology,pg,provenance,psm,run,sample |
| 144cb467d946 | [] | ["qpx","quantms"] | ["1.0.2"] | 80 | 80 | 157345 | 195222 | 21057 | 19601771 | dataset,feature,ontology,pg,provenance,psm,run,sample |

### PXD024364

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 635149102abd | [] | ["chengxin","qpx"] | ["1.0.1"] | 1 | 30 | 509429 | None | None | 3136187763 | dataset,ontology,provenance,psm,run,sample |
| 775071de49f6 | [] | ["chengxin","qpx"] | ["1.0.1"] | 9 | 281 | 7120072 | None | None | 41112860993 | dataset,ontology,provenance,psm,run,sample |

### PXD028735

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 1c11af994483 | [] | ["chengxin","qpx"] | ["1.0.1"] | 39 | 39 | 99467 | None | None | 100801026 | dataset,ontology,provenance,psm,run,sample |
| 47cdbb531860 | [] | ["chengxin","qpx"] | ["1.0.1"] | 39 | 39 | 99467 | None | None | 100200480 | dataset,ontology,provenance,psm,run,sample |
| 651462c269cd | [] | ["chengxin","qpx"] | ["1.0.1"] | 80 | 80 | 1511325 | None | None | 2071870380 | dataset,ontology,provenance,psm,run,sample |

### PXD048538

| 哈希 | writer_version | creator | qpx_version | samples | runs | PSM | Feature | PG | bytes | views |
|---|---|---|---|---|---|---|---|---|---|---|
| 41b03dd48c8b | ["1.1.4"] | ["diann","qpx"] | ["1.1"] | 42 | 42 | None | 480976 | 126871 | 57387567 | dataset,feature,ontology,pg,provenance,run,sample |
| e60b9e9aa4c8 | ["1.1.4"] | ["diann","qpx"] | ["1.1"] | 42 | 42 | None | 3559027 | 301173 | 384706532 | dataset,feature,ontology,pg,provenance,run,sample |

## 逐目录缺少的视图

下表穷举已知视图的缺失情况。这是覆盖清单，不表示 site/proteoform 等可选视图必须存在。

| 数据集/哈希 | 缺少的元数据视图 | 缺少的数据视图 |
|---|---|---|
| HuiYan-E480/c6a0b932f37f |  | feature,mz,pepmap,pg,proteoform,site |
| HuiYanAstralMouse/39e2db14f075 |  | mz,pepmap,pg,proteoform,psm,site |
| IPX0000937001/664c2e4da7e4 |  | feature,mz,pepmap,pg,proteoform,site |
| IPX0000937003/b89d17ae8c62 |  | feature,mz,pepmap,pg,proteoform,site |
| IPX0001289001/92438d55c6e8 |  | feature,mz,pepmap,pg,proteoform,site |
| IPX0001590001/bc04a24cfeb2 |  | feature,mz,pepmap,pg,proteoform,site |
| IPX0001804001/5ef266f7654c |  | feature,mz,pepmap,pg,proteoform,site |
| IPX0001804002/0e8d80a52200 |  | feature,mz,pepmap,pg,proteoform,site |
| IPX0001804002/85e196217f8c |  | feature,mz,pepmap,pg,proteoform,site |
| IPX0002031000/d9555895ba47 |  | feature,mz,pepmap,pg,proteoform,site |
| IPX0004073001/80af31fe2c1f |  | feature,mz,pepmap,pg,proteoform,site |
| MSV000085836/8e4c044b513d |  | mz,pepmap,proteoform,site |
| MSV000085836/a1f8a70ca82d |  | mz,pepmap,proteoform,site |
| PDC000127/e5ff9ac2afbb |  | feature,mz,pepmap,pg,proteoform,site |
| PDC000219/f71256d7465e |  | feature,mz,pepmap,pg,proteoform,site |
| PMID23933261/173d20caf9ec |  | mz,pepmap,proteoform,site |
| PMID23933261/c1da3b2adbb3 |  | mz,pepmap,proteoform,site |
| PXD000561/7db3c391b6bd |  | feature,mz,pepmap,pg,proteoform,site |
| PXD000612/639a01e7a0ae |  | feature,mz,pepmap,pg,proteoform,site |
| PXD000672/2036c2011bce |  | mz,pepmap,proteoform,site |
| PXD000865/4e8f893120ff |  | feature,mz,pepmap,pg,proteoform,site |
| PXD000865/5e3c1f8ac4cb |  | feature,mz,pepmap,pg,proteoform,site |
| PXD000865/64b391b9e5f0 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD000865/add2e6b6d09e |  | feature,mz,pepmap,pg,proteoform,site |
| PXD002137/b0c5382e2661 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD002395/8393835554c6 |  | mz,pepmap,proteoform,site |
| PXD002395/f87700c3dc02 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD002767/a84ef6549a1c |  | feature,mz,pepmap,pg,proteoform,site |
| PXD002854/af4bd4f283d9 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD002899/2b053d0e6ef5 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD003497/eb3cacb68497 |  | mz,pepmap,proteoform,site |
| PXD003539/715c024ccd2e |  | mz,pepmap,proteoform,psm,site |
| PXD003903/4510b70e36f6 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD003947/23f3c6a58576 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD004242/9f9c227d578d |  | feature,mz,pepmap,pg,proteoform,site |
| PXD004452/0630ad88d3d8 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD004452/37e008c13798 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD004683/ca6b5c6f5f9a |  | mz,pepmap,proteoform,site |
| PXD004684/21f8df4db8dc |  | mz,pepmap,proteoform,site |
| PXD004701/d82ee8d4dcac |  | mz,pepmap,proteoform,psm,site |
| PXD004732/da737c110798 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD005526/a4ada00a3100 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD006225/c39c57536766 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD006675/48e09b99db12 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD008333/ce0819a5cc52 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD008722/c9894b9ff502 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD008840/92f495d07775 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD009348/dbafe53ba86a |  | feature,mz,pepmap,pg,proteoform,site |
| PXD009449/22f1c199c7eb |  | feature,mz,pepmap,pg,proteoform,site |
| PXD009449/ff35aa00d5b8 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD009737/2eb11e97949a |  | feature,mz,pepmap,pg,proteoform,site |
| PXD009737/45331c925ca2 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD009737/6c54e9cd8136 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD009737/71aaf28cc8ba |  | feature,mz,pepmap,pg,proteoform,site |
| PXD010154/cfdbe6ad96ad |  | feature,mz,pepmap,pg,proteoform,site |
| PXD010429/d380bb98c7d4 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD010595/5d2e0553047a |  | feature,mz,pepmap,pg,proteoform,site |
| PXD010899/6b1d29c2c3f2 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD010899/75753f784246 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD010957/e8719722d723 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD011896/a516cc54b8d0 |  | mz,pepmap,proteoform,site |
| PXD012131/d553c5a3cc6a |  | feature,mz,pepmap,pg,proteoform,site |
| PXD012174/9a3c69313ff0 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD012574/82f1b1b2f7de |  | mz,pepmap,proteoform,site |
| PXD012636/24099cedae93 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD012636/7ba1c0f999a7 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD012636/8bed4e5ecf4d |  | feature,mz,pepmap,pg,proteoform,site |
| PXD012636/bcda99599fb4 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD012636/cbac7e076dc6 | sample | feature,mz,pepmap,pg,proteoform,site |
| PXD012636/f2e29e04cfec |  | feature,mz,pepmap,pg,proteoform,site |
| PXD013231/ba2e08eae4e1 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD013658/efb28af0a92c |  | mz,pepmap,proteoform,psm,site |
| PXD013868/3dd0d4bbb5a3 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014145/a4974c318c8f |  | mz,pepmap,proteoform,site |
| PXD014414/9688c6886714 |  | mz,pepmap,proteoform,site |
| PXD014525/1d3f20844724 |  | mz,pepmap,proteoform,psm,site |
| PXD014877/0079a1a0cddc |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/05fcb8f8fffd |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/12842b7a98c7 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/16d4ba616103 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/1d71cf9a83ae |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/236ee48e5d00 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/325d45e1eb37 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/3e14de6f60dc |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/5049d389133f |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/5b9291f80b08 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/5fd219bdb167 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/60276dde84d2 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/6394a99c8b43 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/639c34eccbd3 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/667179404f57 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/69227d2f0923 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/7031613618e2 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/7be8d9598918 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/7f763f444c61 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/8292fde0ce8a |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/84fa58904700 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/aa549478e27e |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/b37da9c013a7 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/b5b498bbdeb8 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/bd077d4a10cf |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/c3f45bb746d6 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/c6cc08263c39 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/c933f3cf414f |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/c9bba9d82c4e |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/ce4624e887a2 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/cf3a19e0813b |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/d46c60994357 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/dcae5aa6734b |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/e0d4174d1dfc |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/ea474b486b0c |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/ec2d96088881 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/eca3cfc4d136 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/eec763b2b182 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/f0adae9aac96 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/f6b218c74636 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD014877/ffa252045067 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD016986/7c8762959c63 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD017199/72ea224b5db7 |  | mz,pepmap,proteoform,psm,site |
| PXD017199/c29f87a1e559 |  | mz,pepmap,proteoform,psm,site |
| PXD018450/7282e25039e0 |  | mz,pepmap,proteoform,site |
| PXD018830/5afa726ca1ad |  | mz,pepmap,proteoform,site |
| PXD018830/cd7751176142 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD019483/05b90171c8ea |  | feature,mz,pepmap,pg,proteoform,site |
| PXD019483/13632f8ce583 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD019483/2d1030090289 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD019483/2fb69fb71518 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD019483/5579d1e5db33 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD019483/5978da4231af |  | feature,mz,pepmap,pg,proteoform,site |
| PXD019483/5f28441d1bac |  | feature,mz,pepmap,pg,proteoform,site |
| PXD019483/a3578f6d9889 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD019483/b4001cf5b39c |  | feature,mz,pepmap,pg,proteoform,site |
| PXD019483/b42d35fa09ac |  | feature,mz,pepmap,pg,proteoform,site |
| PXD019483/db89baf48a68 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD019483/e5461f0f5e96 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD019643/46da54d6e3e9 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD020109/4d8132335b73 |  | mz,pepmap,proteoform,site |
| PXD020192/5d4b06811efd |  | feature,mz,pepmap,pg,proteoform,site |
| PXD020248/83ab638d361d |  | mz,pepmap,proteoform,site |
| PXD021013/1ed4852abc60 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD021394/8a6a14abdcee |  | mz,pepmap,proteoform,site |
| PXD022469/ff99b3326179 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD022992/004371a95fdc |  | mz,pepmap,proteoform,psm,site |
| PXD022992/473a6fdbf46d |  | mz,pepmap,proteoform,site |
| PXD023508/0e3f6a8fa278 |  | mz,pepmap,proteoform,site |
| PXD023508/105e86a003fb |  | mz,pepmap,proteoform,site |
| PXD023508/144cb467d946 |  | mz,pepmap,proteoform,site |
| PXD023662/4bd01d820826 |  | mz,pepmap,proteoform,site |
| PXD024364/635149102abd |  | feature,mz,pepmap,pg,proteoform,site |
| PXD024364/775071de49f6 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD024742/7117bf6e49cf |  | mz,pepmap,proteoform,psm,site |
| PXD025864/f79dd7dee87c |  | mz,pepmap,proteoform,site |
| PXD027008/0db5a150c55e |  | mz,pepmap,proteoform,site |
| PXD027817/276af406f3a2 |  | mz,pepmap,proteoform,site |
| PXD028251/556541954ff6 |  | mz,pepmap,proteoform,site |
| PXD028618/5d414a029db0 |  | mz,pepmap,proteoform,site |
| PXD028735/1c11af994483 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD028735/47cdbb531860 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD028735/651462c269cd |  | feature,mz,pepmap,pg,proteoform,site |
| PXD030304/fb6d543960a7 |  | mz,pepmap,proteoform,psm,site |
| PXD030348/06fcf0657451 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD030671/c5de547b2f93 |  | mz,pepmap,proteoform,site |
| PXD030983/d5db60f4d306 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD034656/63f22f75171a |  | feature,mz,pepmap,pg,proteoform,site |
| PXD036643/6fc2220a9134 |  | mz,pepmap,proteoform,site |
| PXD036826/11181fff63d2 |  | mz,pepmap,proteoform,psm,site |
| PXD040266/261169dfab06 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD041047/9c3873d590d7 |  | mz,pepmap,proteoform,psm,site |
| PXD041268/4da5d1c864c0 |  | feature,mz,pepmap,pg,proteoform,site |
| PXD041421/aff39c0adcec |  | mz,pepmap,proteoform,psm,site |
| PXD042233/9d3045d63b19 |  | mz,pepmap,proteoform,site |
| PXD046290/bf08b403513f |  | mz,pepmap,proteoform,psm,site |
| PXD046320/be118036d98e |  | mz,pepmap,proteoform,psm,site |
| PXD048538/41b03dd48c8b |  | mz,pepmap,proteoform,psm,site |
| PXD048538/e60b9e9aa4c8 |  | mz,pepmap,proteoform,psm,site |
| PXD052856/1fefbb7618e7 |  | mz,pepmap,proteoform,psm,site |
| PXD054415/05757be280ee |  | mz,pepmap,proteoform,psm,site |
| PXD058009/c0defd8c2d4f |  | mz,pepmap,proteoform,psm,site |
| PXD062529/a2f209c499ec |  | feature,mz,pepmap,pg,proteoform,site |
| PXD070780/20445ebcb175 |  | mz,pepmap,proteoform,psm,site |
| PXD071155/a1520a92f6e9 |  | mz,pepmap,proteoform,psm,site |

## 读取失败

最终文件级失败：0。

| URL | 错误类型 | 错误 |
|---|---|---|

目录索引异常：
```json
[]
```

## 逐目录字段缺失和空值

| 数据集/哈希 | 视图 | 字段 | 状态 |
|---|---|---|---|
| HuiYan-E480/c6a0b932f37f | run | acquisition_method | missing_column |
| HuiYan-E480/c6a0b932f37f | sample | cell_line | missing_column |
| HuiYan-E480/c6a0b932f37f | sample | disease | missing_column |
| HuiYan-E480/c6a0b932f37f | dataset | project_title | all_null |
| HuiYan-E480/c6a0b932f37f | dataset | project_description | all_null |
| HuiYan-E480/c6a0b932f37f | dataset | pubmed_id | all_null |
| HuiYan-E480/c6a0b932f37f | dataset | software_version | all_null |
| HuiYanAstralMouse/39e2db14f075 | sample | cell_type | all_null |
| HuiYanAstralMouse/39e2db14f075 | sample | cell_line | all_null |
| HuiYanAstralMouse/39e2db14f075 | dataset | project_title | all_null |
| HuiYanAstralMouse/39e2db14f075 | dataset | project_description | all_null |
| HuiYanAstralMouse/39e2db14f075 | dataset | pubmed_id | all_null |
| HuiYanAstralMouse/39e2db14f075 | dataset | software_version | all_null |
| IPX0000937001/664c2e4da7e4 | run | acquisition_method | missing_column |
| IPX0000937001/664c2e4da7e4 | sample | cell_type | missing_column |
| IPX0000937001/664c2e4da7e4 | sample | cell_line | missing_column |
| IPX0000937001/664c2e4da7e4 | sample | disease | missing_column |
| IPX0000937001/664c2e4da7e4 | dataset | project_title | all_null |
| IPX0000937001/664c2e4da7e4 | dataset | project_description | all_null |
| IPX0000937001/664c2e4da7e4 | dataset | pubmed_id | all_null |
| IPX0000937001/664c2e4da7e4 | dataset | software_version | all_null |
| IPX0000937003/b89d17ae8c62 | run | acquisition_method | missing_column |
| IPX0000937003/b89d17ae8c62 | sample | cell_type | missing_column |
| IPX0000937003/b89d17ae8c62 | sample | cell_line | missing_column |
| IPX0000937003/b89d17ae8c62 | sample | disease | missing_column |
| IPX0000937003/b89d17ae8c62 | dataset | project_title | all_null |
| IPX0000937003/b89d17ae8c62 | dataset | project_description | all_null |
| IPX0000937003/b89d17ae8c62 | dataset | pubmed_id | all_null |
| IPX0000937003/b89d17ae8c62 | dataset | software_version | all_null |
| IPX0001289001/92438d55c6e8 | run | acquisition_method | missing_column |
| IPX0001289001/92438d55c6e8 | sample | cell_type | missing_column |
| IPX0001289001/92438d55c6e8 | sample | cell_line | missing_column |
| IPX0001289001/92438d55c6e8 | sample | disease | missing_column |
| IPX0001289001/92438d55c6e8 | dataset | project_title | all_null |
| IPX0001289001/92438d55c6e8 | dataset | project_description | all_null |
| IPX0001289001/92438d55c6e8 | dataset | pubmed_id | all_null |
| IPX0001289001/92438d55c6e8 | dataset | software_version | all_null |
| IPX0001590001/bc04a24cfeb2 | run | acquisition_method | missing_column |
| IPX0001590001/bc04a24cfeb2 | sample | cell_type | missing_column |
| IPX0001590001/bc04a24cfeb2 | sample | cell_line | missing_column |
| IPX0001590001/bc04a24cfeb2 | sample | disease | missing_column |
| IPX0001590001/bc04a24cfeb2 | dataset | project_title | all_null |
| IPX0001590001/bc04a24cfeb2 | dataset | project_description | all_null |
| IPX0001590001/bc04a24cfeb2 | dataset | pubmed_id | all_null |
| IPX0001590001/bc04a24cfeb2 | dataset | software_version | all_null |
| IPX0001804001/5ef266f7654c | run | acquisition_method | missing_column |
| IPX0001804001/5ef266f7654c | sample | cell_type | missing_column |
| IPX0001804001/5ef266f7654c | sample | cell_line | missing_column |
| IPX0001804001/5ef266f7654c | sample | disease | missing_column |
| IPX0001804001/5ef266f7654c | dataset | project_title | all_null |
| IPX0001804001/5ef266f7654c | dataset | project_description | all_null |
| IPX0001804001/5ef266f7654c | dataset | pubmed_id | all_null |
| IPX0001804001/5ef266f7654c | dataset | software_version | all_null |
| IPX0001804002/0e8d80a52200 | run | acquisition_method | missing_column |
| IPX0001804002/0e8d80a52200 | sample | cell_type | missing_column |
| IPX0001804002/0e8d80a52200 | sample | cell_line | missing_column |
| IPX0001804002/0e8d80a52200 | sample | disease | missing_column |
| IPX0001804002/0e8d80a52200 | dataset | project_title | all_null |
| IPX0001804002/0e8d80a52200 | dataset | project_description | all_null |
| IPX0001804002/0e8d80a52200 | dataset | pubmed_id | all_null |
| IPX0001804002/85e196217f8c | run | acquisition_method | missing_column |
| IPX0001804002/85e196217f8c | sample | cell_type | missing_column |
| IPX0001804002/85e196217f8c | sample | cell_line | missing_column |
| IPX0001804002/85e196217f8c | sample | disease | missing_column |
| IPX0001804002/85e196217f8c | dataset | project_title | all_null |
| IPX0001804002/85e196217f8c | dataset | project_description | all_null |
| IPX0001804002/85e196217f8c | dataset | pubmed_id | all_null |
| IPX0002031000/d9555895ba47 | run | acquisition_method | missing_column |
| IPX0002031000/d9555895ba47 | sample | cell_type | missing_column |
| IPX0002031000/d9555895ba47 | sample | cell_line | missing_column |
| IPX0002031000/d9555895ba47 | sample | disease | missing_column |
| IPX0002031000/d9555895ba47 | dataset | project_title | all_null |
| IPX0002031000/d9555895ba47 | dataset | project_description | all_null |
| IPX0002031000/d9555895ba47 | dataset | pubmed_id | all_null |
| IPX0004073001/80af31fe2c1f | run | acquisition_method | missing_column |
| IPX0004073001/80af31fe2c1f | sample | cell_type | missing_column |
| IPX0004073001/80af31fe2c1f | sample | cell_line | missing_column |
| IPX0004073001/80af31fe2c1f | sample | disease | missing_column |
| IPX0004073001/80af31fe2c1f | dataset | project_title | all_null |
| IPX0004073001/80af31fe2c1f | dataset | project_description | all_null |
| IPX0004073001/80af31fe2c1f | dataset | pubmed_id | all_null |
| MSV000085836/8e4c044b513d | sample | cell_type | all_null |
| MSV000085836/8e4c044b513d | dataset | project_title | all_null |
| MSV000085836/8e4c044b513d | dataset | project_description | all_null |
| MSV000085836/8e4c044b513d | dataset | pubmed_id | all_null |
| MSV000085836/8e4c044b513d | dataset | software_version | all_null |
| MSV000085836/a1f8a70ca82d | run | dissociation_method | all_null |
| MSV000085836/a1f8a70ca82d | dataset | project_title | all_null |
| MSV000085836/a1f8a70ca82d | dataset | project_description | all_null |
| MSV000085836/a1f8a70ca82d | dataset | pubmed_id | all_null |
| MSV000085836/a1f8a70ca82d | dataset | software_version | all_null |
| PDC000127/e5ff9ac2afbb | run | acquisition_method | missing_column |
| PDC000127/e5ff9ac2afbb | sample | cell_type | missing_column |
| PDC000127/e5ff9ac2afbb | sample | cell_line | missing_column |
| PDC000127/e5ff9ac2afbb | dataset | project_title | all_null |
| PDC000127/e5ff9ac2afbb | dataset | project_description | all_null |
| PDC000127/e5ff9ac2afbb | dataset | pubmed_id | all_null |
| PDC000219/f71256d7465e | run | acquisition_method | missing_column |
| PDC000219/f71256d7465e | sample | cell_type | missing_column |
| PDC000219/f71256d7465e | sample | cell_line | missing_column |
| PDC000219/f71256d7465e | dataset | project_title | all_null |
| PDC000219/f71256d7465e | dataset | project_description | all_null |
| PDC000219/f71256d7465e | dataset | pubmed_id | all_null |
| PMID23933261/173d20caf9ec | dataset | project_title | all_null |
| PMID23933261/173d20caf9ec | dataset | project_description | all_null |
| PMID23933261/173d20caf9ec | dataset | pubmed_id | all_null |
| PMID23933261/173d20caf9ec | dataset | software_version | all_null |
| PMID23933261/c1da3b2adbb3 | dataset | project_title | all_null |
| PMID23933261/c1da3b2adbb3 | dataset | project_description | all_null |
| PMID23933261/c1da3b2adbb3 | dataset | pubmed_id | all_null |
| PMID23933261/c1da3b2adbb3 | dataset | software_version | all_null |
| PXD000561/7db3c391b6bd | run | acquisition_method | missing_column |
| PXD000561/7db3c391b6bd | sample | cell_type | missing_column |
| PXD000561/7db3c391b6bd | sample | cell_line | missing_column |
| PXD000561/7db3c391b6bd | sample | disease | missing_column |
| PXD000561/7db3c391b6bd | dataset | project_title | all_null |
| PXD000561/7db3c391b6bd | dataset | project_description | all_null |
| PXD000561/7db3c391b6bd | dataset | pubmed_id | all_null |
| PXD000612/639a01e7a0ae | run | acquisition_method | missing_column |
| PXD000612/639a01e7a0ae | dataset | project_title | all_null |
| PXD000612/639a01e7a0ae | dataset | project_description | all_null |
| PXD000612/639a01e7a0ae | dataset | pubmed_id | all_null |
| PXD000672/2036c2011bce | run | acquisition_method | missing_column |
| PXD000672/2036c2011bce | run | dissociation_method | all_null |
| PXD000672/2036c2011bce | sample | cell_type | all_null |
| PXD000672/2036c2011bce | sample | cell_line | all_null |
| PXD000672/2036c2011bce | dataset | project_title | all_null |
| PXD000672/2036c2011bce | dataset | project_description | all_null |
| PXD000672/2036c2011bce | dataset | pubmed_id | all_null |
| PXD000865/4e8f893120ff | run | acquisition_method | missing_column |
| PXD000865/4e8f893120ff | sample | cell_type | missing_column |
| PXD000865/4e8f893120ff | sample | cell_line | missing_column |
| PXD000865/4e8f893120ff | dataset | project_title | all_null |
| PXD000865/4e8f893120ff | dataset | project_description | all_null |
| PXD000865/4e8f893120ff | dataset | pubmed_id | all_null |
| PXD000865/5e3c1f8ac4cb | run | acquisition_method | missing_column |
| PXD000865/5e3c1f8ac4cb | sample | cell_type | missing_column |
| PXD000865/5e3c1f8ac4cb | sample | cell_line | missing_column |
| PXD000865/5e3c1f8ac4cb | dataset | project_title | all_null |
| PXD000865/5e3c1f8ac4cb | dataset | project_description | all_null |
| PXD000865/5e3c1f8ac4cb | dataset | pubmed_id | all_null |
| PXD000865/64b391b9e5f0 | run | acquisition_method | missing_column |
| PXD000865/64b391b9e5f0 | sample | cell_type | missing_column |
| PXD000865/64b391b9e5f0 | sample | cell_line | missing_column |
| PXD000865/64b391b9e5f0 | dataset | project_title | all_null |
| PXD000865/64b391b9e5f0 | dataset | project_description | all_null |
| PXD000865/64b391b9e5f0 | dataset | pubmed_id | all_null |
| PXD000865/add2e6b6d09e | run | acquisition_method | missing_column |
| PXD000865/add2e6b6d09e | sample | cell_type | missing_column |
| PXD000865/add2e6b6d09e | sample | cell_line | missing_column |
| PXD000865/add2e6b6d09e | dataset | project_title | all_null |
| PXD000865/add2e6b6d09e | dataset | project_description | all_null |
| PXD000865/add2e6b6d09e | dataset | pubmed_id | all_null |
| PXD002137/b0c5382e2661 | run | acquisition_method | missing_column |
| PXD002137/b0c5382e2661 | sample | cell_type | missing_column |
| PXD002137/b0c5382e2661 | dataset | project_title | all_null |
| PXD002137/b0c5382e2661 | dataset | project_description | all_null |
| PXD002137/b0c5382e2661 | dataset | pubmed_id | all_null |
| PXD002395/8393835554c6 | dataset | project_title | all_null |
| PXD002395/8393835554c6 | dataset | project_description | all_null |
| PXD002395/8393835554c6 | dataset | pubmed_id | all_null |
| PXD002395/8393835554c6 | dataset | software_version | all_null |
| PXD002395/f87700c3dc02 | run | acquisition_method | missing_column |
| PXD002395/f87700c3dc02 | dataset | project_title | all_null |
| PXD002395/f87700c3dc02 | dataset | project_description | all_null |
| PXD002395/f87700c3dc02 | dataset | pubmed_id | all_null |
| PXD002767/a84ef6549a1c | run | acquisition_method | missing_column |
| PXD002767/a84ef6549a1c | sample | cell_type | missing_column |
| PXD002767/a84ef6549a1c | sample | cell_line | missing_column |
| PXD002767/a84ef6549a1c | sample | disease | missing_column |
| PXD002767/a84ef6549a1c | dataset | project_title | all_null |
| PXD002767/a84ef6549a1c | dataset | project_description | all_null |
| PXD002767/a84ef6549a1c | dataset | pubmed_id | all_null |
| PXD002854/af4bd4f283d9 | run | acquisition_method | missing_column |
| PXD002854/af4bd4f283d9 | run | dissociation_method | all_null |
| PXD002854/af4bd4f283d9 | sample | cell_line | missing_column |
| PXD002854/af4bd4f283d9 | dataset | project_title | all_null |
| PXD002854/af4bd4f283d9 | dataset | project_description | all_null |
| PXD002854/af4bd4f283d9 | dataset | pubmed_id | all_null |
| PXD002899/2b053d0e6ef5 | run | acquisition_method | missing_column |
| PXD002899/2b053d0e6ef5 | sample | cell_type | missing_column |
| PXD002899/2b053d0e6ef5 | sample | cell_line | missing_column |
| PXD002899/2b053d0e6ef5 | sample | disease | missing_column |
| PXD002899/2b053d0e6ef5 | dataset | project_title | all_null |
| PXD002899/2b053d0e6ef5 | dataset | project_description | all_null |
| PXD002899/2b053d0e6ef5 | dataset | pubmed_id | all_null |
| PXD003497/eb3cacb68497 | run | acquisition_method | missing_column |
| PXD003497/eb3cacb68497 | run | dissociation_method | all_null |
| PXD003497/eb3cacb68497 | sample | cell_type | all_null |
| PXD003497/eb3cacb68497 | sample | cell_line | all_null |
| PXD003497/eb3cacb68497 | dataset | project_title | all_null |
| PXD003497/eb3cacb68497 | dataset | project_description | all_null |
| PXD003497/eb3cacb68497 | dataset | pubmed_id | all_null |
| PXD003539/715c024ccd2e | dataset | project_title | all_null |
| PXD003539/715c024ccd2e | dataset | project_description | all_null |
| PXD003539/715c024ccd2e | dataset | pubmed_id | all_null |
| PXD003539/715c024ccd2e | dataset | software_version | all_null |
| PXD003903/4510b70e36f6 | run | acquisition_method | missing_column |
| PXD003903/4510b70e36f6 | sample | cell_type | missing_column |
| PXD003903/4510b70e36f6 | sample | cell_line | missing_column |
| PXD003903/4510b70e36f6 | sample | disease | missing_column |
| PXD003903/4510b70e36f6 | dataset | project_title | all_null |
| PXD003903/4510b70e36f6 | dataset | project_description | all_null |
| PXD003903/4510b70e36f6 | dataset | pubmed_id | all_null |
| PXD003947/23f3c6a58576 | run | acquisition_method | missing_column |
| PXD003947/23f3c6a58576 | sample | cell_type | missing_column |
| PXD003947/23f3c6a58576 | sample | cell_line | missing_column |
| PXD003947/23f3c6a58576 | dataset | project_title | all_null |
| PXD003947/23f3c6a58576 | dataset | project_description | all_null |
| PXD003947/23f3c6a58576 | dataset | pubmed_id | all_null |
| PXD004242/9f9c227d578d | run | acquisition_method | missing_column |
| PXD004242/9f9c227d578d | sample | cell_type | missing_column |
| PXD004242/9f9c227d578d | sample | cell_line | missing_column |
| PXD004242/9f9c227d578d | dataset | project_title | all_null |
| PXD004242/9f9c227d578d | dataset | project_description | all_null |
| PXD004242/9f9c227d578d | dataset | pubmed_id | all_null |
| PXD004452/0630ad88d3d8 | run | acquisition_method | missing_column |
| PXD004452/0630ad88d3d8 | dataset | project_title | all_null |
| PXD004452/0630ad88d3d8 | dataset | project_description | all_null |
| PXD004452/0630ad88d3d8 | dataset | pubmed_id | all_null |
| PXD004452/37e008c13798 | run | acquisition_method | missing_column |
| PXD004452/37e008c13798 | sample | disease | missing_column |
| PXD004452/37e008c13798 | dataset | project_title | all_null |
| PXD004452/37e008c13798 | dataset | project_description | all_null |
| PXD004452/37e008c13798 | dataset | pubmed_id | all_null |
| PXD004683/ca6b5c6f5f9a | run | acquisition_method | missing_column |
| PXD004683/ca6b5c6f5f9a | sample | cell_type | all_null |
| PXD004683/ca6b5c6f5f9a | sample | cell_line | all_null |
| PXD004683/ca6b5c6f5f9a | dataset | project_title | all_null |
| PXD004683/ca6b5c6f5f9a | dataset | project_description | all_null |
| PXD004683/ca6b5c6f5f9a | dataset | pubmed_id | all_null |
| PXD004684/21f8df4db8dc | run | acquisition_method | missing_column |
| PXD004684/21f8df4db8dc | run | dissociation_method | all_null |
| PXD004684/21f8df4db8dc | sample | cell_type | all_null |
| PXD004684/21f8df4db8dc | sample | cell_line | all_null |
| PXD004684/21f8df4db8dc | dataset | project_title | all_null |
| PXD004684/21f8df4db8dc | dataset | project_description | all_null |
| PXD004684/21f8df4db8dc | dataset | pubmed_id | all_null |
| PXD004701/d82ee8d4dcac | dataset | project_title | all_null |
| PXD004701/d82ee8d4dcac | dataset | project_description | all_null |
| PXD004701/d82ee8d4dcac | dataset | pubmed_id | all_null |
| PXD004701/d82ee8d4dcac | dataset | software_version | all_null |
| PXD004732/da737c110798 | run | acquisition_method | missing_column |
| PXD004732/da737c110798 | sample | cell_type | missing_column |
| PXD004732/da737c110798 | sample | cell_line | missing_column |
| PXD004732/da737c110798 | sample | disease | missing_column |
| PXD004732/da737c110798 | dataset | project_title | all_null |
| PXD004732/da737c110798 | dataset | project_description | all_null |
| PXD004732/da737c110798 | dataset | pubmed_id | all_null |
| PXD005526/a4ada00a3100 | run | acquisition_method | missing_column |
| PXD005526/a4ada00a3100 | sample | cell_type | missing_column |
| PXD005526/a4ada00a3100 | sample | cell_line | missing_column |
| PXD005526/a4ada00a3100 | sample | disease | missing_column |
| PXD005526/a4ada00a3100 | dataset | project_title | all_null |
| PXD005526/a4ada00a3100 | dataset | project_description | all_null |
| PXD005526/a4ada00a3100 | dataset | pubmed_id | all_null |
| PXD006225/c39c57536766 | run | acquisition_method | missing_column |
| PXD006225/c39c57536766 | sample | cell_type | missing_column |
| PXD006225/c39c57536766 | sample | cell_line | missing_column |
| PXD006225/c39c57536766 | sample | disease | missing_column |
| PXD006225/c39c57536766 | dataset | project_title | all_null |
| PXD006225/c39c57536766 | dataset | project_description | all_null |
| PXD006225/c39c57536766 | dataset | pubmed_id | all_null |
| PXD006675/48e09b99db12 | run | acquisition_method | missing_column |
| PXD006675/48e09b99db12 | run | dissociation_method | all_null |
| PXD006675/48e09b99db12 | sample | cell_line | missing_column |
| PXD006675/48e09b99db12 | dataset | project_title | all_null |
| PXD006675/48e09b99db12 | dataset | project_description | all_null |
| PXD006675/48e09b99db12 | dataset | pubmed_id | all_null |
| PXD008333/ce0819a5cc52 | run | acquisition_method | missing_column |
| PXD008333/ce0819a5cc52 | sample | cell_line | missing_column |
| PXD008333/ce0819a5cc52 | sample | disease | missing_column |
| PXD008333/ce0819a5cc52 | dataset | project_title | all_null |
| PXD008333/ce0819a5cc52 | dataset | project_description | all_null |
| PXD008333/ce0819a5cc52 | dataset | pubmed_id | all_null |
| PXD008722/c9894b9ff502 | run | acquisition_method | missing_column |
| PXD008722/c9894b9ff502 | run | dissociation_method | all_null |
| PXD008722/c9894b9ff502 | sample | cell_line | missing_column |
| PXD008722/c9894b9ff502 | dataset | project_title | all_null |
| PXD008722/c9894b9ff502 | dataset | project_description | all_null |
| PXD008722/c9894b9ff502 | dataset | pubmed_id | all_null |
| PXD008840/92f495d07775 | run | acquisition_method | missing_column |
| PXD008840/92f495d07775 | sample | cell_type | missing_column |
| PXD008840/92f495d07775 | sample | cell_line | missing_column |
| PXD008840/92f495d07775 | dataset | project_title | all_null |
| PXD008840/92f495d07775 | dataset | project_description | all_null |
| PXD008840/92f495d07775 | dataset | pubmed_id | all_null |
| PXD009348/dbafe53ba86a | run | acquisition_method | missing_column |
| PXD009348/dbafe53ba86a | run | dissociation_method | all_null |
| PXD009348/dbafe53ba86a | sample | cell_type | missing_column |
| PXD009348/dbafe53ba86a | sample | cell_line | missing_column |
| PXD009348/dbafe53ba86a | sample | disease | missing_column |
| PXD009348/dbafe53ba86a | dataset | project_title | all_null |
| PXD009348/dbafe53ba86a | dataset | project_description | all_null |
| PXD009348/dbafe53ba86a | dataset | pubmed_id | all_null |
| PXD009449/22f1c199c7eb | run | acquisition_method | missing_column |
| PXD009449/22f1c199c7eb | sample | cell_type | missing_column |
| PXD009449/22f1c199c7eb | sample | cell_line | missing_column |
| PXD009449/22f1c199c7eb | sample | disease | missing_column |
| PXD009449/22f1c199c7eb | dataset | project_title | all_null |
| PXD009449/22f1c199c7eb | dataset | project_description | all_null |
| PXD009449/22f1c199c7eb | dataset | pubmed_id | all_null |
| PXD009449/ff35aa00d5b8 | run | acquisition_method | missing_column |
| PXD009449/ff35aa00d5b8 | sample | cell_type | missing_column |
| PXD009449/ff35aa00d5b8 | sample | cell_line | missing_column |
| PXD009449/ff35aa00d5b8 | sample | disease | missing_column |
| PXD009449/ff35aa00d5b8 | dataset | project_title | all_null |
| PXD009449/ff35aa00d5b8 | dataset | project_description | all_null |
| PXD009449/ff35aa00d5b8 | dataset | pubmed_id | all_null |
| PXD009737/2eb11e97949a | run | acquisition_method | missing_column |
| PXD009737/2eb11e97949a | sample | cell_type | missing_column |
| PXD009737/2eb11e97949a | sample | cell_line | missing_column |
| PXD009737/2eb11e97949a | sample | disease | missing_column |
| PXD009737/2eb11e97949a | dataset | project_title | all_null |
| PXD009737/2eb11e97949a | dataset | project_description | all_null |
| PXD009737/2eb11e97949a | dataset | pubmed_id | all_null |
| PXD009737/45331c925ca2 | run | acquisition_method | missing_column |
| PXD009737/45331c925ca2 | sample | cell_type | missing_column |
| PXD009737/45331c925ca2 | sample | cell_line | missing_column |
| PXD009737/45331c925ca2 | sample | disease | missing_column |
| PXD009737/45331c925ca2 | dataset | project_title | all_null |
| PXD009737/45331c925ca2 | dataset | project_description | all_null |
| PXD009737/45331c925ca2 | dataset | pubmed_id | all_null |
| PXD009737/6c54e9cd8136 | run | acquisition_method | missing_column |
| PXD009737/6c54e9cd8136 | sample | cell_type | missing_column |
| PXD009737/6c54e9cd8136 | sample | cell_line | missing_column |
| PXD009737/6c54e9cd8136 | sample | disease | missing_column |
| PXD009737/6c54e9cd8136 | dataset | project_title | all_null |
| PXD009737/6c54e9cd8136 | dataset | project_description | all_null |
| PXD009737/6c54e9cd8136 | dataset | pubmed_id | all_null |
| PXD009737/71aaf28cc8ba | run | acquisition_method | missing_column |
| PXD009737/71aaf28cc8ba | sample | cell_type | missing_column |
| PXD009737/71aaf28cc8ba | sample | cell_line | missing_column |
| PXD009737/71aaf28cc8ba | sample | disease | missing_column |
| PXD009737/71aaf28cc8ba | dataset | project_title | all_null |
| PXD009737/71aaf28cc8ba | dataset | project_description | all_null |
| PXD009737/71aaf28cc8ba | dataset | pubmed_id | all_null |
| PXD010154/cfdbe6ad96ad | run | acquisition_method | missing_column |
| PXD010154/cfdbe6ad96ad | sample | cell_type | missing_column |
| PXD010154/cfdbe6ad96ad | sample | cell_line | missing_column |
| PXD010154/cfdbe6ad96ad | sample | disease | missing_column |
| PXD010154/cfdbe6ad96ad | dataset | project_title | all_null |
| PXD010154/cfdbe6ad96ad | dataset | project_description | all_null |
| PXD010154/cfdbe6ad96ad | dataset | pubmed_id | all_null |
| PXD010429/d380bb98c7d4 | run | acquisition_method | missing_column |
| PXD010429/d380bb98c7d4 | run | dissociation_method | all_null |
| PXD010429/d380bb98c7d4 | sample | cell_type | missing_column |
| PXD010429/d380bb98c7d4 | sample | cell_line | missing_column |
| PXD010429/d380bb98c7d4 | dataset | project_title | all_null |
| PXD010429/d380bb98c7d4 | dataset | project_description | all_null |
| PXD010429/d380bb98c7d4 | dataset | pubmed_id | all_null |
| PXD010595/5d2e0553047a | run | acquisition_method | missing_column |
| PXD010595/5d2e0553047a | sample | cell_type | missing_column |
| PXD010595/5d2e0553047a | sample | cell_line | missing_column |
| PXD010595/5d2e0553047a | sample | disease | missing_column |
| PXD010595/5d2e0553047a | dataset | project_title | all_null |
| PXD010595/5d2e0553047a | dataset | project_description | all_null |
| PXD010595/5d2e0553047a | dataset | pubmed_id | all_null |
| PXD010899/6b1d29c2c3f2 | run | acquisition_method | missing_column |
| PXD010899/6b1d29c2c3f2 | run | dissociation_method | all_null |
| PXD010899/6b1d29c2c3f2 | sample | cell_type | missing_column |
| PXD010899/6b1d29c2c3f2 | sample | cell_line | missing_column |
| PXD010899/6b1d29c2c3f2 | dataset | project_title | all_null |
| PXD010899/6b1d29c2c3f2 | dataset | project_description | all_null |
| PXD010899/6b1d29c2c3f2 | dataset | pubmed_id | all_null |
| PXD010899/75753f784246 | run | acquisition_method | missing_column |
| PXD010899/75753f784246 | run | dissociation_method | all_null |
| PXD010899/75753f784246 | sample | cell_type | missing_column |
| PXD010899/75753f784246 | sample | cell_line | missing_column |
| PXD010899/75753f784246 | dataset | project_title | all_null |
| PXD010899/75753f784246 | dataset | project_description | all_null |
| PXD010899/75753f784246 | dataset | pubmed_id | all_null |
| PXD010957/e8719722d723 | run | acquisition_method | missing_column |
| PXD010957/e8719722d723 | sample | cell_type | missing_column |
| PXD010957/e8719722d723 | sample | cell_line | missing_column |
| PXD010957/e8719722d723 | dataset | project_title | all_null |
| PXD010957/e8719722d723 | dataset | project_description | all_null |
| PXD010957/e8719722d723 | dataset | pubmed_id | all_null |
| PXD011896/a516cc54b8d0 | run | dissociation_method | all_null |
| PXD011896/a516cc54b8d0 | sample | cell_type | all_null |
| PXD011896/a516cc54b8d0 | dataset | project_title | all_null |
| PXD011896/a516cc54b8d0 | dataset | project_description | all_null |
| PXD011896/a516cc54b8d0 | dataset | pubmed_id | all_null |
| PXD011896/a516cc54b8d0 | dataset | software_version | all_null |
| PXD012131/d553c5a3cc6a | run | acquisition_method | missing_column |
| PXD012131/d553c5a3cc6a | run | dissociation_method | all_null |
| PXD012131/d553c5a3cc6a | sample | cell_type | missing_column |
| PXD012131/d553c5a3cc6a | sample | cell_line | missing_column |
| PXD012131/d553c5a3cc6a | dataset | project_title | all_null |
| PXD012131/d553c5a3cc6a | dataset | project_description | all_null |
| PXD012131/d553c5a3cc6a | dataset | pubmed_id | all_null |
| PXD012174/9a3c69313ff0 | run | acquisition_method | missing_column |
| PXD012174/9a3c69313ff0 | sample | cell_type | missing_column |
| PXD012174/9a3c69313ff0 | sample | cell_line | missing_column |
| PXD012174/9a3c69313ff0 | sample | disease | missing_column |
| PXD012174/9a3c69313ff0 | dataset | project_title | all_null |
| PXD012174/9a3c69313ff0 | dataset | project_description | all_null |
| PXD012174/9a3c69313ff0 | dataset | pubmed_id | all_null |
| PXD012574/82f1b1b2f7de | run | acquisition_method | missing_column |
| PXD012574/82f1b1b2f7de | sample | cell_type | all_null |
| PXD012574/82f1b1b2f7de | sample | cell_line | all_null |
| PXD012574/82f1b1b2f7de | dataset | project_title | all_null |
| PXD012574/82f1b1b2f7de | dataset | project_description | all_null |
| PXD012574/82f1b1b2f7de | dataset | pubmed_id | all_null |
| PXD012636/24099cedae93 | run | acquisition_method | missing_column |
| PXD012636/24099cedae93 | run | dissociation_method | all_null |
| PXD012636/24099cedae93 | sample | cell_type | missing_column |
| PXD012636/24099cedae93 | sample | cell_line | missing_column |
| PXD012636/24099cedae93 | sample | disease | missing_column |
| PXD012636/24099cedae93 | dataset | project_title | all_null |
| PXD012636/24099cedae93 | dataset | project_description | all_null |
| PXD012636/24099cedae93 | dataset | pubmed_id | all_null |
| PXD012636/7ba1c0f999a7 | run | acquisition_method | missing_column |
| PXD012636/7ba1c0f999a7 | run | dissociation_method | all_null |
| PXD012636/7ba1c0f999a7 | sample | cell_type | missing_column |
| PXD012636/7ba1c0f999a7 | sample | cell_line | missing_column |
| PXD012636/7ba1c0f999a7 | sample | disease | missing_column |
| PXD012636/7ba1c0f999a7 | dataset | project_title | all_null |
| PXD012636/7ba1c0f999a7 | dataset | project_description | all_null |
| PXD012636/7ba1c0f999a7 | dataset | pubmed_id | all_null |
| PXD012636/8bed4e5ecf4d | run | acquisition_method | missing_column |
| PXD012636/8bed4e5ecf4d | run | dissociation_method | all_null |
| PXD012636/8bed4e5ecf4d | sample | cell_type | missing_column |
| PXD012636/8bed4e5ecf4d | sample | cell_line | missing_column |
| PXD012636/8bed4e5ecf4d | sample | disease | missing_column |
| PXD012636/8bed4e5ecf4d | dataset | project_title | all_null |
| PXD012636/8bed4e5ecf4d | dataset | project_description | all_null |
| PXD012636/8bed4e5ecf4d | dataset | pubmed_id | all_null |
| PXD012636/bcda99599fb4 | run | acquisition_method | missing_column |
| PXD012636/bcda99599fb4 | run | dissociation_method | all_null |
| PXD012636/bcda99599fb4 | sample | cell_type | missing_column |
| PXD012636/bcda99599fb4 | sample | cell_line | missing_column |
| PXD012636/bcda99599fb4 | sample | disease | missing_column |
| PXD012636/bcda99599fb4 | dataset | project_title | all_null |
| PXD012636/bcda99599fb4 | dataset | project_description | all_null |
| PXD012636/bcda99599fb4 | dataset | pubmed_id | all_null |
| PXD012636/cbac7e076dc6 | run | acquisition_method | missing_column |
| PXD012636/cbac7e076dc6 | run | dissociation_method | all_null |
| PXD012636/cbac7e076dc6 | sample | organism | missing_column |
| PXD012636/cbac7e076dc6 | sample | organism_part | missing_column |
| PXD012636/cbac7e076dc6 | sample | cell_type | missing_column |
| PXD012636/cbac7e076dc6 | sample | cell_line | missing_column |
| PXD012636/cbac7e076dc6 | sample | disease | missing_column |
| PXD012636/cbac7e076dc6 | dataset | project_title | all_null |
| PXD012636/cbac7e076dc6 | dataset | project_description | all_null |
| PXD012636/cbac7e076dc6 | dataset | pubmed_id | all_null |
| PXD012636/f2e29e04cfec | run | acquisition_method | missing_column |
| PXD012636/f2e29e04cfec | run | dissociation_method | all_null |
| PXD012636/f2e29e04cfec | sample | cell_type | missing_column |
| PXD012636/f2e29e04cfec | sample | cell_line | missing_column |
| PXD012636/f2e29e04cfec | sample | disease | missing_column |
| PXD012636/f2e29e04cfec | dataset | project_title | all_null |
| PXD012636/f2e29e04cfec | dataset | project_description | all_null |
| PXD012636/f2e29e04cfec | dataset | pubmed_id | all_null |
| PXD013231/ba2e08eae4e1 | run | acquisition_method | missing_column |
| PXD013231/ba2e08eae4e1 | run | dissociation_method | all_null |
| PXD013231/ba2e08eae4e1 | sample | cell_type | missing_column |
| PXD013231/ba2e08eae4e1 | sample | cell_line | missing_column |
| PXD013231/ba2e08eae4e1 | dataset | project_title | all_null |
| PXD013231/ba2e08eae4e1 | dataset | project_description | all_null |
| PXD013231/ba2e08eae4e1 | dataset | pubmed_id | all_null |
| PXD013658/efb28af0a92c | run | acquisition_method | missing_column |
| PXD013658/efb28af0a92c | run | dissociation_method | all_null |
| PXD013658/efb28af0a92c | sample | cell_type | all_null |
| PXD013658/efb28af0a92c | sample | cell_line | all_null |
| PXD013658/efb28af0a92c | dataset | project_title | all_null |
| PXD013658/efb28af0a92c | dataset | project_description | all_null |
| PXD013658/efb28af0a92c | dataset | pubmed_id | all_null |
| PXD013658/efb28af0a92c | dataset | software_version | all_null |
| PXD013868/3dd0d4bbb5a3 | run | acquisition_method | missing_column |
| PXD013868/3dd0d4bbb5a3 | run | dissociation_method | all_null |
| PXD013868/3dd0d4bbb5a3 | sample | cell_line | missing_column |
| PXD013868/3dd0d4bbb5a3 | dataset | project_title | all_null |
| PXD013868/3dd0d4bbb5a3 | dataset | project_description | all_null |
| PXD013868/3dd0d4bbb5a3 | dataset | pubmed_id | all_null |
| PXD014145/a4974c318c8f | run | acquisition_method | missing_column |
| PXD014145/a4974c318c8f | run | dissociation_method | all_null |
| PXD014145/a4974c318c8f | dataset | project_title | all_null |
| PXD014145/a4974c318c8f | dataset | project_description | all_null |
| PXD014145/a4974c318c8f | dataset | pubmed_id | all_null |
| PXD014414/9688c6886714 | run | acquisition_method | missing_column |
| PXD014414/9688c6886714 | sample | cell_type | all_null |
| PXD014414/9688c6886714 | sample | cell_line | all_null |
| PXD014414/9688c6886714 | dataset | project_title | all_null |
| PXD014414/9688c6886714 | dataset | project_description | all_null |
| PXD014414/9688c6886714 | dataset | pubmed_id | all_null |
| PXD014525/1d3f20844724 | sample | disease | all_null |
| PXD014525/1d3f20844724 | dataset | project_title | all_null |
| PXD014525/1d3f20844724 | dataset | project_description | all_null |
| PXD014525/1d3f20844724 | dataset | pubmed_id | all_null |
| PXD014525/1d3f20844724 | dataset | software_version | all_null |
| PXD014877/0079a1a0cddc | run | acquisition_method | missing_column |
| PXD014877/0079a1a0cddc | sample | cell_type | missing_column |
| PXD014877/0079a1a0cddc | sample | cell_line | missing_column |
| PXD014877/0079a1a0cddc | sample | disease | missing_column |
| PXD014877/0079a1a0cddc | dataset | project_title | all_null |
| PXD014877/0079a1a0cddc | dataset | project_description | all_null |
| PXD014877/0079a1a0cddc | dataset | pubmed_id | all_null |
| PXD014877/05fcb8f8fffd | run | acquisition_method | missing_column |
| PXD014877/05fcb8f8fffd | sample | cell_type | missing_column |
| PXD014877/05fcb8f8fffd | sample | cell_line | missing_column |
| PXD014877/05fcb8f8fffd | sample | disease | missing_column |
| PXD014877/05fcb8f8fffd | dataset | project_title | all_null |
| PXD014877/05fcb8f8fffd | dataset | project_description | all_null |
| PXD014877/05fcb8f8fffd | dataset | pubmed_id | all_null |
| PXD014877/12842b7a98c7 | run | acquisition_method | missing_column |
| PXD014877/12842b7a98c7 | sample | cell_type | missing_column |
| PXD014877/12842b7a98c7 | sample | cell_line | missing_column |
| PXD014877/12842b7a98c7 | sample | disease | missing_column |
| PXD014877/12842b7a98c7 | dataset | project_title | all_null |
| PXD014877/12842b7a98c7 | dataset | project_description | all_null |
| PXD014877/12842b7a98c7 | dataset | pubmed_id | all_null |
| PXD014877/16d4ba616103 | run | acquisition_method | missing_column |
| PXD014877/16d4ba616103 | sample | cell_type | missing_column |
| PXD014877/16d4ba616103 | sample | cell_line | missing_column |
| PXD014877/16d4ba616103 | sample | disease | missing_column |
| PXD014877/16d4ba616103 | dataset | project_title | all_null |
| PXD014877/16d4ba616103 | dataset | project_description | all_null |
| PXD014877/16d4ba616103 | dataset | pubmed_id | all_null |
| PXD014877/1d71cf9a83ae | run | acquisition_method | missing_column |
| PXD014877/1d71cf9a83ae | sample | cell_type | missing_column |
| PXD014877/1d71cf9a83ae | sample | cell_line | missing_column |
| PXD014877/1d71cf9a83ae | sample | disease | missing_column |
| PXD014877/1d71cf9a83ae | dataset | project_title | all_null |
| PXD014877/1d71cf9a83ae | dataset | project_description | all_null |
| PXD014877/1d71cf9a83ae | dataset | pubmed_id | all_null |
| PXD014877/236ee48e5d00 | run | acquisition_method | missing_column |
| PXD014877/236ee48e5d00 | sample | cell_type | missing_column |
| PXD014877/236ee48e5d00 | sample | cell_line | missing_column |
| PXD014877/236ee48e5d00 | sample | disease | missing_column |
| PXD014877/236ee48e5d00 | dataset | project_title | all_null |
| PXD014877/236ee48e5d00 | dataset | project_description | all_null |
| PXD014877/236ee48e5d00 | dataset | pubmed_id | all_null |
| PXD014877/325d45e1eb37 | run | acquisition_method | missing_column |
| PXD014877/325d45e1eb37 | sample | cell_type | missing_column |
| PXD014877/325d45e1eb37 | sample | cell_line | missing_column |
| PXD014877/325d45e1eb37 | sample | disease | missing_column |
| PXD014877/325d45e1eb37 | dataset | project_title | all_null |
| PXD014877/325d45e1eb37 | dataset | project_description | all_null |
| PXD014877/325d45e1eb37 | dataset | pubmed_id | all_null |
| PXD014877/3e14de6f60dc | run | acquisition_method | missing_column |
| PXD014877/3e14de6f60dc | sample | cell_type | missing_column |
| PXD014877/3e14de6f60dc | sample | cell_line | missing_column |
| PXD014877/3e14de6f60dc | sample | disease | missing_column |
| PXD014877/3e14de6f60dc | dataset | project_title | all_null |
| PXD014877/3e14de6f60dc | dataset | project_description | all_null |
| PXD014877/3e14de6f60dc | dataset | pubmed_id | all_null |
| PXD014877/5049d389133f | run | acquisition_method | missing_column |
| PXD014877/5049d389133f | sample | cell_type | missing_column |
| PXD014877/5049d389133f | sample | cell_line | missing_column |
| PXD014877/5049d389133f | sample | disease | missing_column |
| PXD014877/5049d389133f | dataset | project_title | all_null |
| PXD014877/5049d389133f | dataset | project_description | all_null |
| PXD014877/5049d389133f | dataset | pubmed_id | all_null |
| PXD014877/5b9291f80b08 | run | acquisition_method | missing_column |
| PXD014877/5b9291f80b08 | sample | cell_type | missing_column |
| PXD014877/5b9291f80b08 | sample | cell_line | missing_column |
| PXD014877/5b9291f80b08 | sample | disease | missing_column |
| PXD014877/5b9291f80b08 | dataset | project_title | all_null |
| PXD014877/5b9291f80b08 | dataset | project_description | all_null |
| PXD014877/5b9291f80b08 | dataset | pubmed_id | all_null |
| PXD014877/5fd219bdb167 | run | acquisition_method | missing_column |
| PXD014877/5fd219bdb167 | sample | cell_type | missing_column |
| PXD014877/5fd219bdb167 | sample | cell_line | missing_column |
| PXD014877/5fd219bdb167 | sample | disease | missing_column |
| PXD014877/5fd219bdb167 | dataset | project_title | all_null |
| PXD014877/5fd219bdb167 | dataset | project_description | all_null |
| PXD014877/5fd219bdb167 | dataset | pubmed_id | all_null |
| PXD014877/60276dde84d2 | run | acquisition_method | missing_column |
| PXD014877/60276dde84d2 | sample | cell_type | missing_column |
| PXD014877/60276dde84d2 | sample | cell_line | missing_column |
| PXD014877/60276dde84d2 | sample | disease | missing_column |
| PXD014877/60276dde84d2 | dataset | project_title | all_null |
| PXD014877/60276dde84d2 | dataset | project_description | all_null |
| PXD014877/60276dde84d2 | dataset | pubmed_id | all_null |
| PXD014877/6394a99c8b43 | run | acquisition_method | missing_column |
| PXD014877/6394a99c8b43 | sample | cell_type | missing_column |
| PXD014877/6394a99c8b43 | sample | cell_line | missing_column |
| PXD014877/6394a99c8b43 | sample | disease | missing_column |
| PXD014877/6394a99c8b43 | dataset | project_title | all_null |
| PXD014877/6394a99c8b43 | dataset | project_description | all_null |
| PXD014877/6394a99c8b43 | dataset | pubmed_id | all_null |
| PXD014877/639c34eccbd3 | run | acquisition_method | missing_column |
| PXD014877/639c34eccbd3 | sample | cell_type | missing_column |
| PXD014877/639c34eccbd3 | sample | cell_line | missing_column |
| PXD014877/639c34eccbd3 | sample | disease | missing_column |
| PXD014877/639c34eccbd3 | dataset | project_title | all_null |
| PXD014877/639c34eccbd3 | dataset | project_description | all_null |
| PXD014877/639c34eccbd3 | dataset | pubmed_id | all_null |
| PXD014877/667179404f57 | run | acquisition_method | missing_column |
| PXD014877/667179404f57 | sample | cell_type | missing_column |
| PXD014877/667179404f57 | sample | cell_line | missing_column |
| PXD014877/667179404f57 | sample | disease | missing_column |
| PXD014877/667179404f57 | dataset | project_title | all_null |
| PXD014877/667179404f57 | dataset | project_description | all_null |
| PXD014877/667179404f57 | dataset | pubmed_id | all_null |
| PXD014877/69227d2f0923 | run | acquisition_method | missing_column |
| PXD014877/69227d2f0923 | sample | cell_type | missing_column |
| PXD014877/69227d2f0923 | sample | cell_line | missing_column |
| PXD014877/69227d2f0923 | sample | disease | missing_column |
| PXD014877/69227d2f0923 | dataset | project_title | all_null |
| PXD014877/69227d2f0923 | dataset | project_description | all_null |
| PXD014877/69227d2f0923 | dataset | pubmed_id | all_null |
| PXD014877/7031613618e2 | run | acquisition_method | missing_column |
| PXD014877/7031613618e2 | sample | cell_type | missing_column |
| PXD014877/7031613618e2 | sample | cell_line | missing_column |
| PXD014877/7031613618e2 | sample | disease | missing_column |
| PXD014877/7031613618e2 | dataset | project_title | all_null |
| PXD014877/7031613618e2 | dataset | project_description | all_null |
| PXD014877/7031613618e2 | dataset | pubmed_id | all_null |
| PXD014877/7be8d9598918 | run | acquisition_method | missing_column |
| PXD014877/7be8d9598918 | sample | cell_type | missing_column |
| PXD014877/7be8d9598918 | sample | cell_line | missing_column |
| PXD014877/7be8d9598918 | sample | disease | missing_column |
| PXD014877/7be8d9598918 | dataset | project_title | all_null |
| PXD014877/7be8d9598918 | dataset | project_description | all_null |
| PXD014877/7be8d9598918 | dataset | pubmed_id | all_null |
| PXD014877/7f763f444c61 | run | acquisition_method | missing_column |
| PXD014877/7f763f444c61 | sample | cell_type | missing_column |
| PXD014877/7f763f444c61 | sample | cell_line | missing_column |
| PXD014877/7f763f444c61 | sample | disease | missing_column |
| PXD014877/7f763f444c61 | dataset | project_title | all_null |
| PXD014877/7f763f444c61 | dataset | project_description | all_null |
| PXD014877/7f763f444c61 | dataset | pubmed_id | all_null |
| PXD014877/8292fde0ce8a | run | acquisition_method | missing_column |
| PXD014877/8292fde0ce8a | sample | cell_type | missing_column |
| PXD014877/8292fde0ce8a | sample | cell_line | missing_column |
| PXD014877/8292fde0ce8a | sample | disease | missing_column |
| PXD014877/8292fde0ce8a | dataset | project_title | all_null |
| PXD014877/8292fde0ce8a | dataset | project_description | all_null |
| PXD014877/8292fde0ce8a | dataset | pubmed_id | all_null |
| PXD014877/84fa58904700 | run | acquisition_method | missing_column |
| PXD014877/84fa58904700 | sample | cell_type | missing_column |
| PXD014877/84fa58904700 | sample | cell_line | missing_column |
| PXD014877/84fa58904700 | sample | disease | missing_column |
| PXD014877/84fa58904700 | dataset | project_title | all_null |
| PXD014877/84fa58904700 | dataset | project_description | all_null |
| PXD014877/84fa58904700 | dataset | pubmed_id | all_null |
| PXD014877/aa549478e27e | run | acquisition_method | missing_column |
| PXD014877/aa549478e27e | sample | cell_type | missing_column |
| PXD014877/aa549478e27e | sample | cell_line | missing_column |
| PXD014877/aa549478e27e | sample | disease | missing_column |
| PXD014877/aa549478e27e | dataset | project_title | all_null |
| PXD014877/aa549478e27e | dataset | project_description | all_null |
| PXD014877/aa549478e27e | dataset | pubmed_id | all_null |
| PXD014877/b37da9c013a7 | run | acquisition_method | missing_column |
| PXD014877/b37da9c013a7 | sample | cell_type | missing_column |
| PXD014877/b37da9c013a7 | sample | cell_line | missing_column |
| PXD014877/b37da9c013a7 | sample | disease | missing_column |
| PXD014877/b37da9c013a7 | dataset | project_title | all_null |
| PXD014877/b37da9c013a7 | dataset | project_description | all_null |
| PXD014877/b37da9c013a7 | dataset | pubmed_id | all_null |
| PXD014877/b5b498bbdeb8 | run | acquisition_method | missing_column |
| PXD014877/b5b498bbdeb8 | sample | cell_type | missing_column |
| PXD014877/b5b498bbdeb8 | sample | cell_line | missing_column |
| PXD014877/b5b498bbdeb8 | sample | disease | missing_column |
| PXD014877/b5b498bbdeb8 | dataset | project_title | all_null |
| PXD014877/b5b498bbdeb8 | dataset | project_description | all_null |
| PXD014877/b5b498bbdeb8 | dataset | pubmed_id | all_null |
| PXD014877/bd077d4a10cf | run | acquisition_method | missing_column |
| PXD014877/bd077d4a10cf | sample | cell_type | missing_column |
| PXD014877/bd077d4a10cf | sample | cell_line | missing_column |
| PXD014877/bd077d4a10cf | sample | disease | missing_column |
| PXD014877/bd077d4a10cf | dataset | project_title | all_null |
| PXD014877/bd077d4a10cf | dataset | project_description | all_null |
| PXD014877/bd077d4a10cf | dataset | pubmed_id | all_null |
| PXD014877/c3f45bb746d6 | run | acquisition_method | missing_column |
| PXD014877/c3f45bb746d6 | sample | cell_type | missing_column |
| PXD014877/c3f45bb746d6 | sample | cell_line | missing_column |
| PXD014877/c3f45bb746d6 | sample | disease | missing_column |
| PXD014877/c3f45bb746d6 | dataset | project_title | all_null |
| PXD014877/c3f45bb746d6 | dataset | project_description | all_null |
| PXD014877/c3f45bb746d6 | dataset | pubmed_id | all_null |
| PXD014877/c6cc08263c39 | run | acquisition_method | missing_column |
| PXD014877/c6cc08263c39 | sample | cell_type | missing_column |
| PXD014877/c6cc08263c39 | sample | cell_line | missing_column |
| PXD014877/c6cc08263c39 | sample | disease | missing_column |
| PXD014877/c6cc08263c39 | dataset | project_title | all_null |
| PXD014877/c6cc08263c39 | dataset | project_description | all_null |
| PXD014877/c6cc08263c39 | dataset | pubmed_id | all_null |
| PXD014877/c933f3cf414f | run | acquisition_method | missing_column |
| PXD014877/c933f3cf414f | sample | cell_type | missing_column |
| PXD014877/c933f3cf414f | sample | cell_line | missing_column |
| PXD014877/c933f3cf414f | sample | disease | missing_column |
| PXD014877/c933f3cf414f | dataset | project_title | all_null |
| PXD014877/c933f3cf414f | dataset | project_description | all_null |
| PXD014877/c933f3cf414f | dataset | pubmed_id | all_null |
| PXD014877/c9bba9d82c4e | run | acquisition_method | missing_column |
| PXD014877/c9bba9d82c4e | sample | cell_type | missing_column |
| PXD014877/c9bba9d82c4e | sample | cell_line | missing_column |
| PXD014877/c9bba9d82c4e | sample | disease | missing_column |
| PXD014877/c9bba9d82c4e | dataset | project_title | all_null |
| PXD014877/c9bba9d82c4e | dataset | project_description | all_null |
| PXD014877/c9bba9d82c4e | dataset | pubmed_id | all_null |
| PXD014877/ce4624e887a2 | run | acquisition_method | missing_column |
| PXD014877/ce4624e887a2 | sample | cell_type | missing_column |
| PXD014877/ce4624e887a2 | sample | cell_line | missing_column |
| PXD014877/ce4624e887a2 | sample | disease | missing_column |
| PXD014877/ce4624e887a2 | dataset | project_title | all_null |
| PXD014877/ce4624e887a2 | dataset | project_description | all_null |
| PXD014877/ce4624e887a2 | dataset | pubmed_id | all_null |
| PXD014877/cf3a19e0813b | run | acquisition_method | missing_column |
| PXD014877/cf3a19e0813b | sample | cell_type | missing_column |
| PXD014877/cf3a19e0813b | sample | cell_line | missing_column |
| PXD014877/cf3a19e0813b | sample | disease | missing_column |
| PXD014877/cf3a19e0813b | dataset | project_title | all_null |
| PXD014877/cf3a19e0813b | dataset | project_description | all_null |
| PXD014877/cf3a19e0813b | dataset | pubmed_id | all_null |
| PXD014877/d46c60994357 | run | acquisition_method | missing_column |
| PXD014877/d46c60994357 | sample | cell_type | missing_column |
| PXD014877/d46c60994357 | sample | cell_line | missing_column |
| PXD014877/d46c60994357 | sample | disease | missing_column |
| PXD014877/d46c60994357 | dataset | project_title | all_null |
| PXD014877/d46c60994357 | dataset | project_description | all_null |
| PXD014877/d46c60994357 | dataset | pubmed_id | all_null |
| PXD014877/dcae5aa6734b | run | acquisition_method | missing_column |
| PXD014877/dcae5aa6734b | sample | cell_type | missing_column |
| PXD014877/dcae5aa6734b | sample | cell_line | missing_column |
| PXD014877/dcae5aa6734b | sample | disease | missing_column |
| PXD014877/dcae5aa6734b | dataset | project_title | all_null |
| PXD014877/dcae5aa6734b | dataset | project_description | all_null |
| PXD014877/dcae5aa6734b | dataset | pubmed_id | all_null |
| PXD014877/e0d4174d1dfc | run | acquisition_method | missing_column |
| PXD014877/e0d4174d1dfc | sample | cell_type | missing_column |
| PXD014877/e0d4174d1dfc | sample | cell_line | missing_column |
| PXD014877/e0d4174d1dfc | sample | disease | missing_column |
| PXD014877/e0d4174d1dfc | dataset | project_title | all_null |
| PXD014877/e0d4174d1dfc | dataset | project_description | all_null |
| PXD014877/e0d4174d1dfc | dataset | pubmed_id | all_null |
| PXD014877/ea474b486b0c | run | acquisition_method | missing_column |
| PXD014877/ea474b486b0c | sample | cell_type | missing_column |
| PXD014877/ea474b486b0c | sample | cell_line | missing_column |
| PXD014877/ea474b486b0c | sample | disease | missing_column |
| PXD014877/ea474b486b0c | dataset | project_title | all_null |
| PXD014877/ea474b486b0c | dataset | project_description | all_null |
| PXD014877/ea474b486b0c | dataset | pubmed_id | all_null |
| PXD014877/ec2d96088881 | run | acquisition_method | missing_column |
| PXD014877/ec2d96088881 | sample | cell_type | missing_column |
| PXD014877/ec2d96088881 | sample | cell_line | missing_column |
| PXD014877/ec2d96088881 | sample | disease | missing_column |
| PXD014877/ec2d96088881 | dataset | project_title | all_null |
| PXD014877/ec2d96088881 | dataset | project_description | all_null |
| PXD014877/ec2d96088881 | dataset | pubmed_id | all_null |
| PXD014877/eca3cfc4d136 | run | acquisition_method | missing_column |
| PXD014877/eca3cfc4d136 | sample | cell_type | missing_column |
| PXD014877/eca3cfc4d136 | sample | cell_line | missing_column |
| PXD014877/eca3cfc4d136 | sample | disease | missing_column |
| PXD014877/eca3cfc4d136 | dataset | project_title | all_null |
| PXD014877/eca3cfc4d136 | dataset | project_description | all_null |
| PXD014877/eca3cfc4d136 | dataset | pubmed_id | all_null |
| PXD014877/eec763b2b182 | run | acquisition_method | missing_column |
| PXD014877/eec763b2b182 | sample | cell_type | missing_column |
| PXD014877/eec763b2b182 | sample | cell_line | missing_column |
| PXD014877/eec763b2b182 | sample | disease | missing_column |
| PXD014877/eec763b2b182 | dataset | project_title | all_null |
| PXD014877/eec763b2b182 | dataset | project_description | all_null |
| PXD014877/eec763b2b182 | dataset | pubmed_id | all_null |
| PXD014877/f0adae9aac96 | run | acquisition_method | missing_column |
| PXD014877/f0adae9aac96 | sample | cell_type | missing_column |
| PXD014877/f0adae9aac96 | sample | cell_line | missing_column |
| PXD014877/f0adae9aac96 | sample | disease | missing_column |
| PXD014877/f0adae9aac96 | dataset | project_title | all_null |
| PXD014877/f0adae9aac96 | dataset | project_description | all_null |
| PXD014877/f0adae9aac96 | dataset | pubmed_id | all_null |
| PXD014877/f6b218c74636 | run | acquisition_method | missing_column |
| PXD014877/f6b218c74636 | sample | cell_type | missing_column |
| PXD014877/f6b218c74636 | sample | cell_line | missing_column |
| PXD014877/f6b218c74636 | sample | disease | missing_column |
| PXD014877/f6b218c74636 | dataset | project_title | all_null |
| PXD014877/f6b218c74636 | dataset | project_description | all_null |
| PXD014877/f6b218c74636 | dataset | pubmed_id | all_null |
| PXD014877/ffa252045067 | run | acquisition_method | missing_column |
| PXD014877/ffa252045067 | sample | cell_type | missing_column |
| PXD014877/ffa252045067 | sample | cell_line | missing_column |
| PXD014877/ffa252045067 | sample | disease | missing_column |
| PXD014877/ffa252045067 | dataset | project_title | all_null |
| PXD014877/ffa252045067 | dataset | project_description | all_null |
| PXD014877/ffa252045067 | dataset | pubmed_id | all_null |
| PXD016986/7c8762959c63 | run | acquisition_method | missing_column |
| PXD016986/7c8762959c63 | sample | cell_type | missing_column |
| PXD016986/7c8762959c63 | sample | cell_line | missing_column |
| PXD016986/7c8762959c63 | sample | disease | missing_column |
| PXD016986/7c8762959c63 | dataset | project_title | all_null |
| PXD016986/7c8762959c63 | dataset | project_description | all_null |
| PXD016986/7c8762959c63 | dataset | pubmed_id | all_null |
| PXD017199/72ea224b5db7 | dataset | project_title | all_null |
| PXD017199/72ea224b5db7 | dataset | project_description | all_null |
| PXD017199/72ea224b5db7 | dataset | pubmed_id | all_null |
| PXD017199/72ea224b5db7 | dataset | software_version | all_null |
| PXD017199/c29f87a1e559 | dataset | project_title | all_null |
| PXD017199/c29f87a1e559 | dataset | project_description | all_null |
| PXD017199/c29f87a1e559 | dataset | pubmed_id | all_null |
| PXD017199/c29f87a1e559 | dataset | software_version | all_null |
| PXD018450/7282e25039e0 | run | dissociation_method | all_null |
| PXD018450/7282e25039e0 | dataset | project_title | all_null |
| PXD018450/7282e25039e0 | dataset | project_description | all_null |
| PXD018450/7282e25039e0 | dataset | pubmed_id | all_null |
| PXD018450/7282e25039e0 | dataset | software_version | all_null |
| PXD018830/5afa726ca1ad | run | acquisition_method | missing_column |
| PXD018830/5afa726ca1ad | sample | cell_type | all_null |
| PXD018830/5afa726ca1ad | sample | cell_line | all_null |
| PXD018830/5afa726ca1ad | dataset | project_title | all_null |
| PXD018830/5afa726ca1ad | dataset | project_description | all_null |
| PXD018830/5afa726ca1ad | dataset | pubmed_id | all_null |
| PXD018830/cd7751176142 | run | acquisition_method | missing_column |
| PXD018830/cd7751176142 | sample | cell_type | missing_column |
| PXD018830/cd7751176142 | sample | cell_line | missing_column |
| PXD018830/cd7751176142 | dataset | project_title | all_null |
| PXD018830/cd7751176142 | dataset | project_description | all_null |
| PXD018830/cd7751176142 | dataset | pubmed_id | all_null |
| PXD019483/05b90171c8ea | run | acquisition_method | missing_column |
| PXD019483/05b90171c8ea | sample | cell_type | missing_column |
| PXD019483/05b90171c8ea | sample | cell_line | missing_column |
| PXD019483/05b90171c8ea | sample | disease | missing_column |
| PXD019483/05b90171c8ea | dataset | project_title | all_null |
| PXD019483/05b90171c8ea | dataset | project_description | all_null |
| PXD019483/05b90171c8ea | dataset | pubmed_id | all_null |
| PXD019483/13632f8ce583 | run | acquisition_method | missing_column |
| PXD019483/13632f8ce583 | sample | cell_type | missing_column |
| PXD019483/13632f8ce583 | sample | cell_line | missing_column |
| PXD019483/13632f8ce583 | sample | disease | missing_column |
| PXD019483/13632f8ce583 | dataset | project_title | all_null |
| PXD019483/13632f8ce583 | dataset | project_description | all_null |
| PXD019483/13632f8ce583 | dataset | pubmed_id | all_null |
| PXD019483/2d1030090289 | run | acquisition_method | missing_column |
| PXD019483/2d1030090289 | sample | cell_type | missing_column |
| PXD019483/2d1030090289 | sample | cell_line | missing_column |
| PXD019483/2d1030090289 | sample | disease | missing_column |
| PXD019483/2d1030090289 | dataset | project_title | all_null |
| PXD019483/2d1030090289 | dataset | project_description | all_null |
| PXD019483/2d1030090289 | dataset | pubmed_id | all_null |
| PXD019483/2fb69fb71518 | run | acquisition_method | missing_column |
| PXD019483/2fb69fb71518 | sample | cell_type | missing_column |
| PXD019483/2fb69fb71518 | sample | cell_line | missing_column |
| PXD019483/2fb69fb71518 | sample | disease | missing_column |
| PXD019483/2fb69fb71518 | dataset | project_title | all_null |
| PXD019483/2fb69fb71518 | dataset | project_description | all_null |
| PXD019483/2fb69fb71518 | dataset | pubmed_id | all_null |
| PXD019483/5579d1e5db33 | run | acquisition_method | missing_column |
| PXD019483/5579d1e5db33 | sample | cell_type | missing_column |
| PXD019483/5579d1e5db33 | sample | cell_line | missing_column |
| PXD019483/5579d1e5db33 | sample | disease | missing_column |
| PXD019483/5579d1e5db33 | dataset | project_title | all_null |
| PXD019483/5579d1e5db33 | dataset | project_description | all_null |
| PXD019483/5579d1e5db33 | dataset | pubmed_id | all_null |
| PXD019483/5978da4231af | run | acquisition_method | missing_column |
| PXD019483/5978da4231af | sample | cell_type | missing_column |
| PXD019483/5978da4231af | sample | cell_line | missing_column |
| PXD019483/5978da4231af | sample | disease | missing_column |
| PXD019483/5978da4231af | dataset | project_title | all_null |
| PXD019483/5978da4231af | dataset | project_description | all_null |
| PXD019483/5978da4231af | dataset | pubmed_id | all_null |
| PXD019483/5f28441d1bac | run | acquisition_method | missing_column |
| PXD019483/5f28441d1bac | sample | cell_type | missing_column |
| PXD019483/5f28441d1bac | sample | cell_line | missing_column |
| PXD019483/5f28441d1bac | sample | disease | missing_column |
| PXD019483/5f28441d1bac | dataset | project_title | all_null |
| PXD019483/5f28441d1bac | dataset | project_description | all_null |
| PXD019483/5f28441d1bac | dataset | pubmed_id | all_null |
| PXD019483/a3578f6d9889 | run | acquisition_method | missing_column |
| PXD019483/a3578f6d9889 | sample | cell_type | missing_column |
| PXD019483/a3578f6d9889 | sample | cell_line | missing_column |
| PXD019483/a3578f6d9889 | sample | disease | missing_column |
| PXD019483/a3578f6d9889 | dataset | project_title | all_null |
| PXD019483/a3578f6d9889 | dataset | project_description | all_null |
| PXD019483/a3578f6d9889 | dataset | pubmed_id | all_null |
| PXD019483/b4001cf5b39c | run | acquisition_method | missing_column |
| PXD019483/b4001cf5b39c | sample | cell_type | missing_column |
| PXD019483/b4001cf5b39c | sample | cell_line | missing_column |
| PXD019483/b4001cf5b39c | sample | disease | missing_column |
| PXD019483/b4001cf5b39c | dataset | project_title | all_null |
| PXD019483/b4001cf5b39c | dataset | project_description | all_null |
| PXD019483/b4001cf5b39c | dataset | pubmed_id | all_null |
| PXD019483/b42d35fa09ac | run | acquisition_method | missing_column |
| PXD019483/b42d35fa09ac | sample | cell_type | missing_column |
| PXD019483/b42d35fa09ac | sample | cell_line | missing_column |
| PXD019483/b42d35fa09ac | sample | disease | missing_column |
| PXD019483/b42d35fa09ac | dataset | project_title | all_null |
| PXD019483/b42d35fa09ac | dataset | project_description | all_null |
| PXD019483/b42d35fa09ac | dataset | pubmed_id | all_null |
| PXD019483/db89baf48a68 | run | acquisition_method | missing_column |
| PXD019483/db89baf48a68 | sample | cell_type | missing_column |
| PXD019483/db89baf48a68 | sample | cell_line | missing_column |
| PXD019483/db89baf48a68 | sample | disease | missing_column |
| PXD019483/db89baf48a68 | dataset | project_title | all_null |
| PXD019483/db89baf48a68 | dataset | project_description | all_null |
| PXD019483/db89baf48a68 | dataset | pubmed_id | all_null |
| PXD019483/e5461f0f5e96 | run | acquisition_method | missing_column |
| PXD019483/e5461f0f5e96 | sample | cell_type | missing_column |
| PXD019483/e5461f0f5e96 | sample | disease | missing_column |
| PXD019483/e5461f0f5e96 | dataset | project_title | all_null |
| PXD019483/e5461f0f5e96 | dataset | project_description | all_null |
| PXD019483/e5461f0f5e96 | dataset | pubmed_id | all_null |
| PXD019643/46da54d6e3e9 | run | acquisition_method | missing_column |
| PXD019643/46da54d6e3e9 | sample | cell_type | missing_column |
| PXD019643/46da54d6e3e9 | sample | cell_line | missing_column |
| PXD019643/46da54d6e3e9 | sample | disease | missing_column |
| PXD019643/46da54d6e3e9 | dataset | project_title | all_null |
| PXD019643/46da54d6e3e9 | dataset | project_description | all_null |
| PXD019643/46da54d6e3e9 | dataset | pubmed_id | all_null |
| PXD020109/4d8132335b73 | run | acquisition_method | missing_column |
| PXD020109/4d8132335b73 | sample | cell_type | all_null |
| PXD020109/4d8132335b73 | sample | cell_line | all_null |
| PXD020109/4d8132335b73 | dataset | project_title | all_null |
| PXD020109/4d8132335b73 | dataset | project_description | all_null |
| PXD020109/4d8132335b73 | dataset | pubmed_id | all_null |
| PXD020192/5d4b06811efd | run | acquisition_method | missing_column |
| PXD020192/5d4b06811efd | sample | cell_type | missing_column |
| PXD020192/5d4b06811efd | sample | cell_line | missing_column |
| PXD020192/5d4b06811efd | dataset | project_title | all_null |
| PXD020192/5d4b06811efd | dataset | project_description | all_null |
| PXD020192/5d4b06811efd | dataset | pubmed_id | all_null |
| PXD020248/83ab638d361d | run | acquisition_method | missing_column |
| PXD020248/83ab638d361d | dataset | project_title | all_null |
| PXD020248/83ab638d361d | dataset | project_description | all_null |
| PXD020248/83ab638d361d | dataset | pubmed_id | all_null |
| PXD021013/1ed4852abc60 | run | acquisition_method | missing_column |
| PXD021013/1ed4852abc60 | sample | cell_type | missing_column |
| PXD021013/1ed4852abc60 | sample | cell_line | missing_column |
| PXD021013/1ed4852abc60 | sample | disease | missing_column |
| PXD021013/1ed4852abc60 | dataset | project_title | all_null |
| PXD021013/1ed4852abc60 | dataset | project_description | all_null |
| PXD021013/1ed4852abc60 | dataset | pubmed_id | all_null |
| PXD021394/8a6a14abdcee | run | acquisition_method | missing_column |
| PXD021394/8a6a14abdcee | sample | cell_type | all_null |
| PXD021394/8a6a14abdcee | sample | cell_line | all_null |
| PXD021394/8a6a14abdcee | dataset | project_title | all_null |
| PXD021394/8a6a14abdcee | dataset | project_description | all_null |
| PXD021394/8a6a14abdcee | dataset | pubmed_id | all_null |
| PXD022469/ff99b3326179 | run | acquisition_method | missing_column |
| PXD022469/ff99b3326179 | run | dissociation_method | all_null |
| PXD022469/ff99b3326179 | sample | cell_type | missing_column |
| PXD022469/ff99b3326179 | sample | cell_line | missing_column |
| PXD022469/ff99b3326179 | sample | disease | missing_column |
| PXD022469/ff99b3326179 | dataset | project_title | all_null |
| PXD022469/ff99b3326179 | dataset | project_description | all_null |
| PXD022469/ff99b3326179 | dataset | pubmed_id | all_null |
| PXD022992/004371a95fdc | run | dissociation_method | all_null |
| PXD022992/004371a95fdc | sample | cell_type | all_null |
| PXD022992/004371a95fdc | dataset | project_title | all_null |
| PXD022992/004371a95fdc | dataset | project_description | all_null |
| PXD022992/004371a95fdc | dataset | pubmed_id | all_null |
| PXD022992/004371a95fdc | dataset | software_version | all_null |
| PXD022992/473a6fdbf46d | run | acquisition_method | missing_column |
| PXD022992/473a6fdbf46d | sample | cell_type | all_null |
| PXD022992/473a6fdbf46d | dataset | project_title | all_null |
| PXD022992/473a6fdbf46d | dataset | project_description | all_null |
| PXD022992/473a6fdbf46d | dataset | pubmed_id | all_null |
| PXD023508/0e3f6a8fa278 | run | acquisition_method | missing_column |
| PXD023508/0e3f6a8fa278 | run | dissociation_method | all_null |
| PXD023508/0e3f6a8fa278 | sample | cell_type | all_null |
| PXD023508/0e3f6a8fa278 | sample | cell_line | all_null |
| PXD023508/0e3f6a8fa278 | dataset | project_title | all_null |
| PXD023508/0e3f6a8fa278 | dataset | project_description | all_null |
| PXD023508/0e3f6a8fa278 | dataset | pubmed_id | all_null |
| PXD023508/105e86a003fb | run | acquisition_method | missing_column |
| PXD023508/105e86a003fb | run | dissociation_method | all_null |
| PXD023508/105e86a003fb | sample | cell_type | all_null |
| PXD023508/105e86a003fb | sample | cell_line | all_null |
| PXD023508/105e86a003fb | dataset | project_title | all_null |
| PXD023508/105e86a003fb | dataset | project_description | all_null |
| PXD023508/105e86a003fb | dataset | pubmed_id | all_null |
| PXD023508/144cb467d946 | run | acquisition_method | missing_column |
| PXD023508/144cb467d946 | run | dissociation_method | all_null |
| PXD023508/144cb467d946 | sample | cell_type | all_null |
| PXD023508/144cb467d946 | sample | cell_line | all_null |
| PXD023508/144cb467d946 | dataset | project_title | all_null |
| PXD023508/144cb467d946 | dataset | project_description | all_null |
| PXD023508/144cb467d946 | dataset | pubmed_id | all_null |
| PXD023662/4bd01d820826 | run | dissociation_method | all_null |
| PXD023662/4bd01d820826 | dataset | project_title | all_null |
| PXD023662/4bd01d820826 | dataset | project_description | all_null |
| PXD023662/4bd01d820826 | dataset | pubmed_id | all_null |
| PXD023662/4bd01d820826 | dataset | software_version | all_null |
| PXD024364/635149102abd | run | acquisition_method | missing_column |
| PXD024364/635149102abd | sample | disease | missing_column |
| PXD024364/635149102abd | dataset | project_title | all_null |
| PXD024364/635149102abd | dataset | project_description | all_null |
| PXD024364/635149102abd | dataset | pubmed_id | all_null |
| PXD024364/775071de49f6 | run | acquisition_method | missing_column |
| PXD024364/775071de49f6 | dataset | project_title | all_null |
| PXD024364/775071de49f6 | dataset | project_description | all_null |
| PXD024364/775071de49f6 | dataset | pubmed_id | all_null |
| PXD024742/7117bf6e49cf | dataset | project_title | all_null |
| PXD024742/7117bf6e49cf | dataset | project_description | all_null |
| PXD024742/7117bf6e49cf | dataset | pubmed_id | all_null |
| PXD024742/7117bf6e49cf | dataset | software_version | all_null |
| PXD025864/f79dd7dee87c | run | acquisition_method | missing_column |
| PXD025864/f79dd7dee87c | run | dissociation_method | all_null |
| PXD025864/f79dd7dee87c | sample | cell_type | all_null |
| PXD025864/f79dd7dee87c | sample | cell_line | all_null |
| PXD025864/f79dd7dee87c | dataset | project_title | all_null |
| PXD025864/f79dd7dee87c | dataset | project_description | all_null |
| PXD025864/f79dd7dee87c | dataset | pubmed_id | all_null |
| PXD027008/0db5a150c55e | run | acquisition_method | missing_column |
| PXD027008/0db5a150c55e | sample | cell_type | all_null |
| PXD027008/0db5a150c55e | sample | cell_line | all_null |
| PXD027008/0db5a150c55e | dataset | project_title | all_null |
| PXD027008/0db5a150c55e | dataset | project_description | all_null |
| PXD027008/0db5a150c55e | dataset | pubmed_id | all_null |
| PXD027817/276af406f3a2 | run | acquisition_method | missing_column |
| PXD027817/276af406f3a2 | run | dissociation_method | all_null |
| PXD027817/276af406f3a2 | sample | cell_type | all_null |
| PXD027817/276af406f3a2 | sample | cell_line | all_null |
| PXD027817/276af406f3a2 | dataset | project_title | all_null |
| PXD027817/276af406f3a2 | dataset | project_description | all_null |
| PXD027817/276af406f3a2 | dataset | pubmed_id | all_null |
| PXD028251/556541954ff6 | run | acquisition_method | missing_column |
| PXD028251/556541954ff6 | sample | cell_type | all_null |
| PXD028251/556541954ff6 | sample | cell_line | all_null |
| PXD028251/556541954ff6 | dataset | project_title | all_null |
| PXD028251/556541954ff6 | dataset | project_description | all_null |
| PXD028251/556541954ff6 | dataset | pubmed_id | all_null |
| PXD028618/5d414a029db0 | run | acquisition_method | missing_column |
| PXD028618/5d414a029db0 | run | dissociation_method | all_null |
| PXD028618/5d414a029db0 | sample | cell_type | all_null |
| PXD028618/5d414a029db0 | sample | cell_line | all_null |
| PXD028618/5d414a029db0 | dataset | project_title | all_null |
| PXD028618/5d414a029db0 | dataset | project_description | all_null |
| PXD028618/5d414a029db0 | dataset | pubmed_id | all_null |
| PXD028735/1c11af994483 | run | acquisition_method | missing_column |
| PXD028735/1c11af994483 | run | dissociation_method | all_null |
| PXD028735/1c11af994483 | sample | cell_type | missing_column |
| PXD028735/1c11af994483 | sample | disease | missing_column |
| PXD028735/1c11af994483 | dataset | project_title | all_null |
| PXD028735/1c11af994483 | dataset | project_description | all_null |
| PXD028735/1c11af994483 | dataset | pubmed_id | all_null |
| PXD028735/47cdbb531860 | run | acquisition_method | missing_column |
| PXD028735/47cdbb531860 | run | dissociation_method | all_null |
| PXD028735/47cdbb531860 | sample | cell_type | missing_column |
| PXD028735/47cdbb531860 | sample | disease | missing_column |
| PXD028735/47cdbb531860 | dataset | project_title | all_null |
| PXD028735/47cdbb531860 | dataset | project_description | all_null |
| PXD028735/47cdbb531860 | dataset | pubmed_id | all_null |
| PXD028735/651462c269cd | run | acquisition_method | missing_column |
| PXD028735/651462c269cd | run | dissociation_method | all_null |
| PXD028735/651462c269cd | sample | cell_type | missing_column |
| PXD028735/651462c269cd | sample | disease | missing_column |
| PXD028735/651462c269cd | dataset | project_title | all_null |
| PXD028735/651462c269cd | dataset | project_description | all_null |
| PXD028735/651462c269cd | dataset | pubmed_id | all_null |
| PXD030304/fb6d543960a7 | sample | cell_type | all_null |
| PXD030304/fb6d543960a7 | dataset | project_title | all_null |
| PXD030304/fb6d543960a7 | dataset | project_description | all_null |
| PXD030304/fb6d543960a7 | dataset | pubmed_id | all_null |
| PXD030304/fb6d543960a7 | dataset | software_version | all_null |
| PXD030348/06fcf0657451 | run | acquisition_method | missing_column |
| PXD030348/06fcf0657451 | sample | cell_type | missing_column |
| PXD030348/06fcf0657451 | sample | cell_line | missing_column |
| PXD030348/06fcf0657451 | sample | disease | missing_column |
| PXD030348/06fcf0657451 | dataset | project_title | all_null |
| PXD030348/06fcf0657451 | dataset | project_description | all_null |
| PXD030348/06fcf0657451 | dataset | pubmed_id | all_null |
| PXD030671/c5de547b2f93 | run | acquisition_method | missing_column |
| PXD030671/c5de547b2f93 | run | dissociation_method | all_null |
| PXD030671/c5de547b2f93 | sample | cell_type | all_null |
| PXD030671/c5de547b2f93 | dataset | project_title | all_null |
| PXD030671/c5de547b2f93 | dataset | project_description | all_null |
| PXD030671/c5de547b2f93 | dataset | pubmed_id | all_null |
| PXD030983/d5db60f4d306 | run | acquisition_method | missing_column |
| PXD030983/d5db60f4d306 | sample | cell_type | missing_column |
| PXD030983/d5db60f4d306 | sample | cell_line | missing_column |
| PXD030983/d5db60f4d306 | sample | disease | missing_column |
| PXD030983/d5db60f4d306 | dataset | project_title | all_null |
| PXD030983/d5db60f4d306 | dataset | project_description | all_null |
| PXD030983/d5db60f4d306 | dataset | pubmed_id | all_null |
| PXD034656/63f22f75171a | run | acquisition_method | missing_column |
| PXD034656/63f22f75171a | sample | cell_type | missing_column |
| PXD034656/63f22f75171a | sample | cell_line | missing_column |
| PXD034656/63f22f75171a | dataset | project_title | all_null |
| PXD034656/63f22f75171a | dataset | project_description | all_null |
| PXD034656/63f22f75171a | dataset | pubmed_id | all_null |
| PXD036643/6fc2220a9134 | dataset | project_title | all_null |
| PXD036643/6fc2220a9134 | dataset | project_description | all_null |
| PXD036643/6fc2220a9134 | dataset | pubmed_id | all_null |
| PXD036643/6fc2220a9134 | dataset | software_version | all_null |
| PXD036826/11181fff63d2 | dataset | project_title | all_null |
| PXD036826/11181fff63d2 | dataset | project_description | all_null |
| PXD036826/11181fff63d2 | dataset | pubmed_id | all_null |
| PXD036826/11181fff63d2 | dataset | software_version | all_null |
| PXD040266/261169dfab06 | run | acquisition_method | missing_column |
| PXD040266/261169dfab06 | sample | cell_type | missing_column |
| PXD040266/261169dfab06 | sample | cell_line | missing_column |
| PXD040266/261169dfab06 | sample | disease | missing_column |
| PXD040266/261169dfab06 | dataset | project_title | all_null |
| PXD040266/261169dfab06 | dataset | project_description | all_null |
| PXD040266/261169dfab06 | dataset | pubmed_id | all_null |
| PXD041047/9c3873d590d7 | run | acquisition_method | missing_column |
| PXD041047/9c3873d590d7 | sample | cell_type | all_null |
| PXD041047/9c3873d590d7 | sample | disease | all_null |
| PXD041047/9c3873d590d7 | dataset | project_title | all_null |
| PXD041047/9c3873d590d7 | dataset | project_description | all_null |
| PXD041047/9c3873d590d7 | dataset | pubmed_id | all_null |
| PXD041047/9c3873d590d7 | dataset | software_version | all_null |
| PXD041268/4da5d1c864c0 | run | acquisition_method | missing_column |
| PXD041268/4da5d1c864c0 | run | dissociation_method | all_null |
| PXD041268/4da5d1c864c0 | sample | cell_line | missing_column |
| PXD041268/4da5d1c864c0 | dataset | project_title | all_null |
| PXD041268/4da5d1c864c0 | dataset | project_description | all_null |
| PXD041268/4da5d1c864c0 | dataset | pubmed_id | all_null |
| PXD041421/aff39c0adcec | dataset | project_title | all_null |
| PXD041421/aff39c0adcec | dataset | project_description | all_null |
| PXD041421/aff39c0adcec | dataset | pubmed_id | all_null |
| PXD041421/aff39c0adcec | dataset | software_version | all_null |
| PXD042233/9d3045d63b19 | run | dissociation_method | all_null |
| PXD042233/9d3045d63b19 | dataset | project_title | all_null |
| PXD042233/9d3045d63b19 | dataset | project_description | all_null |
| PXD042233/9d3045d63b19 | dataset | pubmed_id | all_null |
| PXD042233/9d3045d63b19 | dataset | software_version | all_null |
| PXD046290/bf08b403513f | run | acquisition_method | missing_column |
| PXD046290/bf08b403513f | sample | cell_type | all_null |
| PXD046290/bf08b403513f | sample | cell_line | all_null |
| PXD046290/bf08b403513f | sample | disease | all_null |
| PXD046290/bf08b403513f | dataset | project_title | all_null |
| PXD046290/bf08b403513f | dataset | project_description | all_null |
| PXD046290/bf08b403513f | dataset | pubmed_id | all_null |
| PXD046290/bf08b403513f | dataset | software_version | all_null |
| PXD046320/be118036d98e | run | acquisition_method | missing_column |
| PXD046320/be118036d98e | sample | cell_type | all_null |
| PXD046320/be118036d98e | sample | cell_line | all_null |
| PXD046320/be118036d98e | sample | disease | all_null |
| PXD046320/be118036d98e | dataset | project_title | all_null |
| PXD046320/be118036d98e | dataset | project_description | all_null |
| PXD046320/be118036d98e | dataset | pubmed_id | all_null |
| PXD046320/be118036d98e | dataset | software_version | all_null |
| PXD048538/41b03dd48c8b | dataset | project_title | all_null |
| PXD048538/41b03dd48c8b | dataset | project_description | all_null |
| PXD048538/41b03dd48c8b | dataset | pubmed_id | all_null |
| PXD048538/41b03dd48c8b | dataset | software_version | all_null |
| PXD048538/e60b9e9aa4c8 | dataset | project_title | all_null |
| PXD048538/e60b9e9aa4c8 | dataset | project_description | all_null |
| PXD048538/e60b9e9aa4c8 | dataset | pubmed_id | all_null |
| PXD048538/e60b9e9aa4c8 | dataset | software_version | all_null |
| PXD052856/1fefbb7618e7 | dataset | project_title | all_null |
| PXD052856/1fefbb7618e7 | dataset | project_description | all_null |
| PXD052856/1fefbb7618e7 | dataset | pubmed_id | all_null |
| PXD052856/1fefbb7618e7 | dataset | software_version | all_null |
| PXD054415/05757be280ee | run | dissociation_method | all_null |
| PXD054415/05757be280ee | sample | cell_line | all_null |
| PXD054415/05757be280ee | dataset | project_title | all_null |
| PXD054415/05757be280ee | dataset | project_description | all_null |
| PXD054415/05757be280ee | dataset | pubmed_id | all_null |
| PXD054415/05757be280ee | dataset | software_version | all_null |
| PXD058009/c0defd8c2d4f | dataset | project_title | all_null |
| PXD058009/c0defd8c2d4f | dataset | project_description | all_null |
| PXD058009/c0defd8c2d4f | dataset | pubmed_id | all_null |
| PXD058009/c0defd8c2d4f | dataset | software_version | all_null |
| PXD062529/a2f209c499ec | run | acquisition_method | missing_column |
| PXD062529/a2f209c499ec | sample | cell_type | missing_column |
| PXD062529/a2f209c499ec | sample | cell_line | missing_column |
| PXD062529/a2f209c499ec | dataset | project_title | all_null |
| PXD062529/a2f209c499ec | dataset | project_description | all_null |
| PXD062529/a2f209c499ec | dataset | pubmed_id | all_null |
| PXD070780/20445ebcb175 | run | dissociation_method | all_null |
| PXD070780/20445ebcb175 | dataset | project_title | all_null |
| PXD070780/20445ebcb175 | dataset | project_description | all_null |
| PXD070780/20445ebcb175 | dataset | pubmed_id | all_null |
| PXD070780/20445ebcb175 | dataset | software_version | all_null |
| PXD071155/a1520a92f6e9 | dataset | project_title | all_null |
| PXD071155/a1520a92f6e9 | dataset | project_description | all_null |
| PXD071155/a1520a92f6e9 | dataset | pubmed_id | all_null |
| PXD071155/a1520a92f6e9 | dataset | software_version | all_null |

## 缺少 schema 级 writer/creator/version 字段

| 字段 | 缺失 Parquet 文件数 | 已读取 Parquet 文件数 |
|---|---|---|
| writer_version | 992 | 1198 |
| creator | 394 | 1198 |
| qpx_version | 394 | 1198 |
| file_type | 394 | 1198 |

缺失值按原样保留；不会把 qpx_version 当 writer_version，把 software_provider 当 creator。

## 无法确定的采集类别

| 数据集/哈希 | 说明 |
|---|---|
| HuiYan-E480/c6a0b932f37f | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| IPX0000937001/664c2e4da7e4 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| IPX0000937003/b89d17ae8c62 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| IPX0001289001/92438d55c6e8 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| IPX0001590001/bc04a24cfeb2 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| IPX0001804001/5ef266f7654c | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| IPX0001804002/0e8d80a52200 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| IPX0001804002/85e196217f8c | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| IPX0002031000/d9555895ba47 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| IPX0004073001/80af31fe2c1f | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PDC000127/e5ff9ac2afbb | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PDC000219/f71256d7465e | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD000561/7db3c391b6bd | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD000612/639a01e7a0ae | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD000672/2036c2011bce | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD000865/4e8f893120ff | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD000865/5e3c1f8ac4cb | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD000865/64b391b9e5f0 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD000865/add2e6b6d09e | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD002137/b0c5382e2661 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD002395/f87700c3dc02 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD002767/a84ef6549a1c | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD002854/af4bd4f283d9 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD002899/2b053d0e6ef5 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD003497/eb3cacb68497 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD003903/4510b70e36f6 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD003947/23f3c6a58576 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD004242/9f9c227d578d | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD004452/0630ad88d3d8 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD004452/37e008c13798 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD004683/ca6b5c6f5f9a | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD004684/21f8df4db8dc | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD004732/da737c110798 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD005526/a4ada00a3100 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD006225/c39c57536766 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD006675/48e09b99db12 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD008333/ce0819a5cc52 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD008722/c9894b9ff502 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD008840/92f495d07775 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD009348/dbafe53ba86a | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD009449/22f1c199c7eb | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD009449/ff35aa00d5b8 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD009737/2eb11e97949a | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD009737/45331c925ca2 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD009737/6c54e9cd8136 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD009737/71aaf28cc8ba | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD010154/cfdbe6ad96ad | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD010429/d380bb98c7d4 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD010595/5d2e0553047a | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD010899/6b1d29c2c3f2 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD010899/75753f784246 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD010957/e8719722d723 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD012131/d553c5a3cc6a | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD012174/9a3c69313ff0 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD012574/82f1b1b2f7de | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD012636/24099cedae93 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD012636/7ba1c0f999a7 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD012636/8bed4e5ecf4d | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD012636/bcda99599fb4 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD012636/cbac7e076dc6 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD012636/f2e29e04cfec | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD013231/ba2e08eae4e1 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD013658/efb28af0a92c | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD013868/3dd0d4bbb5a3 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014145/a4974c318c8f | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014414/9688c6886714 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/0079a1a0cddc | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/05fcb8f8fffd | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/12842b7a98c7 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/16d4ba616103 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/1d71cf9a83ae | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/236ee48e5d00 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/325d45e1eb37 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/3e14de6f60dc | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/5049d389133f | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/5b9291f80b08 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/5fd219bdb167 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/60276dde84d2 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/6394a99c8b43 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/639c34eccbd3 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/667179404f57 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/69227d2f0923 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/7031613618e2 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/7be8d9598918 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/7f763f444c61 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/8292fde0ce8a | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/84fa58904700 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/aa549478e27e | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/b37da9c013a7 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/b5b498bbdeb8 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/bd077d4a10cf | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/c3f45bb746d6 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/c6cc08263c39 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/c933f3cf414f | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/c9bba9d82c4e | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/ce4624e887a2 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/cf3a19e0813b | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/d46c60994357 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/dcae5aa6734b | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/e0d4174d1dfc | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/ea474b486b0c | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/ec2d96088881 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/eca3cfc4d136 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/eec763b2b182 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/f0adae9aac96 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/f6b218c74636 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD014877/ffa252045067 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD016986/7c8762959c63 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD018830/5afa726ca1ad | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD018830/cd7751176142 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD019483/05b90171c8ea | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD019483/13632f8ce583 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD019483/2d1030090289 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD019483/2fb69fb71518 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD019483/5579d1e5db33 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD019483/5978da4231af | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD019483/5f28441d1bac | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD019483/a3578f6d9889 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD019483/b4001cf5b39c | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD019483/b42d35fa09ac | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD019483/db89baf48a68 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD019483/e5461f0f5e96 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD019643/46da54d6e3e9 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD020109/4d8132335b73 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD020192/5d4b06811efd | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD020248/83ab638d361d | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD021013/1ed4852abc60 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD021394/8a6a14abdcee | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD022469/ff99b3326179 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD022992/473a6fdbf46d | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD023508/0e3f6a8fa278 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD023508/105e86a003fb | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD023508/144cb467d946 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD024364/635149102abd | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD024364/775071de49f6 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD025864/f79dd7dee87c | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD027008/0db5a150c55e | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD027817/276af406f3a2 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD028251/556541954ff6 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD028618/5d414a029db0 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD028735/1c11af994483 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD028735/47cdbb531860 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD028735/651462c269cd | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD030348/06fcf0657451 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD030671/c5de547b2f93 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD030983/d5db60f4d306 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD034656/63f22f75171a | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD040266/261169dfab06 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD041047/9c3873d590d7 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD041268/4da5d1c864c0 | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD046290/bf08b403513f | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD046320/be118036d98e | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |
| PXD062529/a2f209c499ec | No explicit recognized acquisition_method in run/dataset; tool names and repository accession are not acquisition evidence |

## Feature peptidoform 去重数

| URL | 去重数 | footer 依据 |
|---|---|---|
| https://browse.quantms.org/quantms/datasets/HuiYanAstralMouse/39e2db14f075/HuiYanAstralMouse.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/MSV000085836/8e4c044b513d/openms.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/MSV000085836/a1f8a70ca82d/MSV000085836.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PMID23933261/173d20caf9ec/PMID23933261.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PMID23933261/c1da3b2adbb3/PMID23933261.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD000672/2036c2011bce/qpx/PXD000672.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD002395/8393835554c6/PXD002395.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD003497/eb3cacb68497/qpx/PXD003497.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD003539/715c024ccd2e/PXD003539.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD004683/ca6b5c6f5f9a/qpx/PXD004683.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD004684/21f8df4db8dc/qpx/PXD004684.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD004701/d82ee8d4dcac/PXD004701.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD011896/a516cc54b8d0/openms.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD012574/82f1b1b2f7de/qpx/PXD012574.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD013658/efb28af0a92c/PXD013658.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD014145/a4974c318c8f/qpx/PXD014145.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD014414/9688c6886714/qpx/PXD014414.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD014525/1d3f20844724/PXD014525.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD017199/72ea224b5db7/PXD017199.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD017199/c29f87a1e559/PXD017199.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD018450/7282e25039e0/PXD018450.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD018830/5afa726ca1ad/qpx/PXD018830.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD020109/4d8132335b73/qpx/PXD020109.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD020248/83ab638d361d/qpx/PXD020248.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD021394/8a6a14abdcee/qpx/PXD021394.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD022992/004371a95fdc/PXD022992.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD022992/473a6fdbf46d/qpx/PXD022992.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD023508/0e3f6a8fa278/qpx/PXD023508.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD023508/105e86a003fb/qpx/PXD023508.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD023508/144cb467d946/qpx/PXD023508.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD023662/4bd01d820826/openms.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD024742/7117bf6e49cf/PXD024742.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD025864/f79dd7dee87c/qpx/PXD025864.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD027008/0db5a150c55e/qpx/PXD027008.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD027817/276af406f3a2/qpx/PXD027817.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD028251/556541954ff6/qpx/PXD028251.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD028618/5d414a029db0/qpx/PXD028618.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD030304/fb6d543960a7/PXD030304.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD030671/c5de547b2f93/qpx/PXD030671.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD036643/6fc2220a9134/PXD036643.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD036826/11181fff63d2/PXD036826.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD041047/9c3873d590d7/PXD041047.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD041421/aff39c0adcec/PXD041421.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD042233/9d3045d63b19/PXD042233.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD046290/bf08b403513f/PXD046290.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD046320/be118036d98e/PXD046320.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD048538/41b03dd48c8b/PXD048538.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD048538/e60b9e9aa4c8/PXD048538.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD052856/1fefbb7618e7/PXD052856.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD054415/05757be280ee/PXD054415.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD058009/c0defd8c2d4f/PXD058009.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD070780/20445ebcb175/PXD070780.feature.parquet | None | distinct_count absent in footer statistics |
| https://browse.quantms.org/quantms/datasets/PXD071155/a1520a92f6e9/PXD071155.feature.parquet | None | distinct_count absent in footer statistics |

## provenance.json.stats 与 footer 的差异

stats.proteins/peptides 的统计口径未声明，不替代本次 PG/peptidoform 计数。以下只比相同命名的记录总数。

| 数据集/哈希 | 字段 | 发布 stats | 本次 footer |
|---|---|---|---|
| IPX0000937003/b89d17ae8c62 | psms | 2220597 | 6551233 |
| IPX0001804001/5ef266f7654c | psms | 4393014 | 23982246 |
| PDC000127/e5ff9ac2afbb | psms | 7379161 | 7515500 |
| PMID23933261/173d20caf9ec | psms | 6388912 | 6427317 |
| PMID23933261/173d20caf9ec | features | 2755588 | 2770774 |
| PMID23933261/c1da3b2adbb3 | psms | 1405504 | 1414304 |
| PMID23933261/c1da3b2adbb3 | features | 1153342 | 1161217 |
| PXD000672/2036c2011bce | psms | 0 | 726062 |
| PXD000672/2036c2011bce | features | 0 | 726062 |
| PXD000672/2036c2011bce | runs | 0 | 36 |
| PXD000672/2036c2011bce | samples | 0 | 36 |
| PXD002395/8393835554c6 | psms | 3412179 | 3430841 |
| PXD002395/8393835554c6 | features | 2548721 | 2560647 |
| PXD003497/eb3cacb68497 | psms | 0 | 1231033 |
| PXD003497/eb3cacb68497 | features | 0 | 1231033 |
| PXD003497/eb3cacb68497 | runs | 0 | 60 |
| PXD003497/eb3cacb68497 | samples | 0 | 30 |
| PXD004683/ca6b5c6f5f9a | psms | 0 | 241669 |
| PXD004683/ca6b5c6f5f9a | features | 0 | 210891 |
| PXD004683/ca6b5c6f5f9a | runs | 0 | 48 |
| PXD004683/ca6b5c6f5f9a | samples | 0 | 12 |
| PXD004684/21f8df4db8dc | psms | 0 | 340478 |
| PXD004684/21f8df4db8dc | features | 0 | 340478 |
| PXD004684/21f8df4db8dc | runs | 0 | 15 |
| PXD004684/21f8df4db8dc | samples | 0 | 8 |
| PXD012574/82f1b1b2f7de | psms | 0 | 262920 |
| PXD012574/82f1b1b2f7de | features | 0 | 201422 |
| PXD012574/82f1b1b2f7de | runs | 0 | 24 |
| PXD012574/82f1b1b2f7de | samples | 0 | 30 |
| PXD014145/a4974c318c8f | psms | 0 | 145741 |
| PXD014145/a4974c318c8f | features | 0 | 126289 |
| PXD014145/a4974c318c8f | runs | 0 | 12 |
| PXD014145/a4974c318c8f | samples | 0 | 11 |
| PXD014414/9688c6886714 | psms | 0 | 100593 |
| PXD014414/9688c6886714 | features | 0 | 84382 |
| PXD014414/9688c6886714 | runs | 0 | 24 |
| PXD014414/9688c6886714 | samples | 0 | 30 |
| PXD018450/7282e25039e0 | psms | 1468563 | 1470804 |
| PXD018450/7282e25039e0 | features | 529299 | 530458 |
| PXD018830/5afa726ca1ad | psms | 0 | 963471 |
| PXD018830/5afa726ca1ad | features | 0 | 963471 |
| PXD018830/5afa726ca1ad | runs | 0 | 25 |
| PXD018830/5afa726ca1ad | samples | 0 | 25 |
| PXD020109/4d8132335b73 | psms | 0 | 80542 |
| PXD020109/4d8132335b73 | features | 0 | 161974 |
| PXD020109/4d8132335b73 | runs | 0 | 12 |
| PXD020109/4d8132335b73 | samples | 0 | 4 |
| PXD020248/83ab638d361d | psms | 0 | 100086 |
| PXD020248/83ab638d361d | features | 0 | 88735 |
| PXD020248/83ab638d361d | runs | 0 | 4 |
| PXD020248/83ab638d361d | samples | 0 | 12 |
| PXD021394/8a6a14abdcee | psms | 0 | 1123166 |
| PXD021394/8a6a14abdcee | features | 0 | 1123166 |
| PXD021394/8a6a14abdcee | runs | 0 | 24 |
| PXD021394/8a6a14abdcee | samples | 0 | 24 |
| PXD022992/473a6fdbf46d | psms | 0 | 1491773 |
| PXD022992/473a6fdbf46d | features | 0 | 1491773 |
| PXD022992/473a6fdbf46d | runs | 0 | 12 |
| PXD022992/473a6fdbf46d | samples | 0 | 6 |
| PXD023508/0e3f6a8fa278 | psms | 0 | 157506 |
| PXD023508/0e3f6a8fa278 | features | 0 | 196157 |
| PXD023508/0e3f6a8fa278 | runs | 0 | 80 |
| PXD023508/0e3f6a8fa278 | samples | 0 | 80 |
| PXD023508/105e86a003fb | psms | 0 | 157275 |
| PXD023508/105e86a003fb | features | 0 | 194877 |
| PXD023508/105e86a003fb | runs | 0 | 80 |
| PXD023508/105e86a003fb | samples | 0 | 80 |
| PXD023508/144cb467d946 | psms | 0 | 157345 |
| PXD023508/144cb467d946 | features | 0 | 195222 |
| PXD023508/144cb467d946 | runs | 0 | 80 |
| PXD023508/144cb467d946 | samples | 0 | 80 |
| PXD025864/f79dd7dee87c | psms | 0 | 278200 |
| PXD025864/f79dd7dee87c | features | 0 | 500000 |
| PXD025864/f79dd7dee87c | runs | 0 | 18 |
| PXD025864/f79dd7dee87c | samples | 0 | 6 |
| PXD027008/0db5a150c55e | psms | 0 | 509591 |
| PXD027008/0db5a150c55e | features | 0 | 500000 |
| PXD027008/0db5a150c55e | runs | 0 | 10 |
| PXD027008/0db5a150c55e | samples | 0 | 10 |
| PXD027817/276af406f3a2 | psms | 0 | 138584 |
| PXD027817/276af406f3a2 | features | 0 | 138584 |
| PXD027817/276af406f3a2 | runs | 0 | 48 |
| PXD027817/276af406f3a2 | samples | 0 | 48 |
| PXD028251/556541954ff6 | psms | 0 | 1366791 |
| PXD028251/556541954ff6 | features | 0 | 500000 |
| PXD028251/556541954ff6 | runs | 0 | 51 |
| PXD028251/556541954ff6 | samples | 0 | 51 |
| PXD028618/5d414a029db0 | psms | 0 | 295418 |
| PXD028618/5d414a029db0 | features | 0 | 295418 |
| PXD028618/5d414a029db0 | runs | 0 | 18 |
| PXD028618/5d414a029db0 | samples | 0 | 18 |
| PXD030671/c5de547b2f93 | psms | 0 | 184022 |
| PXD030671/c5de547b2f93 | features | 0 | 111220 |
| PXD030671/c5de547b2f93 | runs | 0 | 18 |
| PXD030671/c5de547b2f93 | samples | 0 | 33 |
| PXD036643/6fc2220a9134 | psms | 2549618 | 2552135 |
| PXD036643/6fc2220a9134 | features | 1032606 | 1032909 |
| PXD042233/9d3045d63b19 | psms | 29596953 | 29845342 |
| PXD042233/9d3045d63b19 | features | 10959110 | 10978201 |
