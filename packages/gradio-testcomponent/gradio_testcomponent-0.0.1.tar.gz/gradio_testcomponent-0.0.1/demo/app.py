
import gradio as gr
from gradio_testcomponent import TestComponent


example = TestComponent().example_value()

demo = gr.Interface(
    lambda x:x,
    TestComponent(),  # interactive version of your component
    TestComponent(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


if __name__ == "__main__":
    demo.launch()
