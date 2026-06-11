"""
职配AI 后端服务
- 提供 /api/chat 接口，对接 Ollama 大模型
- 静态文件服务（index.html）
- 支持局域网访问

启动方式: python app.py
访问地址: http://localhost:5000 或 http://[本机IP]:5000
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# ========== 配置 ==========
OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'qwen2:7b')
PORT = int(os.environ.get('PORT', 5000))

SYSTEM_PROMPT = """你是「职配AI」的智能求职助手，专为大学生提供求职指导。
请用中文回答，风格友好、专业。

你的职责：
1. 解答求职相关疑问（简历、面试、职业规划等）
2. 分析行业趋势和岗位要求
3. 提供面试技巧和简历优化建议
4. 解释匹配算法和评分依据

回复要求：
- 简洁有条理，不超过300字
- 使用要点列表（1. 2. 3.）
- 结合当前职位库实际数据
- 不确定时诚实说明，建议用户查看具体岗位详情"""


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question', '').strip()
    if not question:
        return jsonify({'answer': '请输入您的问题'})

    payload = {
        'model': OLLAMA_MODEL,
        'messages': [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': question}
        ],
        'stream': False,
        'options': {
            'temperature': 0.7,
            'num_predict': 512
        }
    }

    try:
        resp = requests.post(
            f'{OLLAMA_HOST}/api/chat',
            json=payload,
            timeout=60
        )
        resp.raise_for_status()
        result = resp.json()
        answer = result.get('message', {}).get('content', '模型未返回有效回答')
        return jsonify({'answer': answer.strip()})
    except requests.exceptions.ConnectionError:
        return jsonify({
            'answer': '❌ 无法连接到 Ollama 服务。\n\n'
                      '请确认 Ollama 已启动：\n'
                      '1. 打开终端运行 ollama serve\n'
                      '2. 确保模型已下载：ollama pull qwen2:7b\n'
                      '3. 端口 11434 未被占用'
        }), 503
    except requests.exceptions.Timeout:
        return jsonify({'answer': '⏳ AI 思考超时，请重新提问或简化您的问题。'}), 504
    except Exception as e:
        return jsonify({'answer': f'⚠️ 服务异常：{str(e)}'}), 500


if __name__ == '__main__':
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print(f'\n{"="*50}')
    print(f'  职配AI 后端服务已启动')
    print(f'  本地访问: http://localhost:{PORT}')
    print(f'  局域网访问: http://{local_ip}:{PORT}')
    print(f'  Ollama: {OLLAMA_HOST} (模型: {OLLAMA_MODEL})')
    print(f'{"="*50}\n')

    app.run(host='0.0.0.0', port=PORT, debug=False)
