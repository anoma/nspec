/* enumerate-headings: remove "1." prefix from numbers
 * see https://github.com/timvink/mkdocs-enumerate-headings-plugin/issues/31
 */
var enumBody = document.getElementsByClassName("enumerate-headings-plugin enumerate-heading-plugin");
for (var i = 0; i < enumBody.length; i++) {
	enumBody[i].innerHTML = enumBody[i].innerHTML.replace("1.", "");
}
var enumNavi = document.getElementsByClassName("md-nav__link")
for (var i = 0; i < enumNavi.length; i++) {
	enumNavi[i].innerHTML = enumNavi[i].innerHTML.replace("1.", "");
}
