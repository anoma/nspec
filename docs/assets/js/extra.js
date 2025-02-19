
document.querySelectorAll('a.md-tag').forEach(function(link) {
     var tag = link.textContent.trim();
     if (tag === 'work-in-progress') {
            console.log('work-in-progress' + link.textContent);
            link.style.backgroundColor = 'gold';
            link.style.color = 'black';
        }
        if (tag === 'new') {
            console.log('new' + link.textContent);
            link.style.backgroundColor = 'lightgreen';
            link.style.color = 'black';
        }
        if (tag === 'deprecated') {
            console.log('deprecated' + link.textContent);
            link.style.backgroundColor = 'lightcoral';
            link.style.color = 'black';
        }
    });