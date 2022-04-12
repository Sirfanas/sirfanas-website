// Admin module

function toggleEditTranslation() {
    $("#buttonToggleEdiTranslation").detach();
    $(".tr").each(function(i, item) {
        item = $(item);
        content = item.html();
        text_area = $("<textarea>");
        text_area.attr("id", item.attr("id"));
        text_area.attr("name", item.attr("id"));
        text_area.attr("rows", 10);
        text_area.attr("translateNode", "yes");
        text_area.text(content);
        item.before(text_area);
        item.detach();
    });
}

function applyTranslation() {
    $("[translateNode*='yes']").each(function (i, item) {
        item = $(item);
        $.ajax({
            type: "POST",
            async: false,
            url: "/api/translate/edit",
            data: {
                route: window.location.pathname,
                tid: item.attr("id"),
                content: item.val()
            }
        })
    });
}
