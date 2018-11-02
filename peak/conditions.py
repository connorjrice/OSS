import collections

criteria = collections.namedtuple('criteria', ['description', 'query', 'response'])


class FrontDesk(object):

    def __init__(self):
        ...

    def checkin_id(self, memberid):
        user = self.get_user_by_id(memberid)


class Criteria(object):

    def __init__(self):
        
