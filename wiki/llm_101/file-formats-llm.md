---
type: concept
summary: Formats binaires pour stocker les weights — safetensors, GGUF, ONNX, EXL2/GPTQ/AWQ, TensorRT engines. Choix lié au runtime, pas cosmétique.
lifecycle: verified
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
  - raw/web/gpu-memory-math-for-llms-2026.md
tags:
  - file-formats
  - safetensors
  - local-llm-deployment
---

Le choix du format de weights **détermine quelles runtimes peuvent loader le modèle, quelles quantizations sont possibles, et la vitesse d'exécution**. Ce n'est pas cosmétique.

## Sécurité d'abord : safetensors vs .bin pickle

**safetensors** — format de sérialisation tensors *sans* Python pickle. Préférer pour tout PyTorch/Transformers.

**.bin** files (pickle-based) — peuvent **exécuter du code arbitraire à la deserialization**. Loader un fichier random depuis une source non vérifiée = RCE potentielle.

> *Do not let a stranger's model file become a stranger's code execution.*

Règle : **safetensors ou GGUF depuis source réputable** par défaut. Pas de `trust_remote_code=True` casual.

## Les principaux formats

| Format | Écosystème principal | Use case |
|---|---|---|
| **safetensors** | PyTorch / Transformers, vLLM, SGLang | Standard sûr, le plus portable |
| **GGUF** | llama.cpp, LM Studio | CPU inference, Apple Silicon, desktop, quantized portables — embarque tokenizer + template + config dans un seul fichier |
| **ONNX** | déploiement standardisé, accélérateurs hardware (Intel NPU, ARM, custom) | Hors stack PyTorch classique |
| **TensorRT engines** | TensorRT-LLM, NVIDIA prod | Throughput max sur NVIDIA — conversion préalable longue mais excellente perf |
| **EXL2 / GPTQ / AWQ** | ExLlama, AutoGPTQ — communautés GPU local | Squeeze de gros modèles sur un seul GPU |

## Format ↔ runtime

Le runtime contraint le format :
- [[llama-cpp]] → **GGUF**
- [[vllm]] / [[sglang]] → **safetensors** ou HF checkpoints (+ GGUF, GPTQ, AWQ, FP8/FP4 selon hardware)
- [[tensorrt-llm]] → **ONNX** ou engines optimisés (conversion préalable)
- ExLlamaV2/V3 / TabbyAPI → **EXL2 / EXL3** principalement
- MLX / MLX-LM → formats MLX (HF Hub integration)

**Choisir le runtime d'abord, trouver les modèles dans le bon format ensuite.**

## Caveat important : GGUF est runtime-specific

GGUF est optimisé pour [[llama-cpp]] (CPU+GPU hybrid, ultra-efficient memory). Les chiffres de "fit en X GB" **ne tiennent que dans ce runtime**. Charger un GGUF dans un autre engine peut entraîner dequantization à la volée → mémoire qui explose. Voir [[ahmad-osman-gpu-memory-math-2026]].

## Related

- [[llm-runtimes]] — chaque runtime locke un format ou deux
- [[quantization-llm]] — les formats EXL2/GPTQ/AWQ implémentent des schémas spécifiques
- [[model-package]] — les weights ne sont qu'une pièce du package
- [[vllm]], [[sglang]], [[tensorrt-llm]], [[llama-cpp]] — les engines clés et leurs formats
- [[mlx]] — formats MLX (HF Hub integration)
- [[exllamav2]], [[exllamav3]] — formats EXL2/EXL3
- [[mlc-llm]] — formats compilés cross-platform
- [[ahmad-osman-inference-engines-2026]] — taxonomie engines / formats
- [[ahmad-osman-gpu-memory-math-2026]] — GGUF runtime-specific

## My take

Page utile en référence rapide. Le piège classique : prendre un GGUF parce que c'est le format le plus visible sur HF, puis vouloir l'utiliser dans vLLM (qui ne le supporte pas). L'ordre runtime → format évite ça.
