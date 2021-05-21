<script>
    export let onClick = () => alert("Action was not set!");
    export let variant = "default";
</script>

<button
    class={`button ${
        variant === "info"
            ? "info"
            : variant === "warning"
            ? "warning"
            : variant === "failure"
            ? "failure"
            : ""
    }`}
    on:click={onClick}
>
    <span>
        <slot />
    </span>
</button>

<style lang="scss">
    .button {
        display: inline-block;
        border-radius: 4px;
        vertical-align: middle;
        background-color: #f4511e;
        border: none;
        color: #ffffff;
        text-align: center;
        font-size: 16px;
        padding: 15px;
        min-width: 170px;
        transition: all 0.5s;
        cursor: pointer;
        margin: 5px;

        span {
            cursor: pointer;
            display: inline-block;
            position: relative;
            transition: 0.5s;

            &:after {
                content: "\00bb";
                position: absolute;
                opacity: 0;
                top: 0;
                right: -20px;
                transition: 0.5s;
            }
        }

        &:hover {
            span {
                padding-right: 20px;
                &:after {
                    opacity: 1;
                    right: 0;
                }
            }
        }

        &.info {
            background-color: darkcyan;
        }

        &.warning {
            background-color: orange;
        }

        &.failure {
            background-color: red;
        }
    }
</style>
