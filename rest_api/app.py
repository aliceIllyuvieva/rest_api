#!flask/bin/python
from flask import Flask, jsonify
import config
from functions import getGroupsWithMutual, getGroupsWithoutMutual
import dbd

app = Flask(__name__)

@app.route('/method_1/<substring>', methods=['GET'])
def method_1(substring):

    result = getGroupsWithMutual(config.VK_API_KEY, config.API_VERSION, config.USER_ID, substring)

    return jsonify({'groups': result})


@app.route('/method_2/<substring>', methods=['GET'])
def method_2(substring):

    session = dbd.connect()
    answer, parameters, dt = getGroupsWithoutMutual(config.VK_API_KEY, config.API_VERSION, config.USER_ID, substring)
    dbd.add_vk_parsing(dt, str(parameters), str(answer), session)

    return jsonify({'groups': answer})


@app.route('/method_3', methods=['GET'])
def method_3():
    session = dbd.connect()
    result = dbd.get_from_vk_parsing(session)

    return jsonify({'groups': result})


if __name__ == '__main__':
    app.run(debug=True)


