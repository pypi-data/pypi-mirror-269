document$.subscribe(function () {
    document.querySelectorAll('code').forEach(function (code) {
        code.setAttribute('data-executable', 'true');
    });

    var bootstrapThebe = function () {
        // the clipboard feature will clash with thebe so we remove the buttons
        document.querySelectorAll('.md-clipboard').forEach(function (button) {
            button.remove();
        });

        document.querySelectorAll('.run-code-btn').forEach(function (button) {
            button.remove();
        });

        thebelab.bootstrap();
    }

    document.querySelectorAll('div.language-python.highlight').forEach(function (div) {
        var pre = div.querySelector('pre');
        var button = document.createElement('button');
        button.classList.add('run-code-btn', 'play-btn');
        button.addEventListener('click', bootstrapThebe)
        pre.appendChild(button);
    });



    document.querySelector("#activate-interactivity").addEventListener('click', bootstrapThebe)


})
