import json
from .base import BaseResource


class ReportResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(ReportResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps(self.db.reports.list(req.context['user'], req.params, self.session))

    def on_post(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps(self.db.reports.store(req.context['user'], req.params, self.session))


class ReportDetailResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(ReportDetailResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        resp.content_type = 'application/json'
        resp.body = json.dumps(self.db.reports.detail(req.context['user'], req.params, self.session))
