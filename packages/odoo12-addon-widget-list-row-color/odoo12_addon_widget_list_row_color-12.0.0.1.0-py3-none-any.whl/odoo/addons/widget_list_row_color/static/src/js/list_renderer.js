odoo.define('widget_list_row_color.ListRenderer', function (require) {
    "use strict";

    var ListRenderer = require('web.ListRenderer');

    ListRenderer.include({
            /**
         * @constructor
         * @param {Widget} parent
         * @param {any} state
         * @param {Object} params
         * @param {boolean} params.hasSelectors
         */
        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            this.active_colors = false;
            if (typeof this.state.getContext().active_colors != 'undefined'){
                this.active_colors = this.state.getContext().active_colors
            }
            this.rowColor = 'color_row';
            this.backgroundRowColor = 'color_background_row';
        },

        _renderRow: function (record) {
            var self = this;

            var $tr = this._super.apply(this, arguments);

            if (this.active_colors && record.data.hasOwnProperty(this.rowColor) && record.data[this.rowColor] !== null) {
                $($tr).css("color", record.data[this.rowColor].toString());
            }

            if (this.active_colors && record.data.hasOwnProperty(this.backgroundRowColor) && record.data[this.rowColor] !== null) {
                $($tr).css("background-color", record.data[this.backgroundRowColor].toString());
            }

            return $tr;
        },
    });

    return ListRenderer;
});
