# LLM Wiki 維護規則

- 以繁體中文寫給 RAG 初學者，保留常見英文術語。
- 先閱讀原始正文，記錄版本、網址、存取狀態與保存方式至 raw/。合法本機副本放在 raw/local/，公開 Git 只追蹤允許發布的內容。
- 逐篇建立 wiki/sources/SNN.md。來源頁使用「原始文件」連結及「Ingest 狀態：完成」欄位。取得或閱讀失敗時記錄原因，並在成功前維持未完成狀態。
- 完成單篇摘要後再整合 wiki/concepts/。重要主張使用相對連結指向來源頁，如 [S01 §2.2](wiki/sources/S01.md)，並保留原文章節或頁碼。來源頁提供原文入口及對應章節。
- 若來源主張衝突，並列原文依據及各自情境，不自行裁定。新增或修改 Wiki 頁面時更新 wiki/index.md 及 wiki/log.md。
- Wiki Markdown 以一級標題、二級標題、段落、無序清單與標準連結為主。更新 Wiki HTML 時執行 python scripts/build_wiki.py，再執行 python scripts/lint_wiki.py。將實際結果寫入 workflow/report.md，最多三輪。
- 簡報以 Wiki 為唯一知識來源。依 [簡報 Workflow](workflow/workflow.md) 逐關執行，N6 通過後才生成 HTML。
- 網站使用相對路徑及原生 HTML、CSS、JavaScript。
