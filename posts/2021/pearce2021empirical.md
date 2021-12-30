---
date: 2021-12-29
category: Deep Learning
tags: Evaluation, Code Generation, NLP, Deep Learning
blogpost: true
---

# Asleep at the Keyboard? Assessing the Security of GitHub Copilot’s Code Contributions

- Paper: https://arxiv.org/pdf/2108.09293.pdf
- Codex: https://arxiv.org/pdf/2107.03374.pdf
- GitHub Copilot: https://copilot.github.com/

## Summary

[GitHub Copilot](https://copilot.github.com/) is an AI-based code completion extension available on VS code, which automatically generates code when the developer gives some programming context. It is based on Codex, a GPT-3-based lanuage model fine-tuned on code from GitHub. However, a recent research discovers that GitHub Copilot may **recommend insecure code**. Because the prediction score is evaluated to offer **the most common/likely** code snippets (instead of the code with highest quality) with the given context, as the model is trained on public open-source code that may **contain bugs or vulnerabilities**, it inevitably suggests code completion that can introduce high-risk cybersecurity weaknesses in some scenarios. 