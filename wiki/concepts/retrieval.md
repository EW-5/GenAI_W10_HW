# Retrieval（檢索）

Retriever 從知識庫找回與問題相關的候選。例如向量搜尋可依相似度取前 k 筆（Top-k）。初步取回的候選也可以透過 Reranking（重新排序）再按相關性排列。 [S02 §§II-A、IV-A.1](../sources/S02.md) · [S03「The retriever」](../sources/S03.md)

## 來源的比較條件

- [S04「What is the difference between Retrieval-Augmented Generation and semantic search?」](../sources/S04.md) 認為只用傳統關鍵字搜尋，在知識密集任務中的效果有限。
- [S01 §4.5 Retrieval Ablations](../sources/S01.md) 在 FEVER 實驗裡觀察到 BM25 表現較佳，並指出該組聲明高度集中於實體名稱。論文中其他任務則是可學習的檢索器表現較好。
- [S05「Maximize relevance and recall」](../sources/S05.md) 在其產品情境建議 Hybrid Search（混合搜尋），合併關鍵字與向量搜尋的結果。

## 延伸閱讀

- [回 Wiki 索引](../index.md)
- [Embedding（嵌入向量）](embedding.md)
- [Generation（生成）](generation.md)
- [RAG 的限制](limits.md)
