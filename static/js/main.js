
CUR_CONTENT_NAME = ""

function load_items(content_name, cur_template_items) {
    var cur_template_name = content_name + "_template";
    var item_eg = $("#" + cur_template_name + " .item_eg").first();
    for (var item_index in cur_template_items) {
        var item_row = item_eg.clone(true);
        var item_conf = cur_template_items[item_index];
        
        item_row.find(".item_val").each(function (){
            var item_var_type = $(this).attr("val");
            var icon = $(this).children(".glyphicon").first();
            if (icon.length == 0)
                $(this).html(item_conf[item_var_type]);
            else {
                for (var cnt=0; cnt < item_conf[item_var_type]; cnt++) {
                    $(this).append(icon.clone());
                }
            }
        });
        $("#" + cur_template_name + " .items").prepend(item_row);
        item_row.show();
    }    
}


function save_want_todo() {
    var title = $('#want_todo_title').val();
    var total_score = $('#want_todo_total_score').val();
    if (title.length == 0 || total_score.length == 0)
        return;
    var post_data = {
        'title': title,
        'total_score': total_score
    }
    $.post("/add_want_todo", post_data, function(data) {
        load_items("want_todo", data);
        $('#wantodoModal').modal('hide');
    },
    "json"
    );
}

function show_content(content_name, content_status) {
    
    var cur_template_name = content_name + "_template";
    var cur_template_items = null;
    // 不存在此 conten_template 下载之
    if($("#" + cur_template_name).length == 0) {
        $.get("/show_" + cur_template_name, function (data) {
            // 加载 content_template
            $("#content").append(data);
            // 下载 content_items
            $.getJSON("/show_" + content_name + "_items/" + content_status, function (data) {
                cur_template_items = data;
                // 加载 content_items
                load_items(content_name, cur_template_items);
                

            });
        });
    }
    
    // 其他 ccontent template hide
    $("#content").children().each(function() {
        if ($(this)[0].id == cur_template_name) {
            $(this).show();
        }
        else
            $(this).hide();
        
    });

    CUR_CONTENT_NAME = content_name;


}


function show_content_items(content_name, content_status) {
    $.get("/show_" + content_name + "/" + content_status, function (data) {
        $("#content").html(data);

    });
}

$("#my_list li").click(function () {
    var flag = $(this).attr("flag");
    var this_li = this;
    $("#my_list li").each(function() {
        if (this == this_li) {
            $(this).addClass("active");
            show_content(flag, '0');
        }
        else
            $(this).removeClass("active");
    });
});

function save_memory() {
    var title = $('#memory_title').val();
    var score = $('#memory_score').val();
    if (title.length == 0 || score.length == 0)
        return;
    var post_data = {
        'title': title,
        'score': score
    }

    $.post("/add_memory", post_data, function(data) {
        load_items("memory", data);
        $('#memoryModal').modal('hide');
    },
    "json"
    );
}

$(function () {
    show_content('want_todo', '0');
});

