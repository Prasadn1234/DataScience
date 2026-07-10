# ============================================================================
# TODO 8.4: CREATE GRADIO INTERFACE
# ============================================================================
#
# Assumes `demo` (the gr.Blocks interface built in week8_gradio_interface.py)
# is already in scope. share=True gives a public URL, needed in Colab since
# it can't expose localhost ports directly.

# Launch the Gradio interface
demo.launch(share=True)

print("Gradio interface launched")
