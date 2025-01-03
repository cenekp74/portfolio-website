document.querySelector(".navbar-icon").addEventListener("click", () => {
    document.querySelector(".navbar").classList.toggle("expanded")
})

document.querySelector(".navbar").addEventListener("click", (event) => {
    event.stopPropagation()
})

document.addEventListener("click", () => {
    document.querySelector(".navbar").classList.remove("expanded")
})