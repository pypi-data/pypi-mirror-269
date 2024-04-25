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

import $ from 'jquery';

import { Widget } from '@lumino/widgets';
import { MessageLoop } from '@lumino/messaging';

import { UIOptionsWidgetInterface } from './UIOptionsWidgetInterface';
import { OptionsWidget } from '../OptionsWidget';
import { DOMUtils } from '../../Utils';
import { IUIOptions } from '../../../utils/api';
import { UIOptionsChangedMessage } from '../../Messages';

export class UIOptionsWidget extends Widget implements UIOptionsWidgetInterface {
  public readonly AUTO_CLOSE_SELECTOR = '#auto_close';
  public readonly WIDE_CELLS_SELECTOR = '#wide_cells';
  public readonly IMPROVE_FONTS_SELECTOR = '#improve_fonts';
  public readonly SHOW_CATALOG_SELECTOR = '#show_catalog';
  public readonly AUTO_SAVE_SELECTOR = '#auto_save';

  public readonly UI_OPTIONS = [
    {
      id: 'auto_close',
      name: 'auto_close',
      label: 'Autoclose brackets',
      isLabSupported: true,
    },
    {
      id: 'wide_cells',
      name: 'wide_cells',
      label: 'Wide code cells',
      isLabSupported: false,
    },
    {
      id: 'improve_fonts',
      name: 'improve_fonts',
      label: 'Customize fonts (Roboto Mono and Lato)',
      isLabSupported: true,
    },
    {
      id: 'show_catalog',
      name: 'show_catalog',
      label: 'Show catalog button',
      isLabSupported: false,
    },
    {
      id: 'auto_save',
      name: 'auto_save',
      label: 'Autosave notebooks',
      isLabSupported: true,
    },
  ];

  public readonly HTML_ELEMENT_TEMPLATE = `
<div id="ui_options">
  <div class="form-group"></div>
</div>
`;

  public get $node(): JQuery<HTMLElement> {
    return $(this.node);
  }

  constructor(isLab: boolean) {
    super();

    this.addClass('bx-ui-options-widget');

    this.title.label = 'UI Options';
    this.title.closable = false;

    this.prepareNode(isLab);

    this.$node
      .find(
        [
          this.AUTO_CLOSE_SELECTOR,
          this.IMPROVE_FONTS_SELECTOR,
          this.WIDE_CELLS_SELECTOR,
          this.SHOW_CATALOG_SELECTOR,
          this.AUTO_SAVE_SELECTOR,
        ].join(','),
      )
      .on('change', this.optionsChangedHandler.bind(this));
  }

  public onLoad(options: IUIOptions) {
    this._options = options;

    this.setWideCells(options.wide_cells);
    this.setAutoClose(options.auto_close);
    this.setImproveFonts(options.improve_fonts);
    this.setShowCatalog(options.show_catalog);
    this.setAutoSave(options.auto_save);
  }

  protected onActivateRequest(): void {
    this._updateSize();
  }

  private prepareNode(isLab: boolean) {
    const wrapperElement = $(this.HTML_ELEMENT_TEMPLATE).find('.form-group');
    for (const option of this.UI_OPTIONS) {
      if (isLab && option.isLabSupported === false) {
        continue;
      }
      wrapperElement.append(this.createCheckbox(option));
    }
    wrapperElement.appendTo(this.node);
  }

  private createCheckbox(checkboxDefinition) {
    return $('<div>', {
      class: 'form-check',
    }).append(
      $('<input>', {
        class: 'form-check-input',
        id: checkboxDefinition.id,
        name: checkboxDefinition.name,
        type: 'checkbox',
      }),

      $('<label>', {
        class: 'form-check-label',
        for: checkboxDefinition.id,
        text: checkboxDefinition.label,
      }),
    );
  }

  private _updateSize(): void {
    const h = DOMUtils.getRealElementHeight(this.$node.find('#ui_options').get(0));

    $(this.node).height(h);
    $(this.parent.node).height(h);
    (this.parent.parent as OptionsWidget).updateDimensions();
  }

  private optionsChangedHandler(evt): void {
    this._options[evt.currentTarget.id] = evt.currentTarget.checked;

    MessageLoop.sendMessage(this.parent?.parent, new UIOptionsChangedMessage(this._options));
  }

  private setWideCells(checked: boolean) {
    this.$node.find(this.WIDE_CELLS_SELECTOR).prop('checked', checked);
  }

  private setAutoClose(checked: boolean) {
    this.$node.find(this.AUTO_CLOSE_SELECTOR).prop('checked', checked);
  }

  private setImproveFonts(checked: boolean) {
    this.$node.find(this.IMPROVE_FONTS_SELECTOR).prop('checked', checked);
  }

  private setShowCatalog(checked: boolean) {
    this.$node.find(this.SHOW_CATALOG_SELECTOR).prop('checked', checked);
  }

  private setAutoSave(checked: boolean) {
    this.$node.find(this.AUTO_SAVE_SELECTOR).prop('checked', checked);
  }

  private _options: IUIOptions;
}
