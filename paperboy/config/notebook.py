from six.moves.urllib_parse import urljoin
from datetime import datetime
from traitlets import HasTraits, Unicode, Int, Instance
from .forms import Response, FormEntry, DOMEntry
from .base import Base, _SERVICE_LEVELS, _PRIVACY_LEVELS


class NotebookMetadata(HasTraits):
    username = Unicode()
    userid = Unicode()

    notebook = Unicode()
    privacy = Unicode()
    level = Unicode()
    requirements = Unicode(allow_none=True)
    dockerfile = Unicode(allow_none=True)

    jobs = Int()
    reports = Int()

    created = Instance(datetime)
    modified = Instance(datetime)

    def to_json(self, include_notebook=False):
        ret = {}
        ret['username'] = self.username
        # ret['userid'] = self.userid
        if include_notebook:
            ret['notebook'] = self.notebook
        ret['privacy'] = self.privacy
        ret['level'] = self.level
        ret['jobs'] = self.jobs
        ret['reports'] = self.reports
        ret['created'] = self.created.strftime('%m/%d/%Y %H:%M:%S')
        ret['modified'] = self.modified.strftime('%m/%d/%Y %H:%M:%S')
        return ret

    @staticmethod
    def from_json(jsn):
        ret = NotebookMetadata()
        for k, v in jsn.items():
            if k in ('created', 'modified'):
                ret.set_trait(k, datetime.strptime(v, '%m/%d/%Y %H:%M:%S'))
            else:
                ret.set_trait(k, v)
        return ret


class Notebook(Base):
    name = Unicode()
    id = Unicode()
    meta = Instance(NotebookMetadata)

    def to_json(self, include_notebook=False):
        ret = {}
        ret['name'] = self.name
        ret['id'] = self.id
        ret['meta'] = self.meta.to_json(include_notebook)
        return ret

    def form(self):
        f = Response()
        f.entries = [
            FormEntry(name='file', type='file', label='File', required=True),
            FormEntry(name='name', type='text', label='Name', placeholder='Name for Notebook...', required=True),
            FormEntry(name='privacy', type='select', label='Privacy', options=_PRIVACY_LEVELS, required=True),
            FormEntry(name='level', type='select', label='level', options=_SERVICE_LEVELS, required=True),
            FormEntry(name='build', type='label', label='Build options'),
            FormEntry(name='requirements', type='file', label='requirements.txt', required=False),
            FormEntry(name='dockerfile', type='file', label='Dockerfile', required=False),
            FormEntry(name='submit', type='submit', value='Create', url=urljoin(self.config.apiurl, 'notebooks')),
        ]
        return f.to_json()

    @staticmethod
    def from_json(jsn, config):
        ret = Notebook(config)
        ret.name = jsn.pop('name')
        ret.id = jsn.pop('id')

        if 'meta' in jsn:
            ret.meta = NotebookMetadata.from_json(jsn['meta'])
        else:
            ret.meta = NotebookMetadata.from_json(jsn)

        return ret

    def edit(self):
        f = Response()
        f.entries = [
            FormEntry(name='name', type='text', value=self.name, placeholder='Name for Job...', required=True),
            FormEntry(name='privacy', type='select', value=self.meta.privacy, label='Visibility', options=_PRIVACY_LEVELS, required=True),
            FormEntry(name='level', type='select', value=self.meta.level, label='Level', options=_SERVICE_LEVELS, required=True),
            FormEntry(name='notebook', type='json', value=self.meta.notebook, placeholder='Notebook json...', required=True)
        ]
        if self.meta.requirements:
            f.entries.append(FormEntry(name='requirements', type='textarea', value=self.meta.requirements, label='requirements.txt', required=False))
        if self.meta.dockerfile:
            f.entries.append(FormEntry(name='dockerfile', type='textarea', value=self.meta.dockerfile, label='Dockerfile', required=False))

        f.entries.append(FormEntry(name='save', type='submit', value='save', url=urljoin(self.config.apiurl, 'notebooks')))
        return f.to_json()

    def store(self):
        ret = Response()
        ret.entries = [
            DOMEntry(type='p', value='Success!'),
            DOMEntry(type='p', value='Successfully stored notebook: {}'.format(self.name)),
        ]
        return ret.to_json()
