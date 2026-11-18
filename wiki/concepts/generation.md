# Generation（生成）

生成階段將問題與選出的片段交給 LLM，形成 Augmented Prompt（增強提示）。例如詢問退選期限時，模型可用取回的條文組織答案，應用可保留條文的連結供查核。 [S03「The integration layer」與「The generator」](../sources/S03.md) · [S04「Enhanced user trust」](../sources/S04.md)

候選太多可能稀釋關鍵資訊。生成前可透過 Reranking、片段篩選或壓縮，決定哪些證據送入模型。檢查輸出時，可以分別看 Answer Relevance（回答是否切題）與 Faithfulness（回答是否忠實於提供的證據）。 [S02 §§IV-A、VI-C.1](../sources/S02.md)

## 延伸閱讀

- [回 Wiki 索引](../index.md)
- [RAG 運作流程](flow.md)
- [Retrieval（檢索）](retrieval.md)
- [RAG 的限制](limits.md)
