// JavaScript File to add event handlers
/* global $ */

$("#add-tag").on("click", function (event) {
    $("<ul>").append($(".tag-input"));
    console.log("Adding another tag input");
});