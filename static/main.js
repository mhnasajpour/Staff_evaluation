function selectCategory() {
    window.location.href = document.getElementById("select-category").value
}

function selectUser() {
    window.location.href = `?target=${document.getElementById("select-user").value}`
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