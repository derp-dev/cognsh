dockerimage=https://github.com/chenhunghan/ialacol/pkgs/container/ialacol-cuda12
"""
## Quick Start

### Kubernetes

`ialacol` offer first class citizen support for Kubernetes, which means you can automate/configure everything compare to runing without.

To quickly get started with ialacol on Kubernetes, follow the steps below:

```sh
helm repo add ialacol https://chenhunghan.github.io/ialacol
helm repo update
helm install llama-2-7b-chat ialacol/ialacol
```

By defaults, it will deploy [Meta's Llama 2 Chat](https://huggingface.co/meta-llama/Llama-2-7b-chat) model quantized by [TheBloke](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML).

Port-forward

```sh
kubectl port-forward svc/llama-2-7b-chat 8000:8000
```

Chat with the default model `llama-2-7b-chat.ggmlv3.q4_0.bin` using `curl`

```sh
curl -X POST \
     -H 'Content-Type: application/json' \
     -d '{ "messages": [{"role": "user", "content": "How are you?"}], "model": "llama-2-7b-chat.ggmlv3.q4_0.bin", "stream": false}' \
     http://localhost:8000/v1/chat/completions
```

Alternatively, using OpenAI's client library (see more examples in the `examples/openai` folder).

```sh
openai -k "sk-fake" \
     -b http://localhost:8000/v1 -vvvvv \
     api chat_completions.create -m llama-2-7b-chat.ggmlv3.q4_0.bin \
     -g user "Hello world!"
```

### Run in Container

#### Image from Github Registry

There is a [image](https://github.com/chenhunghan/ialacol/pkgs/container/ialacol) hosted on ghcr.io (alternatively [CUDA11](https://github.com/chenhunghan/ialacol/pkgs/container/ialacol-cuda11),[CUDA12](https://github.com/chenhunghan/ialacol/pkgs/container/ialacol-cuda12),[METAL](https://github.com/chenhunghan/ialacol/pkgs/container/ialacol-metal),[GPTQ](https://github.com/chenhunghan/ialacol/pkgs/container/ialacol-gptq) variants).

```sh
docker run --rm -it -p 8000:8000 \
     -e DEFAULT_MODEL_HG_REPO_ID="TheBloke/Llama-2-7B-Chat-GGML" \
     -e DEFAULT_MODEL_FILE="llama-2-7b-chat.ggmlv3.q4_0.bin" \
     ghcr.io/chenhunghan/ialacol:latest
```

#### From Source

For developers/contributors

##### Python

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
DEFAULT_MODEL_HG_REPO_ID="TheBloke/stablecode-completion-alpha-3b-4k-GGML" DEFAULT_MODEL_FILE="stablecode-completion-alpha-3b-4k.ggmlv1.q4_0.bin" LOGGING_LEVEL="DEBUG" THREAD=4 uvicorn main:app --reload --host 0.0.0.0 --port 9999
```

##### Docker

Build image

```sh
docker build --file ./Dockerfile -t ialacol .
```

Run container

```sh
export DEFAULT_MODEL_HG_REPO_ID="TheBloke/orca_mini_3B-GGML"
export DEFAULT_MODEL_FILE="orca-mini-3b.ggmlv3.q4_0.bin"
docker run --rm -it -p 8000:8000 \
     -e DEFAULT_MODEL_HG_REPO_ID=$DEFAULT_MODEL_HG_REPO_ID \
     -e DEFAULT_MODEL_FILE=$DEFAULT_MODEL_FILE ialacol
```

## GPU Acceleration

To enable GPU/CUDA acceleration, you need to use the container image built for GPU and add `GPU_LAYERS` environment variable. `GPU_LAYERS` is determine by the size of your GPU memory. See the PR/discussion in [llama.cpp](https://github.com/ggerganov/llama.cpp/pull/1412) to find the best value.
### CUDA 11

- `deployment.image` = `ghcr.io/chenhunghan/ialacol-cuda11:latest`
- `deployment.env.GPU_LAYERS` is the layer to off loading to GPU.

### CUDA 12

- `deployment.image` = `ghcr.io/chenhunghan/ialacol-cuda12:latest`
- `deployment.env.GPU_LAYERS` is the layer to off loading to GPU.

Only `llama`, `falcon`, `mpt` and `gpt_bigcode`(StarCoder/StarChat) support CUDA.

#### Llama with CUDA12

```sh
helm install llama2-7b-chat-cuda12 ialacol/ialacol -f examples/values/llama2-7b-chat-cuda12.yaml
```

Deploys llama2 7b model with 40 layers offloadind to GPU. The inference is accelerated by CUDA 12.

#### StarCoderPlus with CUDA12

```sh
helm install starcoderplus-guanaco-cuda12 ialacol/ialacol -f examples/values/starcoderplus-guanaco-cuda12.yaml
```

Deploys [Starcoderplus-Guanaco-GPT4-15B-V1.0 model](https://huggingface.co/LoupGarou/Starcoderplus-Guanaco-GPT4-15B-V1.0) with 40 layers offloadind to GPU. The inference is accelerated by CUDA 12.
### GPTQ

To use GPTQ, you must

- `deployment.image` = `ghcr.io/chenhunghan/ialacol-gptq:latest`
- `deployment.env.MODEL_TYPE` = `gptq`

For example

```sh
helm install llama2-7b-chat-gptq ialacol/ialacol -f examples/values/llama2-7b-chat-gptq.yaml.yaml
```

```sh
kubectl port-forward svc/llama2-7b-chat-gptq 8000:8000
openai -k "sk-fake" -b http://localhost:8000/v1 -vvvvv api chat_completions.create -m gptq_model-4bit-128g.safetensors -g user "Hello world!"
```

## Tips

### Copilot

`ialacol` can be use as a copilot client as GitHub's Copilot is almost identical API as OpenAI completion API.

However, few things need to keep in mind:

1. Copilot client sends a lenthy prompt, to include all the related context for code completion, see [copilot-explorer](https://github.com/thakkarparth007/copilot-explorer), which give heavy load on the server, if you are trying to run `ialacol` locally, opt-in `TRUNCATE_PROMPT_LENGTH` environmental variable to truncate the prompt from the beginning to reduce the workload.

2. Copilot sends request in parallel, to increase the throughput, you probably need a queue like [text-inference-batcher](https://github.com/ialacol/text-inference-batcher).

Start two instances of ialacol:

```bash
gh repo clone chenhunghan/ialacol && cd ialacol && python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install -r requirements.txt
LOGGING_LEVEL="DEBUG"
THREAD=2
DEFAULT_MODEL_HG_REPO_ID="TheBloke/stablecode-completion-alpha-3b-4k-GGML"
DEFAULT_MODEL_FILE="stablecode-completion-alpha-3b-4k.ggmlv1.q4_0.bin"
TRUNCATE_PROMPT_LENGTH=100 # optional
uvicorn main:app --host 0.0.0.0 --port 9998
uvicorn main:app --host 0.0.0.0 --port 9999
```

Start [tib](https://github.com/ialacol/text-inference-batcher), pointing to upstream ialacol instances.

```bash
gh repo clone ialacol/text-inference-batcher && cd text-inference-batcher && npm install
UPSTREAMS="http://localhost:9998,http://localhost:9999" npm start
```

Configure VSCode Github Copilot to use [tib](https://github.com/ialacol/text-inference-batcher).

```json
"github.copilot.advanced": {
     "debug.overrideEngine": "stablecode-completion-alpha-3b-4k.ggmlv1.q4_0.bin",
     "debug.testOverrideProxyUrl": "http://localhost:8000",
     "debug.overrideProxyUrl": "http://localhost:8000"
}
```

### Creative v.s. Conservative

LLMs are known to be sensitive to parameters, the higher `temperature` leads to more "randomness" hence LLM becomes more "creative", `top_p` and `top_k` also contribute to the "randomness"

If you want to make LLM be creative.

```sh
curl -X POST \
     -H 'Content-Type: application/json' \
     -d '{ "messages": [{"role": "user", "content": "Tell me a story."}], "model": "llama-2-7b-chat.ggmlv3.q4_0.bin", "stream": false, "temperature": "2", "top_p": "1.0", "top_k": "0" }' \
     http://localhost:8000/v1/chat/completions
```

If you want to make LLM be more consistent and genereate the same result with the same input.

```sh
curl -X POST \
     -H 'Content-Type: application/json' \
     -d '{ "messages": [{"role": "user", "content": "Tell me a story."}], "model": "llama-2-7b-chat.ggmlv3.q4_0.bin", "stream": false, "temperature": "0.1", "top_p": "0.1", "top_k": "40" }' \
     http://localhost:8000/v1/chat/completions
```
"""