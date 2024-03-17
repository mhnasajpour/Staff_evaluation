function selectCategory() {
    window.location.href = document.getElementById("select-category").value
}

function selectUser() {
    window.location.href = `?target=${document.getElementById("select-user").value}`
}

function selectReport() {
    const period = document.getElementById("select-period").value
    const category = document.getElementById("select-category").value
    const type = document.getElementById("select-type").value
    const user = document.getElementById("select-user").value
    let result = '?'
    if (period) result += 'period=' + period + '&'
    if (category) result += 'category=' + category + '&'
    if (type) result += 'type=' + type + '&'
    if (user) result += 'user=' + user + '&'
    window.location.href = result
}

function calcTotalPoints() {
    debugger
    let total_points = 0
    const maxPoint = document.getElementById("total-points").getAttribute("max")
    const displayElement = document.getElementById("display-points")

    document.querySelectorAll('.questions-grid [type="radio"]').forEach((element) => {
        if (element.checked) total_points += element.getAttribute("point") * element.getAttribute("base")
    })
    const result = Math.round((total_points / maxPoint) * 100)

    if (result < 10 || result > 90) displayElement.classList.add("text-danger")
    else displayElement.classList.remove("text-danger")
    document.getElementById("display-points").innerText = result
}

function openModal(id) {
    document.getElementById(id).classList.remove("hidden")
    document.getElementById('overlay').classList.remove("hidden")
}

function closeModal(id) {
    document.getElementById(id).classList.add("hidden")
    document.getElementById('overlay').classList.add("hidden")
}