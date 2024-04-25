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

export class PlotStyleUtils {
  public static safeWidth(e: JQuery<Element>): number | null | undefined {
    return this.getComputedStyle(e, 'width');
  }

  public static safeHeight(e: JQuery<Element>): number | null | undefined {
    return this.getComputedStyle(e, 'height');
  }

  public static outerWidth(e: JQuery<Element>, includeMargin = false): number | null {
    if (!e || e.length === 0) {
      return null;
    }
    const properties = ['width', 'padding-left', 'padding-right', 'border-left', 'border-right'];
    if (includeMargin) {
      properties.push('margin-left', 'margin-right');
    }
    return properties.map((property) => this.getComputedStyle(e, property) as number).reduce((p, c) => p + c, 0);
  }

  public static outerHeight(e: JQuery<Element>, includeMargin = false): number | null {
    if (!e || e.length === 0) {
      return null;
    }
    const properties = ['height', 'padding-top', 'padding-bottom', 'border-top', 'border-bottom'];
    if (includeMargin) {
      properties.push('margin-top', 'margin-bottom');
    }
    return properties.map((property) => this.getComputedStyle(e, property) as number).reduce((p, c) => p + c, 0);
  }

  public static convertToXHTML(html: string): string {
    const doc = document.implementation.createHTMLDocument('');
    doc.documentElement.setAttribute('xmlns', doc.documentElement.namespaceURI as string);
    doc.write(html);
    return new XMLSerializer().serializeToString(doc.body.firstChild as ChildNode);
  }

  public static getElementStyles(element: Element): string {
    let elementStyles = '';

    for (const styleSheet of <CSSStyleSheet[]>Array.from(document.styleSheets)) {
      for (const cssRule of <CSSStyleRule[]>Array.from(styleSheet.cssRules)) {
        if ((cssRule as CSSStyleRule).style) {
          try {
            const childElements = element.querySelectorAll(cssRule.selectorText);
            if (childElements.length > 0 || element.matches(cssRule.selectorText)) {
              elementStyles += `${cssRule.selectorText} { ${cssRule.style.cssText} }\n`;
            }
          } catch (err) {
            console.log(err);
          }
        }
      }
    }

    return elementStyles;
  }

  public static getActualCss(
    jqElement: JQuery<Element>,
    jqFunction: keyof JQuery,
    jqFunctionParams?: unknown,
  ): unknown {
    //to get actual size/position/etc values of hidden elements
    let value;
    const getValue = () => {
      const fn = jqElement[jqFunction] as () => unknown;
      return jqFunctionParams !== undefined ? fn.call(jqElement, jqFunctionParams) : fn.call(jqElement);
    };
    if (jqElement.is(':visible')) {
      value = getValue();
    } else {
      const hiddenParent = jqElement.parents('.ng-hide:first');
      hiddenParent.removeClass('ng-hide');
      value = getValue();
      hiddenParent.addClass('ng-hide');
    }
    return value;
  }

  private static getComputedStyle(e: JQuery<Element>, styleName: string, defaultValue = 0): number | null {
    if (!e || e.length === 0) {
      return null;
    }

    const getValue: (e: JQuery<Element>) => string = (e: JQuery<Element>) => {
      const value = window.getComputedStyle(e.get()[0], null).getPropertyValue(styleName).match(/\d+/);
      if (!value || value.length === 0) {
        return '';
      }
      return value[0];
    };

    const hiddenParent = e.parents('.ng-hide:first');
    let value;

    if (hiddenParent.length === 0) {
      value = getValue(e);
    } else {
      hiddenParent.removeClass('ng-hide');
      value = getValue(e);
      hiddenParent.addClass('ng-hide');
    }
    return parseInt(value) || defaultValue;
  }
}
