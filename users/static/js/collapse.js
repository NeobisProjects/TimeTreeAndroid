(function (document) {
    document.addEventListener('readystatechange', function() {
        if (document.readyState === 'complete') {
            var collapsible = document.getElementsByClassName('collapsible');
            Array.prototype.forEach.call(collapsible, function (item) {
                item.addEventListener('click', function () {
                    item.classList.toggle('active');
                    var ul = item.getElementsByTagName('ul')[0];
                    if(item.classList.contains('active')){
                        ul.style.height = ul.scrollHeight + 'px';
                    }else{
                        ul.style.height = '0';
                    }
                });
            });
        }
    });
})(document);
