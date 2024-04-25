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

import { Notebook } from '@jupyterlab/notebook';
import { JSONArray } from '@lumino/coreutils';
import { Cell, CodeCell, CodeCellModel } from '@jupyterlab/cells';
import { PageConfig } from '@jupyterlab/coreutils';
import { BeakerXApi } from '../../utils/api';

export function sendJupyterCodeCells(notebook: Notebook, filter: string, url: string): void {
  const codeCells = <JSONArray>getCodeCellsByTag(notebook, filter).map(
    (cell: CodeCell): Record<string, unknown> => ({
      cell_type: cell.model.type,
      ...cell.model.toJSON(),
    }),
  );

  const data: { code_cells: any; url: string } = {
    code_cells: codeCells,
    url: url,
  };

  const service = new BeakerxRestHandler();
  service.post(data);
}

export function getCodeCellsByTag(notebook: Notebook, tag: string): Cell[] {
  const cells = notebook.widgets || [];

  return cells.filter((cell) => {
    // @ts-ignore: Support for both JupyterLab 3 and 4. It does not compile against JupyterLab 4.
    const tags: any = cell.model.getMetadata ? cell.model.getMetadata('tags') : cell.model.metadata.get('tags');

    return cell.model instanceof CodeCellModel && tags && tags.length && tags.includes(tag);
  });
}

export class BeakerxRestHandler {
  private api: any;

  constructor() {
    this.setApi();
  }

  private setApi() {
    let baseUrl;

    if (this.api) {
      return;
    }

    try {
      PageConfig.getOption('pageUrl');
      baseUrl = PageConfig.getBaseUrl();
    } catch (e) {
      baseUrl = `${window.location.origin}/`;
    }

    this.api = new BeakerXApi(baseUrl);
  }

  public post(data) {
    this.api.restService(data).catch((err) => {
      console.log(err);
    });
  }
}
