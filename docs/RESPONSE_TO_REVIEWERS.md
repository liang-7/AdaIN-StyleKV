# 修订说明与回复信 (Revision Response — Round 2)

> 论文：《AdaIN StyleKV：基于自注意力KV融合与自适应归一化的扩散模型免训练风格迁移》
> 修订稿：`paper_revised.tex`（编译通过，11 页）
> 本轮日期：2026-06-12
> 本轮依据：上一轮 `docs/REVISION_LOG.md` 末尾的 5 项「待作者确认/补充」

---

## 论文信息

| 字段 | 值 |
|------|----|
| 修订轮次 | 2 |
| 上轮决定 | 自查待办（非外审意见） |
| 原字数/页数 | 11 页 |
| 修订后页数 | 11 页 |
| 本轮新增图 | 1（用户偏好研究，`fig_userstudy_docx.pdf`） |
| 本轮新增参考文献 | 0（仅补全 [20] 的 arXiv ID） |

---

## 修订追踪表

| # | 待办项（来源 REVISION_LOG §待确认） | 类型 | 章节 | 处理摘要 | 改动位置 | 状态 |
|---|------------------------------------|------|------|----------|----------|------|
| W1 | ControlNet 确切版本 | Major | §2.4 | 明确全部实验基于 SDXL，固定使用 `controlnet-canny-sdxl-1.0`；SD1.5 权重仅作对照说明 | §2.4 末段 | RESOLVED |
| W2 | 基线对比数据 | Major | §6.1 / §7.2 | 不伪造对比数据；保留为已声明局限，并将改进方向具体化为「统一数据集与评估协议下复现并定量对比」 | §7.2 局限性表 | DELIBERATE_LIMITATION |
| W3 | 用户研究扩展 | Major | §4.6.2 | 恢复原 `paper.tex` 中的真实用户偏好研究（7人×7配对），并显式标注样本量有限、不支撑显著性、列为未来工作 | 新增 §4.6.2 + 图 | RESOLVED |
| W4 | 图文件与变体命名一致性 | Minor | §4.3 | 核查 `image1–4.pdf` 引用均存在且编译通过；变体命名 V1–V7 与图注一致，无需改名 | 全文图引用 | RESOLVED |
| W5 | Art-FID 参考文献核实 | Minor | 参考文献[20] | 经检索核实为 Wright & Ommer, GCPR 2022, arXiv:2207.12280；补入 arXiv ID | `\bibitem{artfid}` | RESOLVED |

### 提交承诺台账 (Commitment Ledger)

```yaml
- concern_id: W1
  commitment_extracted:
    - commitment_text: "明确实验所用 Stable Diffusion 与 ControlNet 版本，消除 SD1.5/SDXL 歧义"
      commitment_type: add_clarification
      required_evidence_type: prose_edit
      fulfillment_status: fulfilled

- concern_id: W2
  commitment_extracted:
    - commitment_text: "补充与 InST/StyleDiffusion/InstantStyle 的同条件定量对比"
      commitment_type: add_experiment
      required_evidence_type: new_table
      fulfillment_status: explicitly-rejected-with-rationale
      unfulfilled_rationale: "deferred to future work — 本轮无新跑实验数据，伪造对比数字违反学术诚信(Anti-Pattern #5)。已在 §7.2 局限性表与 §6.1 未来工作中明确声明该缺口及统一评估协议的补全计划。"

- concern_id: W3
  commitment_extracted:
    - commitment_text: "明确用户研究样本量并说明统计显著性边界"
      commitment_type: add_clarification
      required_evidence_type: discussion_paragraph
      fulfillment_status: fulfilled
    - commitment_text: "恢复被误删的用户偏好研究小节与配图"
      commitment_type: restructure
      required_evidence_type: new_section
      fulfillment_status: fulfilled

- concern_id: W4
  commitment_extracted:
    - commitment_text: "核查图文件存在性与变体命名一致性"
      commitment_type: add_clarification
      required_evidence_type: acknowledgment_only
      fulfillment_status: fulfilled

- concern_id: W5
  commitment_extracted:
    - commitment_text: "核实并补全 Art-FID 引用信息"
      commitment_type: add_citation
      required_evidence_type: new_citation
      fulfillment_status: fulfilled
```

---

## 逐条回复 (Point-by-Point Response)

尊敬的编辑与各位审稿人：

感谢上一轮对本文的细致意见。本轮针对修订日志中遗留的 5 项待确认事项逐条处理，回复如下。修订处已在稿件中相应章节落实。

### W1 — ControlNet 确切版本
**类型**：Major　**回应**：已澄清。原文在 §2.4 同时列出 SD1.5 与 SDXL 两个权重名，易让读者误判实验基础。现明确：**全部实验基于 Stable Diffusion XL（SDXL），采用 `diffusers/controlnet-canny-sdxl-1.0`**；SD1.5 权重 `lllyasviel/control_v11p_sd15_canny` 仅作为版本对照说明。同时修正了原 §6.4「扩展至 SDXL」这一与实际基础相矛盾的未来工作项，改为「跨架构适配与轻量化」。
**改动**：§2.4 末段重写。

### W2 — 缺乏外部方法定量对比
**类型**：Major　**回应**：诚实声明为本研究边界，**未补充对比数据**。本轮未重新运行实验，凭空给出 InST/StyleDiffusion/InstantStyle 的对比数字将构成数据捏造，违反学术诚信。我们的处理是：在 §7.2 局限性表中将该缺口列为首要局限，并把改进方向具体化为「在统一数据集与评估协议下复现并定量对比主流方法」，§6.1 未来工作亦作呼应。若审稿方要求，我们可在下一轮补做该对比实验。
**改动**：§7.2 局限性表首行；§6.1。

### W3 — 用户研究样本量
**类型**：Major　**回应**：已恢复并加注边界。原始 `paper.tex` 含一项真实用户偏好研究（7 名参与者对 7 种方法在 7 组配对上排序），在上一轮被整体删除、其配图位置被排名热力图占用。本轮**恢复该小节（§4.6.2）及其专属配图 `fig_userstudy_docx.pdf`**，并显式声明：参与者与配对均为 7，样本量有限，结果仅作定量指标的辅助佐证，不支撑统计显著性；扩大规模与显著性检验列入未来工作及局限性表。
**改动**：新增 §4.6.2 + 图 \ref{fig:user_study}；§7.2 局限性表新增一行。

### W4 — 图文件与变体命名一致性
**类型**：Minor　**回应**：已核查。`image1.pdf`–`image4.pdf` 四个文件均存在于 `figures/` 且全文编译无缺图报错；正文变体编号 V1–V7 与各图注、附录表完全一致，无歧义命名残留，故不改名。
**改动**：无（核查确认）。

### W5 — Art-FID 引用核实
**类型**：Minor　**回应**：已核实并补全。经检索确认该指标出处为 Matthias Wright 与 Björn Ommer，*ArtFID: Quantitative Evaluation of Neural Style Transfer*，GCPR 2022，arXiv:2207.12280（官方代码 github.com/matthias-wright/art-fid）。已在参考文献 [20] 补入 arXiv ID 并将标题更正为原文 “ArtFID”。
**改动**：`\bibitem{artfid}`。

---

## 变更统计

| 指标 | 数量 |
|------|------|
| 处理待办项 | 5 |
| RESOLVED | 4 |
| 已声明局限 (Deliberate Limitation) | 1（W2） |
| 新增小节 | 1（§4.6.2 用户偏好研究） |
| 新增图 | 1 |
| 新增/订正参考文献 | 1（[20] 补 arXiv ID） |
| 编译状态 | 通过，11 页，无未定义引用 |

诚挚感谢各位的时间与建议。

作者敬上
