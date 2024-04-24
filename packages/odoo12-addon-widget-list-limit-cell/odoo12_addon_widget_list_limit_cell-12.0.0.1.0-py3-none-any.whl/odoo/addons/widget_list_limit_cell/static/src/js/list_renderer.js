odoo.define('widget_list_limit_cell.ListRenderer', function (require) {
    "use strict";

    var ListRenderer = require('web.ListRenderer');

    ListRenderer.include({
        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            this.limit_fields = '[]';
            if (typeof this.state.getContext().limit_fields != 'undefined'){
                this.limit_fields = this.state.getContext().limit_fields;
            }

        },
        _check_height: function (element){
            $('body').append(element);
            var height = $(element).height();
            element.remove();
            return height;
        },
        _renderBodyCell: function (record, node, colIndex, options) {
            var $td = this._super.apply(this, arguments);
            if (node.attrs.name.includes(this.limit_fields)
                    && this._check_height($td) > 100){
                var $div = $('<div>', { class: 'comprimir-texto' });
                $div.append($($td).html());
                $td.html($div);
                var $fecha_abajo = $('<i>', { class: 'flecha fa fa-angle-down' });
                $fecha_abajo.on('click', this._onClickFechaAbajo.bind(this));
                $td.append($fecha_abajo);
                var $fecha_arriba = $('<i>', { class: 'flecha fa fa-angle-up d-none' });
                $fecha_arriba.on('click', this._onClickFechaArriba.bind(this));
                $td.append($fecha_arriba);
            }
            return $td;
        },
        _onClickFechaAbajo: function (event){
            event.stopPropagation();
            var $target = $(event.currentTarget);//
            $($target.parent().children()[0]).removeClass('comprimir-texto');
            var fechas = $target.parent().find('.flecha');
            $(fechas[0]).addClass('d-none');
            $(fechas[1]).removeClass('d-none');

        },
        _onClickFechaArriba: function (event){
            event.stopPropagation();
            var $target = $(event.currentTarget);
            $($target.parent().children()[0]).addClass('comprimir-texto');
            var fechas = $target.parent().find('.flecha');
            $(fechas[0]).removeClass('d-none');
            $(fechas[1]).addClass('d-none');
        },

    });

    return ListRenderer;
});
