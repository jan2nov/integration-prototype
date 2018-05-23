//
// Functions for the Scheduling Block Instance editor / form
//

// Get editor and set some defaults.
// https://github.com/ajaxorg/ace/wiki/Configuring-Ace
var editor = ace.edit("sbi-editor");
editor.setTheme("ace/theme/clouds");
editor.session.setMode("ace/mode/json");
editor.session.setTabSize(2);
editor.session.setUseSoftTabs(true);
editor.setHighlightActiveLine(false);
editor.setShowPrintMargin(false);
editor.selection.clearSelection();
editor.setOptions({
    showLineNumbers: true,
    highlightSelectedWord: true,
    showInvisibles: false,
    vScrollBarAlwaysVisible: true,
    showFoldWidgets: true
});


var templates = [
    undefined,
    {
        id: '',
        sub_array_id: 'subarray-01',
        processing_blocks: []
    }
];



var undo_manager = editor.getSession().getUndoManager();
undo_manager.reset();
editor.getSession().setUndoManager(undo_manager);

function editor_undo() {
    editor.undo();
}

function editor_redo() {
    editor.redo();
}

// Function used to Zero Pad dates
function zeroPad(num, places) {
    var zero = places - num.toString().length + 1;
    return Array(+(zero > 0 && zero)).join("0") + num;
}

// Function to display a notification.
function sbi_notify(message) {
    $("#sbi_notification").addClass("alert alert-success hidden")
        .html(message).fadeOut(0).slideDown(400).slideUp(1000);
}

function confirm_update() {
    var n = editor.getValue().length
    if (n > 0) {
        var txt;
        if (confirm("Editor already has content, replace?")) {
            return true
        } else {
            return false
        }
    }
    else {
        return true
    }
}

function get_date() {
    var date = new Date();
    var year = date.getFullYear();
    var month = zeroPad(date.getMonth(), 2);
    var day = zeroPad(date.getDate(), 2);
    return `${year}${month}${day}`
}


function get_sbi_id( callback ) {
    var url = 'http://localhost:5000/api/v1/scheduling-blocks'
    $.getJSON(url, function(json) {
        var _num_blocks = json['scheduling_blocks'].length;
        var _date = get_date();
        var _project = $("#project").val();
        var _id = `${_date}-${_project}-sbi` + zeroPad(num_blocks, 3);
        callback(_id);
    });
}


// Function to update the editor from the form and querying the REST API
function update_editor() {
//    if (confirm_update() == false) return
    var message = '... updated!';
    sbi_notify(message);
    var url = 'http://localhost:5000/api/v1/scheduling-blocks'

    $.getJSON(url, function(json) {
        var num_blocks = json['scheduling_blocks'].length
        config_str = editor.getValue();
        if (config_str.length > 0) {
            var config = JSON.parse(editor.getValue());
            if ('id' in config) {
                var _id = config['id'].split("-")
                _id[_id.length - 1] = 'sbi' + zeroPad(num_blocks, 3)
                _id = _id.join("-")
                config['id'] = _id
                editor.setValue(JSON.stringify(config, null, 2))
            }
            else {
                console.log('EEK')
            }
        } else {
            console.log('oops')
        }
    });
}


// Function to update JSON editor on changing form fields
$("#template, #num_blocks, #project").change(function()
{
    if (confirm_update() == false) return

    template = templates[$("#template")[0].selectedIndex];

    if (template != undefined)
    {
        get_sbi_id( function(_id) {
            template['id'] = _id;
            var num_blocks = $("#num_blocks").val()

            for (i = 0; i < num_blocks; i++) {
                template['processing_blocks'].push({
                    id: 'pb-' + zeroPad(i, 3)
                })
            }
            var json_doc = JSON.stringify(template, null, 2);
            console.log(json_doc);
            editor.setValue(json_doc);
            editor.selection.clearSelection();
        });
    }
    else {
        editor.setValue("");
        editor.selection.clearSelection();
    }
});

