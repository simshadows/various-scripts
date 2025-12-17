function manipulateTheDOM() {
    ytHeaderElement = document.querySelector("#logo")
    if (!ytHeaderElement) throw Error();

    kekElement = document.createElement("h1");
    kekElement.classList.add("simshadows-kek");
    kekElement.textContent = "kekeke";

    ytHeaderElement.prepend(kekElement)
}

manipulateTheDOM()