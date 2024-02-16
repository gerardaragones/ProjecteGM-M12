from . import api_bp
from .errors import not_found
from ..models import Status
from ..helper_json import json_response
from flask import current_app

@api_bp.route('/statuses', methods=['GET'])
def get_statues():
    statues = Status.get_all()
    data = Status.to_dict_collection(statues)
    return json_response(data)