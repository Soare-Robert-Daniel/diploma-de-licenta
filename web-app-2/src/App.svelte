<script>
	import Sidebare from "./Sidebare.svelte";
	import Board from "./Board.svelte";
	import EditorMenu from "./EditorMenu.svelte";
</script>

<main>
	<h1>Învățarea automată pentru un agent într-un mediu 2D</h1>
	<p>
		<a href="https://svelte.dev/tutorial">Documentație framework</a> |
		<a href="https://konvajs.org/docs/index.html"> Librarie grafica</a> |
		<a href="https://lodash.com/docs/4.17.15"> Lodash </a>
	</p>

	<div class="app">
		<div class="sidebar">
			<Sidebare />
		</div>
		<div class="editor">
			<EditorMenu />
			<Board />
		</div>
	</div>
</main>

<style lang="scss">
	// Telefoane
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 2rem;
		font-weight: 100;
	}

	.app {
		margin-top: 100px;
		padding: 10px;

		display: flex;
		flex-direction: row;

		.sidebar {
			min-width: 300px;
			margin-right: 100px;
		}

		.editor {
			display: flex;
			flex-direction: column;
			align-items: center;
		}
	}

	// Desktop | Tablete
	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
