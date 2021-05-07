<script>
    export let isChecked = false;
    export let text = "Placeholder";
    export let onChange = () => {};

    $: onChange(isChecked);
</script>

<div class={isChecked ? "checked" : ""}>
    <label>
        <input type="checkbox" bind:checked={isChecked} />
        <span class="checkmark" />
        {text}
    </label>
</div>

<style lang="scss">
    div {
        display: block;
        border: 3px solid #ddd;
        border-radius: 8px;
        background-color: white;
        padding: 10px 10px;
        transition: all 0.5s;
        margin: 5px;
        width: max-content;

        &.checked {
            border: 3px solid #2196f3;
        }

        label {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            position: relative;
            padding-left: 35px;
            cursor: pointer;
            font-size: 22px;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            input {
                position: absolute;
                opacity: 0;
                cursor: pointer;
                height: 0;
                width: 0;
            }
            .checkmark {
                position: absolute;
                // top: 0;
                left: 0;
                height: 25px;
                width: 25px;
                background-color: #eee;

                &:after {
                    content: "";
                    position: absolute;
                    display: none;
                }

                &:after {
                    left: 9px;
                    top: 5px;
                    width: 5px;
                    height: 10px;
                    border: solid white;
                    border-width: 0 3px 3px 0;
                    -webkit-transform: rotate(45deg);
                    -ms-transform: rotate(45deg);
                    transform: rotate(45deg);
                }
            }

            &:hover input ~ .checkmark {
                background-color: #ccc;
            }

            input:checked ~ .checkmark {
                background-color: #2196f3;
            }

            input:checked ~ .checkmark:after {
                display: block;
            }
        }
    }
</style>
