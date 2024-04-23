from datetime import datetime

from models.models import User, Message, Query, Group


class SerializerDeSerializerModels:
    @staticmethod
    def user_to_json(user):
        return {
            'NAME':user.name,
            'ID': user.id,
            'EMAIL': user.email,
            'AGE': user.age,
        }

    @staticmethod
    def json_to_user(user_dict):
        user = User(name=user_dict.get('NAME', None), id=user_dict.get('ID', None),
                    email=user_dict.get('NAME', None),age=user_dict.get('AGE', None),
                    password=user_dict.get('PASSWORD_HASH', None))
        return user

    @staticmethod
    def message_to_json(message):
        return {
            'ID': message.id,
            'FROM': message.from_user,
            'TO': message.to_user,
            'GROUP': message.group,
            'CREATED_AT': message.created_at.strftime("%I:%M")
        }

    @staticmethod
    def json_to_message(message_dict):
        message = Message(id=message_dict.get('ID', None), from_user=message_dict.get('FROM', None),
                    to_user=message_dict.get('TO', None), group=message_dict.get('GROUP', None),
                    created_at=datetime.strptime(message_dict.get('CREATED_AT', None), "%I:%M").date())
        return message

    @staticmethod
    def query_to_json(query):
        return {
            'ID': query.id,
            'FROM':query.from_user,
            'TO': query.to_user,
        }

    @staticmethod
    def json_to_query(query_dict):
        query = Query(id=query_dict.get('ID', None), from_user=query_dict.get('FROM', None),
                    to_user=query_dict.get('TO', None))
        return query

    @staticmethod
    def friend_to_json(friend):
        return {
            'ID': friend.id,
            'USER1': friend.user1,
            'USER2': friend.user2,
        }

    @staticmethod
    def json_to_friend(friend_dict):
        friend = Query(id=friend_dict.get('ID', None), user1=friend_dict.get('USER1', None),
                    user2=friend_dict.get('USER2', None))
        return friend

    @staticmethod
    def group_to_json(group):
        return {
            'ID': group.id,
            'NAME': group.name,
            'OWNER': group.owner,

        }

    @staticmethod
    def json_to_group(group_dict):
        group = Group(id=group_dict.get('ID', None), name=group_dict.get('NAME', None),
                       owner=group_dict.get('OWNER', None))
        return group


