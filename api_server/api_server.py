from flask import Flask, request, jsonify

app = Flask(__name__)

# Хранилище для текста
text_storage = {'text': None}

@app.route('/', methods=['GET'])
def get_text():
    '''Получить сохранённый текст'''
    if text_storage["text"] is None:
        return jsonify(message='Текста нет!'), 404
    return jsonify(text=text_storage['text'])

@app.route('/', methods=['POST'])
def create_text():
    '''Создать (установить) новый текст'''
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify(error='Отсутствует поле "text"'), 400
    text_storage['text'] = data['text']
    return jsonify(message='Текст сохранён', text=text_storage["text"]), 201

@app.route('/', methods=['PUT', 'PATCH'])
def update_text():
    '''Обновить существующий текст'''
    if text_storage['text'] is None:
        return jsonify(error='Нет текста для обновления'), 404
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify(error='Отсутствует поле "text"'), 400
    text_storage['text'] = data["text"]
    return jsonify(message='Текст обновлён', text=text_storage["text"])

@app.route('/', methods=["DELETE"])
def delete_text():
    '''Удалить текст'''
    if text_storage['text'] is None:
        return jsonify(error='Нет текста для удаления'), 404
    text_storage['text'] = None
    return jsonify(message='Текст удалён')

if __name__ == '__main__':
    app.run(debug=True)
