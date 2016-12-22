# -*- coding:utf-8 -*-
from flask import Blueprint, jsonify
from uuid import uuid1

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/tools/uuid/', methods=['GET','POST'])
def generate_uuid():
    return jsonify({'uuid': uuid1().__str__()})
