"use strict";

function open_fullscreen() {
    let e = document.getElementById("game-area");
    e.requestFullscreen ? e.requestFullscreen() : e.mozRequestFullScreen ? e.mozRequestFullScreen() : e.webkitRequestFullscreen ? e.webkitRequestFullscreen() : e.msRequestFullscreen && e.msRequestFullscreen()
}

$(function () {
    $("nav.greedy");
    var e, n, i, r = $("nav.greedy button"), t = $("nav.greedy .links"), a = $("nav.greedy .hidden-links"), s = 0, l = 0, c = [];

    function d() {
        e = t.width() - 10, (i = c[(n = t.children().length) - 1]) > e ? (t.children().last().prependTo(a), n -= 1, d()) : e > c[n] && (a.children().first().appendTo(t), n += 1), r.attr("count", s - n), n === s ? r.addClass("hidden") : r.removeClass("hidden")
    }

    t.children().outerWidth(function (e, n) {
        l += n, s += 1, c.push(l)
    }), $(window).resize(function () {
        d()
    }), r.on("click", function () {
        a.toggleClass("hidden")
    }), d()
});
var can_resize = !1;

function resize_game_iframe() {
    if (can_resize) {
        let e = $("iframe.game-iframe"), n = {width: Number(e.attr("width")), height: Number(e.attr("height"))}, i = n.height / n.width * 100, r = window.innerHeight / window.innerWidth * 100;
        r <= 110 ? i > 80 && (i = 80) : r >= 130 && i < 100 && (i = 100), $(".game-iframe-container").css("padding-top", i + "%")
    }
}

$("iframe#game-area").length && (can_resize = !0, resize_game_iframe()), $(document).ready(() => {
    resize_game_iframe(), $(window).resize(function () {
        resize_game_iframe()
    })
});
$(document).ready(function () {
    let games = [];
    $.getJSON('/games.json', function (data) {
        games = data;
    });
    $('#search-input').on('input', function () {
        const input = $(this).val().toLowerCase();
        const resultsContainer = $('#search-results');
        resultsContainer.empty();
        if (input.length >= 2) {
            $(".search-results").show();
            const filteredGames = games.filter(game => game.name.toLowerCase().includes(input)).slice(0, 5);
            filteredGames.forEach(game => {
                const gameElement = $('<div class="sikik_selo_liste"></div>');
                const gameImage = $('<img width="40">').attr('src', `/imgs/${game.slug.toLowerCase()}.png`).attr('alt', game.name);
                const gameLink = $('<a></a>').attr('href', '/game/' + game.slug).text(game.name);
                gameElement.append(gameImage);
                gameElement.append(gameLink);
                resultsContainer.append(gameElement);
            });
        } else {
            $(".search-results").hide();
        }
    });
});