function plotDots() {
	const coordinatesInput = document.getElementById("coordinates");
	const coordinates = coordinatesInput.value.trim().split(" ");
	const dotPlot = document.getElementById("dot-plot");

	dotPlot.innerHTML = ""; // Clear previous dots

	for (let i = 0; i < coordinates.length; i += 2) {
		const x = parseFloat(coordinates[i]);
		const y = parseFloat(coordinates[i + 1]);

		const dot = document.createElementNS(
			"http://www.w3.org/2000/svg",
			"circle"
		);
		dot.setAttribute("cx", x);
		dot.setAttribute("cy", y);
		dot.setAttribute("r", 1);
		dot.classList.add("dot");

		dotPlot.appendChild(dot);
	}
}
