# RAG 運作流程

## 建立索引（Indexing）

先整理外部文件，視需求將全文切成片段，建立可搜尋的索引。向量式流程會先為每個片段建立 Embedding。 [S02 §II-A](../sources/S02.md) · [S05「Content preparation for RAG」](../sources/S05.md)

## 回答問題

- **Retrieval（檢索）**。使用問題搜尋索引，取回候選片段。 [S02 §II-A](../sources/S02.md)
- **Augmentation（增強）**。選擇需要的片段，將問題和片段組成模型的輸入。 [S03「The integration layer」](../sources/S03.md)
- **Generation（生成）**。模型根據輸入撰寫回答，應用可以附上引用。 [S03「The generator」](../sources/S03.md) · [S04「Enhanced user trust」](../sources/S04.md)

外部資料有變更時，索引也要反映更新。一個過期的索引仍可能把舊資料交給生成器。 [S04「Update external data」](../sources/S04.md)

## 延伸閱讀

- [回 Wiki 索引](../index.md)
- [Chunking（文件切分）](chunking.md)
- [Embedding（嵌入向量）](embedding.md)
- [Retrieval（檢索）](retrieval.md)
- [Generation（生成）](generation.md)
