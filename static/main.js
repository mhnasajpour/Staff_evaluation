document.getElementById("select-category").addEventListener("change", () => {
    window.location.href = document.getElementById("select-category").value
})

document.getElementById("select-user").addEventListener("change", () => {
    window.location.href = `?target=${document.getElementById("select-user").value}`
})