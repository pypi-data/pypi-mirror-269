/*
 *  Copyright 2017 TWO SIGMA OPEN SOURCE, LLC
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

/* eslint-disable @typescript-eslint/no-explicit-any */

import { CheckboxModel as JupyterCheckboxModel, CheckboxView as JupyterCheckboxView } from '@jupyter-widgets/controls';
import { BEAKERX_MODULE_VERSION } from '../../version';

export class CheckboxModel extends JupyterCheckboxModel {
  defaults(): any {
    return {
      ...super.defaults(),
      _view_name: 'CheckboxView',
      _model_name: 'CheckboxModel',
      _model_module: 'beakerx.forms',
      _view_module: 'beakerx.forms',
      _model_module_version: BEAKERX_MODULE_VERSION,
      _view_module_version: BEAKERX_MODULE_VERSION,
    };
  }
}

export class CheckboxView extends JupyterCheckboxView {
  render(): void {
    super.render();

    // Override rendering for standalone checkbox
    try {
      if (this.options.parent.model.name === 'EasyFormModel') {
        this.renderSingle();
      }
    } catch (e) {
      console.log(e);
    }
  }

  renderSingle(): void {
    this.el.removeChild(this.checkboxLabel);

    // checkbox
    this.checkbox.setAttribute('id', this.model.model_id);
    this.checkbox.classList.add('checkbox');
    this.el.appendChild(this.checkbox);
    this.label.innerHTML = '';
    this.label.appendChild(this.descriptionSpan);
    this.label.setAttribute('for', this.model.model_id);

    this.update(); // Set defaults.
    this.updateDescription();
    this.updateIndent();
  }
}
