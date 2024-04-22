<!-- Copyright 2020 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div>
    <div ref="container">
      <confirm-dialog ref="confirmDialog"></confirm-dialog>
      <confirm-dialog :accept-text="$t('Insert')" :cancel-text="$t('Cancel')" ref="textDialog"></confirm-dialog>
      <div class="card toolbar" ref="toolbar">
        <div class="card-body px-1 py-0">
          <button type="button"
                  :title="$t('Pen')"
                  :class="toolbarBtnClasses + enabledToolClasses('pen')"
                  @click="tool = 'pen'">
            <i class="fa-solid fa-pencil"></i>
          </button>
          <button type="button"
                  :title="$t('Eraser')"
                  :class="toolbarBtnClasses + enabledToolClasses('eraser')"
                  @click="tool = 'eraser'">
            <i class="fa-solid fa-eraser"></i>
          </button>
          <button type="button"
                  :title="$t('Color picker')"
                  :class="toolbarBtnClasses + enabledToolClasses('colorpicker')"
                  @click="tool = 'colorpicker'">
            <i class="fa-solid fa-eye-dropper"></i>
          </button>
          <button type="button"
                  :title="$t('Text')"
                  :class="toolbarBtnClasses + enabledToolClasses('text')"
                  @click="tool = 'text'">
            <i class="fa-solid fa-font"></i>
          </button>
          <button type="button"
                  :title="$t('Move canvas')"
                  :class="toolbarBtnClasses + enabledToolClasses('move')"
                  @click="tool = 'move'">
            <i class="fa-solid fa-up-down-left-right"></i>
          </button>
          <button type="button" :title="$t('Reset view')" :class="toolbarBtnClasses" @click="resetView">
            <i class="fa-solid fa-eye"></i>
          </button>
          <button type="button" :title="$t('Toggle fullscreen')" :class="toolbarBtnClasses" @click="toggleFullscreen">
            <i class="fa-solid fa-expand"></i>
          </button>
          <button type="button" :title="$t('Reset canvas')" :class="toolbarBtnClasses" @click="resetCanvas">
            <i class="fa-solid fa-broom"></i>
          </button>
          <span class="color-picker" :title="$t('Color')" :style="{backgroundColor: color}" @click="pickColor">
          </span>
          <input class="color-input" type="color" v-model="color" ref="colorInput">
          <span class="d-inline-block mr-2" :title="$t('Text size')" v-if="tool === 'text'">
            <input type="range" class="range-input" min="10" max="50" step="2" v-model.number="textSize">
            <strong class="range-input-display-container">{{ textSize }}px</strong>
          </span>
          <span class="d-inline-block mr-2" :title="$t('Stroke width')" v-else>
            <input type="range" class="range-input" min="1" max="31" step="2" v-model.number="strokeWidth">
            <span class="range-input-display-container">
              <span class="stroke-width-display" :style="{'width': strokeWidth + 'px', 'height': strokeWidth + 'px'}">
              </span>
            </span>
          </span>
          <span class="d-inline-block my-1">
            <input class="form-control form-control-sm size-input"
                   :title="$t('Width')"
                   v-model.number="width"
                   @change="updateCanvasSize">
            <i class="fa-solid fa-xmark fa-sm text-muted"></i>
            <input class="form-control form-control-sm size-input"
                   :title="$t('Height')"
                   v-model.number="height"
                   @change="updateCanvasSize">
          </span>
          <button type="button" :title="$t('Reset canvas size')" :class="toolbarBtnClasses" @click="resetCanvasSize">
            <i class="fa-solid fa-rotate"></i>
          </button>
        </div>
      </div>
      <div ref="canvasContainer">
        <canvas class="canvas"
                @mousedown="mouseDown"
                @mousemove="mouseMove"
                @mouseup="pointerUp"
                @mouseout="pointerUp"
                @touchstart.prevent="touchStart"
                @touchmove.prevent="touchMove"
                @touchend.prevent="pointerUp"
                @touchcancel.prevent="pointerUp"
                ref="canvas">
        </canvas>
      </div>
      <svg class="d-none" :height="strokeWidth + 2" :width="strokeWidth + 2" ref="colorCursor">
        <circle stroke="black"
                stroke-width="1px"
                :cx="(strokeWidth / 2) + 1"
                :cy="(strokeWidth / 2) + 1"
                :r="strokeWidth / 2"
                :fill="tool === 'pen' ? color : 'white'">
        </circle>
      </svg>
      <svg class="d-none" :height="fontSize" width="7" ref="textCursor">
        <line stroke="black" stroke-width="1px" x1="3" y1="0" x2="3" :y2="fontSize"></line>
        <line stroke="black" stroke-width="3px" x1="0" y1="0" x2="6" y2="0"></line>
        <line stroke="black" stroke-width="3px" x1="0" :y1="fontSize" x2="6" :y2="fontSize"></line>
      </svg>
    </div>
    <div class="card bg-light footer">
      <small class="text-muted">
        {{ $t('Note that existing images can also be pasted into this editor using Ctrl+V.') }}
      </small>
    </div>
    <slot :canvas="memCanvas"></slot>
  </div>
</template>

<style scoped>
.border-active, .canvas {
  border: 1px solid #ced4da;
}

.color-input {
  height: 0px;
  padding: 0px;
  visibility: hidden;
  width: 0px;
  -webkit-appearance: none;
}

.color-picker {
  background-color: black;
  border: 1px solid black;
  cursor: pointer;
  display: inline-block;
  height: 25px;
  margin-left: 15px;
  margin-right: 20px;
  vertical-align: middle;
  width: 25px;
}

.footer {
  border-color: #ced4da;
  border-top-left-radius: 0px;
  border-top-right-radius: 0px;
  margin-top: -1px;
  padding: 2px 10px 2px 10px;
}

.range-input {
  vertical-align: middle;
  width: 150px;
}

.range-input-display-container {
  align-items: center;
  display: inline-flex;
  height: 30px;
  justify-content: center;
  margin-left: 10px;
  margin-right: 15px;
  vertical-align: middle;
  width: 30px;
}

.size-input {
  display: inline;
  margin-left: 5px;
  margin-right: 5px;
  width: 55px;
}

.stroke-width-display {
  background-color: black;
  border-radius: 50%;
  display: inline-block;
  vertical-align: middle;
}

.toolbar {
  border-bottom-left-radius: 0px;
  border-bottom-right-radius: 0px;
  border-color: #ced4da;
  margin-bottom: -1px;
}
</style>

<script>
export default {
  data() {
    return {
      canvas: null, // Visible canvas.
      ctx: null, // 2D drawing context of the visible canvas.
      memCanvas: null, // Actual canvas.
      memCtx: null, // 2D drawing context of the actual canvas.
      currX: 0, // Current X coordinate of the mouse while the left mouse button is down.
      currY: 0, // Current Y coordinate of the mouse while the left mouse button is down.
      prevX: 0, // Previous X coordinate of the mouse while the left mouse button was down.
      prevY: 0, // Previous Y coordinate of the mouse while the left mouse button was down.
      originX: 0, // Current X coordinate of the origin of the visible canvas in relation to the actual canvas.
      originY: 0, // Current Y coordinate of the origin of the visible canvas in relation to the actual canvas.
      width: 0, // Current width of the actual canvas.
      height: 0, // Current height of the actual canvas.
      maxSize: 10_000,
      tool: 'pen',
      color: '#000000',
      strokeWidth: 3,
      textSize: 20,
      fontSize: 0,
      points: [],
      drawing: false,
      unsavedChanges_: false,
    };
  },
  props: {
    imageUrl: {
      type: String,
      default: null,
    },
    unsavedChanges: {
      type: Boolean,
      default: false,
    },
    isRendered: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    toolbarBtnClasses() {
      return 'btn btn-link text-primary my-1';
    },
  },
  watch: {
    imageUrl() {
      this.loadImage(this.imageUrl);
    },
    unsavedChanges() {
      this.unsavedChanges_ = this.unsavedChanges;
    },
    unsavedChanges_() {
      this.$emit('unsaved-changes', this.unsavedChanges_);
    },
    isRendered() {
      this.resizeVisibleCanvas(false);
    },
    tool() {
      this.updateCursor();
    },
    color() {
      this.updateCursor();
    },
    strokeWidth() {
      this.updateCursor();
    },
    textSize() {
      this.updateTextSize();
      this.updateCursor();
    },
    width() {
      if (this.width < 1 || window.isNaN(this.width)) {
        this.width = 1;
      } else if (this.width > this.maxSize) {
        this.width = this.maxSize;
      }
    },
    height() {
      if (this.height < 1 || window.isNaN(this.height)) {
        this.height = 1;
      } else if (this.height > this.maxSize) {
        this.height = this.maxSize;
      }
    },
  },
  methods: {
    enabledToolClasses(tool) {
      return this.tool === tool ? ' border-active' : '';
    },

    loadImage(url, callback = null) {
      const image = new Image();

      image.onload = () => {
        let width = image.width;
        if (width > this.maxSize) {
          width = this.maxSize;
        }

        let height = image.height;
        if (height > this.maxSize) {
          height = this.maxSize;
        }

        this.width = this.memCanvas.width = width;
        this.height = this.memCanvas.height = height;

        this.memCtx.fillStyle = 'white';
        this.memCtx.fillRect(0, 0, this.width, this.height);
        this.memCtx.drawImage(image, 0, 0);

        this.resetView();

        if (callback) {
          callback();
        }
      };
      image.onerror = () => kadi.base.flashDanger($t('Error loading image.'));

      image.src = url;
    },

    async pasteImage(event) {
      if (!this.isRendered) {
        return;
      }

      for (const item of event.clipboardData.items) {
        const file = item.getAsFile();

        if (file && file.type === 'image/png') {
          const url = URL.createObjectURL(file);

          if (this.unsavedChanges_) {
            const msg = $t('Are you sure you want to overwrite the content of the canvas?');
            // eslint-disable-next-line no-await-in-loop
            const input = await this.$refs.confirmDialog.open(msg);

            if (!input.status) {
              return;
            }
          }

          this.loadImage(url, () => this.unsavedChanges_ = true);
          break;
        }
      }
    },

    resetView() {
      this.originX = -Math.round(Math.max(this.canvas.width - this.memCanvas.width, 0) / 2);
      this.originY = -Math.round(Math.max(this.canvas.height - this.memCanvas.height, 0) / 2);
      this.redrawVisibleCanvas();
    },

    toggleFullscreen() {
      kadi.utils.toggleFullscreen(this.$refs.container);
    },

    async resetCanvas() {
      const input = await this.$refs.confirmDialog.open($t('Are you sure you want to reset the canvas?'));

      if (!input.status) {
        return;
      }

      this.clearCanvas(true);
      this.unsavedChanges_ = false;
    },

    pickColor() {
      this.$refs.colorInput.click();
    },

    async resetCanvasSize() {
      const input = await this.$refs.confirmDialog.open($t('Are you sure you want to reset the size of the canvas?'));

      if (!input.status) {
        return;
      }

      this.width = this.canvas.width;
      this.height = this.canvas.height;

      this.updateCanvasSize();
      this.resetView();
    },

    updateCanvasSize() {
      const imageData = this.memCtx.getImageData(0, 0, this.memCanvas.width, this.memCanvas.height);
      this.memCanvas.width = this.width;
      this.memCanvas.height = this.height;

      this.memCtx.fillStyle = 'white';
      this.memCtx.fillRect(0, 0, this.width, this.height);
      this.memCtx.putImageData(imageData, 0, 0);

      this.redrawVisibleCanvas();
      this.unsavedChanges_ = true;
    },

    updateTextSize(calculateFontSize = true) {
      this.ctx.font = `${this.textSize}px Arial, sans-serif`;

      if (calculateFontSize) {
        const metrics = this.ctx.measureText('A');
        this.fontSize = Math.round(metrics.actualBoundingBoxAscent + metrics.actualBoundingBoxDescent);
      }
    },

    updateCoordinates(x, y) {
      this.prevX = this.currX;
      this.prevY = this.currY;
      this.currX = x - this.canvas.getBoundingClientRect().left;
      this.currY = y - this.canvas.getBoundingClientRect().top;
    },

    async updateCursor() {
      await this.$nextTick();

      let cursor = 'default';
      const svgPrefix = 'url("data:image/svg+xml;base64,';

      if (['pen', 'eraser'].includes(this.tool)) {
        const data = window.btoa(new XMLSerializer().serializeToString(this.$refs.colorCursor));
        cursor = `${svgPrefix}${data}") ${this.strokeWidth / 2} ${this.strokeWidth / 2}, auto`;
      } else if (this.tool === 'move') {
        cursor = 'move';
      } else if (this.tool === 'text') {
        const data = window.btoa(new XMLSerializer().serializeToString(this.$refs.textCursor));
        cursor = `${svgPrefix}${data}") 0 ${this.fontSize}, auto`;
      }

      this.$refs.canvasContainer.style.cursor = cursor;
    },

    getCurrentPixelColor() {
      const data = this.ctx.getImageData(this.currX, this.currY, 1, 1).data;
      // eslint-disable-next-line no-bitwise
      return `#${(`000000${((data[0] << 16) | (data[1] << 8) | data[2]).toString(16)}`).slice(-6)}`;
    },

    draw() {
      // Reset the visible canvas to its previous state before drawing the points again.
      this.redrawVisibleCanvas();

      this.points.push({x: this.currX, y: this.currY});

      this.drawPoints();
      this.drawLimits();

      this.unsavedChanges_ = true;
    },

    drawPoints() {
      if (this.tool === 'pen') {
        this.ctx.strokeStyle = this.color;
        this.ctx.fillStyle = this.color;
      } else {
        this.ctx.strokeStyle = 'white';
        this.ctx.fillStyle = 'white';
      }

      this.ctx.lineWidth = this.strokeWidth;
      this.ctx.lineJoin = 'round';
      this.ctx.lineCap = 'round';

      this.ctx.beginPath();

      // Draw a single circle until we have enough points.
      if (this.points.length < 4) {
        this.ctx.arc(this.points[0].x, this.points[0].y, this.strokeWidth / 2, 0, 2 * Math.PI);
        this.ctx.fill();
        return;
      }

      // Taken from https://stackoverflow.com/a/7058606
      let i = 0;
      this.ctx.moveTo(this.points[0].x, this.points[0].y);

      for (i = 1; i < this.points.length - 2; i++) {
        const avgX = (this.points[i].x + this.points[i + 1].x) / 2;
        const avgY = (this.points[i].y + this.points[i + 1].y) / 2;
        this.ctx.quadraticCurveTo(this.points[i].x, this.points[i].y, avgX, avgY);
      }

      this.ctx.quadraticCurveTo(this.points[i].x, this.points[i].y, this.points[i + 1].x, this.points[i + 1].y);
      this.ctx.stroke();
    },

    drawLimits() {
      const bottomEdge = this.memCanvas.height - this.originY;
      const rightEdge = this.memCanvas.width - this.originX;

      this.ctx.fillStyle = '#ced4da';
      this.ctx.fillRect(0, 0, -this.originX, this.canvas.height);
      this.ctx.fillRect(0, 0, this.canvas.width, -this.originY);
      this.ctx.fillRect(0, bottomEdge, this.canvas.width, this.canvas.height - bottomEdge);
      this.ctx.fillRect(rightEdge, 0, this.canvas.width - rightEdge, this.canvas.height);
    },

    async drawText() {
      const input = await this.$refs.textDialog.open($t('Enter the text to insert:'), true);
      const text = input.prompt.trim();

      if (!input.status || !text) {
        return;
      }

      this.updateTextSize(false);
      this.ctx.fillStyle = this.color;
      this.ctx.fillText(text, this.currX, this.currY);

      this.persistCanvas();
      this.drawLimits();

      this.unsavedChanges_ = true;
    },

    persistCanvas() {
      this.memCtx.clearRect(this.originX, this.originY, this.canvas.width, this.canvas.height);
      this.memCtx.drawImage(
        this.canvas,
        0,
        0,
        this.canvas.width,
        this.canvas.height,
        this.originX,
        this.originY,
        this.canvas.width,
        this.canvas.height,
      );
    },

    clearCanvas(resize = false) {
      if (resize) {
        this.resizeVisibleCanvas();
        this.width = this.memCanvas.width = this.canvas.width;
        this.height = this.memCanvas.height = this.canvas.height;
      }

      this.memCtx.fillStyle = 'white';
      this.memCtx.fillRect(0, 0, this.memCanvas.width, this.memCanvas.height);
      this.resetView();
    },

    redrawVisibleCanvas() {
      this.ctx.drawImage(
        this.memCanvas,
        this.originX,
        this.originY,
        this.canvas.width,
        this.canvas.height,
        0,
        0,
        this.canvas.width,
        this.canvas.height,
      );
      this.drawLimits();
    },

    resizeVisibleCanvas(resetView = true) {
      if (!this.isRendered) {
        return;
      }

      const toolbar = this.$refs.toolbar;
      const container = this.$refs.container;

      this.canvas.width = Math.round(container.getBoundingClientRect().width) - 2;

      if (kadi.utils.isFullscreen()) {
        const containerHeight = Math.round(container.getBoundingClientRect().height);
        const toolbarHeight = Math.round(toolbar.getBoundingClientRect().height);

        this.canvas.height = Math.max(containerHeight - toolbarHeight - 1, 1);
        toolbar.style.borderTopLeftRadius = toolbar.style.borderTopRightRadius = '0';
      } else {
        this.canvas.height = Math.round(window.innerHeight / window.innerWidth * this.canvas.width);
        toolbar.style.borderTopLeftRadius = toolbar.style.borderTopRightRadius = '0.25rem';
      }

      this.$refs.canvasContainer.style.height = `${this.canvas.height + 2}px`;

      if (resetView) {
        this.resetView();
      } else {
        this.redrawVisibleCanvas();
      }
    },

    pointerDown() {
      this.drawing = true;

      if (['pen', 'eraser'].includes(this.tool)) {
        this.draw();
      } else if (this.tool === 'colorpicker') {
        this.color = this.getCurrentPixelColor();
      } else if (this.tool === 'text') {
        this.drawText();
      }
    },

    mouseDown(event) {
      this.updateCoordinates(event.clientX, event.clientY);
      this.pointerDown();
    },

    touchStart(event) {
      const touch = event.touches[0];
      this.updateCoordinates(touch.clientX, touch.clientY);
      this.pointerDown();
    },

    pointerMove() {
      if (['pen', 'eraser'].includes(this.tool)) {
        this.draw();
      } else if (this.tool === 'colorpicker') {
        this.color = this.getCurrentPixelColor();
      } else if (this.tool === 'move') {
        this.originX -= this.currX - this.prevX;
        this.originY -= this.currY - this.prevY;
        this.redrawVisibleCanvas();
      }
    },

    mouseMove(event) {
      if (!this.drawing) {
        return;
      }

      this.updateCoordinates(event.clientX, event.clientY);
      this.pointerMove();
    },

    touchMove(event) {
      if (!this.drawing) {
        return;
      }

      const touch = event.touches[0];

      this.updateCoordinates(touch.clientX, touch.clientY);
      this.pointerMove();
    },

    pointerUp() {
      if (this.drawing && ['pen', 'eraser'].includes(this.tool)) {
        this.persistCanvas();
      }

      this.drawing = false;
      this.points = [];
    },

    beforeUnload(e) {
      if (this.unsavedChanges_) {
        e.preventDefault();
        return '';
      }
      return null;
    },
  },
  mounted() {
    this.canvas = this.$refs.canvas;
    // Enabling 'willReadFrequently' seems to get rid of blank pixels sometimes appearing when drawing.
    this.ctx = this.canvas.getContext('2d', {willReadFrequently: true});
    this.memCanvas = document.createElement('canvas');
    this.memCtx = this.memCanvas.getContext('2d');

    this.resizeVisibleCanvas();
    // The initial size of the actual canvas is based on the visible canvas.
    this.width = this.memCanvas.width = this.canvas.width;
    this.height = this.memCanvas.height = this.canvas.height;

    this.clearCanvas();
    this.updateTextSize();
    this.updateCursor();

    if (this.imageUrl) {
      this.loadImage(this.imageUrl);
    }

    window.addEventListener('resize', this.resizeVisibleCanvas);
    window.addEventListener('paste', this.pasteImage);
    window.addEventListener('beforeunload', this.beforeUnload);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeVisibleCanvas);
    window.removeEventListener('paste', this.pasteImage);
    window.removeEventListener('beforeunload', this.beforeUnload);
  },
};
</script>
