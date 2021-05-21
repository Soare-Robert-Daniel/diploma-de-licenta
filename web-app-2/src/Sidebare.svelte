<script>
    import Button from "./components/Button.svelte";
</script>

<div class="sidebar-form">
    <div class="option">
        <Button>Meniu Principal</Button>
    </div>
</div>

<style lang="scss">
    .sidebar-form {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 40px 5px;
        padding: 1rem;
        border: 1px solid #aaa;
        width: 100%;

        .option {
            width: 100%;
            padding: 1rem;
        }
    }
</style>
