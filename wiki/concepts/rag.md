# RAG 定義

RAG（Retrieval-Augmented Generation，檢索增強生成）讓生成模型在回答時使用檢索到的外部資料。以校內規章為例，系統先找出和「退選期限」有關的條文，再讓模型根據條文回答。這是依流程設計的教學例子。 [S02 §II-A](../sources/S02.md) · [S03「How does RAG work?」](../sources/S03.md)

## 來源的用法差異

- [S01 §§1、2.4](../sources/S01.md) 的 RAG 是一套特定的端到端訓練架構，將預訓練生成器與 Wikipedia 段落索引結合。
- [S03「What is the difference between RAG and fine-tuning?」](../sources/S03.md) 以系統整合為主，說明既有模型可於推論時使用外部知識，也可搭配 Fine-tuning。

## 延伸閱讀

- [回 Wiki 索引](../index.md)
- [LLM 的限制](llm-limits.md)
- [RAG 運作流程](flow.md)
