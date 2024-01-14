document.getElementById("select-category").addEventListener("change", () => {
    window.location.href = document.getElementById("select-category").value
})

document.getElementById("select-user").addEventListener("change", () => {
    window.location.href = `?target=${document.getElementById("select-user").value}`
})

function calcTotalPoints() {
    let total_points = 0
    const maxPoint = document.getElementById("total-points").getAttribute("max")
    const displayElement = document.getElementById('display-points')

    document.querySelectorAll('.questions-grid [type="radio"]').forEach((element) => {
        if (element.checked) total_points += element.getAttribute("point") * element.value
    })
    const result = Math.round(total_points / maxPoint * 100)

    if (result < 10 || result > 90)
        displayElement.classList.add('text-danger')
    else
        displayElement.classList.remove('text-danger')
    document.getElementById('display-points').innerText = result
}
