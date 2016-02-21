from flask import current_app


class Aggregation:
    def __init__(self, resouce_name):
        self.resource_name = resouce_name

    def number_events(self, params: dict):
        """
        Counts the number of events performed of type event_type, grouped by horizontal_axis and optionally
        with the series

        :param horizontal_axis:
        :param event_type:
        :param series:
        :return:
        """
        number_events = API['number_events']
        for type, key in params.items():
            if type == 'filter':
                value = key['value']
                key = key['key']
            values = number_events[type][key]

    def number_devices_events(self):
        pipeline = [
            {
                '$match': {
                    '@type': 'Receive',
                    'type': 'CollectionPoint',
                }
            },
            {
                '$group': {
                    '_id': {
                        'month': {'$month': '$_created'},
                        'year': {'$year': "$_created"},
                        'receiverOrganization': {'receiverOrganization'}
                    },
                    'devices': {'$push': '$devices'},
                }
            },
            {
                '$project': {
                    '@type': 1,
                    'month': 1,
                    'year': 1,
                    'count': {'$size': 'devices'}
                }
            },
            {
                '$sort': {
                    'year': 1,
                    'month': 1
                }
            }
        ]
        return self.aggregate(pipeline)

    def aggregate(self, pipeline):
        return {'_items': current_app.data.aggregate(self.resource_name, pipeline)}

    def mix_and_aggregate(self, group, match, project, sort):
        pipeline = []
        if match:
            pipeline.append({'$match': match})
        if group:
            pipeline.append({'$group': group})
        if sort:
            pipeline.append({'$sort': sort})
        if project:
            pipeline.append({'$project': project})
        return self.aggregate(pipeline)


API = {
    'number_events': {
        'series': {
            'organization': ('toOrganization', 'fromOrganization', 'byOrganization'),
            'user': ('to', 'from', 'by'),
            'place': ('place',)
        },
        'filter': {
            '@type': ('@type',)
        },
        'xAxis': {
            '_created': ('_created',)
        }
    }
}
