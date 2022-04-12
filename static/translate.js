// Auto translate JS module

function findTranslateNode() {
    return $(".tr");
}

function fillLanguageSelector() {
    $.post({
        url: "/api/language",
        success: function(data) {
            img = "<img height=\"50\" src=\"" + data["available"][data["current"]] + "\"/>";
            $("#languageDropdown").html(img);

            Object.entries(data["available"]).forEach(entry => {
                const [key, value] = entry;
                content = "<li><input height=\"50\" id=\"" + key + "\" type=\"image\" language=\"" + key + "\" src=\"" + value + "\"/></li>";
                selection = $("#languageDropdownOptions");
                selection.html(selection.html() + content);
            });

            Object.entries(data["available"]).forEach(entry => {
                const [key, value] = entry;
                $("#" + key).click(function() {
                    $.post({
                        url: "/api/setLanguage",
                        data: {
                            language: this.id
                        },
                        success: function(data) {
                            location.reload();
                        }
                    });
                });
            });
        }
    });
}

function translateNode(i, node) {
    node = $(node);
    $.post({
        url: "/api/translate",
        data: {
            route: window.location.pathname,
            tid: node.attr("id"),
        },
        success: function(data) {
            console.log(data);
            if (data) {
                node.html(data);
            }
        }
    });
}


$(document).ready(function() {
    nodes = $(findTranslateNode());
    nodes.each(translateNode);
    fillLanguageSelector();
});
