# my-test-agnet

基于 LangGraph + DeepAgents 的本地 Ollama Agent。内置两个示例工具：获取日本时间与加法运算。

## 功能

- 本地 Ollama 模型推理
- 工具调用：`now_jst`、`add`
- LangGraph 入口：`my_agent/agent.py:graph`

## 依赖

- Python 3.13+
- 可用的 Ollama 服务
- Poetry（可选，用于安装依赖）

## 安装

```bash
poetry install
```

或使用 pip：

```bash
python -m pip install -e .
```

## 配置

通过环境变量覆盖模型与服务地址：

- `OLLAMA_MODEL`：默认 `qwen3:8b`
- `OLLAMA_BASE_URL`：例如 `http://127.0.0.1:11434`

## 运行（LangGraph Server）

```bash
# 启动本地 LangGraph Server（默认读取 langgraph.json）
langgraph dev
```

`langgraph.json` 中的 `agent` 指向 `my_agent/agent.py:graph`。启动后按终端提示访问本地服务地址（可用于 LangGraph Studio / SDK / HTTP 调用）。

## 本地调用（可选）

```bash
python - <<'PY'
from my_agent.agent import graph

result = graph.invoke(
    {"messages": [{"role": "user", "content": "现在日本时间是多少？顺便算一下 2+3。"}]}
)
print(result)
PY
```
