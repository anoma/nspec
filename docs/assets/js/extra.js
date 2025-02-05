
window.onload = function () {
document.querySelectorAll('a.md-tag').forEach(function(link) {
     var tag = link.textContent.trim();
     console.log(tag);
     if (tag === 'work-in-progress') {
            console.log('work-in-progress' + link.textContent);
            link.style.backgroundColor = 'gold';
        }
        if (tag === 'new') {
            console.log('new' + link.textContent);  
            link.style.backgroundColor = 'lightgreen';
        }
        if (tag === 'deprecated') {
            console.log('deprecated' + link.textContent);
            link.style.backgroundColor = 'lightcoral';
        }
    });
};