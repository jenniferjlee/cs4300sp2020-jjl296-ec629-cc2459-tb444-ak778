// function boldQuery() {
var divContent = document.getElementById("myDiv").innerHTML;
var words = query.split(" ")
for (var i = 0; i < words.length; i++) {
  divContent = divContent.replace(words[i],"<strong>" + words[i] + "</strong>");
}
document.getElementById("myDiv").innerHTML = divContent;
// }

// function getElements() {
//   var divContent = document.getElementById("myDiv").innerHTML;
//   divContent = divContent.replace(/asp.net/gi, "<b>asp.net</b>");
//   divContent = divContent.replace(/java/gi, "<a style=\"border-bottom-style:dashed;border-bottom-width:thin;text-decoration:none\" rel=\"speechbubble3\" class=\"addspeech\" href=\"#\">java</a>");
//   divContent = divContent.replace(/perl/gi, "<b>perl</b>");
//   document.getElementById("myDiv").innerHTML = divContent;
// }