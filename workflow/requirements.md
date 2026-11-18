# 作業需求

- 以 Andrej Karpathy 的 LLM Wiki 概念建立「RAG 檢索增強生成入門」知識庫，讀者為不了解 RAG 的初學者。
- 使用繁體中文，保留英文專有名詞。收錄來源摘要、核心概念、技術流程、應用與限制。
- 逐篇 ingest 至少五篇真實 RAG 資料。本階段採指定 S01 至 S05，Karpathy 的說明僅作建置方法參考。
- 重要知識標註來源編號與原文章節，必要時用頁碼。來源觀點衝突時並列，不自行裁定。
- 保留階段產出、修改紀錄與實際檢查，最多三輪 lint。
- 網頁可部署至 GitHub Pages，採純 HTML、CSS、JavaScript 及相對路徑，無後端、資料庫、LLM API 或複雜框架。
- 後續由 Wiki 產出約 10 頁教學 HTML 簡報。每頁標註來源及 Wiki 條目。本階段先完成 Wiki。

## 工作流程 Graph

[取得原文與記錄版本](../raw/README.md) → [逐篇 ingest](../wiki/log.md) → [整合概念與交叉連結](../wiki/index.md) → [建置 Wiki 網頁](../wiki.html) → [實際驗證與修正](report.md)

後續階段由 Wiki 產出簡報，再驗證每頁引用。
