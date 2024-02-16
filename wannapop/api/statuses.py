from . import api_bp
from ..models import Status
from ..helper_json import json_response

@api_bp.route('/statuses', methods=['GET'])
def get_statues():
    statues = Status.get_all()
    data = Status.to_dict_collection(statues)
    return json_response(data)