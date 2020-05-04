var divContent = document.getElementById("myDiv").innerHTML;
var words = query.split(" ")
for (var i = 0; i < words.length; i++) {
  divContent = divContent.replace(words[i],"<strong>" + words[i] + "</strong>");
}
document.getElementById("myDiv").innerHTML = divContent;