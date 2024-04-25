/*
 *  Copyright 2018 TWO SIGMA OPEN SOURCE, LLC
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

import { BEAKERX_MODULE_VERSION } from '../version';
import { BoxModel as JupyterBoxModel } from '@jupyter-widgets/controls';
import { FoldoutView } from './Foldout';

export class SparkFoldoutModel extends JupyterBoxModel {
  defaults() {
    return {
      ...super.defaults(),
      _view_name: 'SparkFoldoutView',
      _model_name: 'SparkFoldoutModel',
      _model_module: 'beakerx.spark',
      _view_module: 'beakerx.spark',
      _model_module_version: BEAKERX_MODULE_VERSION,
      _view_module_version: BEAKERX_MODULE_VERSION,
    };
  }
}

export class SparkFoldoutView extends FoldoutView {
  getPreviewContent(): HTMLElement {
    const panels = this.content.node.querySelectorAll('.bx-spark-stagePanel');

    return panels.item(panels.length - 1) as HTMLElement;
  }

  addCustomStyleToPreviewContainer(node: HTMLElement): void {
    node.classList.add('spark-foldout-preview');
  }
}
