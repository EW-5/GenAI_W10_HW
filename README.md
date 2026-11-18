# RAG 檢索增強生成入門

這是面向初學者的生成式 AI 課程作業。從 [專案首頁](index.html) 開始。

- [LLM Wiki](wiki.html) · 九篇概念、五篇來源摘要與原文定位。另有 [Markdown 索引](wiki/index.md)。
- [RAG 是什麼？讓 AI 學會先查資料再回答](slides.html) · 十頁教學 HTML 簡報。
- [Workflow](workflow.html) · 九個節點與退回規則。[完整規格](workflow/workflow.md) · [實測紀錄與反思](workflow/report.md)。
- [來源清冊](raw/README.md) · 原文版本、取得及保存狀態。

本專案採用 Andrej Karpathy 的 LLM Wiki 做法，分開維護原始來源、可交叉連結的 Wiki 與維護規則。簡報取材自 Wiki。[LLM Wiki 方法說明](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

## 重建與檢查

在本目錄執行。建置與結構檢查使用 Python 3.11 標準函式庫。

1. Wiki 有變更時，執行 `python scripts/build_wiki.py` 和 `python scripts/lint_wiki.py`。
2. 依 Workflow 取得並覆核證據後，執行 `python scripts/validate_slides.py --cards` 和 `python scripts/validate_slides.py --drafts`。結構檢查通過後，逐頁對照 Wiki 並完成獨立忠實度審查。
3. 稿件通過 N6 後，執行 `python scripts/build_slides.py` 和 `python scripts/validate_slides.py`。
4. 使用 Edge 和 Python `websocket-client` 執行 `python scripts/check_slides_browser.py`。可用環境變數 `EDGE_PATH` 指定 Edge 執行檔。

## 靜態部署

可直接開啟 `index.html`。以 GitHub Pages 發布時，將本目錄完整作為靜態內容，保留資料夾相對位置。若從儲存庫根目錄發布，專案入口為 `rag-wiki/index.html`。本機原文副本由 Git 排除。
