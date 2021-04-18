<script>
	export let name;
	import Konva from "konva";
	import { onMount } from "svelte";

	let stage;

	onMount(() => {
		stage = new Konva.Stage({
			container: "konva-container", // id of container <div>
			width: 500,
			height: 500,
		});

		// add canvas element
		var layer = new Konva.Layer();
		stage.add(layer);

		// create shape
		var box = new Konva.Rect({
			x: 50,
			y: 50,
			width: 100,
			height: 50,
			fill: "#00D2FF",
			stroke: "black",
			strokeWidth: 4,
			draggable: true,
		});
		layer.add(box);

		layer.draw();

		// add cursor styling
		box.on("mouseover", function () {
			document.body.style.cursor = "pointer";
		});
		box.on("mouseout", function () {
			document.body.style.cursor = "default";
		});
	});
</script>

<main>
	<h1>The project {name}!!!</h1>
	<p>
		Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn
		how to build Svelte apps.
	</p>

	<div id="konva-container" />
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
