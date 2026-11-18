# RAG 檢索增強生成入門

想知道 LLM 如何借助外部資料回答問題，可以依序閱讀下列概念。各條目中的 S01–S05 連到來源摘要，摘要提供原文連結與章節位置。

## 核心概念

- [RAG 定義](concepts/rag.md) · 把外部證據帶進生成流程
- [LLM 的限制](concepts/llm-limits.md) · 理解模型為何需要外部資料
- [RAG 運作流程](concepts/flow.md) · 從準備文件到回答問題
- [Chunking（文件切分）](concepts/chunking.md) · 選擇適合檢索的片段大小
- [Embedding（嵌入向量）](concepts/embedding.md) · 把查詢與片段轉成可比較的表示
- [Retrieval（檢索）](concepts/retrieval.md) · 理解候選排序與混合搜尋
- [Generation（生成）](concepts/generation.md) · 讓模型根據取回的內容作答
- [RAG 的應用](concepts/applications.md) · 從客服到文件問答
- [RAG 的限制](concepts/limits.md) · 從檢索、生成與營運找出失敗點

## 來源摘要

- [S01 · Lewis 等人的 RAG 原始論文](sources/S01.md)
- [S02 · Gao 等人的 RAG 綜述](sources/S02.md)
- [S03 · IBM Think 的 RAG 入門](sources/S03.md)
- [S04 · AWS 的 RAG 入門](sources/S04.md)
- [S05 · Microsoft Learn 的 RAG 指南](sources/S05.md)

## 維護紀錄

- [Ingest 與修改紀錄](log.md)
- [流程與需求](../workflow/requirements.md)
