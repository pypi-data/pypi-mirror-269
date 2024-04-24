monkeyTest = () => {
        return new Promise((resolve, reject) => {
            let callback = () => {
                gremlins.createHorde({
                    species: [gremlins.species.clicker(), gremlins.species.toucher(), gremlins.species.formFiller(), gremlins.species.scroller(), gremlins.species.typer()],
                    mogwais: [gremlins.mogwais.alert(), gremlins.mogwais.fps(), gremlins.mogwais.gizmo()],
                    strategies: [gremlins.strategies.distribution()]
                }).unleash();
                resolve(); // Resuelve la promesa cuando el callback se ejecuta exitosamente
            };

            let s = document.createElement("script");
            s.src = "https://unpkg.com/gremlins.js";
            if (s.addEventListener) {
                s.addEventListener("load", callback, false);
            } else if (s.readyState) {
                s.onreadystatechange = callback;
            }
            document.body.appendChild(s);
        });
    };