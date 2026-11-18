# Chunking（文件切分）

Chunking 把長文件切成可獨立搜尋的片段。切分可依 token 數、句子或其他適合文件結構的邊界。切得太小容易遺失前後文，太大則可能混入無關內容並占用更多輸入空間。 [S02 §III-B.1](../sources/S02.md) · [S03「The knowledge base」](../sources/S03.md)

可以保留文件名稱、頁碼與日期等 Metadata（中繼資料），以便限制搜尋範圍及回查片段位置。 [S02 §III-B.2](../sources/S02.md)

## 延伸閱讀

- [回 Wiki 索引](../index.md)
- [RAG 運作流程](flow.md)
- [Embedding（嵌入向量）](embedding.md)
- [Retrieval（檢索）](retrieval.md)
