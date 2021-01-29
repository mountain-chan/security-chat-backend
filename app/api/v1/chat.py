import uuid

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import logger, db
from app.models import Message, User, GroupUser, Group
from app.utils import send_result, send_error, get_datetime_now, get_timestamp_now, generate_id

api = Blueprint('chats', __name__)


@api.route('/<string:group_id>', methods=['POST'])
@jwt_required
def chat(group_id):
    """ This is api for .

        Request Body:

        Returns:

        Examples::
    """

    check_user = User.get_by_id(group_id)
    if check_user:
        current_user_id = get_jwt_identity()
        receiver_id = group_id
        group_id = generate_id(current_user_id, receiver_id)
        check_group = Group.get_by_id(group_id)
        if check_group is None:
            new_group = Group(id=group_id, group_name=group_id)
            db.session.add(new_group)
            db.session.commit()

    try:
        json_data = request.get_json()
        message_hash = json_data.get('message_hash', None).strip()
    except Exception as ex:
        logger.error('{} Parameters error: '.format(get_datetime_now().strftime('%Y-%b-%d %H:%M:%S')) + str(ex))
        return send_error(message="Parameters error: " + str(ex))

    create_date = get_timestamp_now()
    _id = str(uuid.uuid1())
    new_values = Message(id=_id, message_hash=message_hash, sender_id=get_jwt_identity(), group_id=group_id,
                         create_date=create_date)
    db.session.add(new_values)
    db.session.commit()
    dt = {
        "message_id": _id
    }

    return send_result(data=dt)


@api.route('/<string:group_id>', methods=['GET'])
@jwt_required
def get(group_id):
    """ This api for .

        Returns:

        Examples::

    """
    check_user = User.get_by_id(group_id)
    if check_user:
        current_user_id = get_jwt_identity()
        receiver_id = group_id
        group_id = generate_id(current_user_id, receiver_id)

    messages = Message.get_messages(group_id)
    dt = Message.many_to_json(messages)
    return send_result(data=dt)


@api.route('/<string:message_id>', methods=['DELETE'])
@jwt_required
def delete(message_id):
    """ This is api for .

        Request Body:

        Returns:

        Examples::
    """

    Message.query.get(message_id).delete()
    return send_result()