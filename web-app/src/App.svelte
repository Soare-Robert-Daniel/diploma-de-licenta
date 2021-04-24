<script>
	import Dashboard from "./Dashboard.svelte";
	import Container from "./Container.svelte";
</script>

<main>
	<h1>Învățarea automată pentru un agent într-un mediu 2D</h1>
	<p>
		<a href="https://svelte.dev/tutorial">Documentație framework</a> |
		<a href="https://konvajs.org/docs/index.html"> Librarie grafica</a> |
		<a href="https://lodash.com/docs/4.17.15"> Lodash </a>
	</p>

	<div class="main-container">
		<Dashboard />
		<Container />
	</div>
</main>

<style lang="scss">
	// Telefoane
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;

		.main-container {
			display: flex;
			flex-direction: column;
		}
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 2rem;
		font-weight: 100;
	}

	// Desktop | Tablete
	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
