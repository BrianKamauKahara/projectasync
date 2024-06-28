import gradio as gr
from asyncflows import AsyncFlows
from asyncflows.utils.async_utils import merge_iterators
from asyncflows.log_config import get_logger
from dotenv import load_dotenv
load_dotenv()


with gr.Blocks() as demo:
    #Display the input field and submit button for the user to enter a question
    query = gr.Textbox(label="Question", placeholder="Where does your curiosity lead you?")
    submit_button = gr.Button("Submit")

    #Display the areas where the results from the different religious bots is displayed
    with gr.Row():
        christian_bot = gr.Textbox(label="Christian Bot", interactive=False)
        muslim_bot = gr.Textbox(label="Muslim Bot", interactive=False)
        buddhist_bot = gr.Textbox(label="Buddhist Bot", interactive=False)
        hindu_bot = gr.Textbox(label="Hindu Bot", interactive=False)
        irreligious_bot = gr.Textbox(label="Irreligious Bot", interactive=False)
    bot_o_compare = gr.Textbox(label="Bot of Comparison (synthesis)", interactive=False)

    async def handle_submit(query):
        # Clear the output fields
        yield {
            christian_bot: "",
            muslim_bot: "",
            buddhist_bot: "",
            hindu_bot: "",
            irreligious_bot: "",
            bot_o_compare: "",
        }

        # Load the chatbot flow
        flow = AsyncFlows.from_file("relig.yaml").set_vars(
            query=query,
        )

        log = get_logger()

        # Stream the hats
        async for hat, outputs in merge_iterators(
            log,
            [
                christian_bot,
                muslim_bot,
                buddhist_bot,
                hindu_bot,
                irreligious_bot,
            ],
            [
                flow.stream('christian_bot.result'),
                flow.stream('muslim_bot.result'),
                flow.stream('buddhist_bot.result'),
                flow.stream('hindu_bot.result'),
                flow.stream('irreligious_bot.result'),
            ],
        ):
            yield {
                hat: outputs
            }

        # Stream the comparison bot
        async for outputs in flow.stream("bot_o_compare.result"):
            yield {
                bot_o_compare: outputs
            }

    #Calling the function that will run when you click submit
    submit_button.click(
        fn=handle_submit,
        inputs=[query],
        outputs=[
            christian_bot,
            muslim_bot,
            buddhist_bot,
            hindu_bot,
            irreligious_bot,
            bot_o_compare,
        ],
    )


if __name__ == "__main__":
    demo.launch()