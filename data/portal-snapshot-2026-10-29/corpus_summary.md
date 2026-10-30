# 已发布 QPX 语料统计

生成时间（UTC）：2026-10-30T02:26:45.689183+00:00。数据源：https://browse.quantms.org/quantms/datasets/

## 统计口径与读取方法

- 单位是 QPX 哈希目录。全部版本均保留；同一项目的多个哈希可能包含重复样本、run 和记录。下面的累计数不是跨版本去重后的生物学总数。
- QPX 判定：目录中存在符合 `{prefix}.{view}.parquet` 命名的已知视图；逐文件另存 footer 元数据，不要求所有历史文件都带现代 metadata。
- 文件大小来源：浏览接口 HEAD 返回 405，签名对象 HEAD 返回 403。因此使用成功的 HTTP 206 `Content-Range` 总长度。不是错误响应的 Content-Length，也不是 HTML 估算值。证据：head_probe.json、http_requests.jsonl。未对每个文件重复无效的 HEAD。
- 所有 Parquet 行数只来自 footer `num_rows`。只有 run/sample/dataset/provenance 整表读取；PSM/feature/mz 不读取数据页。
- pg_rows 是所有 run/label 的 PG 记录数。pg_distinct_memberships 是每个哈希内按排序后 pg_accessions 成员集合去重的组数；只用 HTTP range 读该列。跨哈希不去重。
- peptidoform 只在 footer 提供可证明的全局 distinct_count 时统计；不根据 min/max、row 数或 provenance.stats.peptides 推算。
- 未找到视图或读取失败记为 null/空白，不当作真实 0。总计为已知值之和，并列出覆盖目录数。
- CSV 中 writer_version/creator 按原始 schema 元数据记录。缺失 writer_version 不以 qpx_version、software_version 或 parquet.created_by 替代。
- acquisition 使用 run/dataset 的 acquisition_method 原始字段。明确 DDA/DIA 或全称才识别。DDA 再结合 samples[].label 区分 LFQ/TMT/iTRAQ。
- immunopeptidomics 只匹配 dataset project_title/project_description/experiment_type 中明确 immunopeptid 字样，优先于采集类别；保留底层方法。不能根据 IPX/PXD 编号、酶或搜索工具推断。
- unknown 表示缺少足够字段。other 表示明确其他 labeling 或同目录 DDA/DIA 混合。所有原始值和逐文件判定依据保存在 corpus_dataset_details.json。

## 总计（全部 QPX 哈希累计）

| 指标 | 数量 |
|---|---|
| 根目录数据集 | 155 |
| 全部哈希目录 | 280 |
| 含 QPX 的数据集 | 103 |
| QPX 哈希目录 | 181 |
| 全部文件 | 1945 |
| QPX 目录内文件 | 1557 |
| QPX Parquet 文件 | 1198 |
| 成功读取 footer | 1198 |

| 指标 | 已知值之和 | 可统计的 QPX 目录数 |
|---|---|---|
| sample_count | 25350 | 180 |
| run_count | 58208 | 181 |
| psm_rows | 618517802 | 159 |
| feature_rows | 466734475 | 53 |
| pg_rows | 54186502 | 52 |
| pg_distinct_memberships | 449840 | 52 |

QPX 目录全部文件总大小：1,640,685,742,537 bytes（1.640686 TB；1.492195 TiB）。

其中 Parquet：1,624,602,580,979 bytes。大小缺失文件：0。

## 按采集类别

| 类别 | QPX 哈希目录 | 不同数据集 | 样本行数 | run 行数 |
|---|---|---|---|---|
| DDA label-free | 6 | 5 | 673 | 2037 |
| DDA TMT | 4 | 3 | 1170 | 2577 |
| DDA iTRAQ | 0 | 0 | 0 | 0 |
| DIA | 18 | 16 | 3060 | 8419 |
| immunopeptidomics | 0 | 0 | 0 | 0 |
| other | 0 | 0 | 0 | 0 |
| unknown | 153 | 81 | 20447 | 45175 |

## 按物种（保留原始拼写）

多值数据集会出现在多个类别，目录数不互斥。

| 物种 | QPX 哈希目录 | 不同数据集 | 样本行数 |
|---|---|---|---|
| "Akkermansia muciniphilia" | 1 | 1 | 1 |
| "Arabidopsis thaliana" | 1 | 1 | 43 |
| "Bacillus subtilis; Pseudomonas denitrificans; Burkholderia xenovorans; Desulfovibrio vulgaris; Staphylococcus aureus; Alteromonas macleodii; Salmonella enterica typhimurium; Escherichia coli K24; Thermus Thermophilus; Chlamydomonas reinhardtii; Phage M13; Phage F2; Paracoccus denitrificans; Phage P22; Phage F0; Phage ES18; Rhizobium leguminosarum; Nitrosomonas europaeae; Nitrosomonas ureae; Nitrosospira multiformis; Nitrososphaera viennensis; Roseobacter; Pseudomonas pseudoalcaligenes; Chromobacterium violaceum; Agrobacterium tumefaciens; Stenotrophomonas maltophilia; Cupriavidus metallireducens; Pseudomonas fluorescens; Escherichia coli K37; Escherichia coli K61" | 1 | 1 | 1 |
| "Bacillus subtilis; Pseudomonas denitrificans; Burkholderia xenovorans; Desulfovibrio vulgaris; Staphylococcus aureus; Alteromonas macleodii; Salmonella enterica typhimurium; Escherichia coli K25; Thermus Thermophilus; Chlamydomonas reinhardtii; Phage M13; Phage F2; Paracoccus denitrificans; Phage P22; Phage F0; Phage ES18; Rhizobium leguminosarum; Nitrosomonas europaeae; Nitrosomonas ureae; Nitrosospira multiformis; Nitrososphaera viennensis; Roseobacter; Pseudomonas pseudoalcaligenes; Chromobacterium violaceum; Agrobacterium tumefaciens; Stenotrophomonas maltophilia; Cupriavidus metallireducens; Pseudomonas fluorescens; Escherichia coli K39; Escherichia coli K63" | 1 | 1 | 1 |
| "Bacillus subtilis; Pseudomonas denitrificans; Burkholderia xenovorans; Desulfovibrio vulgaris; Staphylococcus aureus; Alteromonas macleodii; Salmonella enterica typhimurium; Escherichia coli K26; Thermus Thermophilus; Chlamydomonas reinhardtii; Phage M13; Phage F2; Paracoccus denitrificans; Phage P22; Phage F0; Phage ES18; Rhizobium leguminosarum; Nitrosomonas europaeae; Nitrosomonas ureae; Nitrosospira multiformis; Nitrososphaera viennensis; Roseobacter; Pseudomonas pseudoalcaligenes; Chromobacterium violaceum; Agrobacterium tumefaciens; Stenotrophomonas maltophilia; Cupriavidus metallireducens; Pseudomonas fluorescens; Escherichia coli K41; Escherichia coli K65" | 1 | 1 | 1 |
| "Bacillus subtilis; Pseudomonas denitrificans; Burkholderia xenovorans; Desulfovibrio vulgaris; Staphylococcus aureus; Alteromonas macleodii; Salmonella enterica typhimurium; Escherichia coli K27; Thermus Thermophilus; Chlamydomonas reinhardtii; Phage M13; Phage F2; Paracoccus denitrificans; Phage P22; Phage F0; Phage ES18; Rhizobium leguminosarum; Nitrosomonas europaeae; Nitrosomonas ureae; Nitrosospira multiformis; Nitrososphaera viennensis; Roseobacter; Pseudomonas pseudoalcaligenes; Chromobacterium violaceum; Agrobacterium tumefaciens; Stenotrophomonas maltophilia; Cupriavidus metallireducens; Pseudomonas fluorescens; Escherichia coli K43; Escherichia coli K67" | 1 | 1 | 1 |
| "Bacillus subtilis; Pseudomonas denitrificans; Burkholderia xenovorans; Desulfovibrio vulgaris; Staphylococcus aureus; Alteromonas macleodii; Salmonella enterica typhimurium; Escherichia coli K28; Thermus Thermophilus; Chlamydomonas reinhardtii; Phage M13; Phage F2; Paracoccus denitrificans; Phage P22; Phage F0; Phage ES18; Rhizobium leguminosarum; Nitrosomonas europaeae; Nitrosomonas ureae; Nitrosospira multiformis; Nitrososphaera viennensis; Roseobacter; Pseudomonas pseudoalcaligenes; Chromobacterium violaceum; Agrobacterium tumefaciens; Stenotrophomonas maltophilia; Cupriavidus metallireducens; Pseudomonas fluorescens; Escherichia coli K45; Escherichia coli K69" | 1 | 1 | 1 |
| "Bacillus subtilis; Pseudomonas denitrificans; Burkholderia xenovorans; Desulfovibrio vulgaris; Staphylococcus aureus; Alteromonas macleodii; Salmonella enterica typhimurium; Escherichia coli K29; Thermus Thermophilus; Chlamydomonas reinhardtii; Phage M13; Phage F2; Paracoccus denitrificans; Phage P22; Phage F0; Phage ES18; Rhizobium leguminosarum; Nitrosomonas europaeae; Nitrosomonas ureae; Nitrosospira multiformis; Nitrososphaera viennensis; Roseobacter; Pseudomonas pseudoalcaligenes; Chromobacterium violaceum; Agrobacterium tumefaciens; Stenotrophomonas maltophilia; Cupriavidus metallireducens; Pseudomonas fluorescens; Escherichia coli K47; Escherichia coli K71" | 1 | 1 | 1 |
| "Bacillus subtilis; Pseudomonas denitrificans; Burkholderia xenovorans; Desulfovibrio vulgaris; Staphylococcus aureus; Alteromonas macleodii; Salmonella enterica typhimurium; Escherichia coli K30; Thermus Thermophilus; Chlamydomonas reinhardtii; Phage M13; Phage F2; Paracoccus denitrificans; Phage P22; Phage F0; Phage ES18; Rhizobium leguminosarum; Nitrosomonas europaeae; Nitrosomonas ureae; Nitrosospira multiformis; Nitrososphaera viennensis; Roseobacter; Pseudomonas pseudoalcaligenes; Chromobacterium violaceum; Agrobacterium tumefaciens; Stenotrophomonas maltophilia; Cupriavidus metallireducens; Pseudomonas fluorescens; Escherichia coli K49; Escherichia coli K73" | 1 | 1 | 1 |
| "Bacillus subtilis; Pseudomonas denitrificans; Burkholderia xenovorans; Desulfovibrio vulgaris; Staphylococcus aureus; Alteromonas macleodii; Salmonella enterica typhimurium; Escherichia coli K31; Thermus Thermophilus; Chlamydomonas reinhardtii; Phage M13; Phage F2; Paracoccus denitrificans; Phage P22; Phage F0; Phage ES18; Rhizobium leguminosarum; Nitrosomonas europaeae; Nitrosomonas ureae; Nitrosospira multiformis; Nitrososphaera viennensis; Roseobacter; Pseudomonas pseudoalcaligenes; Chromobacterium violaceum; Agrobacterium tumefaciens; Stenotrophomonas maltophilia; Cupriavidus metallireducens; Pseudomonas fluorescens; Escherichia coli K51; Escherichia coli K75" | 1 | 1 | 1 |
| "Bacillus subtilis; Pseudomonas denitrificans; Burkholderia xenovorans; Desulfovibrio vulgaris; Staphylococcus aureus; Alteromonas macleodii; Salmonella enterica typhimurium; Escherichia coli K32; Thermus Thermophilus; Chlamydomonas reinhardtii; Phage M13; Phage F2; Paracoccus denitrificans; Phage P22; Phage F0; Phage ES18; Rhizobium leguminosarum; Nitrosomonas europaeae; Nitrosomonas ureae; Nitrosospira multiformis; Nitrososphaera viennensis; Roseobacter; Pseudomonas pseudoalcaligenes; Chromobacterium violaceum; Agrobacterium tumefaciens; Stenotrophomonas maltophilia; Cupriavidus metallireducens; Pseudomonas fluorescens; Escherichia coli K53; Escherichia coli K77" | 1 | 1 | 1 |
| "Bacillus subtilis; Pseudomonas denitrificans; Burkholderia xenovorans; Desulfovibrio vulgaris; Staphylococcus aureus; Alteromonas macleodii; Salmonella enterica typhimurium; Escherichia coli K33; Thermus Thermophilus; Chlamydomonas reinhardtii; Phage M13; Phage F2; Paracoccus denitrificans; Phage P22; Phage F0; Phage ES18; Rhizobium leguminosarum; Nitrosomonas europaeae; Nitrosomonas ureae; Nitrosospira multiformis; Nitrososphaera viennensis; Roseobacter; Pseudomonas pseudoalcaligenes; Chromobacterium violaceum; Agrobacterium tumefaciens; Stenotrophomonas maltophilia; Cupriavidus metallireducens; Pseudomonas fluorescens; Escherichia coli K55; Escherichia coli K79" | 1 | 1 | 1 |
| "Bacillus subtilis; Pseudomonas denitrificans; Burkholderia xenovorans; Desulfovibrio vulgaris; Staphylococcus aureus; Alteromonas macleodii; Salmonella enterica typhimurium; Escherichia coli K34; Thermus Thermophilus; Chlamydomonas reinhardtii; Phage M13; Phage F2; Paracoccus denitrificans; Phage P22; Phage F0; Phage ES18; Rhizobium leguminosarum; Nitrosomonas europaeae; Nitrosomonas ureae; Nitrosospira multiformis; Nitrososphaera viennensis; Roseobacter; Pseudomonas pseudoalcaligenes; Chromobacterium violaceum; Agrobacterium tumefaciens; Stenotrophomonas maltophilia; Cupriavidus metallireducens; Pseudomonas fluorescens; Escherichia coli K57; Escherichia coli K81" | 1 | 1 | 1 |
| "Bacillus subtilis; Pseudomonas denitrificans; Burkholderia xenovorans; Desulfovibrio vulgaris; Staphylococcus aureus; Alteromonas macleodii; Salmonella enterica typhimurium; Escherichia coli K35; Thermus Thermophilus; Chlamydomonas reinhardtii; Phage M13; Phage F2; Paracoccus denitrificans; Phage P22; Phage F0; Phage ES18; Rhizobium leguminosarum; Nitrosomonas europaeae; Nitrosomonas ureae; Nitrosospira multiformis; Nitrososphaera viennensis; Roseobacter; Pseudomonas pseudoalcaligenes; Chromobacterium violaceum; Agrobacterium tumefaciens; Stenotrophomonas maltophilia; Cupriavidus metallireducens; Pseudomonas fluorescens; Escherichia coli K59; Escherichia coli K83" | 1 | 1 | 1 |
| "Bacteroides Fragilis" | 1 | 1 | 1 |
| "Bacteroides Thetaiotaomicron" | 1 | 1 | 1 |
| "Bacteroides Uniformis" | 1 | 1 | 1 |
| "Bifidobacterium Longum Subsp Longum" | 1 | 1 | 1 |
| "Chromera velia" | 1 | 1 | 1 |
| "Clostridium Bolteae" | 1 | 1 | 1 |
| "Clostridium saccharolyticum" | 1 | 1 | 1 |
| "Collinsella Aerofaciens" | 1 | 1 | 1 |
| "Danio rerio" | 2 | 2 | 59 |
| "Dorea formicigenerans" | 1 | 1 | 1 |
| "Drosophila melanogaster" | 1 | 1 | 92 |
| "Drosophila" | 1 | 1 | 1 |
| "Eggerthella Lenta" | 2 | 1 | 2 |
| "Equus caballus" | 1 | 1 | 124 |
| "Escherichia coli K-12" | 2 | 2 | 5 |
| "Escherichia coli" | 2 | 1 | 78 |
| "Fusarium oxysporum" | 1 | 1 | 4 |
| "Fusobacterium Nucleatum Subsp Nucleatum" | 1 | 1 | 1 |
| "Gallus Gallus" | 1 | 1 | 1 |
| "Gossypium hirsutum" | 1 | 1 | 1 |
| "Halobacterium sp" | 1 | 1 | 1 |
| "Herpes simplex Virus" | 3 | 1 | 3 |
| "Homo Sapiens" | 4 | 3 | 66 |
| "Homo sapiens" | 84 | 66 | 10155 |
| "LA crosse encephalitis virus" | 2 | 1 | 2 |
| "Lactobacillus Paracasei" | 1 | 1 | 1 |
| "Mus musculus" | 8 | 8 | 6568 |
| "Mycoplasmen" | 2 | 1 | 2 |
| "Neurospora Crassa" | 1 | 1 | 1 |
| "Odoribacter splanchnicus" | 1 | 1 | 1 |
| "Parabacteroides Distasonis" | 1 | 1 | 1 |
| "Parabacteroides Merdae" | 1 | 1 | 1 |
| "Phaeodactylum tricornutum" | 1 | 1 | 1 |
| "Prevotella Copri" | 1 | 1 | 1 |
| "Rattus norvegicus" | 1 | 1 | 120 |
| "Rift valley Fever" | 2 | 1 | 2 |
| "Riftia pachyptila" | 1 | 1 | 349 |
| "Roseburia Intestinalis" | 1 | 1 | 1 |
| "Ruminococcus Bromii" | 1 | 1 | 1 |
| "Ruminococcus Gnavus" | 1 | 1 | 1 |
| "Ruminococcus Torques" | 1 | 1 | 1 |
| "Saccharomyces cerevisiae" | 1 | 1 | 637 |
| "Solanum tuberosum" | 1 | 1 | 297 |
| "Streptococcus Parasanguinis" | 1 | 1 | 1 |
| "Sulfolobus solfataricus" | 2 | 1 | 2 |
| "Sus scrofa domesticus" | 1 | 1 | 120 |
| "Symbiodinium microadriaticum" | 2 | 1 | 2 |
| "Triticum aestivum" | 1 | 1 | 1 |
| "Veillonella parvula" | 1 | 1 | 1 |
| "Vesicular stomatitis Virus" | 2 | 1 | 2 |
| "Vitris vinifera" | 1 | 1 | 1 |
| "Zika Virus" | 2 | 1 | 4 |
| "homo sapiens" | 17 | 16 | 5946 |
| "unknown" | 2 | 2 | 624 |
| unknown/missing | 1 | 1 | not inferred |

## 按仪器（保留原始拼写）

多值数据集会出现在多个类别，目录数不互斥。

| 仪器 | QPX 哈希目录 | 不同数据集 | run 行数 |
|---|---|---|---|
| "LTQ Orbitrap Elite" | 5 | 2 | 2859 |
| "LTQ Orbitrap Velos" | 6 | 4 | 1785 |
| "LTQ Orbitrap XL ETD" | 2 | 1 | 1007 |
| "LTQ Orbitrap" | 2 | 2 | 1141 |
| "Orbitrap Astral" | 4 | 4 | 1185 |
| "Orbitrap Eclipse" | 1 | 1 | 12 |
| "Orbitrap Exploris 480" | 2 | 2 | 780 |
| "Orbitrap Fusion Lumos" | 17 | 14 | 5168 |
| "Orbitrap Fusion" | 18 | 17 | 10490 |
| "Orbitrap" | 1 | 1 | 347 |
| "Q Exactive HF" | 18 | 17 | 12710 |
| "Q Exactive HF-X" | 68 | 12 | 3187 |
| "Q Exactive Plus" | 10 | 9 | 3033 |
| "Q Exactive" | 25 | 17 | 8045 |
| "TripleTOF 5600" | 5 | 5 | 534 |
| "TripleTOF 6600" | 1 | 1 | 5798 |
| "timsTOF HT" | 1 | 1 | 21 |
| "timsTOF Pro" | 3 | 3 | 106 |
| unknown/missing | 0 | 0 | not inferred |

## 按 creator 原始值

目录数按至少一份 Parquet 含该值计数；unknown/missing 按至少一份缺失计数。同一目录可出现在多行。

| creator | QPX 哈希目录 | 不同数据集 | Parquet 文件 |
|---|---|---|---|
| chengxin | 119 | 55 | 147 |
| diann | 22 | 20 | 43 |
| openms-consensus | 10 | 8 | 30 |
| qpx | 181 | 103 | 521 |
| quantms | 21 | 19 | 63 |
| unknown/missing | 128 | 59 | 394 |

## 按 writer_version 原始值

目录数按至少一份 Parquet 含该值计数；unknown/missing 按至少一份缺失计数。同一目录可出现在多行。

| writer_version | QPX 哈希目录 | 不同数据集 | Parquet 文件 |
|---|---|---|---|
| 1.1.2 | 3 | 3 | 9 |
| 1.1.4 | 25 | 22 | 181 |
| 1.1.5 | 2 | 2 | 16 |
| unknown/missing | 153 | 81 | 992 |

## 按 software_provider 原始值

目录数按至少一份 Parquet 含该值计数；unknown/missing 按至少一份缺失计数。同一目录可出现在多行。

| software_provider | QPX 哈希目录 | 不同数据集 | Parquet 文件 |
|---|---|---|---|
| dcx | 108 | 46 | 123 |
| qpx | 181 | 103 | 657 |
| quantms | 11 | 10 | 24 |
| unknown/missing | 128 | 59 | 394 |

## 按 qpx_version 原始值

目录数按至少一份 Parquet 含该值计数；unknown/missing 按至少一份缺失计数。同一目录可出现在多行。

| qpx_version | QPX 哈希目录 | 不同数据集 | Parquet 文件 |
|---|---|---|---|
| 1.0.1 | 125 | 56 | 397 |
| 1.0.2 | 28 | 26 | 201 |
| 1.1 | 29 | 25 | 206 |
| unknown/missing | 128 | 59 | 394 |

## creator × writer_version

| creator | writer_version | Parquet 文件 | QPX 哈希目录 |
|---|---|---|---|
| chengxin | unknown/missing | 147 | 119 |
| diann | 1.1.2 | 4 | 3 |
| diann | 1.1.4 | 32 | 16 |
| diann | unknown/missing | 7 | 4 |
| openms-consensus | 1.1.4 | 24 | 8 |
| openms-consensus | 1.1.5 | 6 | 2 |
| qpx | 1.1.2 | 5 | 1 |
| qpx | 1.1.4 | 125 | 25 |
| qpx | 1.1.5 | 10 | 2 |
| qpx | unknown/missing | 381 | 153 |
| quantms | unknown/missing | 63 | 21 |
| unknown/missing | unknown/missing | 394 | 128 |

## 视图覆盖

| 视图 | 哈希目录 | 文件数 | footer 行数之和 |
|---|---|---|---|
| dataset | 181 | 181 | 181 |
| feature | 53 | 53 | 466734475 |
| mz | 0 | 0 | 0 |
| ontology | 181 | 181 | 2680 |
| pepmap | 0 | 0 | 0 |
| pg | 52 | 52 | 54186502 |
| proteoform | 0 | 0 | 0 |
| provenance | 181 | 181 | 542 |
| psm | 159 | 189 | 618517802 |
| run | 181 | 181 | 58208 |
| sample | 180 | 180 | 25350 |
| site | 0 | 0 | 0 |

## 文件与详细证据

- corpus_files.csv：所有哈希内所有文件，包括非 QPX 输出。is_qpx 表示所属哈希是 QPX 输出；is_qpx_view_file 表示文件本身为 QPX Parquet 视图。
- corpus_datasets.csv：每个 QPX 哈希一行；dataset_fields 保留 dataset.parquet 全部字段。
- corpus_dataset_details.json：全部 run/sample 字段分布、dataset 全字段、provenance 两种来源、schema metadata、分类依据。
- corpus_evidence.json 与 file_evidence/：逐文件 footer/schema 与小表原始记录。
- hash_directories.json：全部哈希列表，含非 QPX 目录；http_cache/ 保存成功响应和请求头。
- corpus_anomalies.md：缺失、冲突、多个版本、未知分类和读取失败。

复现：`/home/shenyufei/miniforge3/envs/Bigbio/bin/python corpus_stats.py --stage all --workers 8`。
仅重新汇总本次快照：`/home/shenyufei/miniforge3/envs/Bigbio/bin/python corpus_stats.py --stage report`。
默认复用成功请求缓存；`--refresh` 重新采集。
