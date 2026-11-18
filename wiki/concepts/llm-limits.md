# LLM 的限制

大型語言模型（LLM）把訓練中學到的知識存於參數。知識會受訓練資料範圍與時間限制，回答可能過時或欠缺領域細節。模型也可能產生看似合理的錯誤內容（Hallucination），而單靠回答文字難以追溯資訊來自哪裡。 [S01 §1](../sources/S01.md) · [S04「Why is Retrieval-Augmented Generation important?」](../sources/S04.md)

LLM 一次能處理的輸入有 Context Window（上下文視窗）限制。檢索系統因此需要從大量文件中挑選與問題相關的內容。 [S03「The knowledge base」](../sources/S03.md) · [S05「The challenges of RAG」](../sources/S05.md)

## 延伸閱讀

- [回 Wiki 索引](../index.md)
- [RAG 定義](rag.md)
- [RAG 的限制](limits.md)
