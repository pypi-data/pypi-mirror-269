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

import { PlotModelFactory } from '../PlotModelFactory';
import { PlotUtils } from '../../../utils';

export class CombinedPlotFormatter {
  static standardizeModel(model, prefs) {
    const newModel: {
      title: string;
      plots: any[];
      plotSize: { width: number; height: number };
      xAxisLabel?: string;
      yAxisLabel?: string;
    } = {
      title: model.title,
      plots: [],
      plotSize: { width: 1200, height: 600 },
    };

    const version: string = model.version === 'groovy' ? 'groovy' : 'direct';
    let width: number;
    let height: number;
    let showLegend: boolean;
    let useToolTip: boolean;

    if (version === 'groovy') {
      newModel.xAxisLabel = model.x_label;
      newModel.yAxisLabel = model.y_label;
      width = model.init_width;
      height = model.init_height;
      showLegend = model.show_legend;
      useToolTip = model.use_tool_tip;
    } else if (version === 'direct') {
      width = model.width;
      height = model.height;
      showLegend = model.showLegend;
      useToolTip = model.useToolTip;
    }

    if (width !== null) {
      newModel.plotSize.width = width;
    }
    if (height !== null) {
      newModel.plotSize.height = height;
    }

    const layout = {
      bottomLayoutMargin: 30,
    };

    let sumWeights = 0;
    let sumVMargins = 0;
    const vMargins = [];
    const weights: number[] = model.weights == null ? [] : model.weights;

    for (let i = 0; i < model.plots.length; i++) {
      if (weights[i] === null) {
        weights[i] = 1;
      }
      sumWeights += weights[i];
      if (i < model.plots.length - 1) {
        //add margins for correct height calculation
        vMargins[i] = layout.bottomLayoutMargin;
        sumVMargins += vMargins[i];
      } else {
        vMargins[i] = layout.bottomLayoutMargin + PlotUtils.fonts.labelHeight * 2;
        sumVMargins += vMargins[i];
      }
    }

    let i = 0;
    for (const plotModel of model.plots) {
      if (plotModel.version == null) {
        plotModel.version = version;
      }
      if (plotModel.showLegend == null) {
        plotModel.showLegend = showLegend;
      }
      if (plotModel.useToolTip == null) {
        plotModel.useToolTip = useToolTip;
      }

      const newPlotModel = PlotModelFactory.getPlotModel(plotModel, prefs).getStandardizedModel();

      if (i < model.plots.length - 1) {
        // turn off x coordinate labels
        newPlotModel.xAxis.label = null;
        newPlotModel.xAxis.showGridlineLabels = false;
      } else {
        newPlotModel.xAxis.label = newModel.xAxisLabel;
      }

      newPlotModel.plotSize.width = width;
      newPlotModel.plotSize.height = ((height - sumVMargins) * weights[i]) / sumWeights + vMargins[i];
      newPlotModel.auto_zoom = model.auto_zoom;

      newModel.plots.push(newPlotModel);
      i++;
    }

    return newModel;
  }
}
