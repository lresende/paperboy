import {
    Widget, DockPanel, BoxPanel
} from '@phosphor/widgets';

import {request, RequestResult} from './request';
import {toProperCase, DomUtils, apiurl} from './utils';


export
class PrimaryForm extends Widget {
    static createNode(clz: string): HTMLElement {
        let div = document.createElement('div');
        div.classList.add(clz);
        let form = document.createElement('form');
        form.enctype = 'multipart/form-data';
        div.appendChild(form);
        return div;
    }

    constructor(clz: string, type: string){
        super({node: PrimaryForm.createNode(clz)});
        this.title.closable = false;
        this.title.label = toProperCase(clz);
        request('get', apiurl() + 'config?type=' + type).then((res: RequestResult) => {
            DomUtils.createConfigForm(this.node.querySelector('form'), type, res.json());
        });
    }
    clz: string;
    type: string;
}


export
class PrimaryDetail extends Widget {
    static createNode(type: string): HTMLElement {
        let div = document.createElement('div');
        div.classList.add('details');
        div.classList.add(type + '-detail');
        return div;
    }

    constructor(type: string, id: string){
        super({node: PrimaryDetail.createNode(type)});
        this.type = type;
        this.title.closable = true;

        request('get', apiurl() + this.type + '/details?id=' + id).then((res: RequestResult) => {
            let dat = res.json() as any;
            DomUtils.createDetail(dat, this.title, this.node);
        });
    }

    type: string;
}

export
class PrimaryTab extends DockPanel {
    constructor(clz: string, type: string){
        super();
        this.clz = clz;
        this.type = type;

        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.label = toProperCase(type);
        this.node.id = type;
        this.mine.node.classList.add('primary');
        this.node.classList.add(type);

        this.mine.title.closable = false;
        this.mine.title.label = this.title.label;

        request('get', apiurl() + type).then((res: RequestResult) => {
            DomUtils.createPrimarySection(this, type, res.json());
        });

        this.control = this.controlView();

        this.addWidget(this.mine);
        this.addWidget(this.control, {mode: 'tab-after', ref: this.mine});
    }

    controlView(): PrimaryForm {
        return new PrimaryForm(this.clz, this.type);
    }

    detailView(id: string): void {
        this.addWidget(new PrimaryDetail(this.type, id));
    }

    clz: string;
    type: string;
    mine = new BoxPanel();
    control: PrimaryForm;
}
