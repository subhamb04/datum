from builder.graph_builder import build_graph
from utils.tracer_utils import get_tracer, wait_for_tracers
from builder.ui import build_ui

if __name__ == "__main__":
    tracer = get_tracer()
    app = build_graph()
    demo = build_ui(app, tracer)

    try:
        demo.launch(inbrowser=True)
    finally:
        wait_for_tracers()
