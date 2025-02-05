
window.onload = function () {

document.querySelectorAll('nav > a.md-tag').forEach(function(link) {
     var tag = link.textContent.trim();
     console.log(tag);
        if (tag === 'work-in-progress') {
            link.classList.add('work-in-progress');
        }
        if (tag === 'new') {
            link.classList.add('new');
        }
        if (tag === 'deprecated') {
            link.classList.add('deprecated');
        }
    });
};