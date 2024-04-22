/* Copyright 2024 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

class Column {
  constructor(id, size = 1, isPlaceholder = true) {
    this.id = id;
    this.size = size;
    this.isPlaceholder = isPlaceholder;
  }

  static from(other) {
    return other === null
      ? new Column(window.crypto.randomUUID())
      : new Column(other.id, other.size, other.isPlaceholder || false);
  }

  toJSON() {
    return {
      id: this.id,
      size: this.size,
    };
  }
}

class Row {
  constructor(id, columns = []) {
    this.id = id;
    this.columns = columns;
  }

  static from(other) {
    return new Row(other.id, other.columns.map((otherColumn) => Column.from(otherColumn)));
  }

  get maxColumnCount() {
    return 12;
  }

  get minColumnSize() {
    return 3;
  }

  fillWithPlaceholders() {
    for (let i = this.columns.length; i < this.maxColumnCount; ++i) {
      this.columns.push(new Column(window.crypto.randomUUID(), 1, true));
    }
  }

  restore() {
    this.columns.forEach((column, index) => {
      if (column.isPlaceholder) {
        return;
      }

      for (let i = 1; i < column.size; ++i) {
        this._toggleNextPlaceholder(index, false);
      }
    });
  }

  canInsertColumn() {
    return this._countPlaceholders(0, (i) => i < this.maxColumnCount, 1) >= this.minColumnSize;
  }

  countPlaceholders() {
    return this._countPlaceholders(0, (i) => i < this.maxColumnCount, 1);
  }

  insertColumnAt(index) {
    const column = this.columns[index];

    column.isPlaceholder = false;
    column.size = this.minColumnSize;

    for (let i = 1; i < column.size; ++i) {
      this._toggleNextPlaceholder(index, false);
    }
  }

  toJSON() {
    return {
      id: this.id,
      columns: this.columns.map((column) => (column.isPlaceholder ? null : column.toJSON())),
    };
  }

  removeColumn(column) {
    for (let i = 1; i < column.size; ++i) {
      this._toggleNextPlaceholder(this._findColumnIndex(column), true);
    }

    column.isPlaceholder = true;
    column.size = 1;
  }

  growColumn(column) {
    ++column.size;
    this._toggleNextPlaceholder(this._findColumnIndex(column), false);
  }

  shrinkColumn(column) {
    --column.size;
    this._toggleNextPlaceholder(this._findColumnIndex(column), true);
  }

  _countPlaceholders(begin, endCondition, step, consecutive = false) {
    let count = 0;

    for (let i = begin; endCondition(i); i += step) {
      if (this.columns[i].isPlaceholder && this.columns[i].size > 0) {
        ++count;
      } else if (consecutive) {
        break;
      }
    }

    return count;
  }

  _toggleNextPlaceholder(start, show = false) {
    const newSize = show ? 1 : 0;
    const predicate = show ? (size) => size === 0 : (size) => size > 0;

    const tryToggle = (i) => {
      const nextColumn = this.columns[i];

      if (nextColumn.isPlaceholder && predicate(nextColumn.size)) {
        nextColumn.size = newSize;
        return true;
      }

      return false;
    };

    for (let i = start + 1; i < this.maxColumnCount; ++i) {
      if (tryToggle(i)) {
        return;
      }
    }

    for (let i = start - 1; i >= 0; --i) {
      if (tryToggle(i)) {
        return;
      }
    }
  }

  _findColumnIndex(column) {
    return this.columns.findIndex((c) => c.id === column.id);
  }
}

class Layout {
  constructor(id, rows = []) {
    this.id = id;
    this.rows = rows;
  }

  static from(other) {
    return new Layout(other.id, other.rows.map((other) => Row.from(other)));
  }

  addRow() {
    const row = new Row(window.crypto.randomUUID());
    row.fillWithPlaceholders();

    this.rows.push(row);
  }

  removeRow(row) {
    const rowIndex = this._findRowIndexById(row.id);

    if (rowIndex < 0) {
      return;
    }

    this.rows.splice(rowIndex, 1);
  }

  toJSON() {
    return {
      id: this.id,
      rows: this.rows.map((row) => row.toJSON()),
    };
  }

  restore() {
    this.rows.forEach((row) => row.restore());
  }

  _findRowIndexById(rowId) {
    return this.rows.findIndex((row) => row.id === rowId);
  }
}

export {Layout as GridLayout, Row as GridRow, Column as GridColumn};
