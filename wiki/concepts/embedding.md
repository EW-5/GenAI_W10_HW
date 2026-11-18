# Embedding（嵌入向量）

Embedding 是模型產生的一組數值，可用來比較內容的相似程度。例如，提問「剩幾天特休？」與條文「年度休假餘額」的字面不完全相同，向量搜尋仍可以把它們列為可能相關的內容。這是依向量檢索原理設計的教學例子。 [S03「The retriever」](../sources/S03.md) · [S05「Solving query understanding challenges」](../sources/S05.md)

原始 RAG 論文使用 DPR 的查詢編碼器和文件編碼器產生向量，再以內積比較。索引中的向量用來找候選片段，之後提供給生成模型的是片段內容。 [S01 §§2.2–2.3](../sources/S01.md)

## 延伸閱讀

- [回 Wiki 索引](../index.md)
- [Chunking（文件切分）](chunking.md)
- [Retrieval（檢索）](retrieval.md)
