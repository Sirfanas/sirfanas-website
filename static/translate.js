// Auto translate JS module

function findTranslateNode() {
    return $(".tr");
}

function fillLanguageSelector() {
    $.post({
        url: "/api/language",
        success: function(data) {
            img = "<img src=\"" + data["available"][data["current"]] + "\"/>";
            $("#languageDropdown").html(img);

            Object.entries(data["available"]).forEach(entry => {
                const [key, value] = entry;
                console.log(key, value);
                content = "<li><input id=\"" + key + "\" type=\"image\" language=\"" + key + "\" src=\"" + value + "\"/></li>";
                selection = $("#languageDropdownOptions");
                selection.html(selection.html() + content);
            });

            Object.entries(data["available"]).forEach(entry => {
                const [key, value] = entry;
                $("#" + key).click(function() {
                    console.log("Clicked on " + this.id);
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

function translateNode(nodeSelector) {
    node = $(nodeSelector)

    $.post({
        url: "/api/translate",
        data: {
            route: window.location.pathname,
            tid: "test",
        },
        success: function(data) {
            node.text(data);
        }
    });
}

$(document).ready(function() {
    nodes = findTranslateNode();
    translateNode(nodes);
    fillLanguageSelector();
});
